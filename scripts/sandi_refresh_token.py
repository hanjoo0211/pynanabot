import requests

def login_and_get_tokens(username, password):
    url = "https://lifeapp-api.sandimall.com/api/oauth2/token"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json, text/plain, */*",
        "origin": "https://lifeapp.sandimall.com",
        "referer": "https://lifeapp.sandimall.com/",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
    }
    payload = {
        "username": username,
        "password": password,
        "clientId": "MOBILE"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("accessToken")
        refresh_token = data.get("refreshToken")
        print("🔐 로그인 성공. 토큰 발급 완료.")
        return access_token, refresh_token
    else:
        print("❌ 로그인 실패:", response.status_code)
        print(response.text)
        raise Exception("로그인에 실패했습니다.")


if __name__ == "__main__":
    username = ""
    password = ""

    try:
        access_token, refresh_token = login_and_get_tokens(username, password)
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)
    except Exception as e:
        print(e)
