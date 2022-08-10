import asyncio
import json
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
    def __init__(self, user: str = None, host: str = None, password: str = None, database: str = None) -> None:
        """
        Passe os parametros ou alimente o arquivo .env
        :param user:
        :param host:
        :param password:
        """
        if user is None or host is None or password is None:
            self.__user: str = getenv("user")
            self.__host: str = getenv("host")
            self.__password: str = getenv("password")
            self.__database: str = getenv("database")
        else:
            self.__user: str = user
            self.__host: str = host
            self.__password: str = password
            self.__database: str = database

    @property
    def user(self) -> str: return self.__user

    @property
    def host(self) -> str: return self.__host

    @property
    def password(self) -> str: return self.__password

    @contextmanager
    def connectMySQL(self) -> None:
        """
        Conecta ao banco de dados, retornando
        um generator para enconomizar memoria
        :return:
        """
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=getenv("database")
        )
        try:
            cursor = connection.cursor()
            yield cursor
        except Exception:
            ...
        finally:
            connection.commit()
            connection.close()
    @staticmethod
    async def apiGetPlayers() -> None:
        """
        faz o get da api jogadores
        :return:
        """
        endpoint: str = "league-players?key="
        season_id: str = "&season_id=2012&max_per_page=899"
        url: str = str(getenv("api") + endpoint + getenv("key") + season_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    for data in json.loads(resp)['data']:
                        sql: str = "INSERT INTO Jogador(id_jogador, nome,idade, assistencias,gols,cartoes_amarelos,"
                        sql += "cartoes_vermelhos, nacionalidade,penaltis_defendidos, posicao, clube_id)"
                        sql += 'VALUES({0}, "{1}", {2}, {3}, {4}, {5}, {6}, "{7}", {8},"{9}", {10});'.format(
                                           int(data["id"]),
                                           data["full_name"],
                                           int(data['age']),
                                           int(data['assists_overall']),
                                           int(data['goals_overall']),
                                           int(data['red_cards_overall']),
                                           int(data['yellow_cards_overall']),
                                           data['nationality'],
                                           int(data['penalty_misses']),
                                           data['position'],
                                           int(data['club_team_id'])
                                           )
                        print("[+] DOWNLOAD DATA FROM API, PLEASE, WAIT")
                        with BotDatasoccer().connectMySQL() as cursor:
                            try:
                                cursor.execute(sql)
                            except Exception:
                                pass
                        print("[+] SAVE INSERT QUERYS ON FILE NOW...")
                        async with aiofiles.open('../players_insert.txt', 'a') as f:
                            try:
                                await f.writelines("\n" + sql + "\n")
                            except Exception:
                                pass
                    print(f"SALVOS {len(data)} DADOS")
                else:
                    print(f"[-]ERRO GET API PLAYERS - status code {response.status}")

    @staticmethod
    async def apiGetTeam() -> None:
        """
        faz o get da api times
        :return:
        """
        endpoint = "league-teams?key="
        final = "&season_id=2012&include=stats&max_per_page=899"
        url = str(getenv("api") + endpoint + getenv("key") + final)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    for data in json.loads(resp)['data']:
                        sql = "INSERT INTO Time(id_clube, nome,escudo)VALUES("
                        sql += '{0},"{1}","{2}");'.format(int(data['id']), data['name'], data['image'])
                        print("[+] DOWNLOAD DATA FROM API, PLEASE, WAIT")
                        with BotDatasoccer().connectMySQL() as cursor:
                            try:
                                cursor.execute(sql)
                            except Exception:
                                pass
                        print("[+] SAVE INSERT QUERYS ON FILE NOW...")
                        async with aiofiles.open('../teams_insert.txt', 'a') as f:
                            try:
                                await f.writelines(sql + "\n")
                            except Exception:
                                pass
                    print(f"SALVOS {len(data)} DADOS")
                else:
                    print(f"[-]ERRO GET API TEAMS - status code {response.status}")

    @staticmethod
    async def apiGetMatches() -> None:
        """
        faz o get da api disputa
        :return:
        """
        endpoint = "league-matches?key="
        match_id = "&season_id=2012&max_per_page=899"
        url = str(getenv("api") + endpoint + getenv("key") + match_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    data_ = json.loads(resp)["data"]
                    for data in data_:
                        sql = "INSERT INTO Disputa(id_disputa,estadio,numero_rodada,gols_mandante,gols_visitante," \
                              "cartao_vermelho_mandante, cartao_vermelho_visitante, cartao_amarelo_mandante," \
                              "cartao_amarelo_visitante,campeonato_id,clube_id_mandante,clube_id_visitante)VALUES("
                        sql += '{0},"{1}",{2},{3},{4},{5},{6},{7},{8}, {9}, {10},{11});'.format(
                            int(data["id"]),
                            data['stadium_name'],
                            int(data['game_week']),
                            int(data["ht_goals_team_a"]) + int(data["goals_2hg_team_a"]),
                            int(data["ht_goals_team_b"]) + int(data["goals_2hg_team_b"]),
                            int(data["team_a_red_cards"]), int(data["team_b_red_cards"]),
                            int(data["team_a_yellow_cards"]), int(data["team_b_yellow_cards"]),
                            2012, int(data["homeID"]), int(data["awayID"]))
                        with BotDatasoccer().connectMySQL() as cursor:
                            try:
                                cursor.execute(sql)
                            except Exception:
                                pass
                        print("[+] DOWNLOAD DATA FROM API, PLEASE, WAIT")
                        async with aiofiles.open('../matches_insert.txt', 'a') as f:
                            await f.writelines(sql + "\n")
                    print(f"SALVOS {len(data_)} DADOS")
                else:
                    print(f"[-]ERRO GET API MATCHES - status code {response.status}")

    @staticmethod
    async def apiGetCamp() -> None:
        """
        faz o get da api campeonato
        :return:
        """
        endpoint = "league-season?key="
        season_id = "&season_id=2012"
        url = str(getenv("api") + endpoint + getenv("key") + season_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    resp = await response.text()
                    data = json.loads(resp)["data"]
                    sql = "INSERT INTO Campeonato(id_campeonato, logo,pais,temporada)VALUES("
                    sql += '{0},"{1}","{2}", "{3}");'.format(
                        2012,
                        "https://cdn.footystats.org/img/competitions/england-premier-league.png",
                        data['country'],
                        str(data["starting_year"]) + "/" + str( data["ending_year"])
                    )
                    print("[+] DOWNLOAD DATA FROM API, PLEASE, WAIT")
                    with BotDatasoccer().connectMySQL() as cursor:
                        try:
                            cursor.execute(sql)
                        except Exception as e:
                            pass
                    print("[+] SAVE INSERT QUERYS ON FILE NOW...")
                    async with aiofiles.open('../league_insert.txt', 'a') as f:
                        try:
                            await f.writelines(sql + "\n")
                        except Exception:
                            pass
                    print(f"SALVOS {len(data)} DADOS")
                else:
                    print(f"[-]ERRO GET API LEAGUE LIST - status code {response.status}")
