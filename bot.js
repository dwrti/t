const puppeteer = require('puppeteer');
const axios = require('axios');

async function getNewLink() {
    const browser = await puppeteer.launch({ 
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    const webtorUrl = "https://webtor.io/93743992fdffe15b7e075a2e81c5b05c5072c1bc?pwd=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001&file=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001%2faaalan-bokymon-algzaa-alsads-aal-kna-nyo-ty-fy.mp4";

    try {
        await page.goto(webtorUrl, { waitUntil: 'networkidle2', timeout: 60000 });
        await page.waitForSelector('video', { timeout: 30000 });

        const directLink = await page.evaluate(() => {
            const v = document.querySelector('video');
            return v ? v.src : null;
        });

        if (directLink && directLink.startsWith('http')) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: directLink });
            console.log("✅ تم التحديث بنجاح: " + directLink);
        } else {
            console.log("❌ لم يتم العثور على رابط الفيديو");
        }
    } catch (e) {
        console.error("❌ خطأ أثناء التشغيل: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
