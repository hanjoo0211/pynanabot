import os
import environ
import requests
import time
from pathlib import Path
from datetime import datetime, time as dt_time, timedelta
from sandi_refresh_token import login_and_get_tokens

# 환경 변수 설정
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SANDI_USERNAME = env("SANDI_USERNAME")
SANDI_PASSWORD = env("SANDI_PASSWORD")
# LUNCH_WEBHOOK_URL = env("TEAMS_TEST_URL") # 테스트용
LUNCH_WEBHOOK_URL = env("LUNCH_TEAMS_URL")

ACCESS_TOKEN, _REFRESH_TOKEN = login_and_get_tokens(SANDI_USERNAME, SANDI_PASSWORD)


def send_teams_message(name, title, image_urls):
    body = [{
        "type": "TextBlock",
        "text": f"[{name}] {title}",
        "wrap": True,
    }]

    for image_url in image_urls:
        body.append({
            "type": "Image",
            "url": image_url,
            "height": "auto",
            "msTeams": {"allowExpand": True},
        })

    message = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": body,
                }
            }
        ]
    }

    response = requests.post(LUNCH_WEBHOOK_URL, json=message)
    if response.status_code in [200, 201, 202]:
        print(f"✅ MS Teams로 알림 전송 완료: {title}")
    else:
        print(f"❌ 알림 전송 실패: {response.status_code} - {response.text}")



def fetch_menu(store_id, building_id, name):
    global ACCESS_TOKEN

    def _request():
        url = "https://lifeapp-api.sandimall.com/api/v2/app/pinelife/post/list"
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "origin": "https://lifeapp.sandimall.com",
            "referer": "https://lifeapp.sandimall.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
        }
        params = {
            "category": "building-menu",
            "sort": "createdAt.desc",
            "page": 1,
            "pageSize": 10,
            "storeId": store_id,
            "buildingId": building_id,
        }
        return requests.get(url, headers=headers, params=params)

    response = _request()

    if response.status_code == 401:
        print("🔁 토큰 만료로 재로그인 중...")
        ACCESS_TOKEN, _ = login_and_get_tokens(SANDI_USERNAME, SANDI_PASSWORD)
        response = _request()

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        today_str = datetime.now().strftime("%Y/%m/%d")
        # today_for_title_CJ = datetime.now().strftime("%-m월 %-d일")
        # today_for_title_OURHOME = datetime.now().strftime("%m월 %d일")
        today_for_title = [
            datetime.now().strftime("%-m월 %-d일"),
            datetime.now().strftime("%-m월%-d일"),
            datetime.now().strftime("%m월 %d일"),
            datetime.now().strftime("%m월%d일")
        ]

        print(f"\n[{name}] 게시글 확인 중 ({today_str})...")
        for item in items:
            title = item.get("title", "")
            
            # if today_for_title_CJ in title or today_for_title_OURHOME in title:
            if any(today in title for today in today_for_title):
                file_info = item.get("fileInfo", {})
                items = file_info.get("items", [])
                # 이미지 URL 추출
                image_urls = [
                    item.get("url") for item in items if item.get("scale") == "full"
                ]

                if not image_urls:
                    print(f"❌ [{name}] 이미지 URL 없음: {title}")
                    continue

                print(f"📬 [{name}] 오늘 날짜 포함 게시글 발견: {title}")
                send_teams_message(name, title, image_urls)
                return True
        
        else:
            print(f"📭 [{name}] 오늘 날짜가 포함된 게시글이 없습니다.")

            return False
    else:
        print(f"[{name}] 요청 실패: {response.status_code}")
        print(response.text)
        return False


def run_checker(store_id, building_id, name, interval=30):
    start_hour = 10
    end_hour = 13  # 13시 미만까지 체크

    while True:
        now = datetime.now()
        current_hour = now.hour
        current_time_str = now.strftime('%Y-%m-%d %H:%M:%S')

        # 점심시간 확인
        if start_hour <= current_hour < end_hour:
            print(f"⏰ [{name}] 점심 게시글 체크 중... ({current_time_str})")
            is_sent = fetch_menu(store_id, building_id, name)

            if is_sent:
                print(f"✅ [{name}] 게시글 발견 및 전송 완료. 12시간 후 재시작.")
                time.sleep(60 * 60 * 12)
            else:
                print(f"🔄 [{name}] 게시글 없음. {interval}초 후 재시도...")
                time.sleep(interval)
        else:
            print(f"😴 [{name}] 현재 시간 {current_hour}시. 점심 시간 아님. 10분 대기 후 재확인...")
            time.sleep(600)  # 10분 대기


if __name__ == "__main__":
    run_checker(
        store_id="ST_0000290",
        building_id="TG_0003255",
        name="CJ",
    )
