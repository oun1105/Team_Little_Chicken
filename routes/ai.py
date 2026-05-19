from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 회의 내용을 요약하는 AI야. 핵심만 3줄로 요약해줘."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    test = "오늘 회의에서 백엔드는 로그인 API를 만들기로 했고, 프론트는 화면 디자인을 맡기로 했다. 다음 회의는 5월 26일이다."
    print(summarize(test))