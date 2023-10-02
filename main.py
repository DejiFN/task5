from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import os
import uuid
import databases
#import whisper

DATABASE_URL = "postgresql://task5data_user:FoDFry16NFNg4WuBiacx6tUXx9GiJbvW@dpg-ckdgnosgonuc73bm5nrg-a/task5data"
database = databases.Database(DATABASE_URL, force_rollback=True)  # Added force_rollback=True

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    filename = Column(String, index=True)
    captions = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class VideoInfo(BaseModel):
    username: str
    mimetype: str

class VideoChunkInfo(BaseModel):
    chunk_number: int
    bucket_name: str
    filename: str
    is_last_chunk: bool

# Local storage directory for video chunks
local_storage_dir = "./local_storage"
os.makedirs(local_storage_dir, exist_ok=True)

# In-memory array to store video chunks
video_chunks = {}

'''
def transcribe_and_save(video_info: VideoInfo, recording_id: str):
    # Get the video chunks for the given recording_id
    video_content = video_chunks.get(recording_id)

    if video_content is None:
        raise HTTPException(status_code=400, detail="No video content available for transcription")

    # Concatenate the video chunks
    try:
        video_content = b"".join(video_content)
    except TypeError as te:
        print(f"TypeError: {te}")
        raise HTTPException(status_code=500, detail="Error during concatenation of video chunks")

    if not video_content:
        raise HTTPException(status_code=400, detail="No video content available for transcription")

    # Transcribe the uploaded video using Whisper ASR
    captions = whisper.transcribe(video_content, language="en-US")

    if captions is None:
        raise HTTPException(status_code=500, detail="Error during transcription")

    # Save video metadata and captions to the database
    db = SessionLocal()
    try:
        db_video = Video(username=video_info.username, filename=recording_id, captions=captions)
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return captions
'''


@app.post("/start-recording/")
async def start_recording(video_info: VideoInfo):
    # Create a unique ID for the video recording session
    recording_id = str(uuid.uuid4())

    # Create a new array in memory for this recording session
    video_chunks[recording_id] = []

    return JSONResponse(content={"recording_id": recording_id}, status_code=200)

@app.post("/upload-chunk/{recording_id}")
async def upload_chunk(recording_id: str, chunk_info: VideoChunkInfo, file: UploadFile = UploadFile(...)):
    try:
        # Read the video content as bytes
        video_content = await file.read()

        # Save the video chunk to local storage
        chunk_filename = f"{recording_id}_chunk_{chunk_info.chunk_number}.mp4"
        chunk_path = os.path.join(local_storage_dir, chunk_filename)
        with open(chunk_path, "wb") as f:
            f.write(video_content)

        # Append the video content to the array in memory for this recording session
        video_chunks[recording_id].append(video_content)

        if chunk_info.is_last_chunk:
            # If it's the last chunk, start the transcription process in the background
            background_tasks = BackgroundTasks()
            background_tasks.add_task(
               # transcribe_and_save, VideoInfo(username=chunk_info.bucket_name, mimetype="video/mp4"), recording_id
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"message": "Video chunk uploaded successfully"}, status_code=200)

@app.post("/stop-recording/{recording_id}")
async def stop_recording(recording_id: str):
    try:
        # Remove the recording session from the in-memory array
        del video_chunks[recording_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"message": "Recording stopped"}, status_code=200)

def get_video_url(username: str, filename: str):
    return f"/stream-video/{username}/{filename}"

@app.get("/get-video-url/")
async def get_video_url(username: str, filename: str):
    return JSONResponse(content={"video_url": get_video_url(username, filename)}, status_code=200)

@app.get("/stream-video/{username}/{filename}")
async def stream_video(username: str, filename: str):
    # For local storage, return the local file path
    video_path = os.path.join(local_storage_dir, filename)
    return FileResponse(video_path, media_type="video/mp4")


@app.get("/")
async def read_root():
    # Redirect to the health endpoint
    raise HTTPException(status_code=303, detail="See Other", headers={"Location": "/health"})

# Health endpoint
@app.get("/health")
async def health():
    return {"status": "OK"}




