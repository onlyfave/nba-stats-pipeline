import json
from nba_stats import NBAStatsPipeline

def lambda_handler(event, context):
    try:
        pipeline = NBAStatsPipeline()
        
        # Set up DynamoDB table if needed
        pipeline.setup_dynamodb_table()
        
        # Fetch and store stats
        stats = pipeline.fetch_player_stats()
        if stats:
            pipeline.store_team_stats(stats)
            return {
                'statusCode': 200,
                'body': json.dumps('Successfully updated NBA stats')
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to fetch NBA stats')
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
