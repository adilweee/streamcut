import yt_dlp
import os

def cut_video_clip(video_url, start_time, duration, output_filename="clip.mp4"):
    """
    YouTube'dan sadece istenen 15 saniyelik kısmı sunucuyu hiç yormadan,
    doğrudan kırparak 1080p+ kalitede indirir. MoviePy yükünü tamamen kaldırır.
    """
    print(f"\n🎬 {start_time}. saniyeden itibaren {duration} saniyelik YÜKSEK KALİTELİ klip hazırlanıyor...")

    end_time = start_time + duration

    # Streamlit Cloud üzerinde ffmpeg kurulu gelir. yt_dlp'ye doğrudan saniye hedeflemesi yaptırıyoruz.
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': output_filename,
        # İşte sihirli parametre: Videonun tamamını indirmek yerine sadece bu saniyeleri indirir!
        'download_ranges': lambda info_dict, ydl: [{'start_time': start_time, 'end_time': end_time}],
        'force_keyframes_at_cuts': True,
    }

    try:
        # Eğer eski klibin kalıntısı varsa sunucu çakışmasın diye temizleyelim
        if os.path.exists(output_filename):
            os.remove(output_filename)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"✅ Yüksek Kaliteli Klip Hazır: {output_filename}")
        return True

    except Exception as e:
        print(f"❌ Kırpma/İndirme hatası: {e}")
        return False
