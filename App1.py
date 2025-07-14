import streamlit as st
from openai import OpenAI
import os

# 🔑 OpenAI API 키 설정 (환경변수나 secrets에서 읽기)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("openai_api_key", None)
if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경변수나 secrets에 넣어주세요.")
    st.stop()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# 💬 GPT에게 질문 보내는 함수 (최신 문법)
def explain_meme(meme_name):
    prompt = f"""
너는 인터넷 밈을 잘 아는 AI야. 사용자가 '{meme_name}'이라는 밈 이름을 입력하면,
1. 뜻
2. 유래
3. 사용 예시

이 세 가지 항목으로 짧고 간결하게 설명해줘. 한국어로.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 "gpt-4"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

# 🎨 Streamlit UI
st.set_page_config(page_title="AI 밈 설명기", page_icon="🧠")
st.title("🧠 AI 밈 설명기")
st.write("밈 이름을 입력하면 AI가 뜻과 유래를 설명해줍니다!")

# 사용자 입력
meme_input = st.text_input("밈 이름을 입력하세요", placeholder="예: Distracted Boyfriend")

# 버튼 클릭 시 결과 표시
if st.button("설명 보기") and meme_input:
    with st.spinner("AI가 설명을 생성 중입니다..."):
        try:
            explanation = explain_meme(meme_input)
            st.success("설명 완료!")
            st.text_area("밈 설명", explanation, height=250)
        except Exception as e:
            st.error(f"에러 발생: {e}")
