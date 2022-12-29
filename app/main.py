import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core import configurations as config
from app.db.sql import engine
from app.db.sql_models import Base
from app.routers import user, health, category, finance_type

# from fastapi.exception_handlers import http_exception_handler
# from routers import continent, country, city, task_res
# from models import sql_models
# from routers import health

description = """
A Python REST API 🚀

## Usage

lorem ipsum **lorem ipsum lorem ipsum lorem ipsum **.
lorem ipsum **lorem ipsum lorem ipsum lorem ipsum **.

## Changelog
 - lorem ipsum
"""
author = "Shubham Ahinave"
all_tags_metadata = list()
all_tags_metadata.extend(health.tags_metadata)
all_tags_metadata.extend(user.tags_metadata)
all_tags_metadata.extend(category.tags_metadata)
all_tags_metadata.extend(finance_type.tags_metadata)
# all_tags_metadata.extend(health.tags_metadata)
# all_tags_metadata.extend(continent.tags_metadata)
# all_tags_metadata.extend(country.tags_metadata)
# all_tags_metadata.extend(city.tags_metadata)
# all_tags_metadata.extend(task_res.tags_metadata)

# app = FastAPI(title="REST API",
#               prefix="wiki",
#               description=description,
#               version="1.0.0",
#               contact={
#                   "name": "Shubham Ahinave",
#                   "url": "https://github.com/shubham-777",
#                   "email": "codesign.developers@gmail.com",
#               }, openapi_tags=all_tags_metadata)
app = FastAPI(title=config.TITLE,
              prefix="wiki",
              description=description,
              version=config.VERSION,
              contact={
                  "name": config.NAME,
                  "url": config.WEB_URL,
                  "email": config.EMAIL,
              }, openapi_tags=all_tags_metadata)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory='templates', autoescape=False, auto_reload=True)
Base.metadata.create_all(bind=engine)
app.include_router(health.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(finance_type.router)
# app.include_router(home.router)

# app.include_router(health.health_route)
# app.include_router(task_res.router)
# app.include_router(continent.router)
# app.include_router(country.router)
# app.include_router(city.router)

# class CustomException(Exception):
#     def __init__(self, desc: str) -> None:
#         self.desc=desc


# @app.exception_handler(CustomException)
# async def my_custom_exception_handler(request: Request, exc: CustomException):
#     if exc.status_code == 404:
#         return JSONResponse(status_code=500,
#         content={"message": f"Error! {exc.name} "},)
#     else:
#         # Just use FastAPI's built-in handler for other errors
#         return await http_exception_handler(request, exc)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
