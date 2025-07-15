import streamlit as st
import requests

hf_token = st.secrets["hf_token"]
headers = {"Authorization": f"Bearer {hf_token}"}

def build_prompt(meme_name):
    return f"""
너는 인터넷 밈을 잘 아는 AI야. 사용자가 '{meme_name}'이라는 밈 이름을 입력하면,
1. 뜻
2. 유래
3. 사용 예시

이 세 가지 항목으로 짧고 간결하게 설명해줘. 한국어로.
"""

def query_huggingface_model(prompt):
    api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        result = response.json()
        # 그냥 전체 텍스트 반환, 예외처리도 추가
        try:
            return result[0]["generated_text"]
        except Exception:
            return str(result)
    else:
        return f"[에러] 상태 코드: {response.status_code}, 응답: {response.text}"

st.set_page_config(page_title="AI 밈 설명기 (HuggingFace)", page_icon="🤖")
st.title("🤖 HuggingFace 기반 AI 밈 설명기")
st.write("AI가 밈의 뜻과 유래를 설명해드립니다!")

meme_input = st.text_input("밈 이름을 입력하세요 (예: 갓생, 킹받네, Distracted Boyfriend)").strip()

if st.button("설명 보기") and meme_input:
    with st.spinner("AI가 설명을 생성 중입니다..."):
        prompt = build_prompt(meme_input)
        explanation = query_huggingface_model(prompt)
        st.text_area("💬 밈 설명", explanation, height=300)

st.markdown("---")
st.caption("제작: Open 에이아밈 + HuggingFace AI")
st.write("🔐 받은 토큰:", hf_token[:6] + "..." if hf_token else "❌ 없음")
