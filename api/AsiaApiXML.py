import time
import requests
from datetime import datetime
from db.utils import save_data_for_odds
from db.utils import EVENT_DICT
from setting import settings


class Asia:
    # dealer名称映射
    dealer_dict = {
        '1': '澳门', '3': 'ＳＢ/皇冠', '4': '立博', '7': 'SNAI', '8': 'Bet365', '9': '威廉希尔', '12': '易胜博', '14': '韦德',
        '17': '明陞', '19': 'Interwette', '22': '10BET', '23': '金宝博', '24': '12bet/沙巴', '31': '利记', '35': '盈禾',
        '42': '18bet', '47': '平博', '48': '香港马会'}

    @staticmethod
    def __read_name_from_xml():
        """
        亚盘赔率的请求结果中不含主客队名称，需要以matchId进行名称匹配
        :return:以matchId为键，值为以主客队以及联赛名称和比赛时间组成的字典
        """
        response = requests.get('http://interface.win007.com/zq/odds.aspx').content.decode('utf8')
        results = response.split('$')[1].split(';')
        leagues = response.split('$')[0].split(';')
        leagues = {r.split(',')[0]: r.split(',')[3] for r in leagues}
        results = [r.split(',') for r in results]
        name_for_match_id = dict()
        for r in results:
            name_for_match_id[r[0]] = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r[2]) // 1000)),
                                       r[5], r[10], leagues[r[1]]]
        return name_for_match_id

    @staticmethod
    def __read_rate_from_xml():
        """从本地亚盘赔率json中提取所有数据"""
        response = requests.get('http://interface.win007.com/zq/Odds_Mult.aspx').content.decode('utf8')
        results = response.split('$')[0].split(';')
        results = [r.split(',') for r in results]
        return results

    @classmethod
    def __extract_data(cls):
        """
        综合name和rate提取出来的数据，组合成数据库需要的对应字段内容，
        整合为一个元组并存入一个列表，返回值为这个列表。
        """
        # 待保存到数据库的元组的临时存放列表
        save_to_database_list = []

        # asia_rate_list为赔率数据的列表
        asia_rate_list = cls.__read_rate_from_xml()

        # matchId所对应的各名称字典映射
        name_for_match_id = cls.__read_name_from_xml()
        for data in asia_rate_list:
            # 赔率表的matchId不一定在名称映射字典中全部都有，需要进行判断
            try:
                match_name = {
                    "homeChs": name_for_match_id[data[0]][1],
                    "awayChs": name_for_match_id[data[0]][2],
                    "leagueEn": name_for_match_id[data[0]][3],
                    "matchTime": name_for_match_id[data[0]][0]
                }
            except KeyError:
                continue
            try:
                event = EVENT_DICT[match_name['homeChs']] + ' vs ' + EVENT_DICT[match_name['awayChs']]
            except KeyError:
                continue
            if event not in settings.EVENT_ID_DICT:
                settings.EVENT_ID_DICT[event] = settings.EVENT_ID
                settings.EVENT_ID += 1
            event_id = settings.EVENT_ID_DICT[event]
            save_to_database_list.append((0, event, '', event_id, cls.dealer_dict[data[1]],
                                          data[6], data[7], 888, 0,
                                          match_name['matchTime'], datetime.now(), data[5],
                                          "足球", match_name['leagueEn']))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__extract_data()
        save_data_for_odds(save_to_database_list)


if __name__ == '__main__':
    Asia.save_data_to_database()
