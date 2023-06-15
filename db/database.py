from pymongo import MongoClient

cluster = MongoClient('mongodb://localhost:27017')
db = cluster['projetoIntegrador']
collection = db['produtos']


def createProduct(produto):
    collection.insert_one(produto.__dict__)


def readAll():
    return collection.find({})


def searchByName(nome):
    return collection.find({"nome": nome})


def searchByCode(codigo):
    return collection.find_one({"codigo": codigo})


def updateProduto(produto):
    collection.update_one({'codigo': produto.codigo}, {"$set": {produto}})


def updateQuant(codigo, quantidade):
    try:
        collection.update_one({"codigo": codigo}, {
                              "$inc": {"quantidade": quantidade}}, True)
        return "atualizado"
    except:
        return "erro"
