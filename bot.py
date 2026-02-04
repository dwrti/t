import requests
import asyncio
from playwright.async_api import async_playwright
import random

DB_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

async def get_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # 1. محاولة جلب فيلم عشوائي
            await page.goto("https://cineby.bz/movie", wait_until="networkidle")
            links = await page.query_selector_all("a[href^='/movie/']")
            if links:
                chosen = await random.choice(links).get_attribute("href")
                final_url = f"https://cineby.bz{chosen}".replace("/movie/", "/embed/movie/")
                
                # 2. تحديث Firebase
                requests.patch(DB_URL, json={"url": final_url, "status": "playing"})
                print(f"✅ تم تضبيط الفيلم: {final_url}")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_content())
