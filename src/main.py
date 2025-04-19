from fastapi import FastAPI,Query,Body
from src.database import Base, engine
from src.routers import user_router,belvo_service_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI()

"""
origins = [
    "http://localhost:5173",  # npm run preview
    "http://localhost:4173",  # npm run build
    "http://127.0.0.1:5173/",
    "https://*.netlify.app/",
]
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje":"Hola desde fastapi"}

app.include_router(user_router.router)
app.include_router(belvo_service_router.router)
