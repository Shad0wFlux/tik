# Instagram Account Creator ✨

أداة لإنشاء حسابات إنستجرام تلقائيًا باستخدام Gmail، مع رفع صور عشوائية وحفظ بيانات الحسابات، ودعم إشعارات تيليجرام.


شكرا خاص لـ https://t.me/HexGalaxy

## المميزات
- إنشاء حسابات تلقائيًا باستخدام Gmail.  
- توليد نسخ البريد تلقائيًا عبر dot-trick (كل النسخ تصل لصندوق بريد واحد).  
- رفع صور عشوائية لكل حساب.  
- إشعارات تيليجرام عبر bot.json (اختياري).

## التحضير

### 1. Gmail
ضع بياناتك في credentials.txt بصيغة:
yourmail@gmail.com:yourapppassword
anothermail@gmail.com:anotherapppassword

> يجب تفعيل التحقق بخطوتين 
وإنشاء كلمة مرور تطبيق.  

> شاهد هذا الفيديو للشرح: [تفعيل 2FA وإنشاء App Password]

https://www.youtube.com/shorts/WDfvVRVV8Js


### 2. إشعارات تيليجرام (اختياري)
ملف bot.json:
{
    "bot_token": "توكن البوت",
    "chat_id": "ايديك"
}

## ملاحظات
- الأداة تولد dot-trick تلقائيًا، مثال: إذا لديك example@gmail.com سيتم إنشاء حسابات مثل:
e.xample@gmail.com
ex.ample@gmail.com
exa.mple@gmail.com

كل النسخ تصل لصندوق بريد واحد.  
- كل Gmail رئيسي يمكنه إنشاء حتى 15 حسابًا.  
- بيانات الحسابات تحفظ في accounts/ و sessions/.  
- بدون bot.json، تعمل الأداة على إنشاء الحسابات فقط.

---