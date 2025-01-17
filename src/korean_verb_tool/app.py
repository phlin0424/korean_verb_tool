from fastapi import FastAPI

from korean_verb_tool.api.routers import routers
from korean_verb_tool.utils.utils import setup_logging

setup_logging()
app = FastAPI()
app.include_router(routers)

# If deploying to Lambda
# from mangum import Mangum
# handler = Mangum(app)
