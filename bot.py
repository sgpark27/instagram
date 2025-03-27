from instagrapi import Client
import openai
import schedule, time, random
from datetime import datetime

# OpenAI API 설정
openai.api_key = "your_openai_api_key"

# 인스타 로그인
cl = Client()
cl.login("your_username", "your_password")

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
    posts = cl.hashtag_medias_recent("패션", amount=1)
    for post in posts:
        cl.media_like(post.id)
        caption = post.caption_text
        comment = generate_comment(caption)
        cl.media_comment(post.id, comment)
        print(f"댓글 완료: {comment}")

# 랜덤 시간 스케줄 설정
def set_random_schedule():
    hour = random.randint(18, 21)
    minute = random.randint(0, 59)
    time_str = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(time_str).do(run_bot)
    print(f"오늘 스케줄은 {time_str}")

# 매일 랜덤 시간 갱신
set_random_schedule()

while True:
    schedule.run_pending()
    time.sleep(60)
