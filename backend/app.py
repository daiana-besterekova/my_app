from fastapi import FastAPI, Request, Form
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from typing import Optional
import openai
import uvicorn

class Settings(BaseModel):
    OPENAI_API_KEY: str = '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'

    class Config:
        env_file = '.venv'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()

@app.post("/generate_image")
async def generate_image(desc: ImageDescription):
    response = openai.Image.create( 
        prompt=generate_prompt(desc.description),
        n=1,
        size="256x256"
    )
    result = response['data'][0]['url']
    return {"url": result}


def generate_prompt(description):
    text = description if description else "some default prompt"
    return f"A sunlit indoor lounge area with a pool containing a {text}"


if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)