from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes import tc, gallery, auth

load_dotenv()

app = FastAPI(title="Holy Kingdom School API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://holykingdom.in"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tc.router)
app.include_router(gallery.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Holy Kingdom School API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
