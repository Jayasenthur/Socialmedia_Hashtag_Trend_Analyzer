import streamlit as st
import requests
import json
import uuid

# Define the API Gateway URL (replace with your actual URL)
insert_post_api_url = 'https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/prod/processPost'
fetch_post_api_url='https://hvrbau1nj1.execute-api.us-east-1.amazonaws.com/dev/trendingHashtags'

# Streamlit app UI
st.title("Social Media Post Analyzer")

# Post Composition
st.header("Compose a Post")
post_content = st.text_area("Write your post with hashtags here (e.g., Learning #Python is fun!)")

if st.button("Post"):
    if post_content.strip():
        payload = {'post_content': post_content}
        headers = {'Content-Type': 'application/json'}

        try:
            # Send POST request to the API Gateway endpoint
            response = requests.post(insert_post_api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                post_id = response_data.get("PostId", "N/A")
                #st.success(f"Post submitted successfully! Post ID: {post_id}")
                st.success("Post submitted successfully!")

                
            else:
                # Display detailed error from the API response
                try:
                    error_message = response.json().get('error', response.text)
                except json.JSONDecodeError:
                    error_message = response.text
                st.error(f"Failed to submit post: {error_message}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the API: {str(e)}")
    else:
        st.warning("Please write a post before submitting.")

# Show Trending Hashtags
st.header("Trending Hashtags")
if st.button("Show Trending Hashtags"):
    try:
        # Fetch trending hashtags from the API Gateway endpoint
        trending_response = requests.get(fetch_post_api_url)

        if trending_response.status_code == 200:
            # Parse the response for hashtags
            try:
                hashtags = trending_response.json().get("trending_hashtags", [])
            except json.JSONDecodeError:
                st.error("Error parsing response from the server.")
                hashtags = []

            if hashtags:
                st.write("### Current Trending Hashtags")
                for item in hashtags:
                    st.write(f"#{item['Hashtag']}: {item['count']} mentions")
            else:
                st.write("No trending hashtags found.")
        else:
            st.error(f"Failed to fetch trending hashtags: {trending_response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {str(e)}")