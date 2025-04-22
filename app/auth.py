from datetime import datetime, timedelta, UTC
import jwt
from flask import current_app, request
from functools import wraps


def generate_jwt_token(user):             # user is instance of user object 
    
    payload = {
        "user_id": user.id,
        "username": user.username,
        "password": user.password,
        "user_type":  user.user_type,
        "exp"     : datetime.now(UTC) + timedelta(hours=1)

    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'],algorithm="HS256")
    return token


def decode_token(token):
    try:
        decoded = jwt.decode(token , current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token is expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def jwt_required(user_type=None):
    
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]
            if not token:
                return {"message":"token is missing"}, 401
            try:
                decoded = decode_token(token)
                if user_type and decoded['user_type'] != user_type:
                    return {"message":"Denied Authorization:insufficent credential"}, 403
                request.user = decoded
            except Exception as e:
                return {"message": str(e)}, 401
            return f(*args, **kwargs)
        return decorated
    return wrapper


            






# from flask import  render_template, request,jsonify, redirect, url_for, session, flash, get_flashed_messages

# from flask import Blueprint
# from .form import RegistrationForm, LoginForm

# auth_bp = Blueprint('auth_bp', __name__)


# @auth_bp.route('/')
# @auth_bp.route('/home')
# def home():
#     return render_template('home.html')

# @auth_bp.route('/register', methods=['GET','POST'])
# def register():
#     form = RegistrationForm() 
#     if form.validate_on_submit():
#         flash(f"Account has been created for {form.username.data}", 'success')
#         return redirect(url_for('auth_bp.home'))
#     return render_template('register.html', title='Registration Form', form=form)

# # print("route 1 passed")

# @auth_bp.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'himujharwal@gmail.com' and form.password.data=='password':
#             flash("you have been logged in", 'success')
#             return redirect(url_for('auth_bp.home'))
#         else:
#             flash("unsuccesfull log in. you need email and password", 'danger')
#     return render_template('login.html', title = 'LoginForm', form=form)
