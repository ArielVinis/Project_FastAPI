# Para rodar o código, executar no terminal: uvicorn main:app --reload
# Lembrar sempre do processo de Lazyloaded na rotas ao mostrar as mensagens no json.
# Para gerar o documento(requeriments.txt) com as dependencias usadas: pip freeze > requirements.txt
# Para instalar o requeriments.txt: pip install -r requirements.txt

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.responses import HTMLResponse

from starlette.responses import HTMLResponse

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")

from routes import auth_router, order_router

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
def home():
    return {
      "mensagem": "🚀 API rodando com sucesso!",
      "documentation_swagger": "http://localhost:8000/docs"
    }
