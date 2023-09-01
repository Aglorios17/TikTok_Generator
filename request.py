import requests
from dataclasses import dataclass
import sys
@dataclass
class YouTubeVideo:
    url: str
    start_time: int
    end_time: int
    channel: str
    hashtag: str
    message: str

# Define the data for the YouTubeVideo instance
video_data = {
    "url": "https://www.youtube.com/watch?v=Mw2hjvuaiV4&ab_channel=LeoSucculent",
    "start_time": "0",
    "end_time": "0",
    "hashtag": "pourtoi viral LeoSucculent trending animation fyp youtube",
    "message": "Tout est reel! haha lol mdr test etes tes ceci est une phrase super longue"
}

if sys.argv[1] == "POST":
# Send a POST request to your Flask API to create the YouTubeVideo instance
    response = requests.post("http://localhost:5000/add_new_video/data", json=video_data)
elif sys.argv[1] == "GET":
    response = requests.get("http://localhost:5000/create_new_video/data")

if response.status_code == 201:
    print("YouTubeVideo created successfully")
else:
    print("Failed to create YouTubeVideo")