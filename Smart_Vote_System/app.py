from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():

    return """
    <h1>SMART VOTING SYSTEM</h1>
    <h2>Railway Deployment Successful 🚀</h2>
    <p>Biometric Voting System Backend Running</p>
    """


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)