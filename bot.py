import requests
import re

# مصادر مجمعة لروابط IPTV محدثة
SOURCES = [
    "https://raw.githubusercontent.com/skylive-v1/IPTV-Arabic/main/Arabic.m3u",
    "https://iptv-org.github.io/iptv/languages/ara.m3u"
]
DB_URL = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json"

def get_bein_link():
    for source in SOURCES:
        try:
            print(f"Searching in {source}...")
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                content = response.text
                # البحث عن قنوات beIN Sports باستخدام Regex
                # نبحث عن السطر الذي يحتوي على الاسم ثم الرابط الذي يليه
                matches = re.findall(r'#EXTINF.*beIN.*?\n(http.*)', content, re.IGNORECASE)
                
                if matches:
                    # نأخذ أول رابط يعمل (غالباً beIN 1)
                    bein_url = matches[0].strip()
                    print(f"✅ Found: {bein_url}")
                    return bein_url
        except:
            continue
    return None

def update_firebase(url):
    payload = {"url": url, "status": "playing", "time": 0}
    requests.patch(DB_URL, json=payload)

if __name__ == "__main__":
    link = get_bein_link()
    if link:
        update_firebase(link)
        print("Done! Check your player.")
    else:
        print("❌ No working beIN links found today.")
