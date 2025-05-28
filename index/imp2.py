from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm
import time

#MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["NKU"]
mongo_col = mongo_db["nku"]

# Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "nku_pages"

if not es.ping():
    print("[错误] 无法连接到 Elasticsearch，请确认服务是否已启动。")
    exit()

print(f"[MongoDB] 共找到 {mongo_col.count_documents({})} 条文档")

# 删除旧索引（如果存在）
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"[Elasticsearch] 旧索引 '{index_name}' 已删除")

#创建新索引并设置中文分词器
index_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart"
            },
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart"
            },
            "url": {"type": "keyword"},
            "snapshot_filename": {"type": "keyword"},
            "source_type": {"type": "keyword"},
            "crawl_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time"
            }
        }
    }
}

es.indices.create(index=index_name, body=index_body)
print(f"[Elasticsearch] 新索引 '{index_name}' 已创建")

def generate_data():
    for doc in mongo_col.find():
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

#进度条
print("[导入] 正在将数据导入 Elasticsearch ...")
start = time.time()
success, failed = bulk(es, generate_data(), stats_only=True)
end = time.time()

print(f"[完成] 导入成功文档数：{success}")
print(f"[用时] {end - start:.2f} 秒")

input("tap to exit...")