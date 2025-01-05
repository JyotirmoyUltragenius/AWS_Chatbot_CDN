import streamlit as st
import openai
import json
from datetime import datetime

api_key = str(st.secrets["API_KEY"].strip())
if api_key:
    print(f"API Key: {api_key}")import openai
import json
import streamlit as st
from datetime import datetime

api_key = str(st.secrets["API_KEY"].strip())
if api_key:
    print(f"API Key: {api_key}")
    # Use the API key
else:
    print("API Key not found!")

# Initialize OpenAI API key
openai.api_key =api_key
functions = [
    {
        "name": "collect_cdn_technical_info",
        "description": "Collects technical parameters related to CDN optimization requirements.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain_name": {"type": "string", "description": "Primary domain name for CDN deployment"},
                "traffic_volume": {
                    "type": "string",
                    "description": "Expected traffic volume (e.g., low, medium, high, or specific Mbps/Gbps)"
                },
                "cache_policy": {
                    "type": "string",
                    "enum": ["Full Cache", "Partial Cache", "No Cache"],
                    "description": "Preferred cache policy for CDN"
                },
                "geographical_coverage": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Regions or countries where CDN optimization is required"
                },
                "origin_server_type": {
                    "type": "string",
                    "enum": ["Cloud Storage", "On-Premise", "Hybrid", "Other"],
                    "description": "Type of origin server hosting content"
                },
                "protocol_support": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["HTTP", "HTTPS", "QUIC", "WebSockets"]},
                    "description": "Protocols to be supported by the CDN"
                },
                "security_requirements": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["DDoS Protection", "WAF", "TLS/SSL", "Bot Protection"]},
                    "description": "Security features required for CDN"
                },
                "latency_tolerance": {
                    "type": "string",
                    "enum": ["Low", "Medium", "High"],
                    "description": "Tolerance level for latency in content delivery"
                },
                "content_type": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["Static", "Dynamic", "Streaming", "APIs"]},
                    "description": "Types of content being delivered via CDN"
                },
                "compression_support": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["Gzip", "Brotli", "None"]},
                    "description": "Compression methods required for content optimization"
                },
                "log_and_analytics": {
                    "type": "boolean",
                    "description": "Whether detailed logging and analytics are required"
                },
                "cdn_provider_preference": {
                    "type": "string",
                    "description": "Preferred CDN provider, if any"
                },
                "additional_requirements": {
                    "type": "string",
                    "description": "Any additional technical requirements for the CDN setup"
                }
            },
            "required": [
                "domain_name",
                "traffic_volume",
                "cache_policy",
                "geographical_coverage",
                "origin_server_type",
                "protocol_support",
                "security_requirements",
                "latency_tolerance",
                "content_type",
                "compression_support",
                "log_and_analytics"
            ]
        }
    }
]

# Define system message
messages = [
    {
        "role": "system",
        "content": "You are an intelligent data-collecting chatbot designed to interact with users to gather information on at least 10 key parameters. Guide the user through a structured conversation, ensuring that all necessary details are collected. The final output should be formatted in JSON, optimized for use with Amazon CloudFront CDN."
    }
]

st.title("CDN Optimization Chatbot")
st.write("Chat with this AI to collect CDN deployment requirements.")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:
    messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=functions
    )
    
    message_dict = response.choices[0].message.model_dump()
    
    if message_dict.get("function_call") is not None:
        function_call = message_dict["function_call"]
        if function_call["name"] == "collect_cdn_technical_info":
            user_info = json.loads(function_call["arguments"])
            
            output = {
                "user_info": user_info,
                "cdn_meta": {
                    "cdn_provider": "Amazon CloudFront",
                    "distribution_id": "ABC123XYZ",
                    "status": "Success",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
            response_text = json.dumps(output, indent=4)
        else:
            response_text = "Function call not recognized."
    else:
        response_text = message_dict["content"]
    
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Use the API key
else:
    print("API Key not found!")

# Initialize OpenAI API key
openai.api_key = api_key


def get_chatgpt_response(user_input):
    """Fetch response from ChatGPT API based on user input."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": '''You are an intelligent data-collecting chatbot designed to interact with users to gather information on at least 10 key parameters. You will guide the user through a structured conversation, ensuring that all necessary details are collected. The final output should be formatted in JSON, optimized for use with Amazon CloudFront CDN.

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
                   ```
                ''',
            },
            {"role": "user", "content": user_input},
        ],
    )
    return response.choices.message.content 


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
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        }
        json_str = json.dumps(output_json, indent=4)
        st.download_button(
            label="Download JSON File",
            data=json_str,
            file_name="chatbot_response.json",
            mime="application/json",
        )


if __name__ == "__main__":
    collect_user_info()
