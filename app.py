import streamlit as st
import openai
import json
from datetime import datetime

api_key = str(st.secrets["API_KEY"].strip())
if api_key:
    print(f"API Key: {api_key}")
    # Use the API key
else:
    print("API Key not found!")

# Initialize OpenAI API key
openai.api_key =api_key


def get_chatgpt_response(user_input):
    """Fetch response from ChatGPT API based on user input."""
    response = openai.chats.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": '''You are an intelligent data-collecting chatbot designed to interact with users to gather information on at least 10 key parameters. You will guide the user through a structured conversation, ensuring that all necessary details are collected. The final output should be formatted in JSON, optimized for use with Amazon CloudFront CDN.

                                            ### Task Breakdown:
                                        1. **Collect Information**: Ask the user for the following parameters systematically:
                                           - Full Name
                                           - Email Address
                                           - Phone Number
                                           - Location (City, State, Country)
                                           - Preferred Language
                                           - Purpose of Inquiry
                                           - Preferred Contact Method (Email/Phone)
                                           - Budget Range (if applicable)
                                           - Industry/Field of Work
                                           - Additional Custom Input (Optional)
                                        
                                        2. **User-Friendly Interaction**:
                                           - Guide the user conversationally, asking one question at a time.
                                           - Validate responses where necessary (e.g., email format, phone number format).
                                           - Allow corrections if the user wants to change any input.
                                        
                                        3. **Generate Output in Amazon CloudFront JSON Format**:
                                           - Ensure the collected data is structured as JSON and formatted for CloudFront.
                                           - Use the following JSON structure:
                                           ```json
                                           {
                                              "user_info": {
                                                 "full_name": "John Doe",
                                                 "email": "john.doe@example.com",
                                                 "phone": "+1-555-123-4567",
                                                 "location": {
                                                    "city": "New York",
                                                    "state": "NY",
                                                    "country": "USA"
                                                 },
                                                 "language": "English",
                                                 "inquiry_purpose": "Product Inquiry",
                                                 "contact_method": "Email",
                                                 "budget_range": "$500 - $1000",
                                                 "industry": "Technology",
                                                 "additional_info": "Looking for cloud hosting services"
                                              },
                                              "cdn_meta": {
                                                 "cdn_provider": "Amazon CloudFront",
                                                 "distribution_id": "ABC123XYZ",
                                                 "status": "Success",
                                                 "timestamp": "2025-01-05T12:00:00Z"
                                              }
                                           }
                                        "}''',
                {"role": "user", "content": user_input}]
                                            )
    return response["choices"][0].message.content
def collect_user_info():
    """Streamlit app interface to collect user input and display ChatGPT response."""
    st.title("🤖 AI Chatbot - Data Collection")
    st.write("Please provide the required information below:")
    
    user_input = st.text_area("Enter your details here:")
    
    if st.button("Submit Information"):
        chatgpt_output = get_chatgpt_response(user_input)
        
        # Display response
        st.success("✅ Chatbot Response:")
        st.write(chatgpt_output)
        
        # Provide JSON download button
        output_json = {
            "user_input": user_input,
            "chatbot_response": chatgpt_output,
            "cdn_meta": {
                "cdn_provider": "Amazon CloudFront",
                "distribution_id": "ABC123XYZ",
                "status": "Success",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        json_str = json.dumps(output_json, indent=4)
        st.download_button(
            label="Download JSON File",
            data=json_str,
            file_name="chatbot_response.json",
            mime="application/json"
        )

if __name__ == "__main__":
    collect_user_info()
