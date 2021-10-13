from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import pyodbc
from datetime import datetime, timedelta

def get_connection_and_cursor():
    server = 'localhost'
    database = 'mytest'
    username = 'pyuser'
    password = 'Test1234%^&'
    
    mssql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; PORT=1433; DATABASE=' + database + '; UID=' + username + ';PWD=' + password)

    cursor = mssql_conn.cursor()
    
    return mssql_conn, cursor

mssql_conn, cursor = get_connection_and_cursor()

app = Flask(__name__)
api = Api(app)

def get_sms_key():
    sms_key = "7777"
    return sms_key

def get_member_id_from_cookie():
    id = "tom"
    return id

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
            now_time = datetime.now()
            member_id = get_member_id_from_cookie()

            if sms_number == certify_number:
                cert_sql = "insert into sms_cert values (?,?,?)"
                cursor.execute(cert_sql, member_id, "Y", now_time)
                cursor.execute("SELECT @@IDENTITY AS ID;")
                seqno = str(cursor.fetchone()[0])
                mssql_conn.commit()

                result = "N"
            else:
                result = "N"
                seqno = 0
            
            return {"certify_yn": result, "seqno": seqno}
        except Exception as e:
            return {"certify_yn": "N", "seqno": seqno}


class DoPayment(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("item_price", type=str, default="")
        parser.add_argument("seqno", type=str, default="")
        return parser

    def post(self):
        try:
            parser = DoPayment.get_parser()
            args = parser.parse_args()
            item_price = int(args["item_price"])
            seqno = int(args["seqno"])

            member_id = get_member_id_from_cookie()
            due_date = datetime.now() - timedelta(minutes=15)

            check_sql = "select top 1 cert_yn from sms_cert(nolock) where seqno = ? and member_id = ? and cert_date >= ?"
            cursor.execute(check_sql, seqno, member_id, due_date)
            cert_yn = cursor.fetchone()

            if cert_yn:
                if cert_yn[0] == "Y":
                    payment_result = do_payment(item_price)
                else:
                    payment_result = "N"
            else:
                payment_result = "N"
            
            return {"payment_result": payment_result}
        except Exception as e:
            print(e)
            return {"pament_result": "N"}

api.add_resource(CheckSMS, "/check_sms")
api.add_resource(DoPayment, "/do_payment")

@app.route("/secure_design", methods=['GET'])
def design():
    return render_template('secure_design_patch.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)