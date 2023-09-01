import os
from flask import Flask, jsonify, request
import main

# Create a Flask application
app = Flask(__name__)
#app.config['TIMEOUT'] = 999999999  # Set the timeout to 60 seconds

# Define a route for the root URL
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"

# Define a route to create a new item
@app.route("/add_new_video/<name>", methods=["POST"])
def create_item(name):
    try:
        data = request.json
        
        # Open the file for writing
        with open(f"{name}.csv", "w") as file:
            # Write each text element from the list to the file
            file.write(f'{data["url"]}|{data["start_time"]}|{data["end_time"]}| {data["hashtag"]}| {data["message"]}')
        return jsonify({"message": "YouTubeVideo csv created successfully"}), 201
    except:
        return jsonify({"message": "Failed to create YouTubeVideo csv"}), 500

@app.route("/create_new_video/<name>", methods=["GET"])
def create_video(name):
    if main.tiktok_automated(f"{name}.csv", "1") is None:
        return jsonify({"message": "Failed to create YouTubeVideo"}), 500
    else:
        #if os.path.exists("data.csv"):
            # Remove the file
        #    os.remove("data.csv")
        return jsonify({"message": "YouTubeVideo created successfully"}), 201

#
# NOT IN USE OR WORKING
#
@app.route("/post_new_video", methods=["GET"])
def post_video():
    if main.tiktok_automated("data.csv", "0") is None:
        return jsonify({"message": "Failed to post YouTubeVideo"}), 500
    else:
        return jsonify({"message": "YouTubeVideo posted successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)