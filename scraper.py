import time
import random
import requests
from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        found_link = "لم يتم العثور على رابط"
        
        try:
            # عملية الصيد
            page.goto("https://ruxcustomerportal.net/cart.php?a=confproduct&i=0")
            # ... (بقية خطوات التسجيل)
            
            # أهم سطرين عشان ما يعطي خطأ أحمر:
            with open("iptv_link.txt", "w") as f:
                f.write(found_link)
        except:
            with open("iptv_link.txt", "w") as f:
                f.write("خطأ في الجلب")
        browser.close()

if __name__ == "__main__":
    run_scraper()
