
from fastapi import FastAPI

from korean_verb_tool.api.routers import routers

app = FastAPI()
app.include_router(routers)
