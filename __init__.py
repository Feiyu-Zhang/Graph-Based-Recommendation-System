from flask import Flask, request, jsonify
from recommender import recommend

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 显示中文


@app.route('/rec', methods=['GET'])
def rec():
    itemId = request.args.get('item')
    recId = recommend(itemId)  # 推荐算法API
    return jsonify(recId)
    # return '<h1>推荐的知识点 {} </h1>'.format(recId)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
