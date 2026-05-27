from fastapi import Request
from fastapi.responses import JSONResponse

async def req_content_len(request:Request,call_next):

    length = request.headers.get("content-length",0)
    print(length)
    if int(length)> 100000:
        return JSONResponse(
            status_code=413,
            content={"message": "Payload too large"}
        ) 

    return await call_next(request)   
