from flask import Flask, render_template, request,jsonify, redirect, url_for, session, flash, get_flashed_messages

from models import db,User, Task
from form import RegistrationForm, LoginForm
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# create table in database before quering them
with app.app_context():
    db.create_all()

# User Specific routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm() 
    if form.validate_on_submit():
        flash(f"Account has been created for {form.username.data}", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration Form', form=form)

# print("route 1 passed")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'himujharwal@gmail.com' and form.password.data=='password':
            flash("you have been logged in", 'success')
            return redirect(url_for('home'))
        else:
            flash("unsuccesfull log in. you need email and password", 'danger')
    return render_template('login.html', title = 'LoginForm', form=form)

# print("route 2 passed")

# Task Specific routes

@app.route('/tasks', methods=['POST'])
def create_tasks():
    data = request.get_json()
    username = data.get('username')
    tasks_data = data.get('tasks', [])
    user_instance = User.query.filter_by(name=username).first()

    # checking that is user already exist or not
    if user_instance:
        return jsonify({'message': "user already exist."})
    user_instance = User(name=username)
    

    task_instances = [Task(title=task['title'], user=user_instance) for task in tasks_data]

    db.session.add_all(task_instances)
    db.session.commit()

    return jsonify({'message': "data added successfully"})

# print("route 3 passed")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    
    users = User.query.all()
    result = []

    for user in users:
        user_data = {
                    "user_id": user.id,
                    "username": user.name,
                    "tasks": [
                        {"title": task.title}
                        for task in user.tasks_list
                        ]
                    }
        
        result.append(user_data)
    return jsonify(result
    )

# print("route 4 passed")
@app.route('/tasks/<int:ID>', methods=['GET'])
def get_task(ID):
    tasks = Task.query.filter(Task.user_id == ID).all()
    return jsonify([
        {'title': t.title, "user_id":t.user_id,'username': t.user.name}
        for t in tasks
    ])

# print("route 5 passed")
@app.route('/tasks/<int:ID>', methods=['PUT'])
def update_tasks(ID):
    update_tsk = Task.query.filter(Task.user_id == ID).first()
    if update_tsk:
        update_tsk.title = "updated_title"
        db.session.commit()
        return jsonify({'message': 'task updated successfully'})
    return jsonify({'error': 'task not found'}), 404

# print("route 6 passed")
@app.route('/tasks/<int:ID>', methods=['DELETE'])
def delete_tasks(ID):
    delete_task = Task.query.filter(Task.user_id == ID).first()
    if delete_task:
        db.session.delete(delete_task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'})
    return jsonify({'error': 'task not found'}), 404

# print("route 7 passed")

if __name__ == '__main__':
    app.run(debug=True)
