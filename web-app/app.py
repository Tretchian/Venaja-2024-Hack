from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

DATABASE = 'db/Main_DB.db'

DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db = SQLAlchemy(app)
print(db.Model)

class Person(db.Model):
    __tablename__ = 'Persons'

    Id_person = db.Column(db.Integer, primary_key = True, nullable=False, unique=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    Login = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    Mail = db.Column(db.String(70), unique=True, nullable=False)
    Role = db.Column(db.String(1), nullable=False)


# @app.route('/', methods=['GET', 'POST'])
@app.route('/auth', methods=['GET', 'POST'])
def auth_form():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        person = Person.query.filter_by(Login=form.login.data, Password=form.password.data).first()
        print("person")
        # Здесь добавим логику для проверки данных
        if person:
            # Смотрим дальше по роли из баззы данных куда перенаправлять
            # 1 - админка
            flash("Вы успешно вошли!", "success")
            if person.Role == "1":
                return redirect(url_for('admin.html'))
            elif person.Role == "2":
                return redirect(url_for('redact.html'))
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template('auth.html', form=form)

# def auth():
#     form = LoginForm()
#     if form.validate_on_submit():
#         persons = Pe
    
#     return render_template("auth.html")


# login_manager = LoginManager(app)
# class UserLogin:
#     def is_authenticated(self):
#         return True
    
if __name__ == "__main__":
    app.run(debug=DEBUG)