import asyncio
from os import getenv
from BotDatasoccer import BotDatasoccer


def statistics_banner(**kwargs)-> None:
    """
    Exibe um painel com as quantidades de itens
    :return:
    """
    print()
    print("-" * 4 + " STATISTICS" + "-" * 4)
    print(f"Teams: {kwargs['team']} ")
    print(f"Players: {kwargs['players']}")
    print(f"League: {kwargs['league']}")
    print(f"Matches: {kwargs['matches']}")
    print("----" * 4)


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
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(data_soccer.apiGetMatches())


def execute_this() -> None:
    """
    Cria arquivo geral para inserção direta
    :return:
    """
    teams: list[str]
    players: list[str]
    matches: list[str]
    champ: list[str]
    with open("../teams_insert.txt", "r") as read1:
        teams = read1.readlines()
    with open("../players_insert.txt", "r") as read2:
        players = read2.readlines()
    with open("../league_insert.txt", "r") as read3:
        champ = read3.readlines()
    with open("../matches_insert.txt", "r") as read4:
        matches = read4.readlines()
    statistics_banner(team=len(teams), players=len(players), league=len(champ), matches=len(matches))
    with open("insert_into.txt", "a") as wr:
        for team in teams:
            wr.writelines(team + "\n")
        for player in players:
            wr.writelines(player + "\n")
        for ch in champ:
            wr.writelines(ch + "\n")
        for match in matches:
            wr.writelines(match + "\n")


def main() -> None:
    print("[+] BOT DATASOCCER")
    print("[+] INICIANDO INSERÇÕES NO BANCO DE DADOS")
    start_with_teams_and_players()
    cp()
    matches()
    execute_this()


if __name__ == '__main__':
    main()
