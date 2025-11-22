# -----------------------------------------------------------
# main.py
# -----------------------------------------------------------
# Current Time: a sample FastAPI + HTMX + Jinja2 web app
#   GET / → renders a page with a button
#   Clicking the button uses HTMX to call GET /time
#   GET /time → returns a small HTML snippet (just the time)
# -----------------------------------------------------------
# Dependencies:
#   pip install fastapi uvicorn jinja2 python-multipart
# -----------------------------------------------------------
# How to Run using Uvicorn:
#   In the same directory where main.py is located:
#   uvicorn main:app --reload
#   Access in browser: http://127.0.0.1:8000/
# To stop server:
#   CTRL + C
# -----------------------------------------------------------

from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Tell FastAPI where your Jinja2 templates live
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, images) from static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main dashboard page."""
    # In a real app, pull these from a database or ETL process
    summary = {
        "total_records": 15423,
        "jobs_running": 3,
        "last_run": "Today 07:32",
        "alerts": 2,
    }
    recent_activity = [
        "Job #42 completed successfully.",
        "New dataset 'dd_interactions_2025.parquet' loaded.",
        "Alert resolved: Missing values in lab_results.",
        "User 'csylvester' updated ETL configuration.",
    ]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": summary,
            "recent_activity": recent_activity
        },
    )


@app.get("/time", response_class=HTMLResponse)
async def get_time(request: Request):
    """Return a small HTML snippet with the current time."""
    now = datetime.now().strftime("%H:%M:%S")

    # We return a partial template that ONLY contains the snippet HTMX will swap in.
    return templates.TemplateResponse(
        "partials/time.html",
        {
            "request": request,
            "now": now,
        },
    )
