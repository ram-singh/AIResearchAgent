from fastapi import FastAPI
from pydantic import BaseModel
from src.utils import generate_queries

app = FastAPI()

class DateRange(BaseModel):
    start_date: str
    end_date: str

@app.post("/submit_range")
async def submit_range(range: DateRange):
    """Accepts ISO date strings (YYYY-MM-DD) and returns structured queries."""
    queries = generate_queries(range.start_date, range.end_date)
    return {"status": "ok", "queries": queries}


# To run (dev):
# uv run python -m uvicorn src.ui:app --reload
