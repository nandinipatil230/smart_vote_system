from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Smart Voting System</title>

        <style>

            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:100px;
            }

            .container{
                width:70%;
                margin:auto;
                background:#1e293b;
                padding:40px;
                border-radius:20px;
                box-shadow:0px 0px 20px rgba(0,0,0,0.5);
            }

            h1{
                font-size:50px;
                color:#38bdf8;
            }

            h2{
                color:#22c55e;
            }

            p{
                font-size:20px;
                line-height:35px;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>SMART VOTING SYSTEM</h1>

            <h2>Railway Deployment Successful 🚀</h2>

            <p>
            Secure biometric-based electronic voting system
            developed using Python, Flask, DeepFace,
            OpenCV, Verilog HDL, and Database Integration.
            </p>

            <p>
            Features Included:
            </p>

            <p>
            ✔ Secure Login Authentication <br>
            ✔ Face Verification <br>
            ✔ Duplicate Vote Prevention <br>
            ✔ Real-time Vote Counting <br>
            ✔ Dashboard Monitoring <br>
            ✔ Secure Voting Architecture
            </p>

        </div>

    </body>

    </html>
    """


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
