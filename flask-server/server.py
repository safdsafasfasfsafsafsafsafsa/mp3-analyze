from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Members API Route
@app.route("/")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}
# @app.route("/")
# def members():
#     return 'hello'

if __name__ == "__main__":
    app.run(debug=True)