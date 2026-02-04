import time
import random
from playwright.sync_api import sync_playwright

def run_scraper():
    found_link = "لم يتم العثور على الرابط"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 1. الدخول واختيار Free IPTV Trial
            page.goto("https://ruxcustomerportal.net/cart.php?a=confproduct&i=0")
            page.select_option("select[name='gid']", label="Free IPTV Trial")
            
            # 2. الضغط على Continue ثم Checkout
            page.click("button:has-text('Continue')")
            page.wait_for_selector("a:has-text('Checkout')")
            page.click("a:has-text('Checkout')")
            
            # 3. تعبئة البيانات العشوائية (الإيميل والباسورد)
            rid = random.randint(1000, 9999)
            random_email = f"user{rid}{int(time.time())}@gmail.com"
            page.fill("#inputEmail", random_email)
            page.fill("#inputPassword1", "Pass123!@#")
            page.fill("#inputPassword2", "Pass123!@#")
            
            # 4. إنهاء الطلب والانتظار دقيقة كما طلبت (الخطوة 5 و 6)
            page.click("#btnCompleteOrder")
            time.sleep(60) 
            page.click("a:has-text('Continue To Client Area')")

            # 5. الدخول للخدمات والضغط على Active (الخطوة 7)
            page.goto("https://ruxcustomerportal.net/clientarea.php?action=services")
            page.click(".label-active")
            
            # 6. صيد الرابط من خانة Playlist (الخطوة 8 - الصورة الأخيرة)
            page.wait_for_selector("input[readonly]")
            found_link = page.locator("input[readonly]").first.input_value()
            
            browser.close()
    except Exception as e:
        found_link = f"حدث خطأ فني: {str(e)}"

    # حفظ الرابط في الملف ليرسله GitHub لإيميلك ddt42202@gmail.com
    with open("iptv_link.txt", "w") as f:
        f.write(found_link)

if __name__ == "__main__":
    run_scraper()
