import streamlit as st
import pandas as pd
import os  # ← 반드시 필요
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# CSV 경로 확인
csv_path = 'Womens Clothing E-Commerce Reviews.csv'
if not os.path.exists(csv_path):
    st.error(f"❌ CSV 파일이 존재하지 않습니다: `{csv_path}`")
    st.stop()

# 데이터 로딩
data = pd.read_csv(csv_path, index_col=0)
data = data.dropna(subset=['Review Text'])


# 요약 함수
def aireview(prompt, review_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": review_text}
        ]
    )
    return response.choices[0].message.content
