import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LANGUAGES = {"영어": "English", "일본어": "Japanese", "스페인어": "Spanish"}

st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 간단 번역기")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(".env 파일에 OPENAI_API_KEY를 설정해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

text = st.text_area("번역할 글을 입력하세요", height=200)
target = st.radio("번역할 언어", list(LANGUAGES.keys()), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해주세요.")
    else:
        with st.spinner("번역 중..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"You are a professional translator. Translate the user's text into "
                                f"{LANGUAGES[target]}. Output only the translation, without any explanation."
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                )
                st.subheader(f"{target} 번역 결과")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
