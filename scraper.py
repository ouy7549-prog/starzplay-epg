import requests
from bs4 import BeautifulSoup
import json
import os

def grab_epg():
    url = "https://www.aljazeera.net/schedule"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # البحث عن البيانات داخل وسم Script
        script = soup.find('script', id='__NEXT_DATA__')
        data = json.loads(script.string)
        
        # الوصول إلى قائمة البرامج (المسار قد يتغير حسب تحديثات الموقع)
        # هذا المسار افتراضي بناءً على هيكل Next.js المعتاد للجزيرة
        programs = data['props']['pageProps'].get('schedule', [])
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        xml += '  <channel id="Aljazeera">\n    <display-name>Al Jazeera Arabic</display-name>\n  </channel>\n'
        
        for p in programs:
            title = p.get('title', 'No Title')
            start = p.get('startDate', '').replace('-', '').replace(':', '') # تنسيق بسيط للوقت
            xml += f'  <programme start="{start}" channel="Aljazeera">\n'
            xml += f'    <title lang="ar">{title}</title>\n'
            xml += '  </programme>\n'
            
        xml += '</tv>'
        
        with open("aljazeera_epg.xml", "w", encoding="utf-8") as f:
            f.write(xml)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    grab_epg()
