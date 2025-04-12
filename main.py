import re, requests, time, sys, os, random, telebot
from os import path
from concurrent.futures import ThreadPoolExecutor, as_completed
from user_agent import generate_user_agent

# Telegram Bot Token - Replace with your actual token
TOKEN = "7775677901:AAH-t5W-9ruMOCBtfoCqx3IVthhRnz_G6OA"
bot = telebot.TeleBot(TOKEN)

# Expected success response from a report
expected_response = '"status_code":0,"status_msg":"Thanks for your feedback"'

# Global variables to store user data
user_data = {}

# --------------------------
# PROXY HELPER FUNCTIONS
# --------------------------
def format_proxy(proxy):
    """
    Ensure proxy string starts with a proper protocol.
    Supports socks5, socks4, and http.
    If missing, assumes http://.
    """
    proxy = proxy.strip()
    if not (proxy.startswith("http://") or proxy.startswith("https://") or 
            proxy.startswith("socks5://") or proxy.startswith("socks4://")):
        return "http://" + proxy
    return proxy

TEST_URL = "https://httpbin.org/ip"
PROXY_TIMEOUT = 1
MAX_THREADS = 400

def check_proxy(proxy_url):
    """Test a single proxy by trying to fetch TEST_URL."""
    formatted = format_proxy(proxy_url)
    proxies = {"http": formatted, "https": formatted}
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=PROXY_TIMEOUT)
        if response.status_code == 200:
            return proxy_url, True
    except Exception:
        pass
    return proxy_url, False

def check_proxies_concurrently(proxy_list):
    """Concurrently test all proxies and return the list of working ones."""
    working = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(check_proxy, p): p for p in proxy_list}
        for future in as_completed(future_to_proxy):
            proxy, status = future.result()
            if status:
                working.append(format_proxy(proxy))
    return working

# --------------------------
# CHECK SESSION VALIDITY
# --------------------------
def validate_sessions(sessions, chat_id):
    check_url = ('https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/'
                '?scene=normal&multi_login=1&account_sdk_source=app&passport-sdk-version=19&'
                'os_api=25&device_type=A5010&ssmix=a&manifest_version_code=2018093009&dpi=191&'
                'carrier_region=JO&uoo=1&region=US&app_name=musical_ly&version_name=7.1.2&'
                'timezone_offset=28800&ts=1628767214&ab_version=7.1.2&residence=SA&'
                'cpu_support64=false&current_region=JO&ac2=wifi&ac=wifi&app_type=normal&'
                'host_abi=armeabi-v7a&channel=googleplay&update_version_code=2018093009&'
                '_rticket=1628767221573&device_platform=android&iid=7396386396296286392&'
                'build_number=7.1.2&locale=en&op_region=SA&version_code=200705&'
                'timezone_name=Asia%2FShanghai&cdid=f61ca549-c9ee-450b-90da-8854423b74e7&'
                'openudid=3e5afbd3f6dde322&sys_region=US&device_id=7296396296396396393&'
                'app_language=en&resolution=576*1024&device_brand=OnePlus&language=en&'
                'os_version=7.1.2&aid=1233&mcc_mnc=2947')
    base_headers = {
        'Host': 'api16-normal-c-alisg.tiktokv.com',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': generate_user_agent()
    }

    valid_session_count = 0
    expired_session_count = 0
    checked_valid_sessions = []

    bot.send_message(chat_id, f"Validating {len(sessions)} sessions...")
    
    for s in sessions:
        h = base_headers.copy()
        h['Cookie'] = 'sessionid=' + s
        try:
            resp = requests.get(check_url, headers=h, timeout=1)
        except Exception as e:
            bot.send_message(chat_id, f"Error checking session {s[:8]}...: {e}")
            continue
        
        if '"session expired, please sign in again"' in resp.text:
            expired_session_count += 1
            bot.send_message(chat_id, f"â Session expired: {s[:8]}...")
        elif 'user_id' in resp.text:
            valid_session_count += 1
            checked_valid_sessions.append(s)
            bot.send_message(chat_id, f"â Session valid: {s[:8]}...")
    
    bot.send_message(chat_id, f"Valid sessions: {valid_session_count} | Expired sessions: {expired_session_count}")
    
    if not checked_valid_sessions:
        bot.send_message(chat_id, "No valid sessions found!")
        return []
    
    return checked_valid_sessions

# --------------------------
# GET TARGET USERNAME & USER ID
# --------------------------
def get_target_id(username, chat_id):
    head = {
        'Host': 'www.tiktok.com',
        'User-Agent': generate_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'close',
    }
    
    bot.send_message(chat_id, f"Fetching user ID for @{username}...")
    
    try:
        req = requests.get(f'https://www.tiktok.com/@{username}?lang=en', headers=head)
        target_ID = re.findall(r'"user":{"id":"(.*?)"', req.text)[0]
        bot.send_message(chat_id, f"â User ID found: {target_ID}")
        return target_ID
    except:
        bot.send_message(chat_id, "â User not found or banned!")
        return None

# --------------------------
# REPORT FUNCTIONS
# --------------------------
def get_report_params(r_type, target_ID, session):
    base_url = 'https://www.tiktok.com/aweme/v1/aweme/feedback/'
    common = ("?aid=1233&app_name=tiktok_web&device_platform=web_mobile"
              "&region=SA&priority_region=SA&os=ios&"
              "cookie_enabled=true&screen_width=375&screen_height=667&"
              "browser_language=en-US&browser_platform=iPhone&"
              "browser_name=Mozilla&browser_version=5.0+(iPhone;+CPU+iPhone+OS+15_1+like+Mac+OS+X)+"
              "AppleWebKit/605.1.15+(KHTML,+like+Gecko)+InspectBrowser&"
              "browser_online=true&app_language=ar&timezone_name=Asia%2FRiyadh&"
              "is_page_visible=true&focus_state=true&is_fullscreen=false")
    params = {
        1: {"reason": "399", "reporter_id": "7024230440182809606", "device_id": "7008218736944907778"},
        2: {"reason": "310", "reporter_id": "27568146", "device_id": "7008218736944907778"},
        3: {"reason": "317", "reporter_id": "27568146", "device_id": "7008218736944907778"},
        4: {"reason": "3142", "reporter_id": "6955107540677968897", "device_id": "7034110346035136001"},
        5: {"reason": "306", "reporter_id": "6955107540677968897", "device_id": "7034110346035136001"},
        6: {"reason": "308", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        7: {"reason": "3011", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        8: {"reason": "3052", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        9: {"reason": "3072", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        10: {"reason": "303", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        14: {"reason": "9004", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"},
        15: {"reason": "90064", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"},
        16: {"reason": "9010", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"}
    }
    p = params.get(r_type)
    url = (f"{base_url}{common}&reason={p['reason']}&report_type=user"
           f"&object_id={target_ID}&owner_id={target_ID}&target={target_ID}"
           f"&reporter_id={p['reporter_id']}&current_region=SA")
    rep_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=' + session,
        'Host': 'www.tiktok.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': generate_user_agent()
    }
    data = {
        "object_id": target_ID,
        "owner_id": target_ID,
        "report_type": "user",
        "target": target_ID
    }
    return url, rep_headers, data

def get_random_report_type():
    # Include options 1-10, 14, 15 and 16 in random mode
    return random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16])

def send_report(session, report_url, headers, data, proxies=None):
    try:
        rep = requests.post(report_url, headers=headers, data=data, proxies=proxies, timeout=5)
        # When the expected response is found, consider it a failure
        if expected_response in rep.text:
            return False, session  # Failed report
        else:
            return True, session   # Successful report
    except Exception:
        return False, session      # Failed in case of exception

# --------------------------
# START REPORTING
# --------------------------
def start_reporting(chat_id):
    if chat_id not in user_data or not user_data[chat_id].get('sessions') or not user_data[chat_id].get('target_ID'):
        bot.send_message(chat_id, "Error: Missing session data or target ID. Please restart the process.")
        return
    
    sessions = user_data[chat_id]['sessions']
    target_ID = user_data[chat_id]['target_ID']
    username = user_data[chat_id]['username']
    report_type = user_data[chat_id].get('report_type')
    reports_per_session = user_data[chat_id].get('reports_per_session', 1)
    sleep_time = user_data[chat_id].get('sleep_time', 5)
    random_mode = user_data[chat_id].get('random_mode', False)
    proxy_mode = user_data[chat_id].get('proxy_mode', False)
    working_proxies = user_data[chat_id].get('working_proxies', [])
    
    # Initialize stop flag
    user_data[chat_id]['stop_requested'] = False
    
    bot.send_message(chat_id, f"""
TikTok Report Attack Started

Target: @{username} ID: {target_ID[:8]}...
Sessions: {len(sessions)} Reports/Session: {reports_per_session}
Report Type: {report_type if not random_mode else "Random"}
Mode: Continuous (will run until /stop command)
    """)

    successful_reports = 0
    failed_reports = 0
    total_reports = 0
    
    # Start status message
    status_message = bot.send_message(chat_id, "Starting attack...")
    message_id = status_message.message_id
    
    try:
        # Continue until stopped
        while not user_data[chat_id].get('stop_requested', False):
            for session in sessions:
                # Check if stop was requested
                if user_data[chat_id].get('stop_requested', False):
                    break
                    
                for _ in range(reports_per_session):
                    # Check if stop was requested
                    if user_data[chat_id].get('stop_requested', False):
                        break
                        
                    current_r_type = get_random_report_type() if random_mode else report_type
                    url_report, headers_rep, data_rep = get_report_params(current_r_type, target_ID, session)
                    
                    if proxy_mode and working_proxies:
                        proxy_addr = random.choice(working_proxies)
                        proxies = {"http": proxy_addr, "https": proxy_addr}
                    else:
                        proxies = None
                        
                    # Send the report
                    success, curr_session = send_report(session, url_report, headers_rep, data_rep, proxies=proxies)
                    
                    # Update counters
                    if success:
                        successful_reports += 1
                    else:
                        failed_reports += 1
                    total_reports += 1
                    
                    # Update status message
                    bot.edit_message_text(f"""
TikTok Report Attack Running

Target: @{username} ID: {target_ID[:8]}...

Process Statistics
Successful reports: {successful_reports}
Failed reports: {failed_reports}
Session: {curr_session[:8]}...
Total: {total_reports}

Use /stop to end the attack
                    """, chat_id=chat_id, message_id=message_id)
                    
                    # Sleep between reports
                    time.sleep(sleep_time)
        
        bot.send_message(chat_id, f"Attack stopped. Success: {successful_reports} | Failed: {failed_reports} | Total: {total_reports}")
        
    except Exception as e:
        bot.send_message(chat_id, f"Error during attack: {str(e)}")
        bot.send_message(chat_id, f"Final Report: Success: {successful_reports} | Failed: {failed_reports} | Total: {total_reports}")


# --------------------------
# TELEGRAM BOT COMMANDS
# --------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
Welcome to TikTok Reporter Bot v1.0
By 

Use /report to start a new report
Use /help to see all commands
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
TikTok Reporter Bot v1.0 Commands:

/start - Start the bot
/help - Show this help message
/report - Start a new reporting process
/stop - Stop the current reporting process
""")

@bot.message_handler(commands=['report'])
def start_report_process(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    
    # Create report type menu with inline buttons
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        telebot.types.InlineKeyboardButton("Report Content", callback_data="report_1"),
        telebot.types.InlineKeyboardButton("Spam or Harassment", callback_data="report_2"),
        telebot.types.InlineKeyboardButton("Under 13", callback_data="report_3"),
        telebot.types.InlineKeyboardButton("Fake Information", callback_data="report_4"),
        telebot.types.InlineKeyboardButton("Hate Speech", callback_data="report_5"),
        telebot.types.InlineKeyboardButton("Pornographic", callback_data="report_6"),
        telebot.types.InlineKeyboardButton("Terrorism", callback_data="report_7"),
        telebot.types.InlineKeyboardButton("Self Harm", callback_data="report_8"),
        telebot.types.InlineKeyboardButton("Harassment", callback_data="report_9"),
        telebot.types.InlineKeyboardButton("Violence", callback_data="report_10"),
        telebot.types.InlineKeyboardButton("Random Reports", callback_data="report_11"),
        telebot.types.InlineKeyboardButton("Random with Proxies", callback_data="report_12"),
        telebot.types.InlineKeyboardButton("Frauds And Scams", callback_data="report_13"),
        telebot.types.InlineKeyboardButton("Dangerous Acts", callback_data="report_14"),
        telebot.types.InlineKeyboardButton("Report Spam", callback_data="report_15")
    ]
    for button in buttons:
        markup.add(button)
    
    bot.send_message(chat_id, "Choose report type:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('report_'))
def handle_report_type(call):
    chat_id = call.message.chat.id
    option = int(call.data.split('_')[1])
    
    # Map option numbers to the correct report types
    option_mapping = {
        11: None,  # Random without proxy
        12: None,  # Random with proxy
        13: 14,    # Frauds and Scams
        14: 15,    # Dangerous and Challenges Acts
        15: 16     # Report Spam
    }
    
    random_mode = option in [11, 12]
    proxy_mode = option == 12
    
    report_type = option_mapping.get(option, option) if not random_mode else None
    
    user_data[chat_id]['report_type'] = report_type
    user_data[chat_id]['random_mode'] = random_mode
    user_data[chat_id]['proxy_mode'] = proxy_mode
    
    bot.edit_message_text(
        f"Report type selected: {option}",
        chat_id=chat_id,
        message_id=call.message.message_id
    )
    
    if proxy_mode:
        bot.send_message(chat_id, "Please send your proxy file as an attachment.")
    else:
        # Ask for session method
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("Load from file", callback_data="session_file"),
            telebot.types.InlineKeyboardButton("Enter manually", callback_data="session_manual")
        )
        bot.send_message(chat_id, "How would you like to load session IDs?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('session_'))
def handle_session_method(call):
    chat_id = call.message.chat.id
    method = call.data.split('_')[1]
    
    bot.edit_message_text(
        f"Session method selected: {method}",
        chat_id=chat_id,
        message_id=call.message.message_id
    )
    
    if method == 'file':
        bot.send_message(chat_id, "Please send your sessions.txt file as an attachment.")
    else:
        msg = bot.send_message(chat_id, "How many session IDs to enter?")
        bot.register_next_step_handler(msg, process_num_sessions)

def process_num_sessions(message):
    chat_id = message.chat.id
    try:
        num = int(message.text)
        user_data[chat_id]['num_sessions'] = num
        user_data[chat_id]['sessions'] = []
        user_data[chat_id]['current_session_index'] = 0
        
        msg = bot.send_message(chat_id, f"Enter session ID #1:")
        bot.register_next_step_handler(msg, process_session_id)
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number. Try /report again.")

def process_session_id(message):
    chat_id = message.chat.id
    session_id = message.text.strip()
    
    user_data[chat_id]['sessions'].append(session_id)
    current_index = user_data[chat_id]['current_session_index'] + 1
    user_data[chat_id]['current_session_index'] = current_index
    
    if current_index < user_data[chat_id]['num_sessions']:
        msg = bot.send_message(chat_id, f"Enter session ID #{current_index + 1}:")
        bot.register_next_step_handler(msg, process_session_id)
    else:
        bot.send_message(chat_id, f"All {current_index} sessions entered. Validating sessions...")
        
        # Validate sessions
        validated_sessions = validate_sessions(user_data[chat_id]['sessions'], chat_id)
        if validated_sessions:
            user_data[chat_id]['sessions'] = validated_sessions
            msg = bot.send_message(chat_id, "Enter target username:")
            bot.register_next_step_handler(msg, process_target_username)
        else:
            bot.send_message(chat_id, "No valid sessions found. Please try again with /report")

def process_target_username(message):
    chat_id = message.chat.id
    username = message.text.strip()
    user_data[chat_id]['username'] = username
    
    # Get target ID
    target_ID = get_target_id(username, chat_id)
    if target_ID:
        user_data[chat_id]['target_ID'] = target_ID
        
        # Ask for reports per session
        if len(user_data[chat_id]['sessions']) > 1:
            msg = bot.send_message(chat_id, "How many reports per session?")
            bot.register_next_step_handler(msg, process_reports_per_session)
        else:
            user_data[chat_id]['reports_per_session'] = 1
            msg = bot.send_message(chat_id, "Enter sleep time between reports (seconds):")
            bot.register_next_step_handler(msg, process_sleep_time)
    else:
        bot.send_message(chat_id, "Failed to get target ID. Please try again with /report")

def process_reports_per_session(message):
    chat_id = message.chat.id
    try:
        reports = int(message.text)
        if reports < 1:
            reports = 1
        user_data[chat_id]['reports_per_session'] = reports
        
        msg = bot.send_message(chat_id, "Enter sleep time between reports (seconds):")
        bot.register_next_step_handler(msg, process_sleep_time)
    except ValueError:
        bot.send_message(chat_id, "Invalid input. Using 1 report per session.")
        user_data[chat_id]['reports_per_session'] = 1
        
        msg = bot.send_message(chat_id, "Enter sleep time between reports (seconds):")
        bot.register_next_step_handler(msg, process_sleep_time)

def process_sleep_time(message):
    chat_id = message.chat.id
    try:
        sleep_time = int(message.text)
        if sleep_time < 0:
            sleep_time = 0
        user_data[chat_id]['sleep_time'] = sleep_time
    except ValueError:
        bot.send_message(chat_id, "Invalid input. Using 5 seconds as default.")
        user_data[chat_id]['sleep_time'] = 5
    
    # Start confirmation
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("Start Attack", callback_data="start_attack"),
        telebot.types.InlineKeyboardButton("Cancel", callback_data="cancel_attack")
    )
    
    # Prepare confirmation message
    sessions = user_data[chat_id]['sessions']
    target_ID = user_data[chat_id]['target_ID']
    username = user_data[chat_id]['username']
    report_type = user_data[chat_id].get('report_type')
    reports_per_session = user_data[chat_id].get('reports_per_session', 1)
    sleep_time = user_data[chat_id].get('sleep_time', 5)
    random_mode = user_data[chat_id].get('random_mode', False)
    
    confirmation = f"""
Ready to start attack:

Target: @{username} ID: {target_ID[:8]}...
Sessions: {len(sessions)} Reports/Session: {reports_per_session}
Sleep Time: {sleep_time} seconds
Report Type: {report_type if not random_mode else "Random"}
Mode: Continuous (will run until stopped)

Proceed?
    """
    
    bot.send_message(chat_id, confirmation, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["start_attack", "cancel_attack"])
def handle_attack_confirmation(call):
    chat_id = call.message.chat.id
    
    if call.data == "start_attack":
        bot.edit_message_text(
            "Attack initiated...",
            chat_id=chat_id,
            message_id=call.message.message_id
        )
        start_reporting(chat_id)
    else:
        bot.edit_message_text(
            "Attack cancelled.",
            chat_id=chat_id,
            message_id=call.message.message_id
        )

@bot.message_handler(commands=['stop'])
def stop_reporting(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        user_data[chat_id]['stop_requested'] = True
        bot.reply_to(message, "Stopping the attack... This may take a moment to complete.")
    else:
        bot.reply_to(message, "No attack is currently running.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    
    if chat_id not in user_data:
        bot.reply_to(message, "Please start with /report first")
        return
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Save file temporarily
    temp_filename = f"temp_{message.document.file_name}"
    with open(temp_filename, 'wb') as f:
        f.write(downloaded_file)
    
    if user_data[chat_id].get('proxy_mode'):
        # Process proxy file
        proxy_list = []
        with open(temp_filename, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.strip()
                if p:
                    proxy_list.append(p)
        
        if not proxy_list:
            bot.send_message(chat_id, "No proxies loaded from file!")
            os.remove(temp_filename)
            return
        
        bot.send_message(chat_id, f"Checking {len(proxy_list)} proxies. Please wait...")
        working_proxies = check_proxies_concurrently(proxy_list)
        
        if not working_proxies:
            bot.send_message(chat_id, "No working proxies found!")
            os.remove(temp_filename)
            return
        else:
            bot.send_message(chat_id, f"{len(working_proxies)} working proxies found.")
            user_data[chat_id]['working_proxies'] = working_proxies
            
            # Now ask for sessions
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                telebot.types.InlineKeyboardButton("Load from file", callback_data="session_file"),
                telebot.types.InlineKeyboardButton("Enter manually", callback_data="session_manual")
            )
            bot.send_message(chat_id, "How would you like to load session IDs?", reply_markup=markup)
    else:
        # Process sessions file
        sessions = []
        with open(temp_filename, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if s:
                    sessions.append(s)
        
        if not sessions:
            bot.send_message(chat_id, "No sessions loaded from file!")
            os.remove(temp_filename)
            return
        
        bot.send_message(chat_id, f"Loaded {len(sessions)} sessions from file.")
        
        # Validate sessions
        validated_sessions = validate_sessions(sessions, chat_id)
        if validated_sessions:
            user_data[chat_id]['sessions'] = validated_sessions
            msg = bot.send_message(chat_id, "Enter target username:")
            bot.register_next_step_handler(msg, process_target_username)
        else:
            bot.send_message(chat_id, "No valid sessions found. Please try again with /report")
    
    # Clean up temporary file
    os.remove(temp_filename)

# Start the bot
if __name__ == "__main__":
    # Initialize user data
    user_data = {}
    
    try:
        print("TikTok Reporter Bot is starting...")
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optional: add a restart mechanism
        time.sleep(10)
        # Restart the bot after error
    except KeyboardInterrupt:
        print("Bot stopped by user")
        sys.exit(0)