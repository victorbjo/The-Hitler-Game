from flask import Flask, request, jsonify
from flask_cors import CORS
from wiki import find_goal
from time import time
app = Flask(__name__)
CORS(app)

@app.route('/find_goal_api', methods=['POST'])
def find_goal_api():
    data = request.get_json()
    start_link = data["start_link"]
    goal = data["goal"]
    start_time = time()
    request_dict = find_goal(start_link, goal)
    request_dict["time"] = round(time() - start_time, 3)
    return jsonify(request_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)