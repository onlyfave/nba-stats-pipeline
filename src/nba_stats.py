import os
import json
import boto3
import requests
import logging
import watchtower
from datetime import datetime
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
from decimal import Decimal

# Load environment variables
load_dotenv()

def setup_logger():
    logger = logging.getLogger('NBAStatsPipeline')
    logger.setLevel(logging.INFO)

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # CloudWatch handler (updated for newer version)
    try:
        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group_name='NBAStatsPipeline',
            stream_name=f'stats-collection-{datetime.now().strftime("%Y-%m-%d")}'
        )
        cloudwatch_handler.setFormatter(json_formatter)
        logger.addHandler(cloudwatch_handler)
    except Exception as e:
        logger.error(f"Failed to set up CloudWatch logging: {e}")

    return logger

class NBAStatsPipeline:
    def __init__(self):
        self.logger = setup_logger()
        self.api_key = os.getenv('SPORTDATA_API_KEY')
        self.base_url = "https://api.sportsdata.io/v3/nba"
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = os.getenv('DYNAMODB_TABLE_NAME')

        self.logger.info("Initialized NBA Stats Pipeline", 
                        extra={
                            'service': 'nba-stats',
                            'base_url': self.base_url,
                            'table_name': self.table_name
                        })

    def convert_floats_to_decimals(self, item):
        """Helper method to convert all float values to Decimals"""
        if isinstance(item, float):
            return Decimal(str(item))
        elif isinstance(item, dict):
            return {k: self.convert_floats_to_decimals(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self.convert_floats_to_decimals(v) for v in item]
        return item

    def setup_dynamodb_table(self):
        """Set up DynamoDB table if it doesn't exist"""
        try:
            self.logger.info(f"Setting up DynamoDB table: {self.table_name}")
            
            # Create table if it doesn't exist
            try:
                table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'TeamID',
                            'KeyType': 'HASH'  # Partition key
                        },
                        {
                            'AttributeName': 'Timestamp',
                            'KeyType': 'RANGE'  # Sort key
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'TeamID',
                            'AttributeType': 'N'  # Number
                        },
                        {
                            'AttributeName': 'Timestamp',
                            'AttributeType': 'S'  # String
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                
                # Wait for table to be created
                table.meta.client.get_waiter('table_exists').wait(
                    TableName=self.table_name
                )
                self.logger.info(f"Created table {self.table_name}")
                
            except self.dynamodb.meta.client.exceptions.ResourceInUseException:
                self.logger.info(f"Table {self.table_name} already exists")
                table = self.dynamodb.Table(self.table_name)
                
            return table
            
        except Exception as e:
            self.logger.error(f"Failed to set up DynamoDB table", 
                            extra={
                                'error': str(e),
                                'table_name': self.table_name
                            })
            raise

    def fetch_player_stats(self, season="2024"):
        """Fetch player statistics from sportsdata.io"""
        try:
            url = f"{self.base_url}/scores/json/Standings/{season}"
            self.logger.info(f"Fetching data from API", 
                           extra={
                               'url': url,
                               'season': season
                           })

            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info("Successfully fetched data", 
                           extra={
                               'teams_count': len(data),
                               'season': season
                           })
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error("API request failed", 
                            extra={
                                'error': str(e),
                                'url': url,
                                'status_code': getattr(e.response, 'status_code', None)
                            })
            return None
        except Exception as e:
            self.logger.error("Unexpected error occurred", 
                            extra={
                                'error': str(e),
                                'error_type': type(e).__name__
                            })
            return None

    def store_team_stats(self, stats_data):
        """Store team statistics in DynamoDB"""
        try:
            table = self.dynamodb.Table(self.table_name)
            timestamp = datetime.now().isoformat()
            
            self.logger.info("Starting batch write to DynamoDB")
            
            with table.batch_writer() as batch:
                for team in stats_data:
                    # Create base item
                    team_item = {
                        'TeamID': team['TeamID'],
                        'Timestamp': timestamp,
                        'TeamKey': team['Key'],
                        'TeamName': f"{team['City']} {team['Name']}",
                        'Conference': team['Conference'],
                        'Division': team['Division'],
                        'Stats': self.convert_floats_to_decimals({
                            'Wins': team['Wins'],
                            'Losses': team['Losses'],
                            'Percentage': team['Percentage'],
                            'PointsPerGameFor': team['PointsPerGameFor'],
                            'PointsPerGameAgainst': team['PointsPerGameAgainst'],
                            'HomeWins': team['HomeWins'],
                            'HomeLosses': team['HomeLosses'],
                            'AwayWins': team['AwayWins'],
                            'AwayLosses': team['AwayLosses'],
                            'LastTenWins': team['LastTenWins'],
                            'LastTenLosses': team['LastTenLosses']
                        }),
                        'LastUpdated': datetime.now().isoformat()
                    }
                    
                    self.logger.info(f"Storing data for team: {team_item['TeamName']}")
                    batch.put_item(Item=team_item)
                
            self.logger.info("Successfully stored team stats", 
                            extra={'teams_count': len(stats_data)})
                            
        except Exception as e:
            self.logger.error("Failed to store team stats", 
                             extra={
                                 'error': str(e),
                                 'error_type': type(e).__name__
                             })
            raise

def main():
    try:
        pipeline = NBAStatsPipeline()
        
        # Set up DynamoDB table
        pipeline.setup_dynamodb_table()
        
        print("Fetching NBA Stats...")
        stats = pipeline.fetch_player_stats()
        
        if stats:
            # Store in DynamoDB
            pipeline.store_team_stats(stats)
            print("Successfully stored team stats in DynamoDB!")
            
            # Show sample of stored data
            print("\nSample of stored data:")
            print(json.dumps(stats[:2], indent=2))
        else:
            print("Failed to fetch stats")

    except Exception as e:
        logging.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()
