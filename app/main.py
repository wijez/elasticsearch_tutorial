import json
import logging
import os
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile
from elasticsearch import Elasticsearch, exceptions, helpers
from app.settings import settings
import logging

es = Elasticsearch(
    [{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}],
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD))
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
async def root():
    logger.info("Hello World")
    info = es.info()
    return {
        "message": "Hello World",
        "info": info
    }


@app.get("/indices/all")
async def get_all_indices():
    try:
        indices = es.indices.get_alias("*")
        list_indices = list(indices.keys())
        return {"indices": list_indices}
    except exceptions.ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/indices/{index}")
async def create_index(index: str):
    es.indices.create(index=index)
    message = es.ping()

    return {
        "message": message,
        "index": index
    }


@app.post("/indices/multi/{index_name}")
async def create_multi_index(index_name: str, file: UploadFile):
    try:
        # Đọc nội dung tệp tải lên
        content = await file.read()
        data = content.decode("utf-8").splitlines()

        actions = []
        for line in data:
            try:
                doc = json.loads(line)
                action = {
                    "_index": index_name,
                    "_source": doc
                }
                actions.append(action)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Uploaded file contains invalid JSON")

        helpers.bulk(es, actions)

        return {"message": actions}

    except exceptions.TransportError as e:
        raise HTTPException(status_code=e.status_code, detail=e.info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))