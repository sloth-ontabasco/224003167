from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import dotenv

from api.schedule import *

dotenv.load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

api.add_resource(CurrentTrainAPI, '/api/trains')
api.add_resource(GetAccessToken, '/api/auth')

if __name__ == '__main__':
    app.run(debug=True)