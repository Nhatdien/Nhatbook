from fastapi import FastAPI 
from routes import shorten_url
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(shorten_url.router)

#Posts API
@app.get("/")
def root():
    return {"message": "siuuuuuuu!"}




#Users API