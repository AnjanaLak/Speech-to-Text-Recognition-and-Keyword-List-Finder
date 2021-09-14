############ Routes #################################################################
from flask import jsonify
from audioClassification import app, db, main
#from audioClassification.models import Articles, articles_schema, article_schema
from flask import Flask, request


@app.route('/startAudioProcess', methods=['POST'])
def process_audio():
    path = "output.wav"
    value = request.json['value']
    x = main.start()
    if x == "Completed":
        return jsonify({"Status": "Completed"})
    else:
        return jsonify({"Status": "Not Completed"})



#
# @app.route('/get', methods=['GET'])
# def get_articles():
#     # return jsonify({"Hello":"World"})
#     all_articles = Articles.query.all()
#     results = articles_schema.dump(all_articles)  # note that we are using 's' as it will get many objects
#     return jsonify(results)
#
#
# @app.route('/get/<id>/', methods=['GET'])
# def post_articles(id):
#     article = Articles.query.get(id)
#     return article_schema.jsonify(article)
#
#
# @app.route('/add', methods=['POST'])
# def add_articles():
#     title = request.json['title']
#     body = request.json['body']
#
#     articles = Articles(title, body)  # creating an article object
#     db.session.add(articles)  # adding the record to the object
#     db.session.commit()
#     return article_schema.jsonify(articles)
#
#
# # Update
#
# @app.route('/update/<id>/', methods=['PUT'])
# def update_articles(id):
#     article = Articles.query.get(id)
#
#     title = request.json['title']
#     body = request.json['body']
#
#     article.title = title
#     article.body = body
#
#     db.session.commit()
#     return article_schema.jsonify(article)
#
#
# # delete
# @app.route('/delete/<id>/', methods=['DELETE'])
# def delete_articles(id):
#     article = Articles.query.get(id)
#
#     db.session.delete(article)
#     db.session.commit()
#
#     return article_schema.jsonify(article)
