from flask import Flask
from flask_restful import Api
import dotenv

from api.schedule import *

dotenv.load_dotenv()
app = Flask(__name__)
api = Api(app)

api.add_resource(CurrentTrainAPI, '/api/trains')
api.add_resource(GetAccessToken, '/api/auth')

if __name__ == '__main__':
    app.run(debug=True)