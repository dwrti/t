import os
import time
import googleapiclient.discovery

# سحب المفتاح من الخزنة التي سميتها YOUTUBE_API_KEY
API_KEY = os.environ.get('YOUTUBE_API_KEY') 

# الهدف: قناة الجزيرة
TARGET_CHANNEL_ID = "UCfiwzLy-8yKzIbsmZTzxwWA"

def get_latest_video(api_key, channel_id):
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            order="date",
            maxResults=1,
            type="video"
        )
        response = request.execute()
        if response.get('items'):
            return response['items'][0]['id']['videoId']
    except Exception as e:
        print(f"خطأ في الاتصال بالرادار: {e}")
    return None

def main():
    if not API_KEY:
        print("خطأ: لم يتم العثور على المفتاح في الخزنة (Secrets)!")
        return

    print("تم تشغيل البوت بنجاح.. جاري مراقبة قناة الجزيرة.")
    
    # تحديد الفيديو الأخير عند بدء التشغيل
    last_video_id = get_latest_video(API_KEY, TARGET_CHANNEL_ID)
    print(f"آخر فيديو تم رصده حالياً: {last_video_id}")

    # فحص القناة لمرة واحدة (لأن GitHub Actions سيعيد تشغيله تلقائياً)
    current_video_id = get_latest_video(API_KEY, TARGET_CHANNEL_ID)
    
    if current_video_id and current_video_id != last_video_id:
        print(f"!!! فيديو جديد مكتشف: {current_video_id} !!!")
        # هنا ستتم إضافة وظيفة التعليق لاحقاً بمجرد ربط الـ JSON
    else:
        print("لا يوجد فيديو جديد حتى الآن. سأتحقق في الجولة القادمة.")

if __name__ == "__main__":
    main()
