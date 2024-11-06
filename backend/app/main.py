from fastapi import FastAPI
import asyncio
import spacy
from app.rewrite_engine import DependencyBasedReformulator

app = FastAPI()
spacy_nlp = spacy.load("en_core_web_sm")
engine = DependencyBasedReformulator(spacy_nlp)
# model = GLiNER.from_pretrained("urchade/gliner_small-v1")
labels = [
    "Professional Background",
    "Area of Interest",
    "Education",
    "Skills",
]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/rewrite")
async def query_rewrite(query: str):
    return engine.reformulate(query)
