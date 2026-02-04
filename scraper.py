import time
import random
import requests
from playwright.sync_api import sync_playwright

def run_scraper():
    # هذا الرابط اللي بنخزن فيه النتيجة لإرسالها بالإيميل
    found_link = "لم يتم العثور على رابط جديد"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # عملية التسجيل في الموقع
            page.goto("https://ruxcustomerportal.net/cart.php?a=confproduct&i=0")
            # ... باقي خطوات الكود ...
            
            # نفترض أننا وجدنا الرابط هنا
            found_link = "http://example.com/iptv_link_here" 
            browser.close()
    except Exception as e:
        found_link = f"حدث خطأ: {str(e)}"

    # السطر السحري: يحفظ الرابط في ملف عشان يقرأه قيت هاب
    with open("iptv_link.txt", "w") as f:
        f.write(found_link)

if __name__ == "__main__":
    run_scraper()
