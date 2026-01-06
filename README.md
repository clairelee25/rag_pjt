# rag_pjt_kpmg7th
AI 와인 소믈리에 : langchain  rag를 활용한 멀티모달 project
<img src="./images/ai_sommerlier.png" alt="프로젝트 소개 이미지">

# langchain rag 설치 라이브러리
```
pip install -qU python-dotenv

# langchain for opeain 
pip install -Uq langchain langchain-openai 

# langchain of google genai
pip install langchain-google-genai

# vectordb
pip install langchain_pinecone

# LCEL chain 그래프로 시각화 lib
pip install -qU grandalf

- 웹앱 관련 lib
pip install fastapi
pip install "uvicorn[standard]"
```

# 허깅페이스의 임베딩 모델을 사용할 때
- nvidia/llama-nemotron-embed-1b-v2
```
pip install langchain-huggingface sentence-transformers
```

# 허깅페이스의 임베딩 모델을 사용할 때
- nvidia/llama-nemotron-embed-1b-v2
```
pip install langchain-huggingface sentence-transformers
```

# 웹앱 실행
```
python app_start.py
```