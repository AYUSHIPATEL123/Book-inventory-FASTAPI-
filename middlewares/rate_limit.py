from fastapi import Request
from fastapi.responses import JSONResponse

request_counts={}
async def rate_limiting(request:Request,call_next):

        ip = request.client.host
        print(ip)
        request_counts[ip] = request_counts.get(ip,0) + 1

        if request_counts[ip] > 5:
                
            return JSONResponse(status_code=429,content="too many requests")
        
        response = await call_next(request)

        return response
