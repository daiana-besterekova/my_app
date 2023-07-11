from fastapi import FastAPI
from pydantic import BaseModel
import openai
import uvicorn
from color import *

class ImageDescription(BaseModel):
    description: str
    color: str

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
        prompt=generate_prompt(desc.description, desc.color),
        n=1,
        size="256x256"
    )
    result = response['data'][0]['url']
    return {"url": result}

def generate_prompt(description, color):
    color = color if color else "rgb(255,255,255)" # default color is white
    color = closest_remove(color)
    print(color)
    text = description if description else "some default prompt"
    return f"{text} for background сolor use this {color} color"

if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)
