# Name : Afwan Izzul Fadhoil
# Class : XII TKJ 3
# No Anbsence : 02

from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime   
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.yduqk9k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta_plus_week2

api_key = '186a0412-f43c-454c-a711-6c61bf5d6fb6'


@app.route('/')
def main():
    words_result = db.words.find({}, {'_id': False})
    words = []
    for word in words_result:
        definition = word['definitions'][0]['shortdef']
        definition = definition if type(definition) is str else definition[0]
        words.append({
            'word': word['word'],
            'definition': definition,
        })
    msg = request.args.get('msg')
    return render_template(
        'index.html',
        words=words,
        msg=msg,
    )


@app.route('/details/<keyword>') #detail page
def detail_page(keyword):
    url = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()

    if not definitions:
        return redirect(url_for('main', msg=f'Could not find {keyword}'))
    if type(definitions[0]) is str:
        return render_template('error.html', word=keyword, suggestions=definitions)
    
    return render_template('details.html', word=keyword, definitions=definitions, status=request.args.get('status_give', 'new'))

@app.route('/api/save_word', methods=['POST']) #save word when not in database
def save_word():
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d %H-%M-%S')
    doc = {
        'word': word,
        'definitions': definitions,
        'date': mytime, 
    }
    db.words.insert_one(doc)

    return jsonify({
        'result': 'success',
        'msg': f'the word {word}, was saved!!!',
    })


@app.route('/api/delete_word', methods=['POST']) #delete word in database
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    db.examples.delete_many({'word': word}) 

    return jsonify({
        'result': 'success',
        'msg': f'the word {word} was deleted',
    })


# Example API routes below this line 
@app.route("/api/get_exs", methods=["GET"])
def get_exs():
    word = request.args.get("word")
    example_data = db.examples.find({"word": word})
    examples = []
    for example in example_data:
        examples.append(
            {"example": example.get("example"), "id": str(example.get("_id"))}
        )
    print("examples", examples)
    return jsonify({"result": "success", "examples": examples})


@app.route("/api/save_ex", methods=["POST"])
def save_ex():
    word = request.form.get("word")
    example = request.form.get("example")
    doc = {
        "word": word,
        "example": example,
    }
    db.examples.insert_one(doc)
    return jsonify(
        {
            "result": "success",
            "msg": f'Your example, "{example}", for "{word}" was saved!',
        }
    )


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    id = request.form.get('id')
    word = request.form.get('word')
    db.examples.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': 'success', "msg": f'Your word, "{word}", was deleted successfully!'})

if __name__ == '__main__': #run file
    app.run('0.0.0.0', port=5000, debug=True)