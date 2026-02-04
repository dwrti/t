import requests
import random
import smtplib
from email.mime.text import MIMEText

# --- الإعدادات التي جهزتها أنت ---
SENDER_EMAIL = "bcfcwomen@gmail.com"
# ضع الكود المكون من 16 حرفاً من صورتك هنا بدون مسافات
SENDER_PASSWORD = "ejehezvcbrwryihx"
RECEIVER_EMAIL = "ddt42202@gmail.com"

def send_movie_email(movie_id):
    imdb_link = f"https://www.imdb.com/title/{movie_id}"
    # رابط مشاهدة مباشر كخدمة إضافية
    watch_link = f"https://vidsrc.to/embed/movie/{movie_id}"
    
    subject = f"🎬 اقتراح فيلم: {movie_id}"
    body = f"إليك فيلم عشوائي جديد من أرشيف العالم:\n\nرابط IMDb:\n{imdb_link}\n\nرابط المشاهدة:\n{watch_link}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"✅ تم الإرسال بنجاح إلى {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")

def run_bot():
    # توليد معرف فيلم عشوائي تماماً (أكثر من 10 ملايين خيار)
    random_id = random.randint(100000, 9999999)
    movie_id = f"tt{random_id:07d}"
    send_movie_email(movie_id)

if __name__ == "__main__":
    run_bot()
