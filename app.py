import streamlit as st
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
import os


st.set_page_config(page_title="Alakh Pandey Meme Maker", layout="centered")

st.title("💀 PW Meme Generator")
st.write("Jai ho Alakh sir")

uploaded_img = st.file_uploader("Choose a photo...", type=['jpg', 'png', 'jpeg'])
TEMPLATE_PATH = "template.mp4" 

if not os.path.exists(TEMPLATE_PATH):
    st.error(f"Error: '{TEMPLATE_PATH}' not found in folder. Please rename your video file to 'template.mp4'.")
else:
    if uploaded_img is not None:
        with open("temp_user_img.jpg", "wb") as f:
            f.write(uploaded_img.getbuffer())

        if st.button("Generate"):
            with st.spinner("Stretching your image and rendering video..."):
                try:
                    
                    video = VideoFileClip(TEMPLATE_PATH)
                    
                    
                    box_width = 359
                    box_height = 481
                    
                    
                    user_img = (ImageClip("temp_user_img.jpg")
                                .with_duration(video.duration)
                                .resized(new_size=(box_width, box_height))
                                .with_position((0, 400)))

                    
                    final_video = CompositeVideoClip([video, user_img]).with_audio(video.audio)
                    
                    
                    final_video.audio = video.audio

                    output_file = "finished_meme.mp4"
                    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24)

                    st.success("Meme Ready")
                    col1, col2 = st.columns([1, 1]) 

                    with col1:
                        st.video(output_file, format="video/mp4")

                    with col2:
                        st.info("Click below to save")
                        with open(output_file, "rb") as file:
                            st.download_button(
                                label="📥 Download",
                                data=file,
                                file_name="PW_meme.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

st.write("") 
st.divider()
st.markdown(
    """
    <style>
    .footer {
        width: 100%;
        text-align: center;
        color: #808080; 
        padding-top: 20px;
        padding-bottom: 20px;
        font-size: 14px;
    }
    </style>
    <div class="footer">
        Coded by <b>Thunderzz</b> with ❤️
    </div>
    """,
    unsafe_allow_html=True
)