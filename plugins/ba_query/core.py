from typing import List
from .utils.request_cache import RequestCache

# same as ListTopData but a little bit different at labelInfo
class ListByLastRankData:
    rank: int
    bestRankingPoint: int
    hard: str
    battleTime: str


global_header = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",   
    "connection": "keep-alive",
    "host": "api.arona.icu",
    "origin": "https://arona.icu",
    "referer": "https://arona.icu",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

def get_query_url(server: int, season: int):
    '''
    pure
    '''
    return [
        f"https://api.arona.icu/api/rank/list_top?server={server}&season={season}",
        f"https://api.arona.icu/api/rank/list_by_last_rank?server={server}&season={season}"
    ]

def resolve_list_top(res: List[dict]):
    '''
    pure
    '''
    s = '各档最低分数线如下:\n'
    for i in range(len(res)):
        s += f'{i + 1}档 难度: {res[i]["hard"]} 分数线: {res[i]["bestRankingPoint"]} 用时: {res[i]["battleTime"]}\n'
    return s

def resolve_list_by_last_rank(res: List[dict]):
    '''
    pure
    '''
    s = '各难度最低排名如下:\n'
    for i in range(len(res)):
        s += f'{res[i]["hard"]} 难度最低排名: {res[i]["rank"]} 分数线: {res[i]["bestRankingPoint"]}\n'
    return s

def resolve_season(res: dict):
    '''
    pure
    '''
    return f'{res["season"]} - {res["boss"]}\n'

# season cache don't need to update too often
season_cache = RequestCache("https://api.arona.icu/api/season/list", 114514)

def get_lastest_season():
    global season_cache
    return season_cache.get_response()["data"][0]

request_cache_map = {}
def get_url_response(url):
    if url not in request_cache_map:
        request_cache_map[url] = RequestCache(url)
    return request_cache_map[url].get_response()

def main(is_bili: int):
    urls = get_query_url(is_bili, get_lastest_season()["season"])
    list_top = resolve_list_top(get_url_response(urls[0])["data"])
    list_by_last_rank = resolve_list_by_last_rank(get_url_response(urls[1])["data"])

    return f'当前赛季:{resolve_season(get_lastest_season())}查询服务器：{"官服" if is_bili == 1 else "b服"}\n\n{list_top}\n{list_by_last_rank}'

# print(main(2))
