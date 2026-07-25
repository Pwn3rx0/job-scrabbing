# LinkedIn Jobs Scraper - واجهة ويب

تطبيق بسيط بواجهة رسومية (Streamlit) للبحث عن وظائف على LinkedIn وتحميل النتائج كـ CSV.

## طريقة النشر (5 دقايق، مجاني، وهتاخد رابط تبعته لأي حد)

### الخطوة 1: ارفع الملفات على GitHub
1. اعمل حساب على [github.com](https://github.com) لو معندكش.
2. اعمل Repository جديد (public).
3. ارفع فيه الملفين:
   - `app.py`
   - `requirements.txt`

### الخطوة 2: انشر على Streamlit Community Cloud
1. روح على [share.streamlit.io](https://share.streamlit.io)
2. سجل دخول بحساب GitHub بتاعك (مجاني تمامًا).
3. دوس **"New app"**.
4. اختار الـ Repository اللي رفعته، وحدد الملف الرئيسي: `app.py`
5. دوس **Deploy**.
6. بعد دقيقة أو اتنين هيديك رابط زي:
   `https://your-app-name.streamlit.app`

7. ابعت الرابط ده لأي حد، وهيقدر يفتحه من المتصفح مباشرة (موبايل أو كمبيوتر) من غير ما يحمل أي برنامج.

## ملحوظات مهمة

- ده بيستخدم صفحات LinkedIn العامة (Guest API)، فمفيش تسجيل دخول مطلوب، لكن لو حد استخدمه كتير أو بسرعة عالية ممكن LinkedIn يحظر الـ IP بتاع السيرفر مؤقتًا.
- لو حابب تحمي التطبيق من الاستخدام الكتير (Rate limiting) قولّي وأظبطلك ده.
- Streamlit Community Cloud مجاني بالكامل للمشاريع الصغيرة/الشخصية.
