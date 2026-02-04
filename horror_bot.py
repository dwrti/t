import requests
import random
import smtplib
import os
from email.message import EmailMessage

# سنستخدم مكتبة ترجمة بسيطة وخفيفة
# ملاحظة: يجب إضافة 'pip install deep-translator' في ملف الـ workflow
from deep_translator import GoogleTranslator

def get_random_horror_movie():
    api_key = "B43d8afb"
    year = random.randint(1980, 2025)
    # أضفنا &plot=full لجلب قصة الفلم كاملة
    url = f"http://www.omdbapi.com/?s=horror&type=movie&y={year}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("Response") == "True" and "Search" in data:
            movie_summary = random.choice(data["Search"])
            imdb_id = movie_summary["imdbID"]
            
            # جلب تفاصيل الفلم بدقة أكبر باستخدام الـ ID
            details_url = f"http://www.omdbapi.com/?i={imdb_id}&plot=full&apikey={api_key}"
            movie = requests.get(details_url).json()
            
            title = movie.get("Title", "غير معروف")
            movie_year = movie.get("Year", "غير معروف")
            plot_en = movie.get("Plot", "لا توجد قصة متاحة.")
            
            # ترجمة القصة للعربية
            try:
                plot_ar = GoogleTranslator(source='en', target='ar').translate(plot_en)
            except:
                plot_ar = "تعذرت الترجمة الآلية للقصة."

            return f"🎬 مقترح الليلة العشوائي:\n\n" \
                   f"اسم الفلم: {title}\n" \
                   f"سنة الإنتاج: {movie_year}\n" \
                   f"القصة بالعربي: {plot_ar}\n\n" \
                   f"رابط IMDb: https://www.imdb.com/title/{imdb_id}/"
    except:
        pass
    return "حدث خطأ في الجلب، حاول تشغيل البوت مرة أخرى!"

def send_email(content):
    email_user = "ddt42202@gmail.com"
    email_pass = os.environ.get('EMAIL_PASSWORD') 

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = '👻 بوت الرعب: فلمك مع القصة بالعربي'
    msg['From'] = email_user
    msg['To'] = email_user

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

if __name__ == "__main__":
    movie_info = get_random_horror_movie()
    send_email(movie_info)
