import streamlit as st
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import tempfile

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Edit with Dev - Private Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization for Flow & Security
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state["step"] = "welcome"  # Options: welcome, login, studio

if "attempts" not in st.session_state:
    st.session_state["attempts"] = 0

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

PERSONAL_PASSWORD = "534547"
MAX_ATTEMPTS = 3

# ---------------------------------------------------------
# Screen 1: Welcome Screen
# ---------------------------------------------------------
if st.session_state["step"] == "welcome":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎬 Welcome to Edit with Dev</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Your Personal, Secure, VPN-Free Video Studio</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start App", type="primary", use_container_width=True):
            st.session_state["step"] = "login"
            st.rerun()

# ---------------------------------------------------------
# Screen 2: Security PIN Login Screen (3 Chances Limit)
# ---------------------------------------------------------
elif st.session_state["step"] == "login":
    st.title("🔒 Edit with Dev - Security Verification")
    st.write("Krupaya aplaya secure app madhe pravesh karnyasathi 6-digit PIN taka.")
    
    # Check if attempts exceeded
    if st.session_state["attempts"] >= MAX_ATTEMPTS:
        st.error("❌ Wrong password entered! Maximum attempts reached. Access Denied.")
        if st.button("🔄 Try Again"):
            st.session_state["attempts"] = 0
            st.rerun()
        st.stop()
        
    entered_pass = st.text_input("Enter 6-Digit PIN:", type="password")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Submit PIN", type="primary"):
            if entered_pass == PERSONAL_PASSWORD:
                st.session_state["authenticated"] = True
                st.session_state["step"] = "studio"
                st.rerun()
            else:
                st.session_state["attempts"] += 1
                remaining = MAX_ATTEMPTS - st.session_state["attempts"]
                st.error(f"❌ Chukicha password! Urlele prayatna (Attempts left): {remaining}")

# ---------------------------------------------------------
# Screen 3: Main Video Studio (CapCut Style Features)
# ---------------------------------------------------------
elif st.session_state["step"] == "studio" and st.session_state["authenticated"]:
    # Show Congratulations on successful login (one time notice)
    if "shown_congrats" not in st.session_state:
        st.success("🎉 Congratulations! Welcome to your private video editing studio.")
        st.session_state["shown_congrats"] = True
        
    st.title("🎬 Edit with Dev - Private Video Studio")
    st.caption("⚡ Fast, Secure, VPN-Free Browser Video Editor")

    st.sidebar.title("👤 EDIT-DEV-STUDIO")
    st.sidebar.success("🔑 Authenticated Successfully")
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Tumche video clips upload kara ani tools vaprun edit kara.")

    # Editing Tools Selection
    edit_option = st.sidebar.selectbox(
        "Choose Editing Tool:",
        ["Trim / Cut Video", "Merge Multiple Videos", "Add Text to Video"]
    )

    st.markdown("---")

    # Tool 1: Trim / Cut Video
    if edit_option == "Trim / Cut Video":
        st.header("✂️ Video Trimming Tool")
        uploaded_video = st.file_uploader("Upload Video File for Cutting:", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_video.read())
            
            clip = VideoFileClip(tfile.name)
            duration = int(clip.duration)
            
            st.video(tfile.name)
            st.write(f"⏱️ Total Video Duration: {duration} seconds")
            
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.number_input("Start Time (seconds):", min_value=0, max_value=duration, value=0)
            with col2:
                end_time = st.number_input("End Time (seconds):", min_value=0, max_value=duration, value=min(5, duration))
                
            if st.button("✨ Trim & Process Video", type="primary"):
                if start_time >= end_time:
                    st.error("❌ Start time he End time peksha kami asle pahije!")
                else:
                    with st.spinner("🔄 Processing video..."):
                        trimmed_clip = clip.subclip(start_time, end_time)
                        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                        trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                        
                        st.success("🎉 Video successfully trimmed!")
                        st.video(output_path)
                        
                        with open(output_path, "rb") as file:
                            st.download_button("📥 Download Trimmed Video", file, file_name="trimmed_video.mp4", mime="video/mp4", use_container_width=True)

    # Tool 2: Merge Multiple Videos
    elif edit_option == "Merge Multiple Videos":
        st.header("🔗 Video Merger Tool")
        uploaded_videos = st.file_uploader("Upload 2 or more Video files to join:", type=["mp4", "mov", "avi"], accept_multiple_files=True)
        
        if uploaded_videos and len(uploaded_videos) > 1:
            st.write(f"📁 Total Videos Selected: {len(uploaded_videos)}")
            
            if st.button("✨ Merge Videos Together", type="primary"):
                with st.spinner("🔄 Joining video clips..."):
                    video_clips = []
                    temp_files = []
                    
                    for v in uploaded_videos:
                        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tfile.write(v.read())
                        temp_files.append(tfile.name)
                        video_clips.append(VideoFileClip(tfile.name))
                        
                    final_clip = concatenate_videoclips(video_clips)
                    output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    
                    st.success("🎉 Videos merged successfully!")
                    st.video(output_path)
                    
                    with open(output_path, "rb") as file:
                        st.download_button("📥 Download Merged Video", file, file_name="merged_video.mp4", mime="video/mp4", use_container_width=True)
        else:
            st.info("👈 Krupaya kamit kamit don video files upload kara.")

    # Tool 3: Add Text Overlay
    elif edit_option == "Add Text to Video":
        st.header("📝 Add Text / Watermark to Video")
        uploaded_video = st.file_uploader("Upload Video File:", type=["mp4", "mov", "avi"])
        
        user_text = st.text_input("Enter Text to display on Video:", "Edit with Dev")
        
        if uploaded_video is not None and user_text:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_video.read())
            
            if st.button("✨ Apply Text & Generate", type="primary"):
                with st.spinner("🔄 Adding text overlay..."):
                    clip = VideoFileClip(tfile.name)
                    
                    txt_clip = TextClip(user_text, fontsize=50, color='white', bg_color='black')
                    txt_clip = txt_clip.set_position('bottom').set_duration(clip.duration)
                    
                    result_clip = CompositeVideoClip([clip, txt_clip])
                    output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                    result_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    
                    st.success("🎉 Text added successfully!")
                    st.video(output_path)
                    
                    with open(output_path, "rb") as file:
                        st.download_button("📥 Download Edited Video", file, file_name="text_video.mp4", mime="video/mp4", use_container_width=True)
