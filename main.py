import requests
import time
import json


first_reports = [
    {
        "code": "[\"adult_content-nudity_or_sexual_activity\"]",
        "name": "عري أو نشاط جنسي"
    },
    {
        "code": "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]",
        "name": "يبدو كاستغلال جنسي دون 18"
    },
    {
        "code": "[\"adult_content-threat_to_share_nude_images-u18-yes\"]",
        "name": "تهديد بمشاركة صور عارية أو مشاركتها بالفعل دون 18"
    },
    {
        "code": "[\"suicide_or_self_harm_concern-suicide_or_self_injury\"]",
        "name": "انتحار أو إيذاء الذات"
    },
    {
        "code": "[\"ig_scam_financial_investment\"]",
        "name": "خداع بشأن الأموال أو الاستثمار"
    }
]

# القائمة الثانية للبلاغات بعد تغيير VPN
second_reports = [
    {
        "code": "[\"selling_or_promoting_restricted_items-drugs-high-risk\"]",
        "name": "أدوية شديدة الإدمان، مثل الكوكايين أو الهيروين أو الفينتانيل"
    },
    {
        "code": "[\"violent_hateful_or_disturbing-credible_threat\"]",
        "name": "تهديد جدّي للسلامة"
    },
    {
        "code": "[\"suicide_or_self_harm_concern-eating_disorder\"]",
        "name": "اضطرابات الأكل"
    },
    {
        "code": "[\"adult_content-threat_to_share_nude_images-u18-yes\"]",
        "name": "تهديد بمشاركة صور عارية أو مشاركتها بالفعل دون 18"
    },
    {
        "code": "[\"harrassment_or_abuse-harassment-me-u18-yes\"]",
        "name": "مضايقة أو اساءة لي (me)"
    },
    {
        "code": "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]",
        "name": "يبدو كاستغلال جنسي"
    }
]

url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"

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

def show_menu():
    print("\nثغره كارتنس")
    print("\nاختر طريقة الإبلاغ:")
    print("1. الإبلاغ العادي (من حساب واحد)")
    print("2. الإبلاغ المتعدد (من عدة حسابات)")
    
    while True:
        choice = input("\nأدخل اختيارك (1 أو 2): ").strip()
        if choice in ['1', '2']:
            return int(choice)
        print("اختيار غير صحيح. الرجاء إدخال 1 أو 2.")

def get_sleep_time():
    print("\nإعدادات الوقت بين البلاغات")
    print("أدخل المدة بالثواني بين كل بلاغ وآخر.")
    print("يُوصى بـ 2-5 ثواني لتجنب الاكتشاف")
    
    while True:
        try:
            sleep_time = int(input("\nأدخل الوقت بين البلاغات (بالثواني): ").strip())
            if sleep_time >= 0:
                return sleep_time
            print("الرجاء إدخال رقم موجب أو 0 لعدم وجود تأخير.")
        except ValueError:
            print("الرجاء إدخال رقم صحيح.")

