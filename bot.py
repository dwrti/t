import requests
import asyncio
from playwright.async_api import async_playwright
import random

# إعداد قاعدة البيانات الخاصة بك
DB_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

async def get_random_movie():
    async with async_playwright() as p:
        # تشغيل المتصفح
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        try:
            print("🚀 جاري البحث عن فيلم...")
            await page.goto("https://cineby.bz/movie", wait_until="networkidle")
            
            # جلب الروابط المتاحة
            links = await page.query_selector_all("a[href^='/movie/']")
            if not links:
                print("❌ لم يتم العثور على أفلام.")
                return

            chosen_link = random.choice(links)
            href = await chosen_link.get_attribute("href")
            movie_url = f"https://cineby.bz{href}"
            
            # الخطوة السحرية: تحويل الرابط إلى صيغة Embed المباشرة
            # معظم الأفلام في الموقع تعمل بهذا المسار المباشر
            final_embed = movie_url.replace("/movie/", "/embed/movie/")
            
            print(f"✅ تم اختيار: {final_embed}")

            # تحديث Firebase
            # نرسل الرابط كـ "url" ليتم التقاطه بواسطة iframe في كود الـ HTML الخاص بك
            payload = {
                "url": final_embed,
                "status": "playing",
                "time": 0,
                "syncEnabled": True
            }
            
            response = requests.patch(DB_URL, json=payload)
            if response.status_code == 200:
                print("✨ تم إرسال الفيلم للمشغل بنجاح!")
            else:
                print(f"⚠️ فشل التحديث: {response.status_code}")

        except Exception as e:
            print(f"🔥 خطأ تقني: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_random_movie())
