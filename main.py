from flask import Flask, redirect
from uuid import uuid4

from controllers.user import user

app = Flask(__name__)
app.secret_key = str(uuid4())
app.config["WTF_CSRF_ENABLED"] = False

app.register_blueprint(user, url_prefix='/users/')


@app.route("/")
def redirectToUsers():
    return redirect("/users/")


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8080)
