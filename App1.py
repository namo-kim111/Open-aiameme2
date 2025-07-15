import streamlit as st
import requests

# ✅ HuggingFace API 토큰 (Streamlit Cloud의 Secrets에 입력 필요)
hf_token = st.secrets["hf_token"]
headers = {"Authorization": f"Bearer {hf_token}"}

# ✅ 사용자 입력에 기반한 프롬프트 구성
def build_prompt(meme_name):
    return f"""### 사용자:
'{meme_name}'이라는 밈을 한국어로 간단히 설명해줘.
1. 뜻
2. 유래
3. 사용 예시

이 세 가지로 구성해줘.

### AI:"""

# ✅ HuggingFace API 호출 함수
def query_huggingface_model(prompt):
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300}}
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            result = response.json()
            return result[0].get("generated_text", "[⚠️ 예상 응답 없음]")
        except Exception:
            return "[⚠️ JSON 파싱 실패]: " + str(result)
    else:
        return f"[❌ API 오류] 상태 코드: {response.status_code}, 응답: {response.text}"

# ✅ Streamlit UI 구성
st.set_page_config(page_title="AI 밈 설명기 (Mistral)", page_icon="🤖")
st.title("🤖 Mistral 기반 AI 밈 설명기")
st.write("AI가 밈의 뜻과 유래를 설명해드립니다!")

meme_input = st.text_input("밈 이름을 입력하세요 (예: 갓생, 킹받네, 리멤버 노무현)").strip()

if st.button("설명 보기") and meme_input:
    with st.spinner("AI가 설명을 생성 중입니다..."):
        prompt = build_prompt(meme_input)
        explanation = query_huggingface_model(prompt)
        st.text_area("💬 밈 설명", explanation.strip(), height=300)

st.markdown("---")
st.caption("제작: Open 에이아밈 + Mistral AI")

st.write("🔐 받은 토큰:", hf_token[:6] + "..." if hf_token else "❌ 없음")
