from flask import Flask, request, Response
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import time
import random

# Load environment variables
load_dotenv()

# Get YouTube API key from .env file
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    # Rate limiting: Wait for a random time between 2 to 6 seconds before processing
    sleep_time = random.uniform(2, 6)
    time.sleep(sleep_time)
    
    video_url = request.json.get('video_url')
    transcript_text = ""
    video_id = ""

    try:
        if "v=" in video_url:
            video_id = video_url.split("v=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            for entry in transcript:
                transcript_text += entry['text'] + ' '
            
            # Create a text file response
            response = Response(transcript_text, content_type='text/plain; charset=utf-8')
            response.headers["Content-Disposition"] = f"attachment; filename={video_id}.txt"
            
            return response
        else:
            return {"error": "Invalid YouTube URL. Please make sure you've entered the correct video link."}, 400
    except Exception as e:
        return {"error": f"Oops! Something went wrong while fetching the transcript. Please try again later. Detailed error: {str(e)}"}, 400

if __name__ == '__main__':
    app.run(debug=True)
