import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import re
from analyzer import get_chat_data, find_highlights
from cutter import cut_video_clip
# 🌟 Dil dosyamızı buraya da ekliyoruz
from languages import LANGUAGES


class StreamCutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StreamCut AI — Desktop Pro")
        self.root.geometry("520x400")
        self.root.configure(bg="#1e1e1e")

        # Varsayılan dil EN (İngilizce)
        self.current_lang = "EN"
        self.lang = LANGUAGES[self.current_lang]

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#1e1e1e", foreground="#ffffff")
        self.style.configure("TLabel", background="#1e1e1e",
                             foreground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=(
            "Segoe UI", 14, "bold"), foreground="#ff4b4b")
        self.style.configure("Action.TButton", background="#ff4b4b", foreground="white", font=(
            "Segoe UI", 11, "bold"), borderwidth=0)
        self.style.map("Action.TButton", background=[("active", "#e03e3e")])

    def create_widgets(self):
        # Üst Bar: Dil Seçimi
        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(fill="x", px=15, py=5)

        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.Combobox(top_frame, textvariable=self.lang_var, values=[
                                 "EN", "TR", "ES"], width=5, state="readonly")
        lang_menu.pack(side="right")
        lang_menu.bind("<<ComboboxSelected>>", self.change_language)

        # Ana Başlık
        self.lbl_title = ttk.Label(
            self.root, text="StreamCut AI", style="Header.TLabel")
        self.lbl_title.pack(py=10)

        # Alt Başlık / Açıklama
        self.lbl_desc = ttk.Label(self.root, text=self.lang["title"], font=(
            "Segoe UI", 10, "italic"), foreground="#888")
        self.lbl_desc.pack(py=2)

        # Giriş Alanı
        self.lbl_input = ttk.Label(self.root, text=self.lang["input_label"])
        self.lbl_input.pack(fill="x", px=40, py=(15, 5))

        self.ent_url = ttk.Entry(self.root, font=("Segoe UI", 11), width=45)
        self.ent_url.pack(px=40, py=5, fill="x")

        # Tetikleyici Buton
        self.btn_action = ttk.Button(
            self.root, text=self.lang["btn_analyze"], style="Action.TButton", command=self.start_process_thread)
        self.btn_action.pack(px=40, py=20, fill="x")

        # Durum Çubuğu
        self.lbl_status = ttk.Label(
            self.root, text="Ready / Hazır", font=("Segoe UI", 9), foreground="#888")
        self.lbl_status.pack(side="bottom", fill="x", px=15, py=10)

    def change_language(self, event):
        self.current_lang = self.lang_var.get()
        self.lang = LANGUAGES[self.current_lang]

        # Arayüz metinlerini anında güncelle
        self.lbl_input.config(text=self.lang["input_label"])
        self.btn_action.config(text=self.lang["btn_analyze"])
        self.lbl_desc.config(text=self.lang["title"])

    def update_status(self, text):
        self.lbl_status.config(text=text)
        self.root.update_idletasks()

    def start_process_thread(self):
        url = self.ent_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", self.lang["warn_link"])
            return

        self.btn_action.config(state="disabled")
        threading.Thread(target=self.process_video,
                         args=(url,), daemon=True).start()

    def process_video(self, url):
        try:
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
            if not video_id_match:
                self.root.after(0, lambda: messagebox.onerror(
                    "Error", self.lang["err_link"]))
                return

            video_id = video_id_match.group(1)

            self.root.after(0, lambda: self.update_status(
                self.lang["status_chat"]))
            df_chat = get_chat_data(video_id)
            important_moments = find_highlights(df_chat)

            if important_moments.empty:
                self.root.after(0, lambda: self.update_status(
                    self.lang["status_no_moment"]))
                return

            self.root.after(0, lambda: self.update_status(
                self.lang["status_found"].format(len(important_moments))))

            OUTPUT_DIR = os.path.join(os.getcwd(), "streamcut_desktop_clips")
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)

            moments_list = list(important_moments.items())[:3]
            for counter, (timestamp, message_count) in enumerate(moments_list, 1):
                status_msg = self.lang["status_preparing"].format(
                    counter, 3, timestamp.time())
                self.root.after(0, lambda m=status_msg: self.update_status(m))

                start_seconds = 1500 + (counter * 30)
                duration = 15
                clip_name = f"DESKTOP_klip_{counter}.mp4"
                final_clip_path = os.path.join(OUTPUT_DIR, clip_name)

                cut_video_clip(url, start_time=start_seconds,
                               duration=duration, output_filename=final_clip_path)

            self.root.after(0, lambda: self.update_status(
                "🎉 All Clips Ready in 'streamcut_desktop_clips' folder!"))
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", "Process Completed!"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.onerror(
                "Critical Error", str(e)))
        finally:
            self.root.after(0, lambda: self.btn_action.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = StreamCutApp(root)
    root.mainloop()
