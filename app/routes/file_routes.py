import io

from bson import ObjectId
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from app.dependencies.mongo_dependencies import get_bucket

router = APIRouter(prefix="/files", tags=["files"])


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    file_bytes = await file.read()
    file_id = await bucket.upload_from_stream(file.filename, file_bytes)
    return {"file_id": str(file_id)}


@router.get("/{file_id}")
async def download_file(
    file_id: str,
    bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    grid_out = await bucket.open_download_stream(ObjectId(file_id))
    file_bytes = await grid_out.read()  # type: ignore[func-returns-value]
    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{grid_out.filename}"'
        },
    )


@router.put("/{file_id}")
async def replace_file(
    file_id: str,
    file: UploadFile = File(...),
    bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    await bucket.delete(ObjectId(file_id))
    file_bytes = await file.read()
    await bucket.upload_from_stream_with_id(ObjectId(file_id), file.filename, file_bytes)
    return {"file_id": file_id}


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    bucket: AsyncIOMotorGridFSBucket = Depends(get_bucket)
):
    await bucket.delete(ObjectId(file_id))
    return {"file_id": file_id}