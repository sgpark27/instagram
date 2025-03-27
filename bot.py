from instagrapi import Client
import openai
import time, random
from datetime import datetime

# 환경변수 사용 시
import os
openai.api_key = os.environ["OPENAI_API_KEY"]
username = os.environ["IG_USERNAME"]
password = os.environ["IG_PASSWORD"]

# 인스타 로그인
cl = Client()
cl.load_settings("session.json")
cl.login(username, password)


# 댓글 생성 함수
def generate_comment(text):
    prompt = f"""
    다음 인스타그램 포스트 내용에 대해 20대 여성이 쓴 것처럼 귀엽고 자연스러운 칭찬 댓글 한 줄만 써줘.
    포스트 내용: "{text}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# 봇 실행 함수
def run_bot():
    posts = cl.hashtag_medias_recent("패션", amount=10)
    for post in posts:
        cl.media_like(post.id)
        caption = post.caption_text
        comment = generate_comment(caption)
        cl.media_comment(post.id, comment)
        print(f"댓글 완료: {comment}")

# 랜덤 딜레이 후 실행 (14~15시 사이)
def run_bot_later():
    delay_seconds = random.randint(0, 60 * 60)  # 최대 1시간
    delay_minutes = delay_seconds // 60
    print(f"⏱️ {delay_minutes}분 후에 run_bot() 실행 예정")
    time.sleep(delay_seconds)
    run_bot()

# 실행 시작
run_bot_later()
