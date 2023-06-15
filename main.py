from flask import Flask, request
from models.produto import produto
import db.database as db
from bson import json_util
import json

app = Flask(__name__)


@app.route('/pesquisarNome')
def pesquisarNome():
    data = request.args.get('nome')
    print(json.loads(json_util.dumps(db.searchByCode(data))))
    if json.loads(json_util.dumps(db.searchByCode(data))) != None:
        return json.loads(json_util.dumps(db.searchByCode(data)))
    else:
        return "0"


@app.route('/pesquisarCodigo')
def pesquisarCodigo():
    data = request.args
    if json.loads(json_util.dumps(db.searchByCode(int(data.get('codigo'))))) != None:
        return json.loads(json_util.dumps(db.searchByCode(int(data.get('codigo')))))
    else:
        return "0"


@app.route('/addProduto', methods=['POST'])
def addProduto():
    data = json.loads(request.json)
    prod = produto(int(data.get('codigo')), int(data.get('quantidade')), float(data.get(
        'preco')), data.get('nome'), data.get('descricao'))
    db.createProduct(prod)
    return "deu certo"


@app.route('/all')
def returnAll():
    pesquisa = db.readAll()
    return json.loads(json_util.dumps(pesquisa))


@app.route("/atualizarQuant", methods=['POST'])
def atualizarQuant():
    data = json.loads(request.json)
    db.updateQuant(int(data.get('codigo')), int(data.get('quantidade')))
    return "0"
