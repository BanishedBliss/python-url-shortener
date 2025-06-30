# Python FastAPI URL-shortener with Async Capabilities
## Overview
This service provides URL shortening functionality with additional 
async request processing capabilities.

## Technology Stack
- Framework: FastAPI
- Database: SQLite (via aiosqlite)
- Async HTTP: HTTPX
- Validation: Pydantic v2
- Environment Management: pydantic-settings

## Deployment
### Prerequisites
- Python 3.9+
- pip package manager

### Steps
1. Clone the repository to your desired directory.
2. Create and activate a virtual environment:
``` 
python -m venv venv
```
Linux/MacOS:
```
source venv/bin/activate
```
Windows:
```
venv\Scripts\activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Copy `.env.example` and rename it to `.env`
5. Configure environment variables in `.env`:

| Variable        | Default                       | Description                              |
|-----------------|-------------------------------|------------------------------------------|
| DATABASE_URL    | sqlite+aiosqlite:///./test.db | Database connection string               |
| SERVICE_TIMEOUT | 5.0                           | Timeout for external requests (seconds)  |
| HOST            | 127.0.0.1                     | Application host                         |                         
| PORT            | 8080                          | Application port                         |                         
| DEBUG           | false                         | Debug mode                               |

6. Run `python -m app.main` in the project root to start the process.

## API Endpoints

### Shorten URL
#### Endpoint: POST /
Request Body:
```json
{
  "url": "https://example.com"
}
```
Response (201 Created):
```json
{
  "short_id": "Abc123"
}
```

### Redirect to Original URL
#### Endpoint: GET /{short_id}
Response:
```
307 Temporary Redirect
```
If short ID doesn't exist:
```
404 Not Found 
```

### Asynchronous HTTP Request
#### Endpoint: POST /async-request
Request Body:
```json
{
  "url": "https://example.com"
}
```
Response (200 OK): 

#### Received data 
```json
{
  "status": 200,
  "headers": {
    "Content-Type": "text/html",
    ...
  },
  "content": "<!doctype html>... (truncated if long)"
}
```