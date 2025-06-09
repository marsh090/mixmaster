from django import template
from bson import ObjectId

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário para uma chave específica.
    Se a chave for '_id', converte o valor para string.
    """
    value = dictionary.get(key)
    if key == '_id' and isinstance(value, ObjectId):
        return str(value)
    return value

@register.filter
def format_list(value):
    """
    Formata uma lista como uma string separada por vírgulas.
    """
    if isinstance(value, list):
        return ', '.join(str(item) for item in value)
    return value

@register.filter
def format_dict(value):
    """
    Formata um dicionário como uma string legível.
    """
    if isinstance(value, dict):
        return ', '.join(f'{k}: {v}' for k, v in value.items())
    return value 