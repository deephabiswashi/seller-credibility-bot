import requests
from bs4 import BeautifulSoup
from facebook_scraper import get_posts
import instaloader
import re

def fetch_data(url: str) -> str:
    """
    Fetch the seller data from the given URL.
    For demonstration, this function supports Facebook and Instagram.
    For other URLs, it fetches the raw HTML content.
    """
    if "facebook.com" in url:
        return fetch_facebook_data(url)
    elif "instagram.com" in url:
        return fetch_instagram_data(url)
    else:
        return fetch_generic_data(url)

def fetch_generic_data(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract visible text from the page
            texts = soup.stripped_strings
            content = " ".join(texts)
            return content
        else:
            return f"Error: Unable to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return "Exception occurred: " + str(e)

def fetch_facebook_data(url: str) -> str:
    """
    Fetch data from a Facebook seller page using facebook_scraper.
    """
    try:
        # Extract username or page ID from the URL
        pattern = r"facebook\.com/([^/?]+)"
        match = re.search(pattern, url)
        if match:
            page_name = match.group(1)
        else:
            return "Error: Unable to extract Facebook page name."
        
        posts = get_posts(page_name, pages=1, extra_info=True)
        content = ""
        for post in posts:
            content += post.get("post_text", "") + " "
        return content
    except Exception as e:
        return "Exception occurred while fetching Facebook data: " + str(e)

def fetch_instagram_data(url: str) -> str:
    """
    Fetch data from an Instagram seller profile using instaloader.
    """
    try:
        # Extract username from URL
        pattern = r"instagram\.com/([^/?]+)"
        match = re.search(pattern, url)
        if match:
            username = match.group(1)
        else:
            return "Error: Unable to extract Instagram username."
        
        L = instaloader.Instaloader(
            download_pictures=False, 
            download_video_thumbnails=False, 
            save_metadata=False, 
            download_comments=False
        )
        profile = instaloader.Profile.from_username(L.context, username)
        content = profile.biography + " "
        # Optionally add captions from recent posts
        posts = profile.get_posts()
        count = 0
        for post in posts:
            if count >= 5:
                break
            content += post.caption or ""
            count += 1
        return content
    except Exception as e:
        return "Exception occurred while fetching Instagram data: " + str(e)
