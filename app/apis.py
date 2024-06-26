from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


@app.route('/user-login', methods=['POST'])
def user_login():

    #INPUT
    #{
    #    "email": "
    #    "password": "password"
    #}
    #OUTPUT
    #{
    #    "token": JSLM-1234-ABCD-5678
    #}

    #Token is a unique uuid that is generated and returned to the user after successful login
    #The token is used to authenticate the user in subsequent requests
    #The token should be stored in the client side and sent in the header of the request



    uri = "mongodb+srv://covalenthub.iqzz0en.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile='certs/db.pem',
                         server_api=ServerApi('1'))

    #connect to the database
    db = client['users']

    #connect to the collection
    collection = db['credentials']

    #find the user with the email
    user = collection.find_one({'email': request.json['email']})

    #check if the user exists
    if user:

        #import the bcrypt library
        import bcrypt

        #get the the queried and stored password
        stored_password = user['password']
        password = request.json['password']

        #check if the password is correct
        if bcrypt.checkpw(password, stored_password):
            #import the uuid and datetime libraries
            from uuid import uuid4
            import datetime

            #generate a random token
            rand_token = uuid4()

            #connect to the sessions database
            db = client['sessions']

            #connect to the tokens collection
            collection = db['tokens']

            #insert the token into the database
            collection.insert_one({'user_id': user['_id'], 'token': rand_token, 'created_at': datetime.datetime.now()})

            #return the token with a status code of 200
            return jsonify({'token': rand_token}), 200
        else:
            #return an invalid password error with a status code of 401
            return 'Invalid password', 401
    else:
        #return a user not found error with a status code of 404
        return 'Not found', 404

@app.route('/user-register', methods=['POST'])
def user_register():
    #INPUT
    #{
    #    "name": "John Doe",
    #    "username": "johndoe",
    #    "age": 25,
    #    "country": "USA",
    #    "email": "
    #    "phone": "+1234567890",
    #    "password": "password"
    #}
    #OUTPUT
    #{
    #    "token": JSLM-1234-ABCD-5678
    #}

    #Token is a unique uuid that is generated and returned to the user after successful registration
    #The token is used to authenticate the user in subsequent requests
    #The token should be stored in the client side and sent in the header of the request

    uri = "mongodb+srv://covalenthub.iqzz0en.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile='certs/db.pem',
                         server_api=ServerApi('1'))

    #connect to the database
    db = client['users']
    collection = db['credentials']
    #import the bcrypt library
    import bcrypt

    #get the password and hash it
    password = request.json['password']
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    #check if the user already exists
    if collection.find_one({'email': request.json['email']}):

        #return a user already exists error with a status code of 400
        return 'User already exists', 400
    else:
        #import the uuid and datetime libraries
        from uuid import uuid4
        import datetime

        #insert the user into the database
        collection.insert_one({'email': request.json['email'], 'password': hashed_password})

        #get the user id
        user_id = collection.find_one({'email': request.json['email']})['_id']

        #connect to the info database
        collection = db['info']

        #insert the user info into the database
        collection.insert_one({'user_id': user_id, 'name': request.json['name'], 'username': request.json['username'],
                               'birthdate': request.json['birthdate'], 'country': request.json['country'],
                               'email': request.json['email'], 'phone': request.json['phone'],
                               'password': hashed_password})

        #connect to the sessions database
        db = client['sessions']

        #connect to the tokens collection
        collection = db['tokens']

        #generate a random token
        rand_token = uuid4()

        #insert the token into the database
        collection.insert_one({'user_id': user_id, 'token': rand_token, 'created_at': datetime.datetime.now()})

        #return the token with a status code of 201
        return jsonify({'token': rand_token}), 201

if __name__ == '__main__':
    app.run()
