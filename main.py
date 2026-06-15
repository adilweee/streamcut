import os
import pandas as pd
from analyzer import get_chat_data, find_highlights
from cutter import cut_video_clip


def main():
    print("🚀 --- CHAT ODAKLI STREAMCUT AI MOTORU BAŞLADI --- 🚀\n")

    YOUTUBE_VIDEO_ID = "KZGdkcceuW4"
    VIDEO_URL = f"https://www.youtube.com/watch?v={YOUTUBE_VIDEO_ID}"

    # 🎯 KESİN ÇÖZÜM: Python şu an çalışan main.py dosyasının klasörünü otomatik bulur
    # Elle C:\Users... yazma derdine ve yazım hatalarına son!
    PROJE_KLASORU = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(PROJE_KLASORU, "clips")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 'clips' klasörü otomatik oluşturuldu: {OUTPUT_DIR}")

    df_chat = get_chat_data(YOUTUBE_VIDEO_ID)
    important_moments = find_highlights(df_chat)

    if important_moments.empty:
        print("ℹ️ Kriterlere uygun patlama anı bulunamadı.")
        return

    print(
        f"\n🎯 Filtrelere takılan {len(important_moments)} coşkulu an doğrudan kırpılıyor...")

    counter = 1
    moments_list = list(important_moments.items())[:3]

    for timestamp, message_count in moments_list:
        start_seconds = 1500 + (counter * 30)
        duration = 15

        # Klibin adı doğrudan projenin içindeki clips klasörüne hedeflenir
        final_clip_name = os.path.join(
            OUTPUT_DIR, f"ONAYLANDI_klip_{counter}.mp4")

        print(
            f"\n[Klip {counter}/3] Zaman: {timestamp.time()} | Chat Yoğunluğu: {message_count}")

        success = cut_video_clip(VIDEO_URL, start_time=start_seconds,
                                 duration=duration, output_filename=final_clip_name)

        if success:
            print(f"🔥 Klip başarıyla klasöre cuk oturdu: {final_clip_name}")

        counter += 1

    print("\n🎉 Tüm işlemler bitti! Şimdi sol taraftaki 'clips' klasörünü açıp bakabilirsin.")


if __name__ == "__main__":
    main()
