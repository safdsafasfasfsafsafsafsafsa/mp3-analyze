from flask import Flask

app = Flask(__name__)

# Members API Route
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2", "Member3"]}
@app.route("/")
def members():
    return 'hello'

if __name__ == "__main__":
    app.run(debug=True)