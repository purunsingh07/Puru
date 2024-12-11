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
    You are an AI model that detects the given  is profile fake or not based on the number of followers , following , bio , verified or not, username trying to impersonate some famous user names , from the post's caption events in real-time or in the past if the data , number of posts etc. You will be provided with the input of users social media profile information and posts and your goal is to respond with a structured solution in this format:
    <div class="final_output">
        <h3> Fake post detection:<h3>
        <table>
            <tr>
                <td>Fake or propaganda information</td>
                <td><span class="propaganda">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Extremist</td>
                <td><span class="Extremist">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Spam message</td>
                <td><span class="Spam">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Violent or hate speech or toxic</td>
                <td><span class="hate">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Impersonate account</td>
                <td><span class="Impersonate">(percentage out of 100)</span></td>
            </tr>
            <tr>
                <td>Incomplete profile</td>
                <td><span class="Incomplete">(percentage out of 100)</span></td>
            </tr>
        </table>
        <li>Percentage of risk :<span class="risk"> (percentage out of 100)</span></li>
        <strong>Reason:</strong>
            If the profile belongs to any of these 6 categories then why just in 10-20 words.
        <strong>Conclusion: </strong>
            Just one precise summary point.
            
            </div>
"""

# Function to get the response
@app.route('/openai', methods=['POST'])
def get_post_response_json():
    print("Model testing started 🌿")
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
        print("Response:", response_content)
        
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
