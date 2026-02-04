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
        console.log("⏳ جاري فتح الصفحة...");
        await page.goto(webtorUrl, { waitUntil: 'networkidle2', timeout: 90000 });

        // 1. الضغط على زر Download (اللي شفته في صورتك)
        console.log("🖱️ جاري الضغط على زر Download...");
        const downloadBtnSelector = 'button.btn-primary, .btn-download, button[data-action="download"]'; // محاولة تحديد الزر
        await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button, a'));
            const downloadBtn = btns.find(b => b.innerText.toLowerCase().includes('download'));
            if (downloadBtn) downloadBtn.click();
        });

        // 2. الانتظار حتى تظهر خيارات النسخ (مثل copy url في صورتك)
        await new Promise(r => setTimeout(r, 15000));

        // 3. سحب الرابط المباشر من زر "Copy URL" أو من طلبات الشبكة
        console.log("🔗 جاري استخراج الرابط المباشر...");
        const directLink = await page.evaluate(() => {
            // محاولة جلب الرابط من أي مكان يحتوي على 'video' أو 'download'
            const links = Array.from(document.querySelectorAll('a, button'));
            const urlBtn = links.find(l => l.innerText.toLowerCase().includes('copy url') || l.href?.includes('download/direct'));
            return urlBtn ? (urlBtn.href || urlBtn.getAttribute('data-url')) : null;
        });

        if (directLink && directLink.startsWith('http')) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: directLink, status: "playing" });
            console.log("✅ كفو! تم تحديث الرابط بنجاح: " + directLink);
        } else {
            console.log("❌ فشل استخراج الرابط بعد الضغط. باخذ لقطة شاشة ثانية...");
            await page.screenshot({ path: 'after_click.png' });
        }
    } catch (e) {
        console.error("❌ حصل خطأ في العملية: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
