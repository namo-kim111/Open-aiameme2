import streamlit as st
import openai
import os

# 🔑 OpenAI API 키 설정 (직접 입력 or 환경변수 사용)
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

# 💬 GPT에게 질문 보내는 함수
def explain_meme(meme_name):
    prompt = f"""
너는 인터넷 밈을 잘 아는 AI야. 사용자가 '{meme_name}'이라는 밈 이름을 입력하면,
1. 뜻
2. 유래
3. 사용 예시

이 세 가지 항목으로 짧고 간결하게 설명해줘. 한국어로.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 또는 "gpt-4"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
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
