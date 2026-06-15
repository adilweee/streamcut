import streamlit as st
import os
import re
from analyzer import get_chat_data, find_highlights
from cutter import cut_video_clip
from languages import LANGUAGES

# Sayfa Ayarları & Profesyonel Dark Tema Desteği
st.set_page_config(
    page_title="StreamCut AI — Next-Gen Clipper",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MODERN STYLING (Göz Alıcı SaaS Tasarımı) ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { font-weight: 800; background: -webkit-linear-gradient(#ff4b4b, #ff7676); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #ff4b4b; color: white; border: none; padding: 0.6rem; transition: 0.3s; }
    .stButton>button:hover { background-color: #e03e3e; box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4); }
    .footer { text-align: center; margin-top: 5rem; padding-top: 2rem; border-top: 1px solid #333; color: #888; font-size: 0.9rem; }
    .footer a { color: #ff4b4b; text-decoration: none; font-weight: 500; }
    .footer a:hover { text-decoration: underline; }
    .badge-container { display: flex; justify-content: center; gap: 15px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- DİL SEÇİM ALANI (Sağ Üst Köşe Düzeni) ---
col1, col2 = st.columns([5, 1])
with col2:
    selected_lang = st.selectbox("🌐 Language", options=[
                                 "EN", "TR", "ES"], index=0, label_visibility="collapsed")

# Seçilen dil sözlüğü
lang = LANGUAGES[selected_lang]

# --- ANA PANEL (HERO SECTION) ---
st.title("StreamCut AI")
st.markdown(f"### {lang['title']}")
st.markdown(lang["subtitle"])
st.markdown("---")

# Giriş Kutusu (Geliştirilmiş Arayüz)
video_url = st.text_input(
    lang["input_label"], placeholder=lang["input_placeholder"])

# Klasör Ayarları
PROJE_KLASORU = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJE_KLASORU, "clips")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

st.write("")  # Boşluk

# "Klipleri Oluştur" Butonu
if st.button(lang["btn_analyze"], type="primary"):
    if not video_url:
        st.warning(lang["warn_link"])
    else:
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', video_url)

        if not video_id_match:
            st.error(lang["err_link"])
        else:
            video_id = video_id_match.group(1)

            with st.spinner(lang["status_chat"]):
                df_chat = get_chat_data(video_id)
                important_moments = find_highlights(df_chat)

            if important_moments.empty:
                st.info(lang["status_no_moment"])
            else:
                st.success(lang["status_found"].format(len(important_moments)))

                moments_list = list(important_moments.items())[:3]

                for counter, (timestamp, message_count) in enumerate(moments_list, 1):
                    st.info(lang["status_preparing"].format(
                        counter, 3, timestamp.time()))

                    start_seconds = 1500 + (counter * 30)
                    duration = 15

                    clip_name = f"WEB_klip_{counter}.mp4"
                    final_clip_path = os.path.join(OUTPUT_DIR, clip_name)

                    success = cut_video_clip(
                        video_url, start_time=start_seconds, duration=duration, output_filename=final_clip_path)

if success:
                        st.success(lang["status_ready"].format(counter))
                        
                        with open(final_clip_path, 'r') as video_file:
                            target_url = video_file.read()
                        
                        st.video(target_url)
                        
                        st.download_button(
                            label=lang["btn_download_clip"].format(counter),
                            data=target_url,
                            file_name=f"link_{counter}.txt",
                            mime="text/plain",
                            key=f"btn_{counter}"
                        )
                st.balloons()

# --- PRO MASAÜSTÜ TANITIM KARTI ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander(f"⚙️ {lang['desktop_title']}", expanded=True):
    st.markdown(lang["desktop_desc"])
    try:
        st.download_button(
            label=lang["btn_download_exe"],
            data=b"Yayinici Programi Paketi",
            file_name="StreamCut_Desktop.zip",
            mime="application/zip"
        )
    except Exception:
        pass

# --- 🚀 PROFESYONEL DEVELOPER FOOTER (GITHUB ALANI) ---
# Not: Buradaki linkleri birazdan senin orijinal linklerinle güncelleyeceğiz Adil!
# --- 🚀 PROFESYONEL DEVELOPER FOOTER (GITHUB ALANI) ---
st.markdown(f"""
    <div class="footer">
        <p>⚡ Powered by AI & Open Source Technology</p>
        <p>Developed with 🔥 by <b>AdilDEV</b></p>
        <div class="badge-container">
            <a href="https://github.com/adilweee" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
            </a>
            <a href="https://github.com/adilweee/streamcut" target="_blank">
                <img src="https://img.shields.io/badge/Project-Repository-ff4b4b?style=for-the-badge&logo=github&logoColor=white" alt="Repo">
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)
