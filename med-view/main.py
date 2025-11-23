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

from fastapi import FastAPI, Request, Form
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
            "recent_activity": recent_activity,
            "active_page": "overview"
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


@app.get("/timer", response_class=HTMLResponse)
async def timer_page(request: Request):
    """Render the main Timer page."""
    return templates.TemplateResponse(
        "timer.html",
        {
            "request": request,
            "active_page": "timer"
        }
    )


@app.post("/timer/start", response_class=HTMLResponse)
async def start_timer(request: Request):
    """
    Triggered when 'Start' is clicked.
    Returns the 'Running' partial.
    """
    now = datetime.now()
    
    return templates.TemplateResponse(
        "partials/timer_running.html",
        {
            "request": request,
            # Formatted for display (e.g., "02:30:45 PM")
            "start_time_display": now.strftime("%I:%M:%S %p"),
            # ISO format for the hidden input value (machine readable)
            "start_timestamp": now.isoformat()
        },
    )


@app.post("/timer/stop", response_class=HTMLResponse)
async def stop_timer(request: Request, start_timestamp: str = Form(...)):
    """
    Triggered when 'Stop' is clicked.
    Calculates duration and returns the 'Stopped' partial.
    """
    stop_dt = datetime.now()
    start_dt = datetime.fromisoformat(start_timestamp)
    
    # Calculate duration
    delta = stop_dt - start_dt
    
    # Format duration (removing microseconds for cleaner display)
    # str(delta) usually looks like "0:00:05.123456"
    duration_str = str(delta).split('.')[0] 

    return templates.TemplateResponse(
        "partials/timer_stopped.html",
        {
            "request": request,
            "start_time_display": start_dt.strftime("%I:%M:%S %p"),
            "stop_time_display": stop_dt.strftime("%I:%M:%S %p"),
            "duration": duration_str
        },
    )