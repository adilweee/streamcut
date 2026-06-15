import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os


def cut_video_clip(video_url, start_time, duration, output_filename="clip.mp4"):
    """
    YouTube'dan EN YÜKSEK KALİTELİ (1080p+) video ve ses akışlarını ayrı ayrı çeker,
    MoviePy ile sadece istenen 15 saniyeyi kırpar ve cam gibi birleştirir.
    """
    print(f"\n🎬 {start_time}. saniyeden itibaren {duration} saniyelik YÜKSEK KALİTELİ klip hazırlanıyor...")

    # En iyi video (1080p, 2K, 4K ne varsa) ve en iyi ses linklerini ayıkla
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # YouTube yüksek kalitede video ve sesi ayrı linklerde tutar:
            video_stream_url = info['requested_formats'][0]['url']
            audio_stream_url = info['requested_formats'][1]['url']

        print("⚡ En yüksek kaliteli görüntü ve ses akışına bağlanıldı, kırpılıyor...")

        end_time = start_time + duration

        # 1. Görüntüyü kırp
        with VideoFileClip(video_stream_url) as video_clip:
            sub_video = video_clip.subclipped(start_time, end_time)

            # 2. Sesi kırp
            with AudioFileClip(audio_stream_url) as audio_clip:
                sub_audio = audio_clip.subclipped(start_time, end_time)

                # 3. Görüntü ile sesi yüksek kalitede birleştir
                final_clip = sub_video.with_audio(sub_audio)

                # bitrate parametresi ile kaliteyi (Render kalitesini) zirveye çıkarıyoruz
                final_clip.write_videofile(
                    output_filename,
                    codec="libx264",
                    audio_codec="aac",
                    bitrate="5000k",  # Cam gibi görüntü için yüksek bitrate
                    logger=None
                )

        print(f"✅ Yüksek Kaliteli Klip Hazır: {output_filename}")
        return True

    except Exception as e:
        print(f"❌ Kalite yükseltme hatası: {e}")
        return False
