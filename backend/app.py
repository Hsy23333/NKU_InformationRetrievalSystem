from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
CORS(app)

es = Elasticsearch("http://localhost:9200")

#快照图片所在本地目录
SNAPSHOT_DIR = os.path.abspath("../spider/tutorial/snapshots")

@app.route('/snapshots/<filename>')
def get_snapshot(filename):
    file_path = os.path.join(SNAPSHOT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Snapshot not found"}), 404

    return send_file(file_path, mimetype='image/png')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json(force=True)
        q = data.get('keyword', '').strip()
        search_type = data.get('type', 'normal')
    else:
        q = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'normal')

    print(f"[搜索关键词] {q} | [搜索类型] {search_type}")

    if not q:
        return jsonify([])

    if search_type == 'wildcard':
        body = {
            "query": {
                "wildcard": {
                    "content": {
                        "value": f"*{q}*",
                        "boost": 1.0,
                        "rewrite": "constant_score"
                    }
                }
            }
        }
    elif search_type == 'phrase':
        body = {
            "query": {
                "match_phrase": {
                    "content": q
                }
            }
        }
    else:  # normal 分词搜索
        body = {
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["title", "keywords", "content"],
                    "analyzer": "ik_smart"
                }
            }
        }

    try:
        result = es.search(index="nku_pages", body=body)
        hits = result['hits']['hits']
        print(f"[命中数量] {len(hits)}")
    except Exception as e:
        print("[搜索异常]", e)
        return jsonify([])

    return jsonify([
        {
            "title": hit['_source'].get('title', ''),
            "content": hit['_source'].get('content', ''),
            "url": hit['_source'].get('url', ''),
            "source_type": hit['_source'].get('source_type', ''),
            "snapshot_filename": hit['_source'].get('snapshot_filename','')
        }
        for hit in hits
    ])

if __name__ == '__main__':
    app.run(debug=True)
