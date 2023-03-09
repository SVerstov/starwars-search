import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from classes import SWarsSearch

app = FastAPI()

# Add the CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def search(search: str):
    character_searcher = SWarsSearch(type='people', fields=['name', 'mass', 'height'])
    planet_searcher = SWarsSearch(type='planets', fields=['name', 'diameter', 'population'])
    starship_searcher = SWarsSearch(type='starships', fields=['name', 'length', 'crew'])

    results = await asyncio.gather(
        character_searcher.search(search),
        planet_searcher.search(search),
        starship_searcher.search(search)
    )
    search_results = {}
    for result in results:
        search_results.update(result)

    return {"search_results": search_results}
