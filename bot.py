import requests
import asyncio
from playwright.async_api import async_playwright
import random

DB_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

async def get_random_movie():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # الدخول لصفحة الأفلام
            await page.goto("https://cineby.bz/movie", wait_until="networkidle")
            
            # جلب كل روابط الأفلام
            links = await page.query_selector_all("a[href^='/movie/']")
            chosen_link = random.choice(links)
            href = await chosen_link.get_attribute("href")
            
            # الرابط النهائي للفيلم
            movie_url = f"https://cineby.bz{href}"
            
            # تضبيط الرابط ليفتح المشغل مباشرة (Embed)
            # موقع cineby غالباً يستخدم هذا النمط للمشغل المباشر:
            embed_url = movie_url.replace("/movie/", "/embed/movie/")

            # إرسال الرابط لـ Firebase
            requests.patch(DB_URL, json={"url": embed_url, "status": "playing", "time": 0})
            print(f"Done! Sent: {embed_url}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_random_movie())
