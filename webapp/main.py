from fastapi import FastAPI,  UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
import base64
import os

from wine_pairing import wine_pair_main
# FastAPI() 객체 생성
app = FastAPI()

# templates 설정
templates = Jinja2Templates(directory="templates")

# static 설정 (css/js 사용 시 필요)
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 홈
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# https://thumbnail.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/9d0d/fd3f0d77757f64b2eba0905dcdd85051932ec1ab5e6afc0c3246f403fabc.jpg
@app.post("/winepair")
async def wine_pairing_api(file: UploadFile = File(...)):
    try:
        print("file.filename", file.filename)

        # 1. 이미지 파일 읽기
        image_bytes = await file.read()

        # 3. 핵심 로직 호출 (클라이언트에서 전달된 이미지 바이트 사용)
        result = wine_pair_main(image_bytes)

        return {
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

