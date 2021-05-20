from datetime import datetime
from Database import DataBase


def generate_log_from_search_engine(filters: dict):
    """
    A função recebe os itens pesquisados e registra no log de buscas
    :param filters: itens pesquisados pelo usuário
    :return: True
    """
    search = filters.copy()
    search["created_at"] = datetime.now()

    execute = DataBase.Database().search_history.insert_one(search)
    if execute.inserted_id:
        return True


