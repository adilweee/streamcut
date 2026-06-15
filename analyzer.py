import pandas as pd
import numpy as np


def get_chat_data(video_id):
    """
    Simüle edilmiş chat verisi üretir (Gerçek api entegrasyonu için hazırdır).
    """
    print("\n💬 Chat verileri çekiliyor... Lütfen bekleyin.")
    # Test için 2 saatlik (7200 saniye) yapay chat verisi oluşturalım
    timestamps = pd.date_range(
        start="2026-06-14 20:00:00", periods=720, freq="10s")
    messages = []

    # İçinde ez, gg, haha geçen kelime havuzu
    spam_pool = ["naber", "gg ez", "hahaha gooo", "asdasd",
                 "patladım haha", "go go go", "normal mesaj"]

    for i, ts in enumerate(timestamps):
        # Bazı dakikalarda kasıtlı patlamalar yaratıyoruz
        # 30. indeks yaklaşık 5. dakikaya denk gelir (Elenmeli)
        if i in [30, 100, 250, 400]:
            count = 45
        # 150. indeks yaklaşık 25. dakikaya denk gelir (Alınmalı)
        elif i in [150, 450]:
            count = 50
        else:
            count = np.random.randint(1, 10)

        for _ in range(count):
            messages.append(
                {"timestamp": ts, "message": np.random.choice(spam_pool)})

    return pd.DataFrame(messages)


def find_highlights(df):
    """
    Yayın başı korumalı ve anahtar kelime filtreli gelişmiş chat analizör motoru.
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    # 🌟 İYİLEŞTİRME 1: Yayının ilk 10 dakikasını (600 saniye) tamamen ele
    yayin_baslangici = df.index.min()
    df = df[df.index > (yayin_baslangici + pd.Timedelta(minutes=10))]

    # 🌟 İYİLEŞTİRME 2: Sadece içinde go, haha, gg, ez geçen mesajları filtrele
    hedef_kelimeler = r'go|haha|gg|ez'
    filtrelenmis_df = df[df['message'].str.contains(
        hedef_kelimeler, case=False, na=False)]

    # Yoğunluk ölçümü (10 saniyelik pencereler)
    chat_density = filtrelenmis_df.resample('10s').count()['message']

    mean_density = chat_density.mean()
    print(
        f"📊 Filtrelenmiş Ortalama Chat Yoğunluğu (10sn): {mean_density:.2f} mesaj")

    # Ortalamanın 3 katı olan coşkulu anları yakala
    threshold = max(mean_density * 3, 10)
    highlights = chat_density[chat_density > threshold]

    return highlights.sort_values(ascending=False)
