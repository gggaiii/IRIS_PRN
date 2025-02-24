'''
Copyright (c) 2025 - Yuhang Xie
'''

from bs4 import BeautifulSoup
import json

# Function to read text from a file
def read_txt(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

# Function to extract user name
def extract_user_name(tweet):
    user_name = tweet.find("div", {"data-testid": "User-Name"})
    return user_name.get_text(strip=True) if user_name else "Not Found"

# Function to extract user handle
def extract_user_handle(tweet):
    user_handle = tweet.find("div", string=lambda text: text and text.startswith("@"))
    return user_handle.get_text(strip=True) if user_handle else "Not Found"

# Function to extract tweet text
def extract_tweet_text(tweet):
    tweet_text = tweet.find("div", {"data-testid": "tweetText"})
    return tweet_text.get_text(strip=True) if tweet_text else "Not Found"

# Function to extract post date
def extract_post_date(tweet):
    post_date = tweet.find("time")
    return post_date.get_text(strip=True) if post_date else "Not Found"

# Function to extract views
def extract_views(tweet):
    views_element = tweet.find("a", {"aria-label": True}, string=lambda text: text and "views" in text.lower())
    return views_element.get("aria-label", "").split()[0] if views_element else "Not Found"

# Function to extract engagement stats
def extract_engagement_stats(tweet):
    stats = {"Replies": "Not Found", "Reposts": "Not Found", "Likes": "Not Found", "Views": extract_views(tweet)}
    buttons = tweet.find_all("button", {"aria-label": True})
    for button in buttons:
        label = button.get("aria-label")
        if label:
            for key in ["Replies", "Reposts", "Likes"]:
                if key.lower() in label.lower():
                    stats[key] = label.split()[0]
    return stats

# Function to extract embedded media
def extract_embedded_media(tweet):
    media = tweet.find("video") or tweet.find("img")
    return media["poster"] if media and media.name == "video" else media["src"] if media else "Not Found"

# Function to extract all tweets from the HTML
def extract_all_tweets(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tweet containers (articles)
    tweets = soup.find_all("article", {"data-testid": "tweet"})
    
    tweet_data_list = []
    for tweet in tweets:
        tweet_data = {
            "User Name": extract_user_name(tweet),
            "Handle (@username)": extract_user_handle(tweet),
            "Tweet Text": extract_tweet_text(tweet),
            "Post Date": extract_post_date(tweet),
            "Engagement Stats": extract_engagement_stats(tweet),
            "Embedded Media": extract_embedded_media(tweet),
        }
        tweet_data_list.append(tweet_data)
    
    return tweet_data_list

# Read the HTML file
html_content = read_txt('text.txt')

# Extract all tweets
tweets_data = extract_all_tweets(html_content)

# Save extracted data to JSON
output_file = "extracted_tweets.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)

# Display the JSON file path
output_file
