import time
import random
import requests
from playwright.sync_api import sync_playwright

FIREBASE_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/iptv_data.json"

def run_scraper():
    found_link = "لم يتم العثور على رابط جديد بعد"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # الدخول للموقع الحقيقي وبدء التسجيل
            page.goto("https://ruxcustomerportal.net/cart.php?a=confproduct&i=0", wait_until="networkidle")
            page.click("button[type='submit']")
            page.goto("https://ruxcustomerportal.net/cart.php?a=checkout")
            
            # تعبئة البيانات عشوائياً
            rid = random.randint(1000, 9999)
            user_email = f"user_{rid}_{int(time.time())}@mail7.io"
            page.fill("#firstname", f"Sami{rid}")
            page.fill("#lastname", "Player")
            page.fill("#email", user_email)
            page.fill("#address1", "King Road 1")
            page.fill("#city", "Jeddah")
            page.fill("#postcode", "21544")
            page.fill("#phonenumber", f"505{rid}777")
            
            # إنهاء الطلب
            page.evaluate("document.querySelector('#accepttos').click()")
            page.click("#btnCompleteOrder")
            page.wait_for_load_state("networkidle")

            # الذهاب لجلب الرابط
            time.sleep(10)
            page.goto("https://ruxcustomerportal.net/clientarea.php?action=services")
            
            if page.is_visible(".btn-info"):
                page.click(".btn-info")
                page.wait_for_load_state("networkidle")
                
                # صيد الرابط الفعلي
                hrefs = page.locator("a").evaluate_all("list => list.map(a => a.href)")
                for link in hrefs:
                    if "get.php" in link or "m3u" in link:
                        found_link = link
                        break
            
            # تحديث Firebase
            requests.patch(FIREBASE_URL, json={"url": found_link, "email": user_email})
            browser.close()
            
    except Exception as e:
        found_link = f"حدث خطأ أثناء الصيد: {str(e)}"

    # حفظ الرابط في الملف ليرسله GitHub لإيميلك
    with open("iptv_link.txt", "w") as f:
        f.write(found_link)

if __name__ == "__main__":
    run_scraper()
