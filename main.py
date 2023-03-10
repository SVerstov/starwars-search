import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from searcher import search_list

app = FastAPI()
app.mount("/static", StaticFiles(directory="front/static"), name="static")
# Add the CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def search(search: str):
    search_tasks = [x.search(search) for x in search_list]
    results = await asyncio.gather(*search_tasks)
    search_results = {}
    for result in results:
        search_results.update(result)

    return search_results


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("front/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
