from fastapi import Request
import time


async def looging_middleware(request:Request,call_next):

    start = time.perf_counter()

    response = await call_next(request)

    dur = time.perf_counter() - start

    print(f"REQUEST {request.url} => {request.method} Completed in {dur:.4f}s")
    response.headers["X-Process-Time"] = str(dur)

    return response
