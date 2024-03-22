from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


@app.route('/user-login', methods=['POST'])
def user_login():
    uri = "mongodb+srv://covalenthub.iqzz0en.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile='certs/db.pem',
                         server_api=ServerApi('1'))

    db = client['users']
    collection = db['credentials']
    user = collection.find_one({'email': request.json['email']})
    if user:
        import bcrypt

        stored_password = user['password']
        password = request.json['password']
        if bcrypt.checkpw(password, stored_password):
            from uuid import uuid4
            import datetime

            rand_token = uuid4()
            db = client['sessions']
            collection = db['tokens']
            collection.insert_one({'user_id': user['_id'], 'token': rand_token, 'created_at': datetime.datetime.now()})

            return jsonify({'token': rand_token}), 200
        else:
            return 'Invalid password', 401
    else:
        return 'Not found', 404


if __name__ == '__main__':
    app.run()
