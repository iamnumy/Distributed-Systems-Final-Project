# Voting System

## Overview
This Voting System is a microservice-based web application designed for managing elections. It supports roles for candidates and voters, allowing registered voters to cast votes for the eligible candidates.

## Features
- **User Registration and Authentication**: Separate roles for candidates and voters.
- **Voting**: Allows voters to cast votes securely for candidates.
- **Results Calculation**: Live tally of votes available to view.
- **Security**: Secured endpoints with JWT-based authentication.

## Technologies
- **Flask**: For creating web services.
- **MySQL**: Database for storing user and voting data.
- **Docker**: Containerization and environment consistency.
- **RPyC**: Remote Procedure Call framework for Python for handling voting operations.

## Directory Structure

Distributed-Systems-Final-Project/
│
├── authentication_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── voting_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── results_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── cli/
│   └── cli.py
│
└── docker-compose.yml



## Setup and Installation
### Prerequisites
- Docker
- Docker Compose
- Python 3.8 or higher

### Running the Application
1. **Clone the Repository**
   ```bash
git clone https://github.com/iamnumy/Distributed-Systems-Final-Project.git


2. **Build and Run the Docker Containers**
   ```bash
docker-compose up --build

This will start the microservices required for the application as specified in the `docker-compose.yml` file.

### Using the CLI
- **Register a User**
   ```bash
python cli/cli.py register <username> <password> <role>


- **Login**
   ```bash
python cli/cli.py login <username> <password>


- **Cast a Vote**
   ```bash
python cli/cli.py vote <user_id> <candidate_id> <token>


- **View Results**
   ```bash
python cli/cli.py results
