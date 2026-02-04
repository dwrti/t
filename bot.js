const puppeteer = require('puppeteer');
const axios = require('axios');

async function getNewLink() {
    const browser = await puppeteer.launch({ 
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 1000 });

    const webtorUrl = "https://webtor.io/93743992fdffe15b7e075a2e81c5b05c5072c1bc?pwd=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001&file=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001%2faaalan-bokymon-algzaa-alsads-aal-kna-nyo-ty-fy.mp4";

    try {
        console.log("⏳ فتح الصفحة...");
        await page.goto(webtorUrl, { waitUntil: 'networkidle2', timeout: 90000 });

        console.log("🖱️ الضغط على زر Download الأساسي...");
        await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button, a'));
            const downloadBtn = btns.find(b => b.innerText.toLowerCase().includes('download'));
            if (downloadBtn) downloadBtn.click();
        });

        // انتظار ظهور الخيارات الوردية
        await new Promise(r => setTimeout(r, 15000));

        console.log("🎯 استخراج الرابط المباشر بالإجبار...");
        const directLink = await page.evaluate(() => {
            // نبحث عن أي رابط يحتوي على كلمة "direct" أو "token" في الكود المولد
            const allLinks = Array.from(document.querySelectorAll('a'));
            const target = allLinks.find(a => a.href.includes('download/direct') || a.href.includes('stream/token'));
            
            if (target) return target.href;

            // محاولة جلب الرابط من أي نص مخفي داخل الأزرار الوردية
            const pinkBtn = Array.from(document.querySelectorAll('button, a, div')).find(el => el.innerText.toLowerCase().includes('copy url'));
            return pinkBtn ? (pinkBtn.getAttribute('data-url') || pinkBtn.getAttribute('data-link')) : null;
        });

        if (directLink && directLink.startsWith('http')) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: directLink, status: "playing" });
            console.log("✅ كفو! تم صيد الرابط: " + directLink);
        } else {
            console.log("❌ فشلنا في الصيد، باخذ لقطة أخيرة للشاشة للتأكد من المحتوى.");
            await page.screenshot({ path: 'final_check.png' });
        }
    } catch (e) {
        console.error("❌ خطأ فني: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
