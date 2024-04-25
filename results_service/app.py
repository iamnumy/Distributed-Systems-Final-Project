from flask import Flask, jsonify
from models import db, Vote, User
import requests
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@mysql/distributed_voting_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/results', methods=['GET'])
def get_results():
    try:
        # Query the database to get the count of votes for each candidate (user)
        results = db.session.query(db.func.count(Vote.id), User.username).join(User, Vote.candidate_id==User.id).group_by(User.username).all()

        # Convert the results to a dictionary
        result_dict = {username: count for count, username in results}

        return jsonify(result_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003, threaded=True)
