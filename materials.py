from serpapi import GoogleSearch
import requests
import json

def scrape_youtube_videos(search_query):
    # Concatenate the search query with "ktu"
    search_string = search_query + " ktu"
    
    # Define the YouTube Data API search URL
    url = f"https://www.googleapis.com/youtube/v3/search?key=YourYoutubeAPI&q={search_string}&part=snippet&type=video&maxResults=5"
    
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
    

    note_data={}


    
    searchquery=search_query+"ktu notes"
    search = GoogleSearch({
        "q": searchquery, 
        "api_key": "YourAPI"
    })
    result = search.get_dict()

    # Retrieve the organic search results
    organic_results = result.get("organic_results", [])
    

    # Display the first 5 search results
    for index, organic_result in enumerate(organic_results[:5], start=1):
        title = organic_result.get("title")
        link = organic_result.get("link")
        note_data[title]=link
        

    # Return the video data (titles and URLs)
    return video_data,note_data

