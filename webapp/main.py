from fastapi import FastAPI

# fastapi() 객체 생성
app = FastAPI()

# 홈
@app.get("/")
async def home(image_url: str):
    # 사용자 image_url을 받음
    print(image_url)
    # 이미지의 요리명, 요리의 풍미 설명(llm) -> wine top-5 검색 -> 요리에 어울리는 와인 추천
    # 1단계 결과: 이미지의 요리명, 요리의 풍미 설명(llm)
    res = "llm을 통해 추천 받은 것을 사용자에게 반환"
    return {"message": res}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000, reload=True)
