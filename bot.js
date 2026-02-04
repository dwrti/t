const puppeteer = require('puppeteer');
const axios = require('axios');

async function getNewLink() {
    const browser = await puppeteer.launch({ 
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    // ضبط حجم الشاشة عشان تظهر كل العناصر
    await page.setViewport({ width: 1280, height: 800 });

    const webtorUrl = "https://webtor.io/93743992fdffe15b7e075a2e81c5b05c5072c1bc?pwd=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001&file=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001%2faaalan-bokymon-algzaa-alsads-aal-kna-nyo-ty-fy.mp4";

    try {
        console.log("⏳ جاري الدخول للصفحة...");
        await page.goto(webtorUrl, { waitUntil: 'networkidle2', timeout: 90000 });

        // ننتظر 10 ثواني إضافية احتياطاً عشان السكربتات تشتغل
        await new Promise(r => setTimeout(r, 10000));

        console.log("🔍 جاري البحث عن رابط الفيديو...");
        const directLink = await page.evaluate(() => {
            // نبحث في كل عناصر الفيديو أو الـ Source
            const v = document.querySelector('video');
            const s = document.querySelector('source');
            return v ? v.src : (s ? s.src : null);
        });

        if (directLink && directLink.startsWith('http')) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: directLink, status: "playing" });
            console.log("✅ كفو! تم التحديث: " + directLink);
        } else {
            console.log("⚠️ لم نجد فيديو، باخذ لقطة شاشة للفحص...");
            await page.screenshot({ path: 'error.png' });
            console.log("❌ الرابط غير موجود في الصفحة حالياً.");
        }
    } catch (e) {
        console.error("❌ حصل خطأ: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
