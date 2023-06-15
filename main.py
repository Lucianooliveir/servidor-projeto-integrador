from flask import Flask, request
from models.produto import produto
import db.database as db
from bson import json_util
import json
import requests

key = "s15i4haqdp7phgz3zwa708cx3kdhfs"

app = Flask(__name__)


@app.route('/pesquisarNome')
def pesquisarNome():
    data = request.args.get('nome')
    print(json.loads(json_util.dumps(db.searchByName(data))))
    if json.loads(json_util.dumps(db.searchByName(data))) != []:
        return json.loads(json_util.dumps(db.searchByName(data)))
    else:
        return "0"


@app.route('/receberProduto')
def receberProduto():
    data = int(request.args.get('codigo'))
    quantidade = int(request.args.get('quantidade'))
    if db.searchByCode(data) == None:
        prod = requests.get(f'https://api.barcodelookup.com/v3/products?barcode={data}&formatted=y&key={key}')
        if prod.status_code == 404:
            return "produto nao encontrado"
        else: 
            prod_dict = prod.json()
            prod_dict = prod_dict.get('products')[0]
            product = produto(int(data),1,0.00,prod_dict.get('title'),prod_dict.get('description'))
            db.createProduct(produto=product)
    else:
        db.updateQuant(data,quantidade)
    return "0"

@app.route('/saidaProduto')
def saidaProduto():
    data = int(request.args.get('codigo'))
    quantidade = int(request.args.get('quantidade'))
    if db.searchByCode(data) == None:
        prod = requests.get(f'https://api.barcodelookup.com/v3/products?barcode={data}&formatted=y&key={key}')
        if prod.status_code == 404:
            return "produto nao encontrado"
        else: 
            prod_dict = prod.json()
            prod_dict = prod_dict.get('products')[0]
            product = produto(int(data),1,0.00,prod_dict.get('title'),prod_dict.get('description'))
            db.createProduct(produto=product)
            return "produto criado"
    else:
        db.updateQuant(data,-abs(quantidade))
    if db.searchByCode(data).get('quantidade')<=1:
        return "estoque baixo"
    else:
        return "produto saiu"

@app.route('/')
def teste():
    print(db.searchByCode(1))
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
    prod = produto(int(data.get('codigo')), data.get('quantidade'), 0, data.get('nome'), '')
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
