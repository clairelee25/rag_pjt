import base64
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv
import os

load_dotenv(override=True, dotenv_path="../.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")

embedding = OpenAIEmbeddings(
     model = OPENAI_EMBEDDING_MODEL
 )

# LLM을 통한 요리 정보 설명
# 1. 함수 정의 : 이미지 -> 요리명, 풍미 설명 출력
def describe_dish_flavor(image_bytes: bytes):
    """
    input_data = {
        "image_bytes": b"...",   # 이미지 바이너리 데이터
        "image_type": "image/jpeg"  # image/png 등
    }
    """

     # 1️⃣ LLM이 인식 가능한 data URL 생성
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data_url = f"data:image/jpeg;base64,{image_base64}"

    # 2️⃣ 프롬프트 구성
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a culinary expert who analyzes food images.
        Identify the commonly recognized name of the dish and
        clearly describe its flavor, focusing on cooking method,
        texture, aroma, and balance of taste.
        """),
        ("human", [
            {
                "type": "text",
                "text": """
                아래 이미지의 요리명과 요리의 풍미를 설명해 주세요.

                출력 형식:
                요리명:
                요리의 풍미:
                """
            },
            {
                "type": "image_url",
                "image_url": image_data_url
            }
        ])
    ])

    llm = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.1,
        api_key=OPENAI_API_KEY
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})

# 2. 함수 정의 : 요리 설명 -> 요리 설명, 와인 추천 (Top-5)
def search_wines(query):
    embedding = OpenAIEmbeddings(
         model = OPENAI_EMBEDDING_MODEL
    )
    
    # 벡터 db에서 유사도계산, top-5 검색
    # 벡터 db 객체 생성
    vector_db = PineconeVectorStore(
        embedding = embedding,  # 질문에 대한 임베딩 벡터가 생성됨
        index_name = PINECONE_INDEX_NAME ,
        namespace = PINECONE_NAMESPACE
    )
    # 벡터 db에서 질문과 가장 유사한, top-5 검색하기
    results = vector_db.similarity_search(query, k=5)  # top-5 검색

    context = "\n".join([doc.page_content for doc in results])

    # 함수를 호출한 쪽으로 query, top-5의 검색 결과에 필터링한 결과를 리턴함
    return {
        "query" : query,
        "wine_reviews" : context
    }

# 3. 함수 정의 : 요리설명, top-5의 context 입력 받고 -> 요리에 어울리는 와인 추천 
def recommand(input_data):
    prompt = ChatPromptTemplate([
        ("system", """
    🍷 Wine Sommelier – System Prompt (Short / Optimized)
    You are a professional wine sommelier specialized in food and wine pairing.

    When responding, you:
    - Analyze food characteristics (ingredients, cooking method, sauce, flavor intensity)
    - Consider wine structure (acidity, tannin, sweetness, body, alcohol)
    - Apply pairing logic (balance, contrast, complement, intensity matching)

    You always:
    - Explain why a pairing works
    - Adapt recommendations to the customer’s taste, budget, and occasion
    - Use clear, accessible language and avoid unnecessary jargon

    Your goal:
    Recommend wine pairings that create harmony between food and wine and maximize the customer’s enjoyment.
        """),
        ("human", """ 아래 와인리뷰 내용에서만 추천을 해줘
        요리 설명 : {query}
        와인 리뷰 : {wine_reviews}
        
        답변은 json으로 다음과 같이 응답해 주고, recommend_wine은 title만 작성해주세요.
        recommend_wine: 
        price:
        country:
        recommend_reason:
        """)
    ])

    llm = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.1,
        api_key=OPENAI_API_KEY
    )

    # str 파서
    # output_parser = StrOutputParser()

    # json 파서로 변경
    output_parser = JsonOutputParser()

    # pipeline : 데이터의 흐름
    chain = prompt | llm | output_parser

    return chain.invoke(input_data)

# 함수를 실행하는 코드
def wine_pair_main(image_bytes: bytes):
    # RunnableLambda 객체 생성(데이터 파이프라인 연결을 위해)
    r1 = RunnableLambda(describe_dish_flavor)
    r2 = RunnableLambda(search_wines)
    r3 = RunnableLambda(recommand)

    # chain으로 연결하기
    chain = r1 | r2 | r3

    # RunnableLambda를 통한 함수 실행
    
    res = chain.invoke(image_bytes)
    return res

# 모듈 테스트용 코드
if __name__ == "__main__":
    import base64
    print(__name__)
    print("-"*30)
    image_path = "../images/eye_catch_sushi.jpg"

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # img_url = "https://thumbnail.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/9d0d/fd3f0d77757f64b2eba0905dcdd85051932ec1ab5e6afc0c3246f403fabc.jpg"
    result = wine_pair_main(image_bytes)
    print(result)

