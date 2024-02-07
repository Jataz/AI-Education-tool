import streamlit as st
import requests

# URL of the Flask app endpoints
FLASK_BACKEND_URL = "http://localhost:5000"  # Update this to your Flask app's URL

def call_flask_endpoint(endpoint, json_data):
    """Send a POST request to the Flask endpoint."""
    response = requests.post(f"{FLASK_BACKEND_URL}/{endpoint}", json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get response from the server.")
        return None

# Custom CSS to enhance appearance
st.markdown("""
<style>
    /* Custom styles */
    .css-1cpxqw2 {
        border-color: #4f8bf9 !important; /* Change input border color */
    }
    /* Other custom styles can be added here */
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("AI Education Tool")

# Use a separate key for the text input to avoid direct session state modification
topic_input = st.text_input("", placeholder="Write the topic you want to learn about.....", key="topic_input")

# Trigger content and question update only when topic changes
if topic_input and (topic_input != st.session_state.get('topic', '')):
    st.session_state['topic'] = topic_input
    with st.spinner('Generating content...'):
        # Fetch and update content response
        content_response = call_flask_endpoint("generate_content", {"topic": topic_input})
        if content_response:
            st.session_state['content_response'] = content_response
        # Fetch and update question response
        question_response = call_flask_endpoint("generate_question", {"topic": topic_input})
        if question_response:
            st.session_state['question_response'] = question_response

# Display context and question if available in session state
if 'content_response' in st.session_state:
    st.markdown("### Context")
    st.info(st.session_state['content_response']['content'])

if 'question_response' in st.session_state:
    st.markdown("### Question")
    st.info(st.session_state['question_response']['question'])
    
    # Handling student's answer and feedback only after a question is available
    student_answer = st.text_area("Your Answer:", key="student_answer")
    if student_answer and st.button('Submit Answer', key='submit_answer'):
        with st.spinner('Assessing your answer...'):
            assessment_response = call_flask_endpoint("assess_answer", {
                "question": st.session_state['question_response']['question'], 
                "answer": student_answer
            })
            if assessment_response:
                st.session_state['assessment_response'] = assessment_response
                st.markdown("### Feedback")
                st.warning(assessment_response['assessment'])

# Footer
st.markdown("---")
st.markdown("### About")
st.info("This AI Education Tool is powered by OpenAI's GPT model, designed to facilitate learning by generating contextual content, questions, and providing feedback on answers. Enjoy learning!")
