from fastapi import FastAPI 
from routes import shorten_url, user, login, post
import uvicorn
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

app.include_router(user.router)
app.include_router(login.router)
app.include_router(post.router)


#Posts API
@app.get("/")
def root():
    return {"message": "siuuuuuuu!"}



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
#Users API