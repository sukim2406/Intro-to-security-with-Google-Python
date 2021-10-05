import re
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/xss_ajax", methods=["GET", "POST"])
def xss():
    reflected_xss_string = ""

    if request.method == "GET":
        if "inputText" in request.args:
            reflected_xss_string = request.args.get("inputText", default="", type=str)
    
    return render_template("xss_ajax.html", reflected_xss_string=reflected_xss_string)

@app.route("/get_data", methods=["GET"])
def get_data():
    your_id = request.args.get('id')
    return "hello, "+ str(your_id)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
