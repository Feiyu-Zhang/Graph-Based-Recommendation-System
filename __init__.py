from flask import Flask, request, jsonify
from recommender import recommendBasedOnSearch, recommendBasedOnHistory

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 显示中文


@app.route('/search', methods=['GET'])
def search():
    itemId = request.args.get('item')
    recId = recommendBasedOnSearch(itemId)  # 推荐算法API
    return jsonify(recId)
    # return '<h1>推荐的知识点 {} </h1>'.format(recId)


@app.route('/recommend', methods=['POST'])
def recommend():
    jsonData = request.json
    data = dict()
    data['knowledge'] = jsonData.get('knowledge')
    data['relatedKnowledge'] = jsonData.get('relatedKnowledge')
    data['currentRelatedKnowledge'] = jsonData.get('currentRelatedKnowledge')
    recList = recommendBasedOnHistory(data)
    return jsonify(recList)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
