import asyncio
from os import getenv
from BotDatasoccer import BotDatasoccer


def start_with_teams_and_players() -> None:
    """
    Inicia as que tabelas que possuem
    nenhuma dependencia ou poucas (foreign keys)
    :return:
    """
    data_soccer = BotDatasoccer(
        host=getenv("host"),
        user=getenv("user"),
        password=getenv("password"),
        database=getenv("database")
    )
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # frirula para rodar no windows
    asyncio.run(data_soccer.apiGetTeam())
    asyncio.run(data_soccer.apiGetPlayers())


def cp() -> None:
    """
    faz a insercao em campeonato
    :return:
    """
    data_soccer = BotDatasoccer(
        host=getenv("host"),
        user=getenv("user"),
        password=getenv("password"),
        database=getenv("database")
    )
    asyncio.run(data_soccer.apiGetCamp())


def matches() -> None:
    """
    Executa tabela de disputas
    :return:
    """
    data_soccer = BotDatasoccer(
        host=getenv("host"),
        user=getenv("user"),
        password=getenv("password"),
        database=getenv("database")
    )
    asyncio.run(data_soccer.apiGetMatches())


if __name__ == '__main__':
    print("[+] BOT DATASOCCER")
    print("[+] INICIANDO INSERÇÕES NO BANCO DE DADOS")
    start_with_teams_and_players()
    cp()
    matches()
