from elasticsearch import Elasticsearch

# 连接 Elasticsearch
es = Elasticsearch("http://localhost:9200")

index_name = "nku_pages"

if not es.ping():
    print("[Elasticsearch] 连接失败！请检查服务是否启动。")
    exit(1)

if not es.indices.exists(index=index_name):
    print(f"[Elasticsearch] 索引 '{index_name}' 不存在！")
    exit(1)

# 查询文档数量
count = es.count(index=index_name)['count']
print(f"[Elasticsearch] 索引 '{index_name}' 中文档数量：{count}")
input("按回车键退出...")