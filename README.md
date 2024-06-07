# DataFlow

## Project Overview

DataFlow is a data processing application that reads JSON data from an AWS SQS queue, masks personal identifiable information (PII) such as IP addresses and device IDs, and stores the processed data in a PostgreSQL database. This project uses Docker to simulate the entire environment locally, including LocalStack for AWS services, making it easy to develop and test without requiring actual AWS resources.

## Features

- **AWS SQS Simulation**: Utilizes LocalStack to simulate SQS for message queueing.
- **Data Masking**: Masks sensitive information before storage.
- **PostgreSQL Database**: Uses PostgreSQL for data persistence.
- **Dockerized Setup**: Includes Docker configurations for easy setup and teardown.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Docker
- Docker Compose
- Python (if running scripts locally outside Docker)
- AWS CLI (optional, for manual interaction with LocalStack)

## Setup and Installation

1. **Clone the Repository**
https://github.com/abhishek-mehra/DataFlow
cd DataFlow

2. **Environment Setup**
- Copy the sample `.env.sample` to `.env` and update the environment variables to fit your local setup.
  ```
  cp .env.sample .env
  ```
- Ensure the `.env` file includes necessary configurations such as database credentials and AWS settings.

3. **Building the Docker Containers**
- Run the following command to build and start the Docker containers. This will set up LocalStack, PostgreSQL, and your application.
  ```
  docker-compose up --build
  ```

4. **Sending Test Messages: Use the AWS CLI or any AWS SDK to send messages to the SQS queue:**

```
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/dataflow-queue --message-body '{"user_id": "1", "device_id": "XYZ123", "ip": "192.168.1.1"}'

```