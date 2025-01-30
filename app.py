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
        "description": "Collects technical parameters required for AWS CloudFront CDN optimization. This function ensures that users provide structured data while guiding them with explanations and recommendations.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain_name": {
                    "type": "string",
                    "description": "Primary domain name for CDN deployment (e.g., example.com)"
                },
                "ssl_support": {
                    "type": "string",
                    "enum": ["SSL", "Non-SSL"],
                    "description": "Does the CDN need to support SSL/TLS encryption?"
                },
                "traffic_volume": {
                    "type": "string",
                    "enum": ["Low (Less than 1TB/month)", "Medium (1TB-10TB/month)", "High (10TB+)", "Not Sure"],
                    "description": "Expected traffic volume for the CDN. If unsure, select 'Not Sure'."
                },
                "cache_policy": {
                    "type": "string",
                    "enum": ["Full Cache", "Partial Cache", "No Cache"],
                    "description": "Preferred cache behavior for CDN content."
                },
                "geographical_coverage": {
                    "type": "string",
                    "enum": ["US & Europe", "Global"],
                    "description": "Regions where CDN optimization is required."
                },
                "price_class": {
                    "type": "string",
                    "enum": ["Price Class 100 (US, Canada, Europe)", "Price Class 200 (Most Locations)", "Price Class All (Global)"],
                    "description": "Amazon CloudFront pricing class selection based on coverage area."
                },
                "origin_server_type": {
                    "type": "string",
                    "enum": ["Amazon S3", "Other AWS (EC2, Lambda, RDS)", "On-Premise", "Hybrid"],
                    "description": "Type of origin server that hosts the content."
                },
                "protocol_support": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["HTTP", "HTTPS"]},
                    "description": "Protocols to be supported by the CDN."
                },
                "security_requirements": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["WAF", "Bot Protection", "DDoS Protection", "Advanced DDoS Protection"]},
                    "description": "Security features required for CDN."
                },
                "latency_tolerance": {
                    "type": "string",
                    "enum": ["Low", "Medium", "High"],
                    "description": "Tolerance level for latency in content delivery."
                },
                "content_type": {
                    "type": "string",
                    "enum": ["Static", "Dynamic", "Streaming", "APIs"],
                    "description": "Type of content being served via CDN."
                },
                "compression_support": {
                    "type": "string",
                    "enum": ["Gzip", "Brotli", "None"],
                    "description": "Compression methods required for content optimization."
                },
                "log_and_analytics": {
                    "type": "boolean",
                    "description": "Whether detailed logging and analytics are required."
                },
                "additional_requirements": {
                    "type": "string",
                    "description": "Any additional technical or business requirements for the CDN setup."
                }
            },
            "required": [
                "domain_name",
                "ssl_support",
                "traffic_volume",
                "cache_policy",
                "geographical_coverage",
                "price_class",
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
        "content": (
            "You are an intelligent chatbot designed to guide users in setting up an optimized AWS CloudFront CDN. "
            "Your goal is to ask structured questions one at a time and explain each technical option in detail so that "
            "even non-technical users can understand and make informed choices.\n\n"

            "**Instructions:**\n"
            "- Start by greeting the user and explaining that you will collect necessary CDN setup details.\n"
            "- Ask each question separately, providing background information before listing available options.\n"
            "- If a user is unsure, offer recommendations based on best practices.\n"
            "- After collecting all details, summarize their responses and format the output as a JSON object optimized for AWS CloudFront.\n\n"

            "**Conversation Flow:**\n"
            "1️⃣ Ask for the **domain name**.\n"
            "2️⃣ Ask if they require **SSL/TLS encryption**.\n"
            "3️⃣ Ask about **expected traffic volume**, providing estimations (low, medium, high, not sure).\n"
            "4️⃣ Ask about **caching preferences** (Full Cache, Partial Cache, No Cache).\n"
            "5️⃣ Ask about **geographical coverage** (US & Europe or Global).\n"
            "6️⃣ Ask about **AWS pricing class**, explaining cost benefits.\n"
            "7️⃣ Ask if they use **Amazon S3 or other origin servers**.\n"
            "8️⃣ Ask which **protocols** they want to support (only HTTP/HTTPS since QUIC & WebSockets are removed).\n"
            "9️⃣ Ask about **security needs**, explaining WAF, Bot Protection, and DDoS options.\n"
            "🔟 Ask about **latency tolerance** and guide them based on their region selection.\n"
            "1️⃣1️⃣ Ask about **content type** (Static, Dynamic, Streaming, APIs) and provide guidance.\n"
            "1️⃣2️⃣ Ask about **compression needs** (Gzip, Brotli, or None).\n"
            "1️⃣3️⃣ Ask if **detailed logging and analytics** are required.\n"
            "1️⃣4️⃣ Ask if they have **any additional requirements**.\n\n"

            "**Final Output:**\n"
            "- After collecting all information, confirm the user’s choices and present a structured JSON output.\n"
            "- Optimize the response specifically for **Amazon CloudFront** deployment.\n"
            "- Ensure all parameters align with AWS best practices and provide final recommendations."
        )
    }
]

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
        "content": (
            "You are an intelligent chatbot designed to guide users in setting up an optimized AWS CloudFront CDN. "
            "Your goal is to ask structured questions one at a time and explain each technical option in detail so that "
            "even non-technical users can understand and make informed choices.\n\n"

            "**Instructions:**\n"
            "- Start by greeting the user and explaining that you will collect necessary CDN setup details.\n"
            "- Ask each question separately, providing background information before listing available options.\n"
            "- If a user is unsure, offer recommendations based on best practices.\n"
            "- After collecting all details, summarize their responses and format the output as a JSON object optimized for AWS CloudFront.\n\n"

            "**Conversation Flow:**\n"
            "1️⃣ Ask for the **domain name**.\n"
            "2️⃣ Ask if they require **SSL/TLS encryption**.\n"
            "3️⃣ Ask about **expected traffic volume**, providing estimations (low, medium, high, not sure).\n"
            "4️⃣ Ask about **caching preferences** (Full Cache, Partial Cache, No Cache).\n"
            "5️⃣ Ask about **geographical coverage** (US & Europe or Global).\n"
            "6️⃣ Ask about **AWS pricing class**, explaining cost benefits.\n"
            "7️⃣ Ask if they use **Amazon S3 or other origin servers**.\n"
            "8️⃣ Ask which **protocols** they want to support (only HTTP/HTTPS since QUIC & WebSockets are removed).\n"
            "9️⃣ Ask about **security needs**, explaining WAF, Bot Protection, and DDoS options.\n"
            "🔟 Ask about **latency tolerance** and guide them based on their region selection.\n"
            "1️⃣1️⃣ Ask about **content type** (Static, Dynamic, Streaming, APIs) and provide guidance.\n"
            "1️⃣2️⃣ Ask about **compression needs** (Gzip, Brotli, or None).\n"
            "1️⃣3️⃣ Ask if **detailed logging and analytics** are required.\n"
            "1️⃣4️⃣ Ask if they have **any additional requirements**.\n\n"

            "**Final Output:**\n"
            "- After collecting all information, confirm the user’s choices and present a structured JSON output.\n"
            "- Optimize the response specifically for **Amazon CloudFront** deployment.\n"
            "- Ensure all parameters align with AWS best practices and provide final recommendations."
        )}
    ]
# Streamlit app layout
st.title("CDN Optimization Chatbot")
st.write("Chat with this AI to collect CDN deployment requirements.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Function to generate assistant response
    def generate_response():
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages,
            functions=functions
        )
        return response.choices[0].message

    # Generate assistant response
    with st.chat_message("assistant"):
        message = generate_response()
        st.markdown(message.content)  # Use dot notation to access 'content'
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": message.content})
