import asyncio
import json
import threading

import aiofiles as aiofiles
import aiohttp
import mysql.connector
from dotenv import load_dotenv
from os import getenv
from contextlib import contextmanager

load_dotenv()


# tabelas: jogadores, disputa, campeonato, times


class BotDatasoccer:
    """
    Faz a requisicao para api e, com o resultado,
    faz os inserts no banco de dados
    """

    def __init__(self, user: str = None, host: str = None, password: str = None) -> None:
        self.__user: str = user
        self.__host: str = host
        self.__password: str = password

    @property
    def user(self):
        return self.__user

    @property
    def host(self):
        return self.__host

    @property
    def password(self):
        return self.__password

    @staticmethod
    async def apiGetPlayers():
        """
        faz o get da api jogadores
        :return:
        """
        endpoint = "league-players?key="
        season_id = "&season_id=2012"
        url = str(getenv("api") + endpoint + getenv("key") + season_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    count = 0
                    for data in json.loads(resp)['data']:
                        sql = "INSERT INTO Jogador(nome,idade,numero_camisa, assistencias,gols,cartoes_amarelos,"
                        sql += "cartoes_vermelhos, nacionalidade,penaltis_defendidos, posicao)"
                        sql += "VALUES('{0}', {1}, {2}, {3}, {4}, {5}, {6}, '{7}', {8},'{9}');".format(
                                           data["full_name"],
                                           int(data['age']),
                                           int(data['club_team_id']),
                                           int(data['assists_overall']),
                                           int(data['goals_overall']),
                                           int(data['red_cards_overall']),
                                           int(data['yellow_cards_overall']),
                                           data['nationality'],
                                           int(data['penalty_misses']),
                                           data['position']
                                           )
                        async with aiofiles.open('players_insert.txt', 'a') as f:
                            await f.writelines(sql + "\n")
                        if count == 1:
                            break
                        count += 1
                        print(data)
                else:
                    print(f"[-]ERRO GET API PLAYERS - status code {response.status}")

    @staticmethod
    async def apiGetTeam():
        """
        faz o get da api times
        :return:
        """
        endpoint = "league-teams?key="
        final = "&season_id=2012&include=stats"
        url = str(getenv("api") + endpoint + getenv("key") + final)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    count = 0
                    for data in json.loads(resp)['data']:
                        sql = "INSERT INTO Time(nome,escudo)VALUES("
                        sql += "'{0}','{1}');".format(data['name'], data['url'])
                        if count == 1:
                            break
                        count += 1
                        print(data)
                    async with aiofiles.open('teams_insert.txt', 'a') as f:
                        await f.writelines(sql + "\n")
                else:
                    print(f"[-]ERRO GET API TEAMS - status code {response.status}")

    @staticmethod
    async def apiGetMatches():
        """
        faz o get da api disputa
        :return:
        """
        endpoint = "league-matches?key="
        seanson_id = "&season_id=2012"
        url = str(getenv("api") + endpoint + getenv("key") + seanson_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    count = 0
                    for data in json.loads(resp)['data']:
                        sql = "INSERT INTO Disputa(estadio,numero_rodada,gols_mandante,gols_visitante," \
                              "cartao_vermelho_mandante, cartao_vermelho_visitante, cartao_amarelo_mandante," \
                              "cartao_amarelo_visitante, Disputacol)VALUES("
                        sql += "'{0}',{1},{2},{3},{4},{5},{6},{7},{8});".format(
                            data['stadium_name'], int(data['game_week']),
                            int(data["ht_goals_team_a"]) + int(data["goals_2hg_team_a"]),
                            int(data["ht_goals_team_b"]) + int(data["goals_2hg_team_b"]),
                            int(data["team_a_red_cards"]), int(data["team_b_red_cards"]),
                            int(data["team_a_yellow_cards"]), int(data["team_b_yellow_cards"]),
                            int(data["matches_completed_minimum"])  # qual o disputacol?

                        )
                        if count == 1:
                            break
                        count += 1
                        print(data)
                    async with aiofiles.open('matches_insert.txt', 'a') as f:
                        await f.writelines(sql + "\n")
                else:
                    print(f"[-]ERRO GET API MATCHES - status code {response.status}")

    @staticmethod
    async def apiGetCamp():
        """
        faz o get da api campeonato
        :return:
        """
        endpoint = "league-list?key="
        url = str(getenv("api") + endpoint + getenv("key"))
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    count = 0
                    for data in json.loads(resp)['data']:
                        sql = "INSERT INTO Campeonato(logo,pais,temporada)VALUES("
                        sql += "'{0}','{1}','{2}');".format(
                            data['name'], data['country'],  # qual o logo?
                            data["season"]
                        )
                        if count == 1:
                            break
                        count += 1
                        print(data)
                    async with aiofiles.open('league_insert.txt', 'a') as f:
                        await f.writelines(sql + "\n")
                else:
                    print(f"[-]ERRO GET API LEAGUE LIST - status code {response.status}")

    @contextmanager
    def connectMySQL(self):
        """
        Conecta ao banco de dados, retornando
        um generator para enconomizar memoria
        :return:
        """
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        try:
            yield connection.cursor()
        except Exception:
            ...
        finally:
            connection.commit()
            connection.close()


def start_threads() -> None:
    """
    Inicia threads
    para execucao das consultas a api
    e insercoes no banco
    :return:
    """
    data_soccer = BotDatasoccer(
        host=getenv("host"),
        user=getenv("user"),
        password=getenv("password")
    )

    th: list = [
        threading.Thread(target=(asyncio.run(data_soccer.apiGetPlayers()))),
        threading.Thread(target=(asyncio.run(data_soccer.apiGetMatches()))),
        threading.Thread(target=(asyncio.run(data_soccer.apiGetTeam()))),
        threading.Thread(target=(asyncio.run(data_soccer.apiGetCamp())))
    ]
    [thread.start() for thread in th]
    [thread.join() for thread in th]


if __name__ == '__main__':
    print("[+] BOT DATASOCCER")
    print("[+] INICIANDO INSERÇÕES NO BANCO DE DADOS")
    start_threads()
