from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        message_dict = [message.to_dict() for message in messages]
        return jsonify(message_dict), 200
    elif request.method == 'POST':
        new_message = Message(
            body=request.json.get('body'),
            username=request.json.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            jsonify(message_dict),
            201
        )
        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if message is None:
        response_body = {
            "message": "Message does not exist."
        }
        return make_response(jsonify(response_body), 404)
    
    if request.method == 'GET':
        message_dict = message.to_dict()
        return jsonify(message_dict), 200
    
    elif request.method == 'PATCH': 
        message.body = request.json.get('body', message.body)
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        return jsonify(message_dict), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "message": "Message deleted successfully."
        }
        return make_response(jsonify(response_body), 200)

if __name__ == '__main__':
    app.run(port=5555)
