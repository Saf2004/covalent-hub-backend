from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi



app = Flask(__name__)


@app.route('/')
def hello_world():
    uri = "mongodb+srv://covalenthub.iqzz0en.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile='certs/db.pem',
                         server_api=ServerApi('1'))

    db = client['sample_mflix']
    collection = db['comments']
    collection.insert_one({'name': 'test'})
    doc_count = 8
    return f'Hello World!{doc_count}'


if __name__ == '__main__':
    app.run()
