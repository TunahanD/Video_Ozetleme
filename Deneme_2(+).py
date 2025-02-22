import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import cv2
from PIL import Image
import whisper
import moviepy as mp
from pydub import AudioSegment
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai
import tempfile

class VideoSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video ve Ses İşleme Uygulaması")
        self.root.geometry("700x637") # Arayüzün boyutu bu kısımdan ayarlanıyor.

        self.root.resizable(False,False) # Arayüzün boyutlarını kullanıcı değiştiremiyor.

        # Renk paleti
        self.bg_color = "#E3F2FD"  # Çok açık deniz mavisi arka plan
        self.header_color = "#1976D2"  # Canlı mavi - başlıklar için
        self.button_bg_color = "#2196F3"  # Mavi - butonlar için
        self.button_fg_color = "#FFFFFF"  # Beyaz - buton yazıları
        self.text_color = "#0D47A1"  # Koyu mavi - genel metin

        # Ana pencere arka planı
        self.root.configure(bg=self.bg_color)

        # OpenAI API anahtarı - Güvenlik için daha sonra değiştirilebilir.
        self.api_key = "API-KEY" # Buraya API anahtarı yazılacak.
        openai.api_key = self.api_key

        # Model yüklemeleri
        self.load_models()

        # Geçici dosyalar için klasör oluşturma
        self.temp_dir = tempfile.mkdtemp()
        
        # Arayüz bileşenlerini oluştur
        self.create_widgets()

    def load_models(self):
        """AI modellerini yükle"""
        try:
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.whisper_model = whisper.load_model("small")
        except Exception as e:
            messagebox.showerror("Model Yükleme Hatası", f"Modeller yüklenirken hata oluştu: {str(e)}")

    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="TFrame")

        # Video yükleme bölümü
        self.create_upload_section(main_frame)
        
        # İşlem seçenekleri bölümü
        self.create_options_section(main_frame)
        
        # İşlem durumu bölümü
        self.create_progress_section(main_frame)
        
        # Sonuç bölümü
        self.create_results_section(main_frame)

    def create_upload_section(self, parent):
        """Video yükleme bölümünü oluştur"""
        upload_frame = ttk.LabelFrame(parent, text="Video Yükleme", padding="10")
        upload_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        upload_frame.configure(style="Header.TLabelframe")

        self.video_path = tk.StringVar()
        ttk.Entry(upload_frame, textvariable=self.video_path, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(upload_frame, text="Video Seç", command=self.select_video, 
                   style="Accent.TButton").grid(row=0, column=1, padx=5)

    def create_options_section(self, parent):
        """İşlem seçenekleri bölümünü oluştur"""
        options_frame = ttk.LabelFrame(parent, text="İşlem Seçenekleri", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        options_frame.configure(style="Header.TLabelframe")

        self.frame_rate = tk.IntVar(value=5)
        ttk.Label(options_frame, text="Kare Yakalama Aralığı (saniye):", background=self.bg_color,
                  foreground=self.text_color).grid(row=0, column=0, padx=5)
        ttk.Entry(options_frame, textvariable=self.frame_rate, width=5).grid(row=0, column=1, padx=5)

        self.include_audio = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ses Analizi Ekle", variable=self.include_audio, 
                        style="TCheckbutton").grid(row=0, column=2, padx=20)

    def create_progress_section(self, parent):
        """İşlem durumu bölümünü oluştur"""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        progress_frame.configure(style="TFrame")

        self.process_button = ttk.Button(progress_frame, text="İşlemi Başlat", command=self.process_video, 
                                          style="Accent.TButton")
        self.process_button.grid(row=0, column=0)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.grid(row=0, column=1, padx=10)

        self.status_label = ttk.Label(progress_frame, text="", background=self.bg_color, 
                                       foreground=self.text_color)
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

    def create_results_section(self, parent):
        """Sonuç bölümünü oluştur"""
        result_frame = ttk.LabelFrame(parent, text="Sonuçlar", padding="10")
        result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        result_frame.configure(style="Header.TLabelframe")

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20, 
                                                     background="white", foreground=self.text_color, state='disabled')
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        button_frame = ttk.Frame(result_frame)
        button_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(button_frame, text="Sonucu Kaydet", command=self.save_results, style="Accent.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Temizle", command=lambda: self.result_text.delete(1.0, tk.END), 
                   style="Accent.TButton").grid(row=0, column=1, padx=5)

    def select_video(self):
        """Video dosyası seçme dialog'unu aç"""
        filename = filedialog.askopenfilename(
            title="Video Dosyası Seç",
            filetypes=[
                ("Video dosyaları", "*.mp4 *.avi *.mov *.mkv"),
                ("Tüm dosyalar", "*.*")
            ]
        )
        if filename:
            self.video_path.set(filename)

    def update_status(self, message, progress=None):
        """Durum mesajını ve ilerleme çubuğunu güncelle"""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update()

    def extract_audio_from_video(self, video_path):
        """Videodan ses çıkar"""
        audio_path = os.path.join(self.temp_dir, "audio.mp3")
        wav_path = os.path.join(self.temp_dir, "audio.wav")
        
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()
        
        AudioSegment.from_mp3(audio_path).export(wav_path, format="wav")
        return wav_path

    def transcribe_audio(self, wav_path):
        """Sesi metne çevir"""
        result = self.whisper_model.transcribe(wav_path)
        return result["text"]

    def extract_frames_and_generate_text(self, video_path):
        """Videodan kareler çıkar ve açıklamalar üret"""
        descriptions = []
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_interval = fps * self.frame_rate.get()
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                inputs = self.processor(images=image, return_tensors="pt")
                outputs = self.model.generate(**inputs)
                caption = self.processor.decode(outputs[0], skip_special_tokens=True)
                descriptions.append(caption)
                
                progress = (frame_count / total_frames) * 100
                self.update_status(f"Kare analizi: {len(descriptions)} kare işlendi", progress)
                
            frame_count += 1
            
        cap.release()
        return descriptions

    def summarize_with_gpt(self, text):
        """GPT ile metin özetleme"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir video özetleme asistanısın. "
                                                "Verilen metni anlamlı ve özlü bir şekilde özetle."},
                    {"role": "user", "content": f"Bu videoyu özetle:\n\n{text}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            messagebox.showerror("GPT Hatası", f"Özetleme sırasında hata oluştu: {str(e)}")
            return "Özetleme yapılamadı."

    def process_video(self):
        """Ana işlem fonksiyonu"""
        if not self.video_path.get():
            messagebox.showerror("Hata", "Lütfen bir video dosyası seçin!")
            return

        self.process_button.config(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        
        try:
            all_texts = []
            
            # Ses analizi
            if self.include_audio.get():
                self.update_status("Ses çıkarılıyor...", 10)
                wav_path = self.extract_audio_from_video(self.video_path.get())
                
                self.update_status("Ses metne dönüştürülüyor...", 30)
                audio_text = self.transcribe_audio(wav_path)
                all_texts.append(f"Ses Analizi:\n{audio_text}")

            # Görüntü analizi
            self.update_status("Video kareleri analiz ediliyor...", 50)
            frame_descriptions = self.extract_frames_and_generate_text(self.video_path.get())
            all_texts.append(f"Görüntü Analizi:\n" + "\n".join(frame_descriptions))

            # Özet oluşturma
            self.update_status("Özet oluşturuluyor...", 90)
            combined_text = "\n\n".join(all_texts)
            final_summary = self.summarize_with_gpt(combined_text)

            # Sonuçları göster
            self.result_text.configure(state='normal')  # Geçici olarak yazılabilir yap
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, final_summary)
            self.result_text.configure(state='disabled')  # Tekrar salt okunur yap
            self.update_status("İşlem tamamlandı!", 100)

        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu:\n{str(e)}")
            self.update_status("Hata oluştu!")
        finally:
            self.process_button.config(state='normal')

    def save_results(self):
        """Sonuçları dosyaya kaydet"""
        if not self.result_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Uyarı", "Kaydedilecek sonuç bulunamadı!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Sonucu Kaydet"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.result_text.get(1.0, tk.END))
                messagebox.showinfo("Başarılı", "Sonuçlar başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSummaryApp(root)
    root.mainloop()
