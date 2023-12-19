import requests
from requests_oauthlib import OAuth1
import time
import os
from dotenv import load_dotenv

# Twitter API 키 및 액세스 토큰
load_dotenv()
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

channel_id = '5f800579267362c952f76f3c6fe695b2'

# API 엔드포인트 URL
tweet_url = 'https://api.twitter.com/2/tweets'
naver_api_url = f'https://api.chzzk.naver.com/service/v1/channels/{channel_id}/live-detail'


# OAuth1 인증 설정
auth = OAuth1(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret
)

# 트윗 게시 함수
def post_tweet(tweet_text):
    data = {'text': tweet_text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(tweet_url, auth=auth, json=data, headers=headers)

    if response.status_code == 201:
        print(f'Tweet posted: {tweet_text}')
    else:
        print(f'Error Status code: {response.status_code}\nResponse: {response.text}')

# Naver API에서 상태 확인 함수
def check_naver_status():
    response = requests.get(naver_api_url)
    if response.status_code == 200:
        return response.json().get('content', {}).get('status')
    else:
        print(f'Error Status code: {response.status_code}\nResponse: {response.text}')
        return None

# 주기적으로 Naver API 호출하여 상태 확인 및 트윗 게시
def check_and_post_periodically():
    while True:
        naver_status = check_naver_status()
        print(naver_status)
        
        if naver_status == 'OPEN':
            response = requests.get(naver_api_url)
            title = response.json().get('content', {}).get('liveTitle')
            channel = response.json().get('content', {}).get('channel').get('channelName')

            tweet_text = f'[치지직 라이브] {channel}님의 방송이 시작되었습니다 !\n▶ 방송 제목: {title}\nhttps://chzzk.naver.com/live/{channel_id}'
            post_tweet(tweet_text)
            print("Open Detect! Tweet Posted.")
            
            # 트윗 게시 후, CLOSE 상태가 될 때까지 대기
            while check_naver_status() == 'OPEN':
                print("Checking for Close status")
                time.sleep(30)  # 30초마다 확인 (조절 가능)
        else:
            print("Not Open Status. Checking again in 10 seconds.")
            time.sleep(10)  # CLOSE 상태인 경우 10초마다 확인 (조절 가능)

if __name__ == "__main__":
    check_and_post_periodically()
