import requests
from bs4 import BeautifulSoup
import json

def grab_epg():
    url = "https://www.aljazeera.net/schedule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print("جاري سحب البيانات من موقع الجزيرة...")
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        script = soup.find('script', id='__NEXT_DATA__')
        
        if not script:
            print("فشل العثور على وسم البيانات __NEXT_DATA__")
            return

        data = json.loads(script.string)
        # استخراج قائمة البرامج من مسار البيانات في Next.js
        programs = data.get('props', {}).get('pageProps', {}).get('schedule', [])
        
        if not programs:
            print("لم يتم العثور على أي برامج في الجدول حالياً.")
            return

        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<tv generator-info-name="Gemini Scraper">\n'
        xml += '  <channel id="Aljazeera.Arabic">\n'
        xml += '    <display-name>Al Jazeera Arabic</display-name>\n'
        xml += '    <icon src="https://www.aljazeera.net/favicon.ico"/>\n'
        xml += '  </channel>\n'
        
        for p in programs:
            title = p.get('title', 'عنوان غير معروف')
            # تنسيق الوقت ليتوافق مع معايير XMLTV
            start = p.get('startDate', '').replace('-', '').replace(':', '').replace('T', '').split('.')[0]
            # إذا لم يتوفر وقت النهاية، نفترض أنه بعد ساعة
            xml += f'  <programme start="{start} +0300" channel="Aljazeera.Arabic">\n'
            xml += f'    <title lang="ar">{title}</title>\n'
            if p.get('description'):
                xml += f'    <desc lang="ar">{p.get("description")}</desc>\n'
            xml += '  </programme>\n'
            
        xml += '</tv>'
        
        with open("aljazeera_epg.xml", "w", encoding="utf-8") as f:
            f.write(xml)
        print("تم إنشاء ملف aljazeera_epg.xml بنجاح.")
            
    except Exception as e:
        print(f"حدث خطأ أثناء التشغيل: {e}")

if __name__ == "__main__":
    grab_epg()
