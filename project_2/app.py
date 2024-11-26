from flask import request, jsonify, Flask

app =Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build an API", "done": False}
]

#get all task
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"task": tasks}), 200

#getting single task using ID
@app.route('/tasks/<int:id>', methods=["GET"])
def get_task(id):
    for task in tasks:
        if task["id"] == id:
            return jsonify(task)
    return jsonify("Not Found"), 404


#creating new task
@app.route('/tasks/add', methods=["POST"])
def create_task():
    data = request.json
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": data["done"]
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

#updating task
@app.route('/tasks/<int:id>', methods=['POST'])
def update_task(id):
    for task in tasks:
        if task["id"] == id:
            task["title"] = request.json.get("title", task["title"])
            return jsonify(task), 201
    return jsonify("Not Found"), 404

#deleting task
@app.route('/tasks/<int:id>', methods=["DELETE"])
def del_task(id):
    task = next((task for task in tasks if task["id"] == id), None)
    
    if task == None:
        return jsonify("NOT FOUND")
    
    tasks.remove(task)
    return jsonify("Successfully removed")

if __name__ == '__main__':
    app.run(debug=True)