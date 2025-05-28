from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

index_name = "nku_pages"

# 查询前5条文档
query = {
    "size": 5,
    "query": {
        "match_all": {}
    }
}

response = es.search(index=index_name, body=query)

hits = response['hits']['hits']

print(f"查询到 {len(hits)} 条文档:")

for doc in hits:
    source = doc['_source']
    title = source.get('title', '无标题')
    url = source.get('url', '无URL')
    print(f"标题: {title}\n链接: {url}\n---")
input("tap to exit...")