from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm
import datetime
#这个用于导入elasticsearcch



# 连接MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["NKU"]
mongo_col = mongo_db["nku"]

total_docs = mongo_col.count_documents({})
print(f"[MongoDB] Connected. Found {total_docs} documents in collection 'nku'.")

# 连接Elasticsearch
es = Elasticsearch("http://localhost:9200")
if not es.ping():
    print("[Elasticsearch] Connection failed.")
    exit(1)
print("[Elasticsearch] Connected successfully.")

#创建索引（带 ik 分词器）
index_name = "nku_pages"
if not es.indices.exists(index=index_name):
    es.indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "ik_max_word"},
                    "content": {"type": "text", "analyzer": "ik_max_word"},
                    "url": {"type": "keyword"},
                    "snapshot_filename": {"type": "keyword"},
                    "source_type": {"type": "keyword"},
                    "crawl_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
                }
            }
        }
    )
    print(f"[Elasticsearch] Index '{index_name}' created.")
else:
    print(f"[Elasticsearch] Index '{index_name}' already exists.")

#构造bulk数据
def generate_data():
    for doc in tqdm(mongo_col.find(), total=total_docs, desc="[Bulk] Indexing"):
        yield {
            "_index": index_name,
            "_id": str(doc["_id"]),
            "_source": {
                "title": doc.get("title", ""),
                "content": doc.get("content", ""),
                "url": doc.get("url", ""),
                "snapshot_filename": doc.get("snapshot_filename", ""),
                "source_type": doc.get("source_type", ""),
                "crawl_time": doc.get("crawl_time", "1970-01-01 00:00:00")
            }
        }

# 执行bulk导入
print("[Bulk] Starting bulk import...")
success, _ = bulk(es, generate_data())
print(f"[Bulk] Successfully indexed {success} documents.")
