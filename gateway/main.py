from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI(title="API Gateway")

# Service URLs (Internal Docker Network)
SERVICE_URLS = {
    "subscription": "http://subscription_service:8000",
}


@app.get("/")
async def root():
    return {"message": "Welcome to the API Gateway"}


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    service_url = f"{SERVICE_URLS[service]}/{path}"

    # Forward the request to the target service
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=service_url,
            headers=request.headers.raw,
            content=await request.body(),
            params=request.query_params,
        )
        return response.json()
