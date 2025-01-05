import openai
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
openai.api_key = api_key

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
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []
if 'messages' not in st.session_state:
    st.session_state.messages = messages
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "user", "content": user_input})
st.session_state.messages.append({"role": "user", "content": user_input})
    
response = openai.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.messages,
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
st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

