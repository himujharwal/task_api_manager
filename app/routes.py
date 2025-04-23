from flask import request,jsonify, redirect, url_for, Blueprint
from .models import db,User, Task
from flask import current_app as app
from app.auth import generate_jwt_token, decode_token, jwt_required


# registration and login route where we generate tokens

@app.route('/register', methods= ['POST'])
def register_user():
    data = request.get_json()
    user_instance = User.query.filter_by(username=data['username']).first()
    if user_instance:
        return jsonify({"message": "user already exist"})
    
    user = User(username=data['username'], user_type=data['user_type'])
    user.set_password(data['password'])  # this will save hashed password in password column becuase of self.password attribute is set that change the column values
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user added successsfully"}),201
                   


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_jwt_token(user)
        return jsonify({"message": "Login successful", "token":token}), 200
    return jsonify({"message": "Invalid credentials"}), 401





#  create task and add them into database talble 

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_tasks():
    # important note do not send the username into the raw body data you just send the authorisation token in header and tasks data in body
    # becuase the token has already the username when you set it into jwt_requried like reqest.user = decoded
    data = request.get_json()
    # print(data)
    user = request.user  # fuck this give the dictories object of user not single user string
    
    username = user['username']
  

    user_instance = User.query.filter_by(username=username).first()
    if not user_instance:
        return jsonify({'message': "User not registered. Please register first."}), 401
    # print("user_id =======", user_instance.id)
    
    tasks_data = data.get('tasks', [])
    add_tasks=[]

    for task in tasks_data:
        new_task =Task(title=task.get("title", "no title found"), status=task.get("status", "pending"))
        new_task.user = user_instance   # becuase of relationship of orm i defined right 
        add_tasks.append(new_task)


    db.session.add_all(add_tasks)    # becuase this is list of task
    db.session.commit()

    return {"message": f"{len(add_tasks)} tasks added for {username}"}, 201
'''
sample of data send to body through jwt authorization token
{
  "tasks": [
    {"description": "Study Flask", "status": "pending"},
    {"description": "Complete assignment", "status": "processing"},
    {"description": "Submit project", "status": "completed"}
  ]
}
'''


# Only admin can access this i.e. user_type = admin

@app.route('/tasks', methods=['GET'])
@jwt_required(user_type="admin")  
def get_tasks():

    user = request.user 

    if user['user_type'] != 'admin':
        return {"message": "Unauthorized: Admin access required."}, 403
    
    users = User.query.all()
    result = []

    for user in users:
        user_data = {
            "user_id": user.id,
            "username": user.username,  
            "tasks": [
                {"title": task.title, "status": task.status} 
                for task in user.tasks_list  
            ]
        }
        result.append(user_data)  

    return jsonify(result)




# Get data by ID

@app.route('/tasks/<int:ID>', methods=['GET'])
@jwt_required()  
def get_task(ID):
    user = request.user

    if user["user_id"] != ID:
        return {"message": "Unauthorized access"}, 403

    user_obj = User.query.get(ID)
    if not user_obj:
        return {"message": "User not found"}, 404
    
    # tasks = user_obj.tasks_list  --> directly access but limitation for filtering and pagination
    tasks = Task.query.filter_by(user_id=ID).all()

    result = {
        "username": user_obj.username,
        "tasks": [
            {
                "title": t.title,  
                "status": t.status
            } for t in tasks
        ]
    }

    return jsonify(result)

 

# Update task by premium user or special user so i.e. user_type = special

@app.route('/tasks/<int:ID>', methods=['PUT'])
@jwt_required(user_type="special")
def update_task(ID):

    user = request.user

    task = Task.query.get(ID)
    if not task:
        return jsonify({'error': 'Task not found'}), 404  


    if task.user_id != user['user_id'] and user['user_type'] != 'special':
        return {"message": "Unauthorized access to this task"}, 403  

    # Get the updated data from the request body
    data = request.json  # This will give us the JSON body in the request

    # Update task fields dynamically based on the incoming data

    if 'title' in data:
        task.title = data['title']
    if 'status' in data:
        task.status = data['status']

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200  # OK status code




# Delete task by special user i.e. user_type = special

@app.route('/tasks/<int:ID>', methods=['DELETE'])
@jwt_required(user_type="special")
def delete_tasks(ID):

    task = Task.query.get(ID)  
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    
    return jsonify({'error': 'task not found'}), 404


