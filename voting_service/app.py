from flask import Flask, request, jsonify
from models import db, Vote

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@mysql/distributed_voting_system'
db.init_app(app)

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/vote', methods=['POST'])
def cast_vote():
    user_id = request.json.get('user_id')
    candidate_id = request.json.get('candidate_id')


    if not user_id or not candidate_id:
        return jsonify({'error': 'Missing user ID or candidate ID'}), 400

    new_vote = Vote(user_id=user_id, candidate_id=candidate_id)
    db.session.add(new_vote)
    db.session.commit()

    return jsonify({'message': 'Vote successfully recorded.'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)
