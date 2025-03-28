from instagrapi import Client

import openai
import os
import time
import random

from openai import OpenAI

# 환경 변수
openai.api_key = os.environ["OPENAI_API_KEY"]
username = os.environ["IG_USERNAME"]
password = os.environ["IG_PASSWORD"]

# 인스타 로그인 (세션 재사용)
cl = Client()
cl.load_settings("session.json")
cl.login(username, password)

# 댓글 생성 함수
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 금지 키워드 리스트
BANNED_KEYWORDS = ["팔로워", "선팔", "맞팔", "DM", "디엠", "링크", "할인", "무료"]

def generate_comment(text):
    prompt = f"""
    다음 인스타그램 포스트 내용에 대해 20대 여성이 쓴 것처럼 귀엽고 자연스러운 칭찬 댓글 한 줄만 써줘.
    너무 기계적이지 않고, 감탄사나 이모지도 살짝 포함해줘.
    절대 '팔로워', '맞팔', '선팔', 'DM', '링크', '무료', '할인' 같은 마케팅/홍보성 단어는 쓰지 말아줘.
    포스트 내용: "{text}"
    """

    for _ in range(3):  # 최대 3번까지 시도
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        comment = response.choices[0].message.content.strip()

        if any(bad in comment for bad in BANNED_KEYWORDS):
            print(f"⚠️ 필터링됨: '{comment}' → 재생성 시도")
            continue  # 금지 단어 포함 → 다시 생성

        return comment

    # 3번 다 실패하면 안전한 기본 문장 사용
    return "분위기 너무 예뻐요! 🥰"

# 좋아요 자동 실행 함수
def auto_like_posts():
    hashtags = ["패션", "코디", "선팔", "맞팔", "스타일"]
    liked = 0
    target_like_count = 30

    for tag in random.sample(hashtags, k=len(hashtags)):
        posts = cl.hashtag_medias_recent(tag, amount=15)
        for post in posts:
            try:
                cl.media_like(post.id)
                liked += 1
                print(f"❤️ 좋아요 {liked}개째 완료 - @{post.user.username}")
                if liked >= target_like_count:
                    return
                time.sleep(random.uniform(10, 30))  # 사람처럼 간격
            except Exception as e:
                print(f"❌ 좋아요 실패: {e}")
                continue

# 댓글 자동 실행 함수
def auto_comment():
    hashtags = ["패션", "코디", "ootd", "스타일"]
    total_comments = 0
    target_comment_count = 10

    for tag in random.sample(hashtags, len(hashtags)):
        posts = cl.hashtag_medias_recent(tag, amount=10)
        for post in posts:
            try:
                caption = post.caption_text
                comment = generate_comment(caption)
                cl.media_like(post.id)
                cl.media_comment(post.id, comment)
                total_comments += 1
                print(f"💬 {total_comments}번째 댓글 완료: {comment}")

                if total_comments >= target_comment_count:
                    return  # 댓글 10개 완료되면 종료

                time.sleep(random.uniform(20, 60))  # 자연스러운 딜레이
            except Exception as e:
                print(f"❌ 댓글 실패: {e}")
                continue

# 메인 실행 함수
def run_bot():
    print("🚀 봇 시작: 좋아요 + 댓글 자동화")
    # auto_like_posts()
    time.sleep(random.uniform(60, 180))  # 좋아요 후 댓글은 약간 쉬었다가
    auto_comment()
    print("✅ 봇 작업 완료!")


# 실행 시작
run_bot()
