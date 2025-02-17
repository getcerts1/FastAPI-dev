from fastapi import FastAPI
import pydantic
import azure.functions as func
import json



def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "GET":
        name = req.params.get("name")
        if not name:
            try:
                req_body = req.get_json()
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid request body"}),
                    status_code=400,
                )
            name = req_body.get("name")

        if name:
            return func.HttpResponse(
                json.dumps({"message":"success"})
            )