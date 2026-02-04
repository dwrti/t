import time
import random
import requests
import os
from playwright.sync_api import sync_playwright

FIREBASE_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/iptv_data.json"
BASE_URL = "https://ruxcustomerportal.net"
TARGET_URL = f"{BASE_URL}/cart.php?a=confproduct&i=0"

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        # القيمة الافتراضية إذا لم يجد الرابط
        found_link = "لم يتم العثور على الرابط تلقائياً، يرجى مراجعة الموقع"

        try:
            print("بدء عملية التسجيل...")
            page.goto(TARGET_URL, wait_until="networkidle")
            page.click("button[type='submit']")
            page.goto(f"{BASE_URL}/cart.php?a=checkout")
            
            rid = random.randint(1000, 9999)
            user_email = f"user_{rid}_{int(time.time())}@mail7.io"
            page.fill("#firstname", f"Sami{rid}")
            page.fill("#lastname", "Player")
            page.fill("#email", user_email)
            page.fill("#address1", "King Road 1")
            page.fill("#city", "Jeddah")
            page.fill("#postcode", "21544")
            page.fill("#phonenumber", f"505{rid}777")
            
            page.evaluate("document.querySelector('#accepttos').click()")
            page.click("#btnCompleteOrder")
            page.wait_for_load_state("networkidle")

            time.sleep(10) # وقت إضافي لتجهيز الخدمة
            page.goto(f"{BASE_URL}/clientarea.php?action=services")
            
            # البحث عن الرابط داخل صفحة الخدمات
            if page.is_visible(".btn-info"):
                page.click(".btn-info")
                page.wait_for_load_state("networkidle")
                
                # البحث عن أي نص يحتوي على http و m3u
                all_links = page.locator("a").all_text_contents()
                for l in all_links:
                    if "http" in l and ("m3u" in l or "get.php" in l):
                        found_link = l
                        break
            
            # تحديث Firebase
            requests.patch(FIREBASE_URL, json={"url": found_link, "email": user_email})
            
            # أهم خطوة: حفظ الرابط في ملف نصي ليقرأه GitHub ويرسله لك
            with open("iptv_link.txt", "w") as f:
                f.write(found_link)

        except Exception as e:
            with open("iptv_link.txt", "w") as f:
                f.write(f"حدث خطأ أثناء البحث: {str(e)}")
        
        browser.close()

if __name__ == "__main__":
    run_scraper()
