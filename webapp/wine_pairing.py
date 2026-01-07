from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.runnables import RunnableLambda

from dotenv import load_dotenv
import os

load_dotenv(override=True, dotenv_path="../.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM을 통한 요리 정보 설명
# 함수 정의 : 이미지 -> 요리명, 풍미 설명 출력
def describe_dish_flavor(input_data):

    prompt = ChatPromptTemplate([
        ("system", """
        You are a culinary expert.
        Based on the input image of a dish,

        you identify the most likely name of the dish by analyzing visual cues such as ingredients, cooking methods, and plating,

        and infer the ingredients and preparation techniques to describe the flavor profile objectively.

        If the dish name is an estimate, this should be stated clearly.
        The flavor description should focus concisely on key taste components (sweetness, saltiness, umami, richness, spiciness, acidity),
        aroma, and textural contrast.
        Subjective judgments and emotional expressions must be excluded, and the explanation should be grounded in observable facts.
        """),
        HumanMessagePromptTemplate.from_template([
            {"text": """아래 이미지의 요리에 대한 요리명과 풍미를 설명해주세요.
             출력형태 :
             요리명 :
             요리의 풍미:
            """},
            {"image_url": "{image_url}"} # image_url는 정해줘 있음.
        ])
    ])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=GOOGLE_API_KEY
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    return chain

# 함수를 실행하는 코드
def wine_pair_main(img_url):
    # 함수를 전달인자로 넣기
    r1 = RunnableLambda(describe_dish_flavor)

    # RunnableLambda를 통한 함수 실행
    input_data = {
        "image_url": img_url
        }
    res = r1.invoke(input_data)
    return res

# 모듈 테스트용 코드
if __name__ == "__main__":
    img = "https://static.wtable.co.kr/image/production/service/recipe/2068/8e90b171-4b7c-44da-affc-bb9bc8297084.jpg?size=800x800"
    result = wine_pair_main(img)
    print(result)


