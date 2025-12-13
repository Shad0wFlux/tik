from curl_cffi import requests, CurlMime

url = "https://www.instagram.com/api/v1/web/accounts/web_change_profile_picture/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "x-csrftoken": "الحقيقي_من_كوكيز",
    "x-ig-app-id": "936619743392459",
    "x-instagram-ajax": "ROLL_OUT_HASH_الحقيقي",
}

cookies = {
    "sessionid": "حقيقي_من_كوكيز",
    "ig_did": "حقيقي_من_كوكيز",
}

mp = CurlMime()
mp.addpart(
    name="profile_pic",  # لازم يكون هكذا
    filename="im.jpg",
    local_path="C:/Users/PC/Desktop/fidra/profiles/im.jpg",
    content_type="image/jpeg"
)

resp = requests.post(url, headers=headers, cookies=cookies, multipart=mp)

print(resp.status_code)
print(resp.text)
