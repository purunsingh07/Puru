from flask import Flask, render_template, request ,jsonify
import openai
import json
from app import app
import os
import requests
# Set your OpenAI API key
#  # Replace with your actual API key
# Input query
# query = """
# cute_ishu_jattni
# 65 posts
# ITBP officer 🤟🤟
# ITBP officer 🤟 No love No tanssion 🤟🙏
# This account is private
# Follow to see their photos and videos.
# """

# ------------------------------------------------------------
# Providing the system prompt
# ------------------------------------------------------------
system_prompt = """
    You are an AI model that detects the given  is profile fake or not based on the number of followers , following , bio , verified or not, username trying to impersonate some famous user names , from the post's caption events in real-time or in the past if the data , number of posts etc. You will be provided with the input of users social media profile information and posts and your goal is to respond with a structured solution in json format:
    - Fake post detection:
        1) Fake or propaganda information: (percentage out of 100)
        2) Extremist: (percentage out of 100)
        3) Spam message: (percentage out of 100)
        4) Violent or hate speech or toxic: (percentage out of 100)
        5) Impersonate account: (percentage out of 100)
        6) Incomplete profile : (percentage out of 100)
    Reason:
        If the profile belongs to any of these 6 categories then why just in 10-20 words.
    Conclusion: 
        Just one precise summary point.
        Percentage pf risk : (percentage out of 100)
"""

# Function to get the response
@app.route('/openai', methods=['POST'])
def get_post_response_json():
    try:
        # Retrieve JSON data from the request
        query = request.get_json()
        user_info = query.get('userinformation', {})
        username = user_info["ProfileInfo"]["Username"]
        print("username from open api:",username)

        # Make OpenAI API call
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(user_info)}
            ]
        )
        
        # Extract response content
        response_content = response["choices"][0]["message"]["content"]
        # print("OpenAI Response:", response_content)
        
        base_dir = os.path.join(os.getcwd(), username)
        os.makedirs(base_dir, exist_ok=True)

        profile_dir = os.path.join(base_dir, f"{username}_profile")
        os.makedirs(profile_dir, exist_ok=True)

        output_path = os.path.join(profile_dir, "output_data.json")
        with open(output_path, "w") as profile_info_file:
            json.dump(response_content, profile_info_file, indent=4)


        return jsonify({"result": response_content})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    # return jsonify({'result': f"Data for '{username}' has been successfully processed."})


# Fetch and print the response
# try:
#     response = get_post_response_json(query)
#     response_content = response["choices"][0]["message"]["content"]  # Extract response content
#     print(response_content)  # Print the raw response
# except Exception as e:
#     print(f"Error: {e}")



# - Fake post detection:
#     1) Fake or propaganda information: 95%
#     2) Extremist: 5%
#     3) Spam message: 20%
#     4) Violent or hate speech or toxic: 0%

# Reason:
#     1) The post is primarily categorised as fake because there is no scientific evidence or credible research supporting that a synthetic material can make one immortal. Secondly, the idea of the medicine being created by the mass killing of humans is outrageous, unethical, and illegal. This suggests the spread of fear and misinformation.
#     2) Extremist: 5%
#     3) Spam message: 20%
#     2) Extremist: 5%
#     3) Spam message: 20%
#     2) Extremist: 5%
#     2) Extremist: 5%
#     3) Spam message: 20%
#     4) Violent or hate speech or toxic: 0%

#     4) Violent or hate speech or toxic: 0%

# Reason:
#     1) The post is primarily categorised as fake because there is no scientific evidence or credible research supporting that a synthetic material can make one immortal. Secondly, the idea of the medicine being created by the mass killing of humans is outrageous, unethical, and illegal. This suggests the spread of fear and misinformation.  
#     2) The post isn't particularly extremist, but it divides people based on wealth which can potentially incite class conflicts, therefore the low score.
#     3) The element of spam is noticeable due to the sensationalistic nature of the post. The assertion of exclusivity and immortality could be a tactic to attract attention or clicks, often seen in spam messages.
#     4) The post does not contain explicitly violent, hate speech or toxic content.

# Conclusion: The post is largely a fake news or misinformation containing sensational claims without any scientific credibility and possibly designed to attract attention or incite unnecessary fear and discord.