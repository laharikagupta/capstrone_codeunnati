import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
import clipboard
import time
import os

st.markdown("""
        <style>
            body {
                background-color: #f0f2f6;
            }
            div.stButton > button:first-child {
                background-color: #007bff;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            div.stButton > button:first-child:hover {
                background-color: #0056b3;
            }
            .reportview-container .markdown-text-container {
                font-family: 'Helvetica Neue', sans-serif;
            }
            .share-button img {
                width: 32px;
                height: 32px;
                margin-right: 8px;
            }
            .share-button {
                display: inline-flex;
                align-items: center;
                margin: 8px 0;
            }
        </style>
    """, unsafe_allow_html=True)

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# Main app layout
def main():
    st.subheader("LinkedIn Post Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)

    # Initialize session state for the generated post
    if 'post' not in st.session_state:
        st.session_state['post'] = ""

    # Generate Button
    if st.button("**Generate LinkedIn Post**"):
        if not selected_tag or not selected_length or not selected_language:
            st.error('🚫 **Please provide keywords to generate a LinkedIn post!**')
        else:
            with st.spinner('🤖 Crafting your LinkedIn post...'):
                # Progress bar for user feedback
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(percent_complete + 1)
                st.session_state['post'] = generate_post(selected_length, selected_language, selected_tag)
            st.success('🎉 **Your LinkedIn post is ready!**')
            st.subheader('📄 **LinkedIn Post Preview**')
            st.write(st.session_state['post'])

    # Only show the Copy to Clipboard button if a post has been generated
    if st.session_state['post']:
        if st.button('📋 Copy to Clipboard'):
            clipboard.copy(st.session_state['post'])
            st.success("✅ LinkedIn post copied to clipboard!")

    # Share Button
    st.markdown("---")
    st.markdown("### Share Your Post")
    share_url = "https://yourappurl.com"
    st.markdown(f"""
        <div class="share-button">
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn">     
            </a>
        </div>
        <div class="share-button">
            <a href="https://api.whatsapp.com/send?text={share_url}" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">    
            </a>
        </div>
        <div class="share-button">
            <a href="https://twitter.com/intent/tweet?url={share_url}" target="_blank">
                <img src="https://static.vecteezy.com/system/resources/previews/011/087/757/large_2x/twitter-social-media-logo-icon-technology-network-background-share-like-illustration-free-vector.jpg" alt="Twitter">         
            </a>
        </div>
        <div class="share-button">
            <a href="https://www.instagram.com/sharing/share-offsite/?url={share_url}" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram">
            </a>
        </div>
    """, unsafe_allow_html=True)
    
# Run the app
if __name__ == "__main__":
    main()