def get_context(user_id, cookies):
    nok = {
        'container_module': 'profilePage',
        'entry_point': '1',
        'location': '2',
        'object_id': user_id,
        'object_type': '5',
        'frx_prompt_request_type': '1',
    }
    
    try:
        response = requests.post(
            'https://www.instagram.com/api/v1/web/reports/get_frx_prompt/',
            cookies=cookies,
            headers=headers,
            data=nok,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['response']['context']
        else:
            return None
    except:
        return None

def send_report(report_data, user_id, cookies, step_num, total_steps, phase_num, sleep_time):
    report_code = report_data["code"]
    report_name = report_data["name"]
    
    print(f"\nالمرحلة {phase_num} - البلاغ {step_num}/{total_steps}: {report_name}")
    print("-" * 50)
    
    time.sleep(1)
    
    context = get_context(user_id, cookies)
    
    if not context:
        print("فشل: تعذر الحصول على السياق")
        return False
    
    payload = {
        'container_module': "profilePage",
        'entry_point': "1",
        'location': "2",
        'object_id': user_id,
        'object_type': "5",
        'context': context,
        'selected_tag_types': report_code,
        'frx_prompt_request_type': "2",
        'jazoest': "22816"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("الحالة: ناجح")
            return True
        else:
            print(f"الحالة: فشل ({response.status_code})")
            return False
    except Exception as e:
        print(f"خطأ: {e}")
        return False

def send_reports_list(reports_list, user_id, cookies, phase_name, phase_num, sleep_time):
    print(f"\n{phase_name}")
    
    successful = 0
    total = len(reports_list)
    
    for i, report_data in enumerate(reports_list, 1):
        if send_report(report_data, user_id, cookies, i, total, phase_num, sleep_time):
            successful += 1
        
        if i < total and sleep_time > 0:
            print(f"\nانتظار {sleep_time} ثانية قبل البلاغ التالي...")
            time.sleep(sleep_time)
    
    print(f"\nاكتملت المرحلة {phase_num}: {successful}/{total} بلاغ")
    return successful

def normal_reporting():
    print("\nوضع الإبلاغ العادي")
    
    user_id = input("\nأدخل معرف المستهدف: ").strip()
    session_id = input("أدخل معرف الجلسة: ").strip()
    sleep_time = get_sleep_time()
    
    print("\nالرجاء تشغيل VPN الآن")
    print("اضغط Enter عندما يكون VPN نشطاً")
    input()
    
    print("\nجاري تهيئة النظام...")
    
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
        'sessionid': session_id,
        'rur': '"RVA\\05476486059622\\0541791670864:01fe3167f0753030cebb866598515e7ba79f9e395da4160195b582c2ab2f4272410b88ee"'
    }
    
    
    print("\nبدء المرحلة الأولى: أول 5 بلاغات")
    
    phase1_success = send_reports_list(first_reports, user_id, cookies, 
                                      "المرحلة الأولى: أول 5 بلاغات", 1, sleep_time)
    
    
    print("\nمطلوب تغيير VPN")
    print("الرجاء تغيير خادم VPN الآن")
    print("اضغط Enter عند تغيير VPN")
    input()
    
    
    print("\nبدء المرحلة الثانية: 6 بلاغات إضافية")
    
    phase2_success = send_reports_list(second_reports, user_id, cookies,
                                      , 2, sleep_time)
    
    
    print("\nاكتملت العملية")
    print(f"المرحلة الأولى (البلاغات 1-5): {phase1_success}/{len(first_reports)}")
    print(f"المرحلة الثانية (البلاغات 6-11): {phase2_success}/{len(second_reports)}")
    print(f"الإجمالي (جميع البلاغات 11): {phase1_success + phase2_success}/{len(first_reports) + len(second_reports)}")
    print(f"الوقت المستخدم بين البلاغات: {sleep_time} ثانية")

def validate_session(session_id):
    """التحقق من صلاحية معرف الجلسة"""
    test_cookies = {
        'sessionid': session_id,
        'csrftoken': 'FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k'
    }
    
    try:
        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram',
            cookies=test_cookies,
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def multi_account_reporting():
    print("\nوضع الإبلاغ المتعدد من عدة حسابات")
    
    user_id = input("\nأدخل معرف المستهدف: ").strip()
    
    print("\nأدخل معرفات الجلسات (واحد لكل سطر)")
    print("مثال:")
    print("23375113665%3AQ52........")
    print("78030994619%RJG%......")
    print(" اضغط Enter  مرتين عند الانتهاء")
    
    sessions = []
    while True:
        session = input().strip()
        if session == "":
            if sessions:
                break
            else:
                print("الرجاء إدخال معرف جلسة واحد على الأقل")
                continue
        sessions.append(session)
    
    sleep_time = get_sleep_time()
    
    # التحقق من الجلسات
    print("\nجاري التحقق من الجلسات...")
    
    valid_sessions = []
    for i, session in enumerate(sessions, 1):
        print(f"جاري التحقق من الجلسة {i}/{len(sessions)}... ", end="")
        if validate_session(session):
            print("صالحة")
            valid_sessions.append(session)
        else:
            print("غير صالحة")
    
    print(f"\nالجلسات الصالحة: {len(valid_sessions)}/{len(sessions)}")
    
    if not valid_sessions:
        print("لم يتم العثور على جلسات صالحة. جاري الخروج.")
        return
    
    print(f"\nبدء الإبلاغ من {len(valid_sessions)} حساب")
    
    total_reports_sent = 0
    total_accounts_used = 0
    
    for account_num, session_id in enumerate(valid_sessions, 1):
        print(f"\nالحساب {account_num}/{len(valid_sessions)}")
        
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
            'sessionid': session_id,
            'rur': '"RVA\\05476486059622\\0541791670864:01fe3167f0753030cebb866598515e7ba79f9e395da4160195b582c2ab2f4272410b88ee"'
        }
        
        print("\nالرجاء تشغيل VPN الآن")
        print("اضغط Enter عندما يكون VPN نشطاً")
        input()
        
        
        print(f"\nالحساب {account_num}: بدء المرحلة الأولى")
        
        phase1_success = send_reports_list(first_reports, user_id, cookies,
                                          f"الحساب {account_num} - المرحلة الأولى", 1, sleep_time)
        
        
        print("\nمطلوب تغيير VPN")
        print("الرجاء تغيير خادم VPN الآن")
        print("اضغط Enter عند تغيير VPN")
        input()
        
        
        print(f"\nالحساب {account_num}: بدء المرحلة الثانية")
        
        phase2_success = send_reports_list(second_reports, user_id, cookies,
                                          f"الحساب {account_num} - المرحلة الثانية", 2, sleep_time)
        
        total_reports_sent += (phase1_success + phase2_success)
        total_accounts_used += 1
        
        print(f"\nاكتمل الحساب {account_num}: {phase1_success + phase2_success}/11 بلاغ")
        
        
        if account_num < len(valid_sessions):
            print(f"\nجاري التحضير للحساب التالي خلال 5 ثواني...")
            time.sleep(5)
    
    
    print("\nاكتملت عملية الإبلاغ المتعدد")
    print(f"الحسابات المستخدمة: {total_accounts_used}/{len(valid_sessions)}")
    print(f"إجمالي البلاغات المرسلة: {total_reports_sent}")
    print(f"الحد الأقصى الممكن للبلاغات: {len(valid_sessions) * 11}")
    print(f"الوقت المستخدم بين البلاغات: {sleep_time} ثانية")

def main():
    choice = show_menu()
    
    if choice == 1:
        normal_reporting()
    else:
        multi_account_reporting()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nتم إلغاء العملية من قبل المستخدم.")
    except Exception as e:
        print(f"\n\nحدث خطأ: {e}")
