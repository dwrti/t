import requests
import random
import smtplib
import os
from email.message import EmailMessage

def get_random_horror_movie():
    # استخدام مفتاح الـ API الجديد الخاص بك
    api_key = "B43d8afb"
    
    # توليد سنة عشوائية لضمان عدم تكرار الأفلام
    year = random.randint(1975, 2025)
    url = f"http://www.omdbapi.com/?s=horror&type=movie&y={year}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # التأكد من وجود نتائج للسنة المختارة
        if data.get("Response") == "True" and "Search" in data:
            movie = random.choice(data["Search"])
            title = movie["Title"]
            movie_year = movie["Year"]
            imdb_id = movie["imdbID"]
            return f"🎬 مقترح الليلة العشوائي:\n\nاسم الفلم: {title}\nسنة الإنتاج: {movie_year}\nرابط IMDb: https://www.imdb.com/title/{imdb_id}/"
        else:
            # إذا لم يجد أفلام في تلك السنة، يبحث بشكل عام عن كلمة رعب
            fallback_url = f"http://www.omdbapi.com/?s=horror&type=movie&apikey={api_key}"
            resp = requests.get(fallback_url).json()
            movie = random.choice(resp["Search"])
            return f"🎬 مقترح الليلة العشوائي:\n\nاسم الفلم: {movie['Title']}\nسنة الإنتاج: {movie['Year']}\nرابط IMDb: https://www.imdb.com/title/{movie['imdbID']}/"
            
    except Exception as e:
        return "The Texas Chain Saw Massacre (1974) - حدث خطأ بسيط في الاتصال، لكن هذا الفلم كلاسيكي ومضمون!"

def send_email(content):
    email_user = "ddt42202@gmail.com"
    # يسحب الباسورد من الـ Secrets في GitHub (تأكد انك سميته EMAIL_PASSWORD)
    email_pass = os.environ.get('EMAIL_PASSWORD') 

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = '👻 بوت الرعب: فلمك العشوائي جاهز'
    msg['From'] = email_user
    msg['To'] = email_user

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            print("تم إرسال الإيميل بنجاح!")
    except Exception as e:
        print(f"فشل إرسال الإيميل: {e}")

if __name__ == "__main__":
    movie_info = get_random_horror_movie()
    send_email(movie_info)
