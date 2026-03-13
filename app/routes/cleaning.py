from fastapi import APIRouter, UploadFile, Form, HTTPException, BackgroundTasks
from supabase import create_client, StorageException
from postgrest.exceptions import APIError
from uuid import uuid4
from app.utils.discord import send_cleaning_to_discord

from app.database import supabase
from app.config import SUPABASE_URL

router = APIRouter(
    prefix="/cleaning",
    tags=["Cleaning"]
)


@router.post("/upload")
async def upload_cleaning(
    background_tasks: BackgroundTasks,
    cleaner_name: str = Form(...),
    room_number: str = Form(...),
    image: UploadFile = Form(...)
):

    if not cleaner_name or not room_number or not image:
        print("Missing Parameters")

    file_name = f"{uuid4()}_{image.filename}"

    try:

        file_bytes = await image.read()

        supabase.storage.from_("cleaning-images").upload(
            file_name,
            file_bytes
        )

        image_url = f"{SUPABASE_URL}/storage/v1/object/public/cleaning-images/{file_name}"

        data = {
            "cleaner_name": cleaner_name,
            "room_number": room_number,
            "image_url": image_url
        }

        supabase.table("cleaning_receipts").insert(data).execute()

        background_tasks.add_task(
            send_cleaning_to_discord,
            cleaner_name,
            room_number,
            image_url
        )

        return {
            "message": "Cleaning receipt stored",
            "image_url": image_url
        }

    except StorageException as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {str(e)}")
        
    except APIError as e:
        supabase.storage.from_("cleaning-images").remove([file_name])
        error_msg = getattr(e, 'message', str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {error_msg}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")