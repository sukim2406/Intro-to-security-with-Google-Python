from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_sms_key():
    sms_key = "7777"
    return sms_key

def do_payment(item_price):
    if item_price > 0:
        payment_result = "Y"
    else:
        payment_result = "N"
    
    return payment_result


class CheckSMS(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("sms_number", type=str, default="")
        
        return parser

    def post(self):
        try:
            parser = CheckSMS.get_parser()
            args = parser.parse_args()
            sms_number = args["sms_number"]

            certify_number = get_sms_key()

            if sms_number == certify_number:
                result = "Y"
            else:
                result = "N"

            return {"certify_yn": result}

        except Exception as e:
            return {"certify_yn": "N"}


class DoPayment(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("item_price", type=str, default="")

        return parser
    
    def post(self):
        try:
            parser = DoPayment.get_parser()
            args = parser.parse_args()

            item_price = int(args["item_price"])
            payment_result = do_payment(item_price)

            return {"payment_result": payment_result}
        except Exception as e:
            return {"payment_result": "N"}


api.add_resource(CheckSMS, "/check_sms")
api.add_resource(DoPayment, "/do_payment")

@app.route("/secure_design", methods=['GET'])
def design():
    return render_template('secure_design_bad.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
