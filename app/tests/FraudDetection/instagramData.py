from flask import Flask, render_template, request ,jsonify
from app import app
import requests
import os
import json
from app import app
from io import BytesIO


@app.route('/detect_fraud_profile', methods=['POST'])
def detect_fraud_profile():
    # Parse JSON from request

    data = request.get_json()
    username = data.get('username') # Extract 'username' from the JSON payload
    print(f"Instagram Data {username} started 🌿🌿🌿")
    if not username:
        return jsonify({'error': 'Username is required.'}), 400

    # Call your function with the username
    user_information_final(username)

    return jsonify({'result': f"Data for '{username}' has been successfully processed."})


# fetch the user information
def get_user_data(username):
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"
    querystring = {"username_or_id_or_url": username}
    headers = {
    'x-rapidapi-key': "2e441ee7e4mshe67c27c1cc16b20p1a6c08jsn304da69448df",
    'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    # fetching the data from the api
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            return data
        else:
            return {"error": "Invalid response structure from API."}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None


# save the image to the device
def save_profile_picture(url, username):
    img_data = requests.get(url).content

    base_dir = os.path.join(os.getcwd(), username)
    os.makedirs(base_dir, exist_ok=True)

    profile_dir = os.path.join(base_dir, f"{username}_profile")
    os.makedirs(profile_dir, exist_ok=True)

    img_filename = 'profile_pic.jpg'

    img_path = os.path.join(base_dir,profile_dir, img_filename) 
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    with open(img_path,'wb') as file:
        file.write(img_data)
     

    return img_path


# Function to download the image and save it locally
def save_post_picture(img_url, username, post_index):
    # Get the image content


    base_dir = os.path.join(os.getcwd(), username)
    os.makedirs(base_dir, exist_ok=True)
    post_dir = os.path.join(base_dir, f"{username}_posts")
    os.makedirs(post_dir, exist_ok=True)

    img_data = requests.get(img_url).content
    img_filename = f'{username}_post_{post_index + 1}.jpg'
    img_path = os.path.join(base_dir,post_dir , img_filename)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)  
    with open(img_path, 'wb') as file:
        file.write(img_data)
        
    # Return the relative path for use in the template
    return img_path

def get_recent_posts(username):
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1.2/posts"
    querystring = {"username_or_id_or_url": username}
    headers = {
        'x-rapidapi-key': "2e441ee7e4mshe67c27c1cc16b20p1a6c08jsn304da69448df",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and 'items' in data['data']:
            posts = data['data']['items'][:10]
            for post_index, post in enumerate(posts):
                # Process posts
                post['caption_text'] = post.get('caption', {}).get('text', 'No caption text available')
                post['created_at'] = post.get('created_at', 'Unknown time')
                image_versions = post.get('image_versions', {}).get('items', [])
                post['image_url'] = image_versions[0]['url'] if image_versions else None
                if post['image_url']:
                    post['image_path'] = save_post_picture(post['image_url'], username, post_index)
            return posts
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recent posts: {e}")
        return []


def profile_pic(username):
    user_data = get_user_data(username)
    profile_pic_url = user_data['data']['profile_pic_url']
    username = user_data['data']['username']
    profile_pic_path = save_profile_picture(profile_pic_url, username)
    return profile_pic_path



def user_information_final(username):
    user_data = get_user_data(username)
    if not user_data or 'error' in user_data:
        print(f"Error fetching user data for {username}")
        return {"error": f"Unable to fetch data for username: {username}"}

    base_dir = os.path.join(os.getcwd(), username)
    os.makedirs(base_dir, exist_ok=True)
    # caption
    caption_dir = os.path.join(base_dir, f"{username}_captions")
    os.makedirs(caption_dir, exist_ok=True)
    # profile
    profile_dir = os.path.join(base_dir, f"{username}_profile")
    os.makedirs(profile_dir, exist_ok=True)

    data = user_data.get('data', {})
    user_info = {
        "Username": data.get("username", "N/A"),
        "Name": data.get("full_name", "N/A"),
        "Bio": data.get("biography", "N/A"),
        "Followers": data.get("follower_count", 0),
        "Following": data.get("following_count", 0),
        "NumberOfPosts": data.get("media_count", 0),
        "Verified": "Yes" if data.get("is_verified") else "No",
        "AccountPrivacy": "Private" if data.get("is_private") else "Public",
        "Profile Picture Path": profile_pic(username),
        "Socialmediasite": "Instagram",
        "Posts": []
    }

    try:
        posts = get_recent_posts(username)
        user_info["Posts"] = posts
    except Exception as e:
        print(f"Error processing posts for {username}: {e}")

    try:
        captions = [{"PostNumber": i + 1, "Caption": post["caption_text"], "Upload Time": post["created_at"]}
                    for i, post in enumerate(posts)]
    except Exception as e:
        print(f"Error processing captions for {username}: {e}")
        captions = []

    profile_info_path = os.path.join(profile_dir, "profile_data.json")
    with open(profile_info_path, "w") as profile_info_file:
        json.dump(user_info, profile_info_file, indent=4)

    captions_path = os.path.join(caption_dir, "captions.json")
    with open(captions_path, "w") as captions_file:
        json.dump(captions, captions_file, indent=4)

    return user_info




# @app.route("/instagram", methods=["GET","POST"])
# def index():
#     if request.method == "POST":
#         username = request.form["username"]

#         # fetch user data
#         user_data = get_user_data(username)
        
#         if user_data:
#             profile_pic_url = user_data['data']['profile_pic_url']
#             username = user_data['data']['username']
#             # save the profile pic locally
#             profile_pic_path = save_profile_picture(profile_pic_url, username)
#             # fetch the recent posts
#             posts  = get_recent_posts(username)
#             return render_template("index.html",data=user_data, profile_pic =  profile_pic_path , posts = posts)
#         else:
#             return f"Error:unable to fetch the data for the {username}",400
        
#     return render_template("index.html", data=None,profile_pic= None, posts = None )
        
if __name__ == "__main__":
    app.run(debug=True)

