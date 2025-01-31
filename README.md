# NBA Statistics Pipeline

## 🚀 Overview
This project is an **NBA Statistics Pipeline** that fetches NBA team statistics from the [SportsData API](https://sportsdata.io/) and stores them in **AWS DynamoDB**. The project also implements structured logging using **AWS CloudWatch**, enabling efficient monitoring and debugging.

This project was built as part of the **30 Days DevOps Challenge** I'm undertaking, demonstrating proficiency in **AWS services, Python, API integrations, and Infrastructure as Code (IaC)**.

## 🛠 Tech Stack
- **Python** (Data processing, API requests, logging)
- **AWS DynamoDB** (NoSQL database for storing NBA stats)
- **AWS CloudWatch** (Logging & monitoring)
- **Boto3** (AWS SDK for Python)
- **Docker** (Containerization)
- **EC2 Instance** (Compute environment for development)

## 🎯 Features
- Fetches real-time NBA statistics from the SportsData API
- Stores team stats in **AWS DynamoDB**
- Structured logging with **AWS CloudWatch**
- Error handling and logging with **JSON structured logs**
- Uses **environment variables** for sensitive credentials
- Implements **batch writing** for efficiency

## 📸 Screenshots

- **API Response Sample**
  
  ![Screenshot 2025-01-31 114651](https://github.com/user-attachments/assets/f1d1fc22-63f2-4916-83b8-7a4b13bb4a23)
- **DynamoDB Table Data**
  
  ![Screenshot 2025-01-31 115147](https://github.com/user-attachments/assets/6815af26-efb0-44c7-95f8-58fc80e35993)
  ![Screenshot 2025-01-31 115315](https://github.com/user-attachments/assets/b6ffbabc-9f8a-4ac2-ade4-a15c98d2380d)
  ![Screenshot 2025-01-31 115438](https://github.com/user-attachments/assets/18bc467b-abd0-4215-8734-4c2a8015ea14)
  ![Screenshot 2025-01-31 115510](https://github.com/user-attachments/assets/f58bc56b-00a5-43fe-9c49-968279550a5e)

- **CloudWatch Logs** (Structured logs for monitoring)
  
  ![Screenshot 2025-01-31 121713](https://github.com/user-attachments/assets/612e75de-32d8-4448-832f-bda15a4cbbdf)
  ![Screenshot 2025-01-31 121916](https://github.com/user-attachments/assets/bb5b4607-602f-4263-8c96-abb9d10dee20)

- **Terminal Output** (Successful execution of the pipeline)
  
  ![Screenshot 2025-01-31 122345](https://github.com/user-attachments/assets/770427da-aaab-4e25-9349-20f374a5360e)
  ![Screenshot 2025-01-31 122416](https://github.com/user-attachments/assets/8ad633f4-966b-4ad8-872e-9c4b962fe5ec)
  ![Screenshot 2025-01-31 122458](https://github.com/user-attachments/assets/7fed27f1-aa5a-4d5e-81a1-5241d14a6ba6)



## 🏗 Project Architecture
```plaintext
└── nba-stats-pipeline
    ├── src
    │  ├── __init__.py
    │  ├── nba_stats.py
    │  ├── lambdafunction.py
    ├── requirements.txt      # Dependencies
    │   ├── .env              # Environment variables
    │   ├── Dockerfile        # Containerization setup (if applicable)
    ├── README.md             # Project documentation
```

## 🚀 Setup & Installation
### 4️⃣ Launch an EC2 Instance and SSH Into It
```bash
ssh -i "nba-stats-pipeline.pem" ubuntu@ec2-18-212-173-76.compute-1.amazonaws.com
```

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/onlyfave/nba-stats-pipeline.git
cd nba-stats-pipeline
```
### 1️⃣ Install Python3
Python3 is required to run the project.
```bash
sudo apt update
sudo apt install python3
```
### 1️⃣ Install Pip
On most systems, pip comes pre-installed with Python3. To verify, run:
```bash
pip3 --version
```
If you don't have pip installed, use the following command:
```bash
sudo apt install python3-pip
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file with the following content:
```ini
SPORTDATA_API_KEY=your_api_key
DYNAMODB_TABLE_NAME=nba-player-stats
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```
### 4️⃣ CD Into the Folder Containing the Pipeline
```bash
cd src
```
### 4️⃣ Run the Pipeline
```bash
python3 nba_stats.py
```

## 📊 Sample Data Format
```json
[
  {
    "TeamID": 1,
    "TeamName": "Los Angeles Lakers",
    "Wins": 25,
    "Losses": 15,
    "PointsPerGameFor": 112.5,
    "PointsPerGameAgainst": 108.3
  }
]
```

## 🏗 Deployment (Optional: Dockerized Version)
To run this project inside a Docker container:
```bash
docker build -t nba-stats-pipeline .
docker run --env-file .env nba-stats-pipeline
```

## 🔥 Key Takeaways
- **AWS Expertise**: Used DynamoDB & CloudWatch for data storage & monitoring
- **DevOps Skills**: Managed credentials, logging, and error handling efficiently
- **Cloud-Native Thinking**: Designed a cloud-based ETL pipeline

## 📌 Next Steps
- Implement **Lambda Functions** for automated execution
- Deploy using **AWS ECS or Kubernetes**
- Integrate with **Grafana** for real-time data visualization

## 📢 Connect With Me
🚀 [LinkedIn](https://www.linkedin.com/in/favour-onyeneke-2b2881297/) | 🐦 [Twitter/X](https://x.com/only_fave)

---
💡 *If you find this project interesting, feel free to ⭐ the repo and contribute!*


