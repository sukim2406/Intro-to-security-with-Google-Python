from flask import Flask, render_template, request

app = Flask(__name__)

def fake_get_from_database():
    data = "<script>alert('stored xss run')"
    return data

@app.route("/xss", methods=["GET", "POST"])
def xss():
    reflected_xss_string = ""
    stored_xss_string = ""

    if request.method == "GET":
        if "inputText" in request.args:
            reflected_xss_string = request.args.get("inputText", default="", type=str)
            stored_xss_string = fake_get_from_database()

    return render_template("xss_patch.html", reflected_xss_string=reflected_xss_string, stored_xss_string=stored_xss_string)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)