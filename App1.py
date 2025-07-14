import streamlit as st
from openai import OpenAI
import os

# ✅ 환경 변수에서 API 키 불러오기
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("openai_api_key", None)
if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경변수나 secrets에 넣어주세요.")
    st.stop()

# ✅ GPT 클라이언트 생성
client = OpenAI(api_key=api_key)

# ✅ GPT 호출 함수
def explain_meme(meme_name):
    prompt = f"""
너는 인터넷 밈을 잘 아는 AI야. 사용자가 '{meme_name}'이라는 밈 이름을 입력하면,
1. 뜻
2. 유래
3. 사용 예시

이 세 가지 항목으로 짧고 간결하게 설명해줘. 한국어로.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

# ✅ Streamlit UI
st.set_page_config(page_title="AI 밈 설명기", page_icon="🧠")
st.title("🧠 AI 밈 설명기")
st.write("밈 이름을 입력하면 AI가 뜻과 유래를 설명해줍니다!")

meme_input = st.text_input("밈 이름을 입력하세요", placeholder="예: 킹받네, Distracted Boyfriend")

if st.button("설명 보기") and meme_input:
    with st.spinner("AI가 설명을 생성 중입니다..."):
        try:
            explanation = explain_meme(meme_input)
            st.success("설명 완료!")
            st.text_area("밈 설명", explanation, height=250)

            # 📝 저장 (선택적 기능)
           # with open("meme_explanation.txt", "w", encoding="utf-8") as f:
             #   f.write(explanation)

        except Exception as e:
            st.error(f"에러 발생: {e}")
