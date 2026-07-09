from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from redis_client import redis_client
from rag import ask_question

import json
import time
import traceback


app = FastAPI(
    title="Salesforce AI Assistant API",
    description="REST API for the Salesforce RAG assistant",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
@app.post("/clear-cache")
def clear_cache():

    redis_client.flushall()

    return {
        "message": "Redis cache cleared successfully."
    }

@app.post("/ask")
def ask(request: QuestionRequest):

    start = time.time()

    try:

        
        # Step 1: Check Redis Cache
        
        cached_response = redis_client.get(request.question)

        if cached_response:

            data = json.loads(cached_response)

            data["cached"] = True
            data["time_taken"] = round(
                time.time() - start,
                2
            )

            return data

        # Step 2: Run the RAG Pipeline
        answer, sources = ask_question(request.question)

        time_taken = round(
            time.time() - start,
            2
        )

        response_data = {
            "answer": answer,
            "sources": sources,
            "cached": False,
            "time_taken": time_taken
        }

        # Step 3: Store in Redis
        # Cache expires after 1 hour
        redis_client.setex(
            request.question,
            3600,
            json.dumps(response_data)
        )

        return response_data

    except Exception as e:

        # Print full error in terminal
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )