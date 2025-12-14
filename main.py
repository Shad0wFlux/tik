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

# القائمة الثانية للبلاغات بعد VPN
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
    print("\n" + "=" * 75)
    print("Instagram Reporting System")
    print("=" * 75)
    print("\nChoose reporting mode:")
    print("1. Normal Reporting (from single account)")
    print("2. Multi-Account Reporting (from multiple accounts)")
    print("=" * 75)
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return int(choice)
        print("Invalid choice. Please enter 1 or 2.")

def get_sleep_time():
    print("\n" + "-" * 75)
    print("Sleep Time Configuration")
    print("-" * 75)
    print("Enter the delay (in seconds) between each report.")
    print("Recommended: 2-5 seconds to avoid detection")
    
    while True:
        try:
            sleep_time = int(input("\nEnter sleep time (seconds): ").strip())
            if sleep_time >= 0:
                return sleep_time
            print("Please enter a positive number or 0 for no delay.")
        except ValueError:
            print("Please enter a valid number.")

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
    
    print(f"\nPhase {phase_num} - Report {step_num}/{total_steps}: {report_name}")
    print("-" * 75)
    
    time.sleep(1)
    
    context = get_context(user_id, cookies)
    
    if not context:
        print("Failed: Could not get context")
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
            print("Status: Success")
            return True
        else:
            print(f"Status: Failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_reports_list(reports_list, user_id, cookies, phase_name, phase_num, sleep_time):
    print(f"\n" + "=" * 75)
    print(f"{phase_name}")
    print("=" * 75)
    
    successful = 0
    total = len(reports_list)
    
    for i, report_data in enumerate(reports_list, 1):
        if send_report(report_data, user_id, cookies, i, total, phase_num, sleep_time):
            successful += 1
        
        if i < total and sleep_time > 0:
            print(f"\nWaiting {sleep_time} seconds before next report...")
            time.sleep(sleep_time)
    
    print(f"\nPhase {phase_num} completed: {successful}/{total} reports")
    return successful

def normal_reporting():
    print("\n" + "=" * 75)
    print("Normal Reporting Mode")
    print("=" * 75)
    
    user_id = input("\nEnter target user ID: ").strip()
    session_id = input("Enter session ID: ").strip()
    sleep_time = get_sleep_time()
    
    print("\n" + "-" * 75)
    print("Please enable VPN now")
    print("Press ENTER when VPN is active")
    input()
    
    print("\n" + "-" * 75)
    print("Initializing system...")
    print("-" * 75)
    
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
    
    # Phase 1
    print("\n" + "=" * 75)
    print("Starting Phase 1: First 5 Reports")
    print("=" * 75)
    
    phase1_success = send_reports_list(first_reports, user_id, cookies, 
                                      "Phase 1: First 5 Reports", 1, sleep_time)
    
    # VPN Change
    print("\n" + "=" * 75)
    print("Change VPN Required")
    print("=" * 75)
    print("Please change your VPN server now")
    print("Press ENTER when VPN is changed")
    input()
    
    # Phase 2
    print("\n" + "=" * 75)
    print("Starting Phase 2: Next 6 Reports")
    print("=" * 75)
    
    phase2_success = send_reports_list(second_reports, user_id, cookies,
                                      "Phase 2: Next 6 Reports", 2, sleep_time)
    
    # Summary
    print("\n" + "=" * 75)
    print("Operation Complete")
    print("=" * 75)
    print(f"Phase 1 (Reports 1-5): {phase1_success}/{len(first_reports)}")
    print(f"Phase 2 (Reports 6-11): {phase2_success}/{len(second_reports)}")
    print(f"Total (All 11 Reports): {phase1_success + phase2_success}/{len(first_reports) + len(second_reports)}")
    print(f"Sleep time used: {sleep_time} seconds")
    print("=" * 75)

def validate_session(session_id):
    """Validate if a session ID is working"""
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
    print("\n" + "=" * 75)
    print("Multi-Account Reporting Mode")
    print("=" * 75)
    
    user_id = input("\nEnter target user ID: ").strip()
    
    print("\n" + "-" * 75)
    print("Enter session IDs (one per line)")
    print("Example:")
    print("23375113665%3AQ52ClMV9J0Q7cw%3A20%3AAYieo0QWoqPKwEe8RJY9EHci9epYVuLdxXSUo3Yc1Q")
    print("78030994619%3AE8HxHqha7KPRJG%3A15%3AAYjFLxPzV56QRsybR4sOnXIjIieD36SrLMhrkQs2Hg")
    print("-" * 75)
    print("Press Enter twice when finished")
    
    sessions = []
    while True:
        session = input().strip()
        if session == "":
            if sessions:
                break
            else:
                print("Please enter at least one session ID")
                continue
        sessions.append(session)
    
    sleep_time = get_sleep_time()
    
    # Validate sessions
    print("\n" + "-" * 75)
    print("Validating sessions...")
    print("-" * 75)
    
    valid_sessions = []
    for i, session in enumerate(sessions, 1):
        print(f"Checking session {i}/{len(sessions)}... ", end="")
        if validate_session(session):
            print("VALID")
            valid_sessions.append(session)
        else:
            print("INVALID")
    
    print(f"\nValid sessions: {len(valid_sessions)}/{len(sessions)}")
    
    if not valid_sessions:
        print("No valid sessions found. Exiting.")
        return
    
    print("\n" + "=" * 75)
    print(f"Starting reporting from {len(valid_sessions)} accounts")
    print("=" * 75)
    
    total_reports_sent = 0
    total_accounts_used = 0
    
    for account_num, session_id in enumerate(valid_sessions, 1):
        print(f"\n" + "=" * 75)
        print(f"Account {account_num}/{len(valid_sessions)}")
        print("=" * 75)
        
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
        
        print("\nPlease enable VPN now")
        print("Press ENTER when VPN is active")
        input()
        
        # Phase 1 for this account
        print("\n" + "=" * 75)
        print(f"Account {account_num}: Starting Phase 1")
        print("=" * 75)
        
        phase1_success = send_reports_list(first_reports, user_id, cookies,
                                          f"Account {account_num} - Phase 1", 1, sleep_time)
        
        # VPN Change for this account
        print("\n" + "=" * 75)
        print("Change VPN Required")
        print("=" * 75)
        print("Please change your VPN server now")
        print("Press ENTER when VPN is changed")
        input()
        
        # Phase 2 for this account
        print("\n" + "=" * 75)
        print(f"Account {account_num}: Starting Phase 2")
        print("=" * 75)
        
        phase2_success = send_reports_list(second_reports, user_id, cookies,
                                          f"Account {account_num} - Phase 2", 2, sleep_time)
        
        total_reports_sent += (phase1_success + phase2_success)
        total_accounts_used += 1
        
        print(f"\nAccount {account_num} completed: {phase1_success + phase2_success}/11 reports")
        
        # Delay between accounts
        if account_num < len(valid_sessions):
            print(f"\n" + "-" * 75)
            print(f"Preparing next account in 5 seconds...")
            print("-" * 75)
            time.sleep(5)
    
    # Final Summary
    print("\n" + "=" * 75)
    print("Multi-Account Operation Complete")
    print("=" * 75)
    print(f"Accounts used: {total_accounts_used}/{len(valid_sessions)}")
    print(f"Total reports sent: {total_reports_sent}")
    print(f"Maximum possible reports: {len(valid_sessions) * 11}")
    print(f"Sleep time used: {sleep_time} seconds")
    print("=" * 75)

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
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
