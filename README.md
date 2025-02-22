# ***VİDEO ÖZETLEME (TÜRKÇE)*** 

Bu proje, videoların özetini oluşturan bir sistem oluşturmayı amaçlamaktadır. Projenin temel hedefi, uzun süren videolardan kısa ve anlamlı bir özet oluşturarak kullanıcıya zaman tasarrufu sağlamaktır. Sistemin çalışma prensibi verilen videonun sesi metne çevrilmesi ve video karelerinden anlamlı görüntüler seçilmesiyle bir metin içeriği oluşturularak bir özet çıkarılmasıdır. 

*Kullanım Alanları*
* 	Eğitim
* 	Reklam ve Pazarlama
* 	Medya ve Haberler
* 	Akademik Araştırma

*Kullanılan Teknolojiler*
1. Whisper: Sesli içeriği metne dönüştürmek için kullanıldı.
2. MoviePy: Video işlemleri ve karelerin işlenmesi için kullanıldı.
3. Pydub: Ses işleme ve dönüştürme işlemi için kullanıldı.
4. PIL (Pillow): Görüntü işleme için kullanıldı.
5. Pyesseract: Video karelerinden metin çıkarmak için kullanıldı.
6. OpenCV: Video kareleri üzerinde analiz yapmak için kullanıldı.
7. BLIP Modeli: Görüntüden anlam çıkarmak için kullanıldı.


#### KURULUM 
Projeyi kullanabilmek için aşağıdaki paketleri yüklemeniz gerekmektedir (Direkt olarak komutu çalıştırabilirsiniz.). Ayrıca ffmpeg programını da bilgisayarınıza kurmanız gerekmektedir.

!pip install openai-whisper moviepy pydub pillow pytesseract opencv-python 

# *Programın Görselleri*
![1](https://github.com/user-attachments/assets/21552ddc-f87d-47fc-be45-1ea2dda76360)

*  Programın arayüzü bu şekildedir.

![3](https://github.com/user-attachments/assets/7bb09468-cdc9-466a-819a-ee1cbf39c702)

*  Ses işleme aşaması.

![4](https://github.com/user-attachments/assets/39ce967b-ec1b-4a55-92bc-a3bcdf832501)

*  Sesin metine döndürülme aşaması.

![5](https://github.com/user-attachments/assets/36ec2b58-1216-4076-b59f-c5911a0ea7aa)

*  Karelerin işlenme aşaması.

![6](https://github.com/user-attachments/assets/5d50db90-74bc-4998-86cd-c4b156f47979)

* Özet oluşturma aşaması.



* Genel olarak örnek bir videodan çıkarılan metinler ve çıkarılan özetin yer aldığı metinler ise şu şekildedir:

![7](https://github.com/user-attachments/assets/2c9a79c2-8ccd-4f58-a2fa-eb87dbe8f3b8)






