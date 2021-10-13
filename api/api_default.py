from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class GetSecret(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("my_name", type=str, default="")
        return parser
    
    def post(self):
        try:
            parser = GetSecret.get_parser()
            args = parser.parse_args()
            my_name = args["my_name"]

            secret = my_name + "' secret number is 123"

            return {"secret": secret}
        except Exception as e:
            return {"secret": str(e)}
    
api.add_resource(GetSecret, "/get_secret")

@app.route("/call_api", methods=["GET"])
def call_api():
    return render_template('api_default.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)