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

        console.log("🖱️ الضغط على Download...");
        await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button, a, span'));
            const downloadBtn = btns.find(b => b.innerText.toLowerCase().includes('download'));
            if (downloadBtn) downloadBtn.click();
        });

        // ننتظر القائمة الوردية تظهر
        await new Promise(r => setTimeout(r, 15000));

        console.log("🔗 استخراج الرابط من زر Copy URL الوردي...");
        const directLink = await page.evaluate(() => {
            // نبحث عن الزر اللي مكتوب فيه 'copy url'
            const allElements = Array.from(document.querySelectorAll('button, a, div, span'));
            const copyBtn = allElements.find(el => el.innerText.toLowerCase().trim() === 'copy url');
            
            if (copyBtn) {
                // في webtor الرابط غالباً يكون مخزن في سمة معينة أو نأخذه من كود الصفحة
                // بنجرب نسحب أحدث رابط مباشر تم توليده في الشبكة
                return window.location.origin + document.querySelector('a[href*="download/direct"]')?.getAttribute('href') 
                       || copyBtn.getAttribute('data-url') 
                       || document.querySelector('a[download]')?.href;
            }
            // محاولة أخيرة: إذا ما لقينا الزر، نسحب أي رابط 'direct' موجود
            const directLinkEl = document.querySelector('a[href*="direct"]');
            return directLinkEl ? directLinkEl.href : null;
        });

        if (directLink && directLink.startsWith('http')) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: directLink, status: "playing" });
            console.log("✅ بطل! تم التحديث: " + directLink);
        } else {
            console.log("❌ الزر الوردي طلع بس الرابط ما انمسك. باخذ صورة أخيرة.");
            await page.screenshot({ path: 'pink_buttons.png' });
        }
    } catch (e) {
        console.error("❌ خطأ: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
