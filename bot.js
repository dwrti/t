const axios = require('axios');

async function getDirectLink() {
    // هذا هو المعرف (Hash) حق الملف الكبير اللي تبي تشغله
    const torrentHash = "93743992fdffe15b7e075a2e81c5b05c5072c1bc"; 
    const apiUrl = `https://api.webtor.io/v1/cached/${torrentHash}`;

    try {
        console.log("⏳ جاري جلب الرابط من سيرفر Webtor...");
        const response = await axios.get(apiUrl);
        
        // هنا نسحب رابط الـ Stream المباشر اللي يدعم الأحجام الكبيرة
        const directStream = `https://viewer.webtor.io/${torrentHash}`; 

        if (directStream) {
            const dbUrl = "https://axnt-68677-default-rtdb.europe-west1.firebasedatabase.app/live_stream.json";
            await axios.patch(dbUrl, { 
                url: directStream,
                status: "playing"
            });
            console.log("✅ انصاد الرابط للملف الكبير: " + directStream);
        }
    } catch (e) {
        console.error("❌ السيرفر رفض الطلب: ", e.message);
    }
}
getDirectLink();
