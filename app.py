import streamlit as st
import openai
import json
import os

api_key = str(st.secrets["API_KEY"].strip())
if api_key:
    print(f"API Key: {api_key}")
    # Use the API key
else:
    print("API Key not found!")

# Initialize OpenAI API key
openai.api_key =api_key

# Function to call ChatGPT API
def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a CloudFront configuration assistant."},
                  {"role": "user", "content": prompt}]
    )
  return response.choices[0].message.content 

# Initialize session state if not already done
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
    st.session_state["current_question"] = "What will you be using CloudFront for?"

# Define question dictionary
question_flow = {
    "What will you be using CloudFront for?": {
        "Static Content": "Where is your static content hosted? (S3, EC2, on-prem, other cloud provider)",
        "Dynamic Content": "What type of dynamic content will you serve? (API responses, personalized content, database queries)",
        "Streaming": "Are you delivering live or on-demand streaming? (Live, On-Demand)",
        "Mixed": "Do you want to configure separate settings for different content types? (Yes/No)"
    },
    "Where is your static content hosted? (S3, EC2, on-prem, other cloud provider)": {
        "S3": "Do you need Origin Access Control (OAC)? (Yes/No)",
        "EC2": "Do you want to enable automatic scaling for EC2? (Yes/No)"
    },
    "What type of dynamic content will you serve? (API responses, personalized content, database queries)": {
        "API responses": "Do you need caching for API responses? (Yes/No)",
        "Personalized content": "Do you require session stickiness? (Yes/No)"
    },
    "Are you delivering live or on-demand streaming? (Live, On-Demand)": {
        "Live": "Do you need low-latency streaming? (Yes/No)",
        "On-Demand": "Do you require signed URLs for content security? (Yes/No)"
    },
    "Do you need an SSL certificate? (Yes/No)": {
        "Yes": "Would you like to use AWS Certificate Manager (ACM) for SSL provisioning? (Yes/No)"
    },
    "Do you want to enable gzip/brotli compression? (Yes/No)": {
        "Yes": "What compression formats do you prefer? (Gzip, Brotli, Both)"
    },
    "Do you need IP or region-based access restrictions? (Yes/No)": {
        "Yes": "Please specify the IPs or regions to allow/block."
    },
    "Do you need AWS WAF protection? (Yes/No)": {
        "Yes": "Would you like predefined security rules or custom rule configuration? (Predefined, Custom)"
    },
    "Do you want to enable access logging? (Yes/No)": {
        "Yes": "Please provide the S3 bucket name for storing logs."
    },
    "Do you want cost optimization suggestions? (Yes/No)": {
        "Yes": "Should we prioritize fewer edge locations to reduce costs? (Yes/No)"
    },
    "Do you want to configure custom error pages? (Yes/No)": {
        "Yes": "Please specify the URLs for different error codes (404, 500, etc.)."
    }
}

# Streamlit UI
st.title("CloudFront Configuration Chatbot")
st.write("This chatbot will dynamically guide you through CloudFront configuration.")

question = st.session_state["current_question"]
user_input = st.text_input(question, key="current")

if st.button("Next") and user_input:
    # Store response
    st.session_state["responses"][question] = user_input
    
    # Determine next question dynamically
    if question in question_flow and user_input in question_flow[question]:
        st.session_state["current_question"] = question_flow[question][user_input]
    else:
        st.session_state["current_question"] = "Would you like to optimize your CloudFront configuration further? (Yes/No)"
    
    st.experimental_rerun()
else:
    st.write("### Configuration Summary:")
    st.json(st.session_state["responses"])
    
    # Save responses to JSON file
    with open("cloudfront_config.json", "w") as f:
        json.dump(st.session_state["responses"], f, indent=4)
    st.success("Configuration saved as cloudfront_config.json")

# To run locally, use: `streamlit run app.py`
