import io

from bson import ObjectId
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from app.dependencies.mongo_dependencies import get_bucket

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload(
    file: UploadFile = File(...), bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    file_bytes = await file.read()
    file_id = await bucket.upload_from_stream(file.filename, file_bytes)
    return str(file_id)


@router.get("/download/{file_id}")
async def download(
    file_id: str, bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    grid_out = await bucket.open_download_stream(ObjectId(file_id))
    return StreamingResponse(
        io.BytesIO(await grid_out.read()),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{grid_out.filename}"'},
    )
