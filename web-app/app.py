from flask import Flask
from flask import render_template
# from flask_login import LoginManager

DATABASE = 'db/Main_DB.sqlite3'
DEBUG = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


# login_manager = LoginManager(app)
# class UserLogin:
#     def is_authenticated(self):
#         return True
    
if __name__ == "__main__":
    app.run(debug=DEBUG)