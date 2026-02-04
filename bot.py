import os
import time
import random
import googleapiclient.discovery

# --- جلب الأسرار من خزنة GitHub ---
# سيقوم البوت بسحب المفتاح الذي وضعته في Secrets تلقائياً
API_KEY = os.environ.get('YOUTUBE_API_KEY') 

# إعدادات القناة (الهدف: الجزيرة)
TARGET_CHANNEL_ID = "UCfiwzLy-8yKzIbsmZTzxwWA"

# قائمة التعليقات الخاصة بك
COMMENTS = [
    "تغطية مميزة كالعادة، شكراً لكم.",
    "متابعكم أولاً بأول، استمروا.",
    "تحية طيبة لكم على هذا النقل."
]

def get_latest_video(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']['videoId']
    return None

def main():
    if not API_KEY:
        print("خطأ: لم يتم العثور على المفتاح في Secrets!")
        return

    print(f"بدأ الرادار بمراقبة قناة الجزيرة باستخدام المفتاح: {API_KEY[:5]}***")
    
    # تحديد آخر فيديو موجود حالياً
    last_video_id = get_latest_video(API_KEY, TARGET_CHANNEL_ID)
    
    # هذه الحلقة ستبقى تعمل لفحص القناة
    while True:
        try:
            current_video_id = get_latest_video(API_KEY, TARGET_CHANNEL_ID)
            
            if current_video_id and current_video_id != last_video_id:
                print("!!! تم رصد فيديو جديد الآن !!!")
                # ملاحظة: التعليق يحتاج لملف JSON سنقوم ببرمجته لاحقاً في الـ Workflow
                print(f"الفيديو الجديد هو: {current_video_id}")
                last_video_id = current_video_id
            
            # فحص كل دقيقة (للحفاظ على رصيد الـ API مجانياً)
            time.sleep(60) 
            
        except Exception as e:
            print(f"انتظار... (حدث خطأ بسيط: {e})")
            time.sleep(120)

if __name__ == "__main__":
    main()
