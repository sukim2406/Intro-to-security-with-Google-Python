from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

def get_secret_key():
    secret_key = "secret"
    return secret_key


class MakeToken(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("my_name", type=str, default="")
        return parser

    def post(self):
        try:
            parser = MakeToken.get_parser()
            args = parser.parse_args()
            my_name = args["my_name"]

            secret_key = get_secret_key()

            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=10),
                'iat': datetime.utcnow(),
                'sub': my_name
            }

            secret = jwt.encode(payload, secret_key, algorithm="HS256")

            return {"token": secret}

        except Exception as e:
            return {"token": str(e)}


class SendToken(Resource):
    def post(self):
        try:
            secret_key = get_secret_key()

            auth_header = request.headers.get('Authorization')
            if auth_header:
                my_token = auth_header.split(" ")[1]
            
            payload = jwt.decode(my_token, secret_key, algorithms=["HS256"])
            user_name = payload["sub"]

            return {"my_name": user_name}
        
        except jwt.ExpiredSignatureError:
            return {"my_name": "Token Expired"}
        
        except Exception as e:
            return {"my_name": str(e)}


api.add_resource(MakeToken, "/make_token")
api.add_resource(SendToken, "/send_token")

@app.route("/call_api", methods=['GET'])
def call_api():
    return render_template('api_with_token.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)