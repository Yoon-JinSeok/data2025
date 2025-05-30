import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# ✅ OpenAI 클라이언트 초기화 (v1 방식)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ CSV 경로 및 파일 유무 확인
csv_path = 'Womens Clothing E-Commerce Reviews.csv'
if not os.path.exists(csv_path):
    st.error(f"❌ CSV 파일이 존재하지 않습니다: `{csv_path}`")
    st.stop()

# ✅ 데이터 로딩
data = pd.read_csv(csv_path, index_col=0)
data = data.dropna(subset=['Review Text'])

# ✅ 리뷰 요약 함수 (GPT-4, 한글 요약)
def aireview(prompt, review_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": review_text}
        ]
    )
    return response.choices[0].message.content

# ✅ Streamlit UI 구성 시작
st.title('🛍️ 의류 리뷰 요약 대시보드')
st.markdown("랜덤 리뷰를 확인하고 GPT-4로 요약해보세요!")

# ✅ 사이드바 필터
st.sidebar.header("🔎 필터 옵션")

departments = ['전체'] + data['Department Name'].dropna().unique().tolist()
selected_dept = st.sidebar.selectbox("부서 선택", departments)

min_age = int(data['Age'].min())
max_age = int(data['Age'].max())
age_range = st.sidebar.slider("리뷰어 나이 범위", min_age, max_age, (min_age, max_age))

# ✅ 필터 적용
filtered_data = data.copy()
if selected_dept != '전체':
    filtered_data = filtered_data[filtered_data['Department Name'] == selected_dept]
filtered_data = filtered_data[
    (filtered_data['Age'] >= age_range[0]) & (filtered_data['Age'] <= age_range[1])
]

st.subheader("📄 필터링된 리뷰 미리보기")
st.write(f"총 {len(filtered_data)}개의 리뷰가 선택되었습니다.")
st.dataframe(filtered_data[['Age', 'Department Name', 'Rating', 'Review Text']].head())

# ✅ 랜덤 리뷰 요약 기능
st.subheader("📝 GPT-4 리뷰 요약")
if len(filtered_data) == 0:
    st.warning("⚠️ 필터 결과에 리뷰가 없습니다.")
else:
    random_review = filtered_data.sample(1)['Review Text'].iloc[0]
    st.text_area("원본 리뷰", random_review, height=150)

    if st.button("요약하기"):
        with st.spinner("요약 중입니다..."):
            prompt = "다음 리뷰를 한 문장으로 요약하고 한글로 출력해줘."
            summary = aireview(prompt, random_review)
            st.success("요약 완료!")
            st.markdown(f"**요약 결과:** {summary}")
