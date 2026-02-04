import requests
import random
import smtplib
import os
from email.message import EmailMessage

def get_random_horror_movie():
    # مفتاح API مجاني (OMDb) يعطيك بيانات IMDb
    # ملاحظة: هذا المفتاح للاختبار، يفضل الحصول على واحد خاص بك مجاناً من omdbapi.com
    api_key = "7628833d"
    
    # اختيار سنة عشوائية لضمان العشوائية المطلقة وعدم تكرار "الأفضل" فقط
    year = random.randint(1970, 2024)
    url = f"http://www.omdbapi.com/?s=horror&type=movie&y={year}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            movie = random.choice(data["Search"])
            title = movie["Title"]
            year = movie["Year"]
            imdb_id = movie["imdbID"]
            return f"الفلم العشوائي: {title} ({year})\nرابط IMDb: https://www.imdb.com/title/{imdb_id}/"
    except:
        pass
    return "The Texas Chain Saw Massacre (1974) - حدث خطأ في الجلب ولكن هذا كلاسيكي!"

def send_email(content):
    email_user = "ddt42202@gmail.com"
    email_pass = os.environ.get('EMAIL_PASSWORD') # يُسحب من GitHub Secrets

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = '👻 مقترح رعب عشوائي'
    msg['From'] = email_user
    msg['To'] = email_user

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

if __name__ == "__main__":
    movie_info = get_random_horror_movie()
    send_email(movie_info)
