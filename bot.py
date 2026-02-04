import requests
import asyncio
from playwright.async_api import async_playwright
import random

# إعدادات Firebase الخاصة بك
DB_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

async def get_random_movie():
    async with async_playwright() as p:
        # تشغيل المتصفح بوضع التخفي
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # الدخول للموقع
            print("جاري الدخول إلى Cineby...")
            await page.goto("https://cineby.bz/movie", wait_until="networkidle")
            
            # اختيار فيلم عشوائي من القائمة
            movies = await page.query_selector_all("a.post-title")
            if not movies:
                print("لم يتم العثور على أفلام!")
                return
            
            random_movie = random.choice(movies)
            movie_url = await random_movie.get_attribute("href")
            movie_name = await random_movie.inner_text()
            full_url = f"https://cineby.bz{movie_url}"
            
            print(f"تم اختيار فيلم: {movie_name}")
            
            # تحديث Firebase
            data = {
                "url": full_url, # ملاحظة: المواقع المشفرة تتطلب مشغل خاص، لكننا سنضع الرابط هنا
                "status": "playing",
                "time": 0
            }
            
            response = requests.patch(DB_URL, json=data)
            if response.status_code == 200:
                print("تم تحديث مشغلك بنجاح! ✅")
            else:
                print("فشل تحديث Firebase.")

        except Exception as e:
            print(f"حدث خطأ: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_random_movie())
