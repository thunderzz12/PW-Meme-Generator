import streamlit as st
import streamlit.components.v1 as components
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
import os
import requests



st.set_page_config(page_title="Alakh Pandey Meme Maker", layout="centered")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display: none;}
            [data-testid="stStatusWidget"] {display: none;}
            .st-emotion-cache-zq5wms.e1nzilvr4 {display: none;} 
            .viewerBadge_container__1QSob {display: none;}
            div[data-testid="stToolbar"] {display: none;}
            #stConnectionStatus {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Initializing engines...")
                progress_bar.progress(10)
                
                video = VideoFileClip(TEMPLATE_PATH)
                
                status_text.text("Fitting your photo into the meme...")
                progress_bar.progress(30)
                
                box_width = 359
                box_height = 481
                
                user_img = (ImageClip("temp_user_img.jpg")
                            .with_duration(video.duration)
                            .resized(new_size=(box_width, box_height))
                            .with_position((0, 400)))

                status_text.text("Rendering video (this takes a few seconds)...")
                progress_bar.progress(60)
                
                final_video = CompositeVideoClip([video, user_img]).with_audio(video.audio)
                final_video.audio = video.audio

                output_file = "finished_meme.mp4"
                final_video.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=24, logger=None)

                status_text.text("Optimization complete")
                progress_bar.progress(100)
                
                status_text.empty()
                st.success("Render successful")
                
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
                status_text.empty()
                progress_bar.empty()
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

st.divider()
st.subheader("While you're waiting...")
st.write("Tap or press space to flap! Have fun while waiting.")
game_html = """
<iframe src="https://flappybird.io/" width="100%" height="400" frameborder="0" allowfullscreen></iframe>
"""
st.components.v1.html(game_html, height=420)

st.divider()
st.subheader("Say me hi on Discord!")
try:
    response = requests.get("https://api.lanyard.rest/v1/users/1408045901745885225")
    data = response.json()
    if data.get('success'):
        user = data['data']
        avatar = user['discord_user']['avatar']
        username = user['discord_user']['username']
        discriminator = user['discord_user']['discriminator']
        display_name = user['discord_user'].get('global_name', username)
        status = user['discord_status']
        activities = user.get('activities', [])
      
        status_color = {'online': '#23a559', 'idle': '#f0b232', 'dnd': '#f23f43', 'offline': '#80848e'}.get(status, '#80848e')
        
        activity_text = ""
        for act in activities:
            if act['type'] == 0:  # Playing
                activity_text += f"🎮 Playing {act['name']}<br>"
            elif act['type'] == 2:  # Listening
                activity_text += f"🎵 Listening to {act['name']}<br>"
            elif act['type'] == 3:  # Watching
                activity_text += f"📺 Watching {act['name']}<br>"
        
        # Build HTML
        html = f"""
        <div style="border: 2px solid {status_color}; border-radius: 15px; padding: 15px; background: linear-gradient(135deg, #2c2f33 0%, #23272a 100%); color: white; display: flex; align-items: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 8px rgba(0,0,0,0.3); max-width: 400px; margin: auto;">
            <img src="https://cdn.discordapp.com/avatars/{user['discord_user']['id']}/{avatar}.png?size=64" style="width: 64px; height: 64px; border-radius: 50%; margin-right: 15px; border: 3px solid {status_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            <div style="flex-grow: 1;">
                <strong style="font-size: 18px; color: #ffffff;">{display_name}</strong><br>
                <small style="color: #b9bbbe; font-size: 12px;">{username}</small><br>
                <span style="color: {status_color}; font-weight: bold; font-size: 14px;">● {status.capitalize()}</span><br>
                <span style="font-size: 12px; color: #b9bbbe;">{activity_text.strip()}</span>
            </div>
        </div>
        """
        st.components.v1.html(html, height=150)
    else:
        st.error("Failed to fetch Discord status.")
except Exception as e:
    st.error(f"Error loading Discord status: {e}")