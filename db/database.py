from pymongo import MongoClient

cluster = MongoClient('mongodb://127.0.0.1:27017/')
db = cluster['projetoIntegrador']
collection = db['produtos']


def createProduct(produto):
    collection.insert_one(produto.__dict__)


def readAll():
    return collection.find({})


def searchByName(nome):
    return collection.find({"nome": {"$regex": nome, "$options": "i"}})


def searchByCode(codigo):
    return collection.find_one({"codigo": codigo})


def updateProduto(produto):
    collection.update_one({'codigo': produto.codigo}, {"$set": {produto}})

def updatePreco(codigo, preco):
    collection.update_one({'codigo':codigo}, {"$set":{'preco':preco}})


def updateQuant(codigo, quantidade):
    try:
        collection.update_one({"codigo": codigo}, {
                              "$inc": {"quantidade": quantidade}}, True)
        return "atualizado"
    except:
        return "erro"
