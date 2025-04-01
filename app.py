import streamlit as st
from src.backend_config import PSUChatBackend
from PIL import Image
import time
icon = Image.open("assets\PSU-logo-vector.png")
# App configuration
st.set_page_config(
    page_title="ParSU Citicharbot",
    page_icon= icon,
    layout="centered",
)

# Initialize session state variables
if "backend" not in st.session_state:
    st.session_state.backend = PSUChatBackend()
    with st.spinner("Initializing system. Please Wait..."):
        success, message = st.session_state.backend.initialize_system()
        st.session_state.initialized = success
        if not success:
            st.session_state.init_error = message

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm the ParSU Citicharbot. I can help you with information about the services and transactions in the Partido State University Citizen Charter. What would you like to know?",
        }
    ]

# Initialize clicked_example if not already in session state
if "clicked_example" not in st.session_state:
    st.session_state.clicked_example = None

# Custom CSS for chat UI
st.markdown("""
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
        display: flex;
        flex-direction: column;
    }
    .message-wrapper {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .user-message, .assistant-message {
        max-width: 100%;
        padding: 10px 15px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        font-size: 20px;
        font-family: "sans-serif";
        
    }
    .user-message {
        background: linear-gradient(to right, #eea849, #f46b45);
        color: black;
        margin-left: auto;
        flex-direction: row-reverse;
    }
    .assistant-message {
        background: linear-gradient(to right, #3a7bd5, #00d2ff);
        color: white;
        margin-right: auto;
        flex-direction: row;
    }
    .user-icon, .assistant-icon {
        width: 35px;
        height: 35px;
        border-radius: 20%;
        margin: 0  10px;
        align-self: flex-start;
        
    }/* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #042a5f;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #0d6efd !important;
        color: black !important;
        border-radius: 5px;
        font-size: 14px;
    }
    
    div.stButton > button:hover {
        background-color: #fd7e14 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/PSU-logo-vector.png", width=120)
    st.title("ParSU Citicharbot")
    st.markdown("---")
    st.markdown("### About")
    st.write("This chatbot provides information about Partido State University services, procedures, and transactions.")
    st.markdown("---")

    # Example questions
    st.markdown("### Example Questions")
    example_questions = [
        "How do I apply for admission?",
        "How to get a Student ID?",
        "How can I enroll?",
        "How do I request for documents for scholarship?",
    ]

    # Function to set example question
    def set_example_question(question):
        st.session_state.clicked_example = question

    # Create buttons for example questions
    for q in example_questions:
        st.button(q, key=f"example_{q}", on_click=set_example_question, args=(q,))

# Check if system is initialized
if not st.session_state.get('initialized', True):
    st.error(f"System initialization failed: {st.session_state.get('init_error', 'Unknown error')}")
    st.button("Retry Initialization", on_click=lambda: st.session_state.pop('backend', None))
else:
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="message-wrapper">
                    <div class="user-message">
                        <img class="user-icon" src="https://cdn-icons-png.flaticon.com/128/847/847969.png">
                        <span>{message["content"]}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="message-wrapper">
                    <div class="assistant-message">
                        <img class="assistant-icon" src="https://cdn-icons-png.flaticon.com/128/4712/4712035.png">
                        <span>{message["content"]}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Close chat-container

    # Chat input
    query = st.chat_input("Ask a question about Partido State University Citizen Charter")

    # Process user input
    if query or st.session_state.clicked_example:
        user_input = query if query else st.session_state.clicked_example
        
        if user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user message with icon
            st.markdown(f"""
                <div class="message-wrapper">
                    <div class="user-message">
                        <img class="user-icon" src="https://cdn-icons-png.flaticon.com/128/847/847969.png">
                        <span>{user_input}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Reset clicked example after using it
            if st.session_state.clicked_example:
                st.session_state.clicked_example = None

            # Simulate processing time
            time.sleep(0.5)

            # Generate assistant response
            success, response = st.session_state.backend.generate_response(user_input) if st.session_state.backend.chain else (True, "Sorry, no response available.")

            # Display assistant message with icon
            st.markdown(f"""
                <div class="message-wrapper">
                    <div class="assistant-message">
                        <img class="assistant-icon" src="https://cdn-icons-png.flaticon.com/128/4712/4712035.png">
                        <span>{response}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Store assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})