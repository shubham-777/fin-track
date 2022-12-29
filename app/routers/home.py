from fastapi import APIRouter, Request
from app.main import templates
from fastapi.responses import HTMLResponse

# router = APIRouter(prefix="/index", tags=["home"], responses={404: {"description": "Not found"}})
# tags_metadata = [
#     {
#         "name": "home",
#         "description": "Home page..",
#     }
# ]
#
#
# # @router.get("/get_all", response_modesal=List[pyd_schemas.Continent], status_code=status.HTTP_200_OK)
# # def get_all_continents():
# #     task = continent.get_all_continent.apply_async()
# #     result = task.wait(timeout=None, interval=0.5)
# #     return result
#
# @router.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})
