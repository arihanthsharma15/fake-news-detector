import streamlit as st
import requests

# --- Configuration ---
# This is the address of our FastAPI backend.
# Make sure your FastAPI server is running at this address.
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000/detect"

# --- Page Setup ---
# Set the title and icon that appear in the browser tab.
st.set_page_config(
    page_title="News Analyzer",
    page_icon="🤖",
    layout="centered"
)

# --- Header Section ---
st.title("🤖 AI-Powered News Analyzer")
st.write("Enter a piece of news text below, and our AI will analyze its sentiment (Positive/Negative).")
st.write("---") # A horizontal line for separation

# --- Main UI - The Text Input Area ---
user_input = st.text_area(
    "Enter News Article Text Here:", 
    height=250, 
    placeholder="e.g., 'The company announced a record-breaking profit this quarter...'"
)

# --- The "Analyze" Button and Logic ---
# This code block will only run when the user clicks the button.
# This is the NEW, improved version of the logic block.

if st.button("Analyze News"):
    
    if user_input.strip():
        with st.spinner("🧠 Thinking... The AI is analyzing the text..."):
            try:
                payload = {"text": user_input}
                response = requests.post(FASTAPI_BACKEND_URL, json=payload, timeout=30) # Added a timeout
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis Complete!")
                    st.subheader("Results:")

                    ai_analysis = result.get("ai_analysis")

                    # --- THIS IS THE NEW, SMARTER CHECK ---
                    # Check if the response is the expected list of lists format
                    if isinstance(ai_analysis, list) and ai_analysis and isinstance(ai_analysis[0], list):
                        top_result = max(ai_analysis[0], key=lambda x: x.get('score', 0))
                        label = top_result.get('label', 'UNKNOWN')
                        score = top_result.get('score', 0)

                        if "POSITIVE" in label.upper():
                            st.markdown(f"### Sentiment: <span style='color:green; font-weight:bold;'>{label.upper()}</span>", unsafe_allow_html=True)
                        elif "NEGATIVE" in label.upper():
                            st.markdown(f"### Sentiment: <span style='color:red; font-weight:bold;'>{label.upper()}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"### Sentiment: {label.upper()}")
                        
                        st.progress(score)
                        st.write(f"Confidence: {score:.2%}")
                    
                    # Check if the model is loading
                    elif isinstance(ai_analysis, dict) and "estimated_time" in ai_analysis:
                        wait_time = ai_analysis["estimated_time"]
                        st.warning(f"⏳ The AI model is loading. Please try again in about {wait_time:.0f} seconds.")
                    
                    # Handle any other unexpected format
                    else:
                        st.error("AI analysis returned an unexpected format.")
                        st.json(ai_analysis) # Show the raw response for debugging

                else:
                    st.error(f"Error from server: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: Could not connect to the backend. Is it running? Error: {e}")
    else:
        st.warning("⚠️ Please enter some text before analyzing.")