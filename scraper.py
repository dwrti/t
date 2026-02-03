import time
from playwright.sync_api import sync_playwright
import requests

# الرابط الخاص بك
WEBTOR_URL = "https://webtor.io/93743992fdffe15b7e075a2e81c5b05c5072c1bc?pwd=%2f%D8%A7%D8%B1%D8%B4%D9%8A%D9%81%20%D9%82%D9%86%D8%A7%D8%A9%20%D8%B3%D8%A8%D9%8A%D8%B3%D8%AA%D9%88%D9%86%20%D9%85%D9%86%20%D8%B3%D9%86%D8%A9%202000%20%D8%A7%D9%84%D9%89%202001&file=%2f%D8%A7%D8%B1%D8%B4%D9%8A%D9%81%20%D9%82%D9%86%D8%A7%D8%A9%20%D8%B3%D8%A8%D9%8A%D8%B3%D8%AA%D9%88%D9%86%20%D9%85%D9%86%20%D8%B3%D9%86%D8%A9%202000%20%D8%A7%D9%84%D9%89%202001%2faaalan-bokymon-algzaa-alsads-aal-kna-nyo-ty-fy.mp4"
FIREBASE_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

def refresh_link():
    with sync_playwright() as p:
        # تشغيل المتصفح مع تمويه الهوية لتجنب الحظر
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()
        
        print("جاري فتح Webtor...")
        page.goto(WEBTOR_URL, wait_until="domcontentloaded")
        
        try:
            # الانتظار حتى استخراج الرابط من المشغل
            page.wait_for_selector('video source', timeout=90000)
            direct_link = page.eval_on_selector("video source", "el => el.src")
            
            if direct_link:
                print(f"تم صيد الرابط: {direct_link}")
                # تحديث Firebase بالرابط الجديد
                requests.patch(FIREBASE_URL, json={"url": direct_link, "status": "playing"})
                print("✅ تم تحديث Firebase بنجاح!")
        except Exception as e:
            print(f"❌ فشل الاستخراج: {e}")
        
        browser.close()

if __name__ == "__main__":
    refresh_link()
