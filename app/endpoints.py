from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from fastapi.responses import RedirectResponse
from .schemas import ShortenRequest, AsyncRequest, ShortenResponse
from .services import create_short_url, get_original_url, verify_url_availability, fetch_url_data

router = APIRouter()

@router.post("/", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(
    request: ShortenRequest,
    background_tasks: BackgroundTasks
):
    short_id = await create_short_url(str(request.url))
    background_tasks.add_task(verify_url_availability, str(request.url))
    return {"short_id": short_id}

@router.get("/{short_id}")
async def redirect_url(short_id: str):
    original_url = await get_original_url(short_id)
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.post("/async-request")
async def async_service_request(request: AsyncRequest):
    try:
        result = await fetch_url_data(str(request.url))
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )