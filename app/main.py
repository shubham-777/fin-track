import uvicorn
from fastapi import FastAPI

from core import configurations as config
from db.sql import engine
from db.sql_models import Base
from routers import user, health, category, transaction, finance_type

# from fastapi.exception_handlers import http_exception_handler
# from routers import continent, country, city, task_res
# from models import sql_models
# from routers import health

description = """
A Personal finance tracking REST API 🚀

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
Base.metadata.create_all(bind=engine)
app.include_router(health.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(finance_type.router)

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
