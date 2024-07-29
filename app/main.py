import io
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
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD),
    scheme="http",
    verify_certs=False
)
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


@app.post("/indices/create/multi")
async def create_multi_index(file: UploadFile):
    try:
        # Đọc nội dung tệp tải lên
        content = await file.read()
        data = content.decode("utf-8").splitlines()

        data_response = []

        for line in data:
            try:
                # Phân tích JSON từ dòng
                index_data = json.loads(line)
                index_name = index_data.pop("index_name", None)  # Lấy và loại bỏ 'index_name' từ dữ liệu JSON

                if not index_name:
                    raise HTTPException(status_code=400, detail="Each JSON object must contain 'index_name'")

                # Tạo chỉ mục
                response = es.indices.create(index=index_name, body=index_data)
                data_response.append(response)

            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Uploaded file contains invalid JSON")
            except exceptions.TransportError as e:
                raise HTTPException(status_code=e.status_code, detail=e.info)

        return {"message": "Indices created successfully", "responses": data_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/{index}")
async def get_search_index(index: str):
    try:
        request_index = "*" + index + "*"
        response = es.search(index=request_index, body={
            "query": {
                "match_all": {}
            }
        })
        return response
    except exceptions.TransportError as e:
        raise HTTPException(status_code=e.status_code, detail=e.info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/indices/{index_name}")
async def delete_index(index_name: str):
    try:
        response = es.indices.delete(index=index_name)
        return {"message": f"Index '{index_name}' deleted successfully", "response": response}

    except exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
    except exceptions.TransportError as e:
        raise HTTPException(status_code=e.status_code, detail=e.info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
