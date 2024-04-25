import sys
import requests
import jwt  # Import JWT library
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import threading


# Database configuration
DB_USERNAME = 'root'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '3307'
DB_NAME = 'distributed_voting_system'

# SQLAlchemy engine and session
engine = create_engine(f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Define the Vote model
class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    candidate_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)


# Create the tables in the database
Base.metadata.create_all(engine)

# Configure base URLs for each microservice
BASE_URLS = {
    'authentication': 'http://localhost:5001',
    'voting': 'http://localhost:5002',
    'results': 'http://localhost:5003'
}

# Secret key for JWT token
SECRET_KEY = 'd293f2dee0997cfff9fbfbc61589683030dbfd6d44f42bae1d07c013a22a49f5'


def register(username, password, role):
    """Register a new user with a role."""
    url = f"{BASE_URLS['authentication']}/register"
    data = {'username': username, 'password': password, 'role': role}
    response = requests.post(url, json=data)
    return response.json()


def login(username, password):
    """Log in a user."""
    url = f"{BASE_URLS['authentication']}/login"
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    return response.json()



def threaded_vote(user_id, candidate_id, token):
    """Function to handle vote casting in a separate thread."""
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print({'error': 'Token has expired.'})
        return
    except jwt.InvalidTokenError:
        print({'error': 'Invalid token.'})
        return

    if Session().query(Vote).filter_by(user_id=user_id).first():
        print({'error': 'User has already voted.'})
        return

    url = f"{BASE_URLS['voting']}/vote"
    data = {'user_id': user_id, 'candidate_id': candidate_id}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        new_vote = Vote(user_id=user_id, candidate_id=candidate_id)
        session = Session()
        session.add(new_vote)
        session.commit()
        print({'message': 'Vote successfully recorded.'})
    else:
        print(response.json())


def results():
    url = f"{BASE_URLS['results']}/results"
    response = requests.get(url)
    return response.json()


def main():
    args = sys.argv[1:]  # Get arguments passed to script
    if not args:
        print("No command provided.")
        return

    command = args[0]

    try:
        if command == 'register' and len(args) == 4:
            username, password, role = args[1], args[2], args[3]
            result = register(username, password, role)
            print(result)
        elif command == 'login' and len(args) == 3:
            username, password = args[1], args[2]
            result = login(username, password)
            print(result)
        elif command == 'vote' and len(args) == 4:
            user_id, candidate_id, token = int(args[1]), int(args[2]), args[3]
            vote_thread = threading.Thread(target=threaded_vote, args=(user_id, candidate_id, token))
            vote_thread.start()
            vote_thread.join()
        elif command == 'results' and len(args) == 1:
            result = results()
            print(result)
        else:
            print("Invalid command or number of arguments.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
