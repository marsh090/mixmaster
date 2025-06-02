from django.conf import settings
from pymongo import MongoClient

# Conectar ao MongoDB Atlas usando variáveis de ambiente
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]

class MongoModel:
    """Classe base para modelos MongoDB"""
    collection_name = None

    @classmethod
    def get_collection(cls):
        return db[cls.collection_name]

    @classmethod
    def find(cls, filter=None):
        """Retorna todos os documentos que correspondem ao filtro"""
        return cls.get_collection().find(filter or {})

    @classmethod
    def find_one(cls, filter):
        """Retorna um documento que corresponde ao filtro"""
        return cls.get_collection().find_one(filter)

    @classmethod
    def insert_one(cls, document):
        """Insere um documento na coleção"""
        return cls.get_collection().insert_one(document)

    @classmethod
    def update_one(cls, filter, update):
        """Atualiza um documento na coleção"""
        return cls.get_collection().update_one(filter, update)

    @classmethod
    def delete_one(cls, filter):
        """Remove um documento da coleção"""
        return cls.get_collection().delete_one(filter)

class TipoIngrediente(MongoModel):
    """Modelo para tipos de ingrediente"""
    collection_name = 'tipos_ingrediente'

class TipoUtensilio(MongoModel):
    """Modelo para tipos de utensílio"""
    collection_name = 'tipos_utensilio'

class UnidadeMedida(MongoModel):
    """Modelo para unidades de medida"""
    collection_name = 'unidades_medida'

class PerfilSabor(MongoModel):
    """Modelo para perfis de sabor"""
    collection_name = 'perfis_sabor'

class Ingrediente(MongoModel):
    """Modelo para ingredientes"""
    collection_name = 'ingredientes'

class Utensilio(MongoModel):
    """Modelo para utensílios"""
    collection_name = 'utensilios'

class Drink(MongoModel):
    """Modelo para drinks"""
    collection_name = 'drinks'
