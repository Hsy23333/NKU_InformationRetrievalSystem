from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)

es = Elasticsearch("http://localhost:9200")

@app.route('/search', methods=['GET'])
def searchs():
    q = request.args.get('q')
    search_type = request.args.get('type', 'normal')

    if not q:
        return jsonify([])

    if search_type == 'wildcard':
        body = {
            "query": {
                "wildcard": {
                    "content": f"*{q}*"
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
    else:
        body = {
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["title", "keywords", "content"],
                    "analyzer": "ik_smart"
                }
            }
        }

    result = es.search(index="nku_pages", body=body)
    hits = result['hits']['hits']
    return jsonify([{
        "title": hit['_source'].get('title', ''),
        "content": hit['_source'].get('content', ''),
        "url": hit['_source'].get('url', '')
    } for hit in hits])

if __name__ == '__main__':
    app.run(debug=True)
