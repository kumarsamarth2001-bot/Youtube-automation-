"""Optional YouTube uploader. Defaults to PRIVATE uploads."""
import json
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_path, title, description="", privacy="private"):
    raw = os.environ.get("YOUTUBE_OAUTH_JSON")
    if not raw:
        raise RuntimeError("Missing YOUTUBE_OAUTH_JSON GitHub Actions secret.")
    data = json.loads(raw)
    creds = Credentials(
        token=None,
        refresh_token=data["refresh_token"],
        token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=SCOPES,
    )
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "categoryId": "27",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    result = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    print("Uploaded video ID:", result.get("id"))
