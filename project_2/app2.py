from flask import Flask, jsonify, request

from model import Task
from db import db

app = Flask(__name__)

# configure sqliteDatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/Desktop/flask_project/project_2/tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
db.init_app(app)


#creating the db tables 
@app.before_request
def create_tables():
    db.create_all()

#get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    
    return jsonify(task_list)

# creating Tasks
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    new_task = Task(
        title=data["title"],
        done=data["done"]
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201
        

#get a task by ID
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"Error": "Not Found"})
    return jsonify(task.to_dict())


#updating a task
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"Error": "Not found"}), 404
    
    data = request.json
    task.title = data.get('title', task.title)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify(task.to_dict()), 200

#delete a task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def del_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"Error": "Not found"}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)