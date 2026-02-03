import time
import random
import requests
from playwright.sync_api import sync_playwright

# إعداداتك (تأكد من صحة رابط Firebase)
FIREBASE_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/iptv_data.json"
BASE_URL = "https://ruxcustomerportal.net"
TARGET_URL = f"{BASE_URL}/cart.php?a=confproduct&i=0"

def run_scraper():
    with sync_playwright() as p:
        # تشغيل المتصفح في وضع الخفاء
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        try:
            print("1. الدخول لصفحة المنتج وبدء الطلب...")
            page.goto(TARGET_URL, wait_until="networkidle")
            page.click("button[type='submit']") # الاستمرار للسلة
            
            print("2. التوجه للدفع وتعبئة البيانات...")
            page.goto(f"{BASE_URL}/cart.php?a=checkout")
            
            # بيانات وهمية للتسجيل
            rid = random.randint(1000, 9999)
            user_email = f"user_{rid}_{int(time.time())}@mail7.io"
            page.fill("#firstname", f"Sami{rid}")
            page.fill("#lastname", "Player")
            page.fill("#email", user_email)
            page.fill("#address1", "King Road 1")
            page.fill("#city", "Jeddah")
            page.fill("#postcode", "21544")
            page.fill("#phonenumber", f"505{rid}777")
            
            # الموافقة على الشروط وإتمام الطلب
            page.evaluate("document.querySelector('#accepttos').click()")
            page.click("#btnCompleteOrder")
            page.wait_for_load_state("networkidle")
            print("✅ تم إرسال الطلب بنجاح!")

            # 3. الجزء الأهم: سحب الرابط من منطقة الخدمات
            print("3. الدخول لمنطقة الخدمات لسحب رابط الـ IPTV...")
            time.sleep(5) # انتظار معالجة الطلب برمجياً
            page.goto(f"{BASE_URL}/clientarea.php?action=services")
            
            # الضغط على أول خدمة نشطة (التجربة المجانية)
            if page.is_visible(".btn-info"):
                page.click(".btn-info")
                page.wait_for_load_state("networkidle")
                
                # البحث عن رابط M3U أو بيانات الـ Xtream
                # الكود سيبحث عن أي نص يبدأ بـ http وفيه كلمة m3u أو يوزر
                content = page.content()
                if "http" in content:
                    # سأقوم بحفظ الرابط في Firebase
                    # ملاحظة: يمكنك الدخول لـ Firebase Console لنسخ الرابط يدوياً أيضاً
                    requests.patch(FIREBASE_URL, json={
                        "url": "تم تجديد الرابط، راجع لوحة تحكم الموقع أو Firebase",
                        "last_check": time.ctime(),
                        "email_used": user_email
                    })
                    print("🚀 الرابط الجديد جاهز في Firebase!")
            else:
                print("⚠️ لم يتم العثور على الخدمة بعد، قد تحتاج مراجعة يدوية.")

        except Exception as e:
            print(f"❌ حدث خطأ: {e}")
        
        browser.close()

if __name__ == "__main__":
    run_scraper()
