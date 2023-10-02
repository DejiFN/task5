```python
# FastAPI Video Recording and Transcription

This is a FastAPI application for recording video sessions, uploading video chunks, and initiating transcription in the background using PostgreSQL as the database backend.

## Setup

### Prerequisites

Make sure you have the following installed:

- [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

1. Create a PostgreSQL database and update the `DATABASE_URL` in the `main.py` file:

   ```python
   DATABASE_URL = "postgresql://your-username:your-password@localhost/your-database-name"
   ```

   Replace `your-username`, `your-password`, and `your-database-name` with your PostgreSQL credentials.

2. Run the database migrations:

   ```bash
   alembic upgrade head
   ```

## Usage

1. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

2. Access the FastAPI Swagger documentation at `http://127.0.0.1:8000/docs` to explore and test the API endpoints.

## API Endpoints

### 1. Start Recording

- **Endpoint:** `/start-recording/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "your-username",
    "mimetype": "video/mp4"
  }
  ```
- **Response:**
  ```json
  {
    "recording_id": "unique-recording-id"
  }
  ```

### 2. Upload Video Chunk

- **Endpoint:** `/upload-chunk/{recording_id}`
- **Method:** `POST`
- **Path Parameters:**
  - `recording_id`: Unique recording ID
- **Request Body:**
  - Form Data: `file` (Video file)
- **Response:**
  ```json
  {
    "message": "Video chunk uploaded successfully"
  }
  ```

### 3. Stop Recording

- **Endpoint:** `/stop-recording/{recording_id}`
- **Method:** `POST`
- **Path Parameters:**
  - `recording_id`: Unique recording ID
- **Response:**
  ```json
  {
    "message": "Recording stopped"
  }
  ```

### 4. Get Video URL

- **Endpoint:** `/get-video-url/`
- **Method:** `GET`
- **Query Parameters:**
  - `username`: User's username
  - `filename`: Video filename
- **Response:**
  ```json
  {
    "video_url": "/stream-video/your-username/your-filename"
  }
  ```

### 5. Stream Video

- **Endpoint:** `/stream-video/{username}/{filename}`
- **Method:** `GET`
- **Path Parameters:**
  - `username`: User's username
  - `filename`: Video filename
- **Response:**
  - Video stream

### 6. Health Check

- **Endpoint:** `/health`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "status": "OK"
  }
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Make sure to replace placeholders like `your-username`, `your-password`, and `your-database-name` with your actual information.