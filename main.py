from fastapi import FastAPI, Query, Request
from fastapi.encoders import jsonable_encoder

from matcloud_mongodb import MatCloudMongoDB
from fastapi.responses import JSONResponse

app = FastAPI(title="MatCloud's OPTiMaDe API implementation",
              description="MatCloud’s OPTiMaDe API implementation",
              openapi_url="/optimade.json",
              version="1.0.0",
              docs_url="/optimade"
              )

md = MatCloudMongoDB()


@app.get("/optimade/v1/Structure/",
         tags=["Structure"],
         summary="Returns a list of records that match the given optimade filter expression",
         )
async def get_items(request: Request,
                    filter: str = Query(None, description="An optimade filter string."),
                    page_offset: int = Query(None, description="Sets the number of records to skip."),
                    page_limit: int = Query(None,
                                            description="Sets a numerical limit on the number of records returned."),
                    sort: str = Query(None, description="Name of the property to sort the results by."),
                    ):
    url = str(request.url)
    if filter == '' or filter is None:
        records = md.find_one(url)
    else:
        records = md.find(url, filter, page_offset, page_limit, sort)

    return records


@app.get("/optimade/v1/Energy/{id}",
         tags=["Energy"],
         summary="Retrieve a single record for the given id",
         )
async def get_item(request: Request, id: str):
    url = str(request.url)
    record = md.find_by_id(url, id)

    return record


@app.get("/optimade/v1/info",
         tags=["Info"],
         summary="Returns information about this optimade implementation",
         )
async def get_info():
    record = md.get_info()

    return JSONResponse(content=jsonable_encoder(record))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
