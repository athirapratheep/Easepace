import requests
import json

def scrape_youtube_videos(search_query):
    # Concatenate the search query with "ktu"
    search_string = search_query + " ktu"
    
    # Define the YouTube Data API search URL
    url = f"https://www.googleapis.com/youtube/v3/search?key=AIzaSyBwuu3UjYHCMt9AsE11EK-yWp7UB2wnIHo&q={search_string}&part=snippet&type=video&maxResults=5"
    
    # Make a GET request to the API
    response = requests.get(url)
    
    # Parse the JSON response
    data = json.loads(response.text)
    
    # Extract the video URLs and titles from the response
    video_data = {}
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_title = item["snippet"]["title"]
        video_data[video_title] = video_url
    
    # Return the video data (titles and URLs)
    return video_data

