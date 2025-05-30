import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 데이터 로드 (구글 드라이브 경로)
data = pd.read_csv('Womens Clothing E-Commerce Reviews.csv', index_col=0)
data = data.dropna(subset=['Review Text'])

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 리뷰 요약 및 한글 번역 함수
def aireview(client, prompt, review_text):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "developer",
                "content": prompt
            },
            {
                "role": "user",
                "content": review_text
            }
        ]
    )
    return response.output_text

st.title('🎉 의류 리뷰 데이터 대시보드')
st.markdown("사이드바에서 필터를 선택하고 데이터를 탐색해보세요!")

st.sidebar.header('🔎 필터 옵션')
departments = ['전체'] + data['Department Name'].unique().tolist()
selected_dept = st.sidebar.selectbox('부서 선택:', departments)

min_age, max_age = int(data['Age'].min()), int(data['Age'].max())
age_range = st.sidebar.slider('리뷰어 나이 범위:', min_age, max_age, (min_age, max_age))

filtered_data = data.copy()
if selected_dept != '전체':
    filtered_data = filtered_data[filtered_data['Department Name'] == selected_dept]
filtered_data = filtered_data[(filtered_data['Age'] >= age_range[0]) & (filtered_data['Age'] <= age_range[1])]

st.subheader('🔍 필터링된 데이터 미리보기')
st.write(f"총 {len(filtered_data)}개의 리뷰가 있습니다.")
st.dataframe(filtered_data.head())

st.subheader('📊 평점 분포')
rating_counts = filtered_data['Rating'].value_counts().sort_index()
st.bar_chart(rating_counts)

st.subheader('📝 리뷰 요약 생성기')
random_review = filtered_data.sample(1)['Review Text'].iloc[0]
st.text_area('원본 리뷰:', random_review, height=100)

if st.button('요약하기'):
    prompt = "다음 리뷰를 한 문장으로 요약하고 한글로 출력해줘."
    summary =aireview(client, prompt, random_review)
    st.write('**요약:**', summary)
