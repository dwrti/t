const puppeteer = require('puppeteer');
const axios = require('axios');

async function getNewLink() {
    const browser = await puppeteer.launch({ 
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    
    // ميزة القناص: مراقبة الروابط اللي تطلع من الصفحة
    let interceptedLink = null;
    await page.setRequestInterception(true);
    page.on('request', request => {
        const url = request.url();
        // إذا الرابط فيه كلمة download و direct يعني هذا هو هدفنا
        if (url.includes('download/direct') || url.includes('stream/token')) {
            interceptedLink = url;
        }
        request.continue();
    });

    const webtorUrl = "https://webtor.io/93743992fdffe15b7e075a2e81c5b05c5072c1bc?pwd=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001&file=%2fارشيف%20قناة%20سبيستون%20من%20سنة%202000%20الى%202001%2faaalan-bokymon-algzaa-alsads-aal-kna-nyo-ty-fy.mp4";

    try {
        console.log("⏳ فتح صفحة سبيستون...");
        await page.goto(webtorUrl, { waitUntil: 'networkidle2', timeout: 90000 });

        console.log("🖱️ الضغط على Download...");
        await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button, a, span'));
            const downloadBtn = btns.find(b => b.innerText.toLowerCase().includes('download'));
            if (downloadBtn) downloadBtn.click();
        });

        await new Promise(r => setTimeout(r, 10000));

        console.log("🎯 محاولة صيد الرابط من الزر الوردي...");
        await page.evaluate(() => {
            const pinkBtns = Array.from(document.querySelectorAll('button, div, span'));
            const copyBtn = pinkBtns.find(el => el.innerText.toLowerCase().trim() === 'copy url');
            if (copyBtn) copyBtn.click(); // نضغط عليه عشان يحفز توليد الرابط
        });

        // ننتظر ثواني للصيد
        await new Promise(r => setTimeout(r, 10000));

        if (interceptedLink) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { url: interceptedLink, status: "playing" });
            console.log("✅ كفووو! انصاد الرابط: " + interceptedLink);
        } else {
            console.log("❌ الرابط ما انصاد من الشبكة. بنجرب حل أخير...");
            // محاولة أخيرة لسحب أي رابط مباشر موجود في الصفحة
            const backupLink = await page.evaluate(() => {
                const link = document.querySelector('a[href*="download/direct"]');
                return link ? link.href : null;
            });
            if (backupLink) {
                await axios.patch("https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json", { url: backupLink });
                console.log("✅ تم التحديث برابط احتياطي!");
            }
        }
    } catch (e) {
        console.error("❌ حصل خطأ: ", e.message);
    } finally {
        await browser.close();
    }
}
getNewLink();
