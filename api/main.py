from fastapi import FastAPI 
from api.routes import user, login, post, votes
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

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
app.include_router(votes.router)


#Posts API
@app.get("/")
def root():
    return RedirectResponse(url="/docs")



if __name__ == "__main__":
    uvicorn.run(app="api.main:app", host="localhost", port=8000, reload=True)
#Users API