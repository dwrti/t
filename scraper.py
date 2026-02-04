import time
import random
from playwright.sync_api import sync_playwright

def run_scraper():
    found_link = "لم يتم العثور على الرابط"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 1. الدخول واختيار التصنيف (الصورة 1 و 9)
            page.goto("https://ruxcustomerportal.net/cart.php?a=confproduct&i=0")
            page.select_option("select[name='gid']", label="Free IPTV Trial")
            
            # 2. الضغط على Continue (الصورة 2 و 10)
            page.wait_for_selector("button:has-text('Continue')")
            page.click("button:has-text('Continue')")
            
            # 3. الضغط على Checkout (الصورة 3 و 11)
            page.wait_for_selector("a:has-text('Checkout')")
            page.click("a:has-text('Checkout')")
            
            # 4. تعبئة الإيميل والباسورد عشوائياً (الصورة 4 و 12)
            rid = random.randint(1000, 9999)
            random_email = f"user{rid}{int(time.time())}@gmail.com"
            random_password = f"Pass{rid}!{rid}"
            page.fill("#inputEmail", random_email)
            page.fill("#inputPassword1", random_password)
            page.fill("#inputPassword2", random_password)
            
            # 5. إنهاء الطلب (الصورة 5 و 13)
            page.click("#btnCompleteOrder")
            
            # 6. التوجه للوحة التحكم (الصورة 6 و 14)
            time.sleep(20) # وقت مستقطع لمعالجة الطلب
            page.wait_for_selector("a:has-text('Continue To Client Area')")
            page.click("a:has-text('Continue To Client Area')")

            # 7. الدخول للخدمات (الصورة 7 و 15)
            page.goto("https://ruxcustomerportal.net/clientarea.php?action=services")
            
            # 8. الضغط على Active (الصورة 16)
            page.wait_for_selector(".label-active")
            page.click(".label-active")
            
            # 9. صيد الرابط النهائي (الصورة 8 و 17)
            time.sleep(5)
            # استخراج النص الموجود في خانة الرابط بجانب كلمة Playlist
            final_link_element = page.locator("input[readonly]").first
            if final_link_element:
                found_link = final_link_element.input_value()
            
            browser.close()
    except Exception as e:
        found_link = f"حدث خطأ: {str(e)}"

    # حفظ الرابط في ملف ليرسله GitHub لإيميلك ddt42202@gmail.com
    with open("iptv_link.txt", "w") as f:
        f.write(found_link)

if __name__ == "__main__":
    run_scraper()
