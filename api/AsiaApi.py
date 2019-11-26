import json
from datetime import datetime
from setting.settings import BASE_DIR
from db.utils import save_data_for_odds


class Asia:
    # dealer名称映射
    dealer_dict = {
        1: '澳门', 3: 'ＳＢ/皇冠', 4: '立博', 7: 'SNAI', 8: 'Bet365', 9: '威廉希尔', 12: '易胜博', 14: '韦德',
        17: '明陞', 19: 'Interwette', 22: '10BET', 23: '金宝博', 24: '12bet/沙巴', 31: '利记', 35: '盈禾',
        42: '18bet', 47: '平博', 48: '香港马会'}

    @staticmethod
    def __read_name_from_local():
        """
        亚盘赔率的请求结果中不含主客队名称，需要以matchId进行名称匹配
        :return:以matchId为键，值为以主客队以及联赛名称和比赛时间组成的字典
        """
        name_for_match_id = dict()
        with open(BASE_DIR + "亚盘单盘口带名称赔率.json", encoding="utf8") as m:
            name_list = json.loads(m.read(), encoding="utf8")['list'][0]['match']
            for name in name_list:
                name_for_match_id[name['matchId']] = {
                    'leagueEn': name['leagueEn'],
                    'homeEn': name['homeEn'],
                    'homeChs': name['homeChs'],
                    'awayEn': name['awayEn'],
                    'awayChs': name['awayChs'],
                    'matchTime': name['matchTime']}
        return name_for_match_id

    @staticmethod
    def __read_rate_from_local():
        """从本地亚盘赔率json中提取所有数据"""
        with open(BASE_DIR + "亚盘多盘口不带名称赔率.json", encoding="utf8") as p:
            asia_rate_list = json.loads(p.read(), encoding="utf8")['List'][0]['handicap']
        return asia_rate_list

    @classmethod
    def __extract_data(cls):
        """
        综合name和rate提取出来的数据，组合成数据库需要的对应字段内容，
        整合为一个元组并存入一个列表，返回值为这个列表。
        """
        # 待保存到数据库的元组的临时存放列表
        save_to_database_list = []

        # asia_rate_list为赔率数据的列表
        asia_rate_list = cls.__read_rate_from_local()

        # matchId所对应的各名称字典映射
        name_for_match_id = cls.__read_name_from_local()
        for data in asia_rate_list:
            # 赔率表的matchId不一定在名称映射字典中全部都有，需要进行判断
            try:
                match_name = {
                    "homeEn": name_for_match_id[data[0]]['homeEn'],
                    "homeChs": name_for_match_id[data[0]]['homeChs'],
                    "awayEn": name_for_match_id[data[0]]['awayEn'],
                    "awayChs": name_for_match_id[data[0]]['awayChs'],
                    "leagueEn": name_for_match_id[data[0]]['leagueEn'],
                    "matchTime": name_for_match_id[data[0]]["matchTime"]
                }
            except KeyError:
                continue
            save_to_database_list.append((0, match_name['homeChs'] + ' vs ' + match_name['awayChs'],
                                          match_name['homeEn'] + ' vs ' + match_name['awayEn'], data[0],
                                          cls.dealer_dict[data[1]],
                                          data[6], data[7], 888, 0,
                                          match_name['matchTime'], datetime.now(), data[5],
                                          "足球", match_name['leagueEn']))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__extract_data()
        save_data_for_odds(save_to_database_list)
