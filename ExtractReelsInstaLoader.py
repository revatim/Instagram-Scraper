import instaloader
import pandas as pd

L = instaloader.Instaloader()
user = "_.theukiyostore"
# Load the profile for the user "instagram"
profile = instaloader.Profile.from_username(L.context, user)

# Get the latest posts for the profile
all_posts = profile.get_posts()

# Loop through the posts and check if they are reels
reels = []
posts = []
for post in all_posts:
    if post.typename == "GraphVideo" or post.typename == "Reels":
        reels.append(post)
    else:
        posts.append(post)

post_to_csv = []
reel_to_csv = []
# Loop through the reels and print their captions and URLs
for reel in reels:
    dict = {
        "caption": reel.caption,
        "url": reel.video_url,
        "caption_hashtags": ', '.join(reel.caption_hashtags),
        "shortcode": reel.shortcode
    }
    reel_to_csv.append(dict)
    print(f"Url: {reel.video_url}")

# Iterate through the posts and print the URL and caption
for post in posts:
    dict = {
        "caption":  reel.caption,
        "url": reel.url
    }
    post_to_csv.append(dict)

post_df = pd.DataFrame(post_to_csv)
post_df.to_csv(user + " posts.csv")
reels_df = pd.DataFrame(reel_to_csv)
reels_df.to_csv(user + " reels.csv")
