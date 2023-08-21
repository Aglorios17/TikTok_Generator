import os
from pytube import YouTube
import sys
from dotenv import load_dotenv
from unidecode import unidecode

def Download(link, output_directory):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        video_title = unidecode(youtubeObject.title) + ".mp4"
        # Set the file path to save the video
        file_path = f"{output_directory}/{video_title}"
        video = youtubeObject.download(output_path=output_directory, filename=video_title)
    except:
        print("An error has occurred")
        return None
    print("Download is completed successfully")
    return video  # Return the path to the downloaded file

def Downloader(link, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return (Download(link, output_directory))

def main():
    for i in range(1, len(sys.argv)):
        Download(sys.argv[i], "./background_videos")

if __name__ == "__main__":
    main()