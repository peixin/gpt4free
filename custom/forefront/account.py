from gpt4free import forefront
import requests
import json
import os
import time

cache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token_info.json")


def fetch_token(cookie: str):
    print("fetch token")
    headers = {
        "authority": "clerk.forefront.ai",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,en-US;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6",
        "cache-control": "max-age=0",
        "cookie": cookie,
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    response = requests.get(
        "https://clerk.forefront.ai/v1/client?_clerk_js_version=4.39.0",
        headers=headers,
    )
    if response.status_code != 200:
        return None

    forefront_info = response.json()

    if forefront_info["response"] is None:
        return None

    forefront_info["fetch_time"] = int(time.time() * 1000)
    with open(
        cache_file,
        "w+",
    ) as f:
        f.write(json.dumps(forefront_info, indent=2))

    return forefront_info


def get_account():
    cookie = os.environ.get("FOREFRONT_COOKIE")

    if cookie is None:
        print("no cookie")
        return None

    forefront_info = None

    with open(
        cache_file,
        "r+",
    ) as f:
        forefront_info_str = f.read().strip()
        if len(forefront_info_str) == 0:
            return None

        try:
            forefront_info = json.loads(forefront_info_str)
            fetch_time = forefront_info.get("fetch_time", 0)
            if int(time.time() * 1000) - fetch_time > 40 * 1000:
                forefront_info = None
        except:
            pass

    if forefront_info is None:
        forefront_info = fetch_token(cookie)

    if forefront_info is None or forefront_info["response"] is None:
        return None

    session = forefront_info["response"]["sessions"][0]
    session_id = session["id"]
    user_id = session["user"]["id"]
    token = session["last_active_token"]["jwt"]

    account_data = forefront.AccountData(
        user_id=user_id, token=token, session_id=session_id
    )

    return account_data
