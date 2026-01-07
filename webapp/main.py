from fastapi import FastAPI
from wine_pairing import wine_pair_main

# fastapi() 객체 생성
app = FastAPI()

# 홈
@app.get("/")
async def home(image_url: str):
    # 사용자 image_url을 받음
    print(image_url)
    # 이미지의 요리명, 요리의 풍미 설명(llm) -> wine top-5 검색 -> 요리에 어울리는 와인 추천
    # 1단계 결과: 이미지의 요리명, 요리의 풍미 설명(llm)
    # img = "https://static.wtable.co.kr/image/production/service/recipe/2068/8e90b171-4b7c-44da-affc-bb9bc8297084.jpg?size=800x800"
    # result = wine_pair_main(image_url)
    result = "요리명 : 궁중 떡볶이 (Gungjung Tteokbokki)\n\n요리의 풍미:\n이 요리는 간장 양념을 기반으로 한 짭짤하고 고소하며 은은한 단맛이 특징입니다. 소고기, 표고버섯, 간장에서 우러나오는 복합적인 우마미가 중심을 이루며, 참기름과 통깨에서 오는 고소한 향과 풍미가 더해집니다. 당근에서는 자연스러운 단맛과 아삭함이, 대파에서는 미세한 향긋함이 느껴집니다. 전반적으로 매운맛은 없으며, 조리된 떡은 쫄깃하면서도 겉은 살짝 구워져 탄력 있는 식감을 제공하고, 소고기는 부드러우며, 채소는 적절히 익어 아삭하거나 부드러운 다양한 식감의 대비를 이룹니다."
    print(result)
    res = "llm을 통해 추천 받은 것을 사용자에게 반환"
    return {"message": result}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000, reload=True)
