from fastapi import APIRouter, HTTPException
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

router = APIRouter()

@router.post("/upload")
async def upload_video(video_path: str, title: str, description: str, access_token: str):
    try:
        youtube = build("youtube", "v3", credentials={"token": access_token})
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["tag1", "tag2"],
                    "categoryId": "22",  # "People & Blogs"
                },
                "status": {"privacyStatus": "public"},
            },
            media_body=MediaFileUpload(video_path),
        )
        response = request.execute()
        return {"video_id": response["id"], "message": "Video uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {e}")
