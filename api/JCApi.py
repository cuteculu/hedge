import json
from datetime import datetime
from setting.settings import BASE_DIR
from db.utils import save_data_for_odds, DatabaseForJCConvert, save_data_for_jc_to_asia


class JC:
    @staticmethod
    def __read_odds_id_from_local():
        """
        读取本地保存的数据json文件，从中提取id所对应的比赛matchId。
        竞彩的json中id是字符类型，通过这个字符id匹配到通用matchId。
        以字符id为键，matchId为值构造字典并返回。
        """
        char_id_to_match_id = dict()
        with open(BASE_DIR + "竞彩名称.json", encoding="utf8") as m:
            char_id_list = json.loads(m.read(), encoding="utf8")
            for char_id in char_id_list['list'][0]['jczq']:
                char_id_to_match_id[char_id['id']] = char_id['matchId']
        return char_id_to_match_id

    @staticmethod
    def __read_odds_rate_from_local():
        """
        读取本地保存的数据json文件，从中提取id所对应的比赛赔率，
        返回列表，列表中对象为字典。
        """
        with open(BASE_DIR + "竞彩赔率.json", encoding="utf8") as p:
            char_id_list = json.loads(p.read(), encoding="utf8")['list']
        return char_id_list

    @classmethod
    def __extract_data(cls):
        """
        遍历比赛赔率列表，以字符id进行匹配，提取对应的通用matchId，
        与数据库字段进行对应处理，将所有结果保存为列表，其中每一条结果为元组。
        """
        # 待存入数据库的元组临时存储列表
        save_to_database_list = []

        # char_id_list为比赛的所有赔率列表
        char_id_list = cls.__read_odds_rate_from_local()

        # char_id_to_match_id为字符id所对应的matchId字典
        char_id_to_match_id = cls.__read_odds_id_from_local()

        for char_id in char_id_list:
            # 飞鲸数据中竞彩的赔率0盘和其他盘在同一条json字典中，需要两次提取。
            # 有些数据的字符id不在字典中，不是所需要的数据，跳过处理。
            try:
                match_id = char_id_to_match_id[char_id['id']]
            except KeyError:
                continue
            save_to_database_list.append((0, char_id['home'] + ' vs ' + char_id['away'], ' ',
                                          match_id, '竞彩', char_id['rqspf']['rq3'], char_id['rqspf']['rq0'],
                                          char_id['rqspf']['rq1'], 0,
                                          char_id['matchTime'], datetime.now(),
                                          char_id['rqspf']['goal'], "足球", char_id['league']))
            save_to_database_list.append((0, char_id['home'] + ' vs ' + char_id['away'], ' ',
                                          match_id, '竞彩', char_id['spf']['spf3'], char_id['spf']['spf0'],
                                          char_id['spf']['spf1'], 0,
                                          char_id['matchTime'], datetime.now(), 0, "足球", char_id['league']))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__extract_data()
        save_data_for_odds(save_to_database_list)


class JCConvert:
    # 竞彩转换亚盘
    @staticmethod
    def __jc_convert():
        event_id_list = DatabaseForJCConvert.distinct_id()
        save_to_database_list = []
        for event_id in event_id_list:
            results = DatabaseForJCConvert.search_data_from_id(event_id['event_id'])
            try:
                data_1 = results[1]
                data_2 = results[0]
            except IndexError:
                continue
            if data_2['handicap'] == 1.0:
                # 0盘
                odd_1 = round(data_1['odd_1'] - ((24 * data_1['odd_1']) / (25 * data_2['odd_1'])) - 0.04, 3)
                odd_2 = round(data_1['odd_2'] - ((24 * data_1['odd_2']) / (25 * data_1['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0, "足球", data_1['league']))

                # -0.25盘
                odd_1 = round(
                    ((2 * data_1['odd_1'] * data_2['odd_1']) - (data_2['odd_1'] / 25) - (49 * data_1['odd_1']) / 25) / (
                            data_1['odd_1'] + data_2['odd_1'])
                    , 3)
                odd_2 = round(
                    data_1['odd_2'] - ((24 * data_1['odd_2']) / (25 * data_1['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -0.25, "足球", data_1['league']))
                # -0.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round(data_1['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -0.5, "足球", data_1['league']))
                # -0.75盘
                odd_1 = round(
                    data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    ((2 * data_1['odd_2'] * data_2['odd_2']) - (data_1['odd_2'] / 25) - (49 * data_2['odd_2'] / 25)) / (
                            data_1['odd_2'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -0.75, "足球", data_1['league']))

                # -1盘
                odd_1 = round(
                    data_2['odd_1'] - (24 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    data_2['odd_2'] - (24 * data_2['odd_2']) / (25 * data_1['odd_2']) - 0.04, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -1, "足球", data_1['league']))

                # -1.25盘
                odd_1 = round(
                    ((2 * data_2['odd_1'] * data_2['odd_draw']) - (49 * data_2['odd_1'] / 25) - (
                            2 * data_2['odd_draw'])) / (data_2['odd_1'] + (2 * data_2['odd_draw']))
                    , 3)
                odd_2 = round(
                    data_2['odd_2'] - (12 * data_2['odd_2']) / (25 * data_1['odd_2']) - 0.52, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -1.25, "足球", data_1['league']))

                # -1.5盘
                odd_1 = round(
                    (data_2['odd_1'] * data_2['odd_draw']) / (data_2['odd_1'] + data_2['odd_draw']) - 1
                    , 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -1.5, "足球", data_1['league']))

                # 0.25盘
                odd_1 = round(
                    ((4 * data_1['odd_2'] * data_2['odd_2']) - data_2['odd_2'] - (3 * data_1['odd_2'])) / (
                            data_2['odd_2'] + 3 * data_1['odd_2']), 3)
                odd_2 = round(
                    ((4 * data_1['odd_1'] * data_2['odd_1']) - data_1['odd_1'] - 3 * data_2['odd_1']) / (
                            data_1['odd_1'] + 3 * data_2['odd_1']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0.25, "足球", data_1['league']))

            elif data_2['handicap'] == -1.0:
                # 0盘
                odd_1 = round(data_1['odd_1'] - ((24 * data_1['odd_1']) / (25 * data_1['odd_draw'])) - 1, 3)
                odd_2 = round(data_1['odd_2'] - ((24 * data_1['odd_2']) / (25 * data_2['odd_2'])) - 0.04, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0, "足球", data_1['league']))

                # 0.25盘
                odd_1 = round(data_1['odd_1'] - ((12 * data_1['odd_1']) / (25 * data_1['odd_draw'])) - 1, 3)
                odd_2 = round(
                    ((2 * data_1['odd_2'] * data_2['odd_2']) - (data_2['odd_2'] / 25) - (49 * data_1['odd_2'] / 25)) / (
                            data_1['odd_2'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0.25, "足球", data_1['league']))

                # 0.5盘
                odd_1 = round(data_1['odd_1'] - 1, 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0.5, "足球", data_1['league']))

                # 0.75盘
                odd_1 = round(
                    ((2 * data_1['odd_1'] * data_2['odd_1']) - (data_1['odd_1'] / 25) - (49 * data_2['odd_1'] / 25)) / (
                            data_1['odd_1'] + data_2['odd_1']), 3)
                odd_2 = round(data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 0.75, "足球", data_1['league']))

                # 1.0盘
                odd_1 = round(data_2['odd_1'] - ((24 * data_2['odd_1']) / (25 * data_1['odd_1'])) - 0.04, 3)
                odd_2 = round(data_2['odd_2'] - ((24 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 1.0, "足球", data_1['league']))

                # 1.25盘
                odd_1 = round(data_2['odd_1'] - ((12 * data_2['odd_1']) / (25 * data_1['odd_1'])) - 0.52, 3)
                odd_2 = round(((2 * data_2['odd_draw'] * data_2['odd_2']) - ((49 * data_2['odd_2']) / 25) - (
                        2 * data_2['odd_draw'])) / (2 * data_2['odd_draw'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 1.25, "足球", data_1['league']))

                # 1.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round((data_2['odd_draw'] * data_2['odd_2']) / (data_2['odd_draw'] + data_2['odd_2']) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 1.5, "足球", data_1['league']))

                # -0.25盘
                odd_1 = round(
                    ((4 * data_1['odd_1'] * data_2['odd_1']) - (3 * data_1['odd_1']) - data_2['odd_1']) / (
                            3 * data_1['odd_1'] + data_2['odd_1']), 3)
                odd_2 = round((4 * data_1['odd_2'] * data_2['odd_2'] - data_1['odd_2'] - 3 * data_2['odd_2']) / (
                        data_1['odd_2'] + 3 * data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -0.25, "足球", data_1['league']))

            elif data_2['handicap'] == 2.0:
                # -1.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round((data_2['odd_draw'] * data_2['odd_2']) / (data_2['odd_draw'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -1.5, "足球", data_1['league']))

                # -1.75盘
                odd_1 = round(data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    ((1200 * data_2['odd_draw'] * data_2['odd_2'] - 1200 * data_2['odd_draw'] - 1176 * data_2[
                        'odd_2']) / 25) / (48 * data_2['odd_draw'] + 24 * data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -1.75, "足球", data_1['league']))

                # -2.0盘
                odd_1 = round(data_2['odd_1'] - (24 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    data_2['odd_2'] - ((24 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -2.0, "足球", data_1['league']))

                # -2.25盘
                odd_1 = round(data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -2.25, "足球", data_1['league']))

                # -2.5盘
                odd_1 = round((data_2['odd_1'] * data_2['odd_draw']) / (data_2['odd_1'] + data_2['odd_draw']), 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -2.5, "足球", data_1['league']))

            elif data_2['handicap'] == 3.0:
                # -2.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round((data_2['odd_draw'] * data_2['odd_2']) / (data_2['odd_draw'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -2.5, "足球", data_1['league']))

                # -2.75盘
                odd_1 = round(data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    ((1200 * data_2['odd_draw'] * data_2['odd_2'] - 1200 * data_2['odd_draw'] - 1176 * data_2[
                        'odd_2']) / 25) / (48 * data_2['odd_draw'] + 24 * data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -2.75, "足球", data_1['league']))

                # -3.0盘
                odd_1 = round(data_2['odd_1'] - (24 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    data_2['odd_2'] - ((24 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -3.0, "足球", data_1['league']))

                # -3.25盘
                odd_1 = round(data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(
                    data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -3.25, "足球", data_1['league']))

                # -3.5盘
                odd_1 = round((data_2['odd_1'] * data_2['odd_draw']) / (data_2['odd_1'] + data_2['odd_draw']), 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), -3.5, "足球", data_1['league']))

            elif data_2['handicap'] == -2.0:
                # 1.5盘
                odd_1 = round((data_2['odd_1'] * data_2['odd_draw']) / (data_2['odd_1'] + data_2['odd_draw']), 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 1.5, "足球", data_1['league']))

                # 1.75盘
                odd_1 = round(
                    ((1200 * data_2['odd_1'] * data_2['odd_draw'] - 1200 * data_2['odd_draw'] - 1176 * data_2[
                        'odd_1']) / 25) / (48 * data_2['odd_draw'] + 24 * data_2['odd_1']), 3)
                odd_2 = round(data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 1.75, "足球", data_1['league']))

                # 2.0盘
                odd_1 = round(
                    data_2['odd_1'] - (24 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(data_2['odd_2'] - ((24 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 2.0, "足球", data_1['league']))

                # 2.25盘
                odd_1 = round(
                    data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 2.25, "足球", data_1['league']))

                # 2.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round((data_2['odd_draw'] * data_2['odd_2']) / (data_2['odd_draw'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 2.5, "足球", data_1['league']))

            elif data_2['handicap'] == -3.0:
                # 2.5盘
                odd_1 = round((data_2['odd_1'] * data_2['odd_draw']) / (data_2['odd_1'] + data_2['odd_draw']), 3)
                odd_2 = round(data_2['odd_2'] - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 2.5, "足球", data_1['league']))

                # 2.75盘
                odd_1 = round(
                    ((1200 * data_2['odd_1'] * data_2['odd_draw'] - 1200 * data_2['odd_draw'] - 1176 * data_2[
                        'odd_1']) / 25) / (48 * data_2['odd_draw'] + 24 * data_2['odd_1']), 3)
                odd_2 = round(data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 2.75, "足球", data_1['league']))

                # 3.0盘
                odd_1 = round(
                    data_2['odd_1'] - (24 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(data_2['odd_2'] - ((24 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 3.0, "足球", data_1['league']))

                # 3.25盘
                odd_1 = round(
                    data_2['odd_1'] - (12 * data_2['odd_1']) / (25 * data_2['odd_draw']) - 1, 3)
                odd_2 = round(data_2['odd_2'] - ((12 * data_2['odd_2']) / (25 * data_2['odd_draw'])) - 1, 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 3.25, "足球", data_1['league']))

                # 3.5盘
                odd_1 = round(data_2['odd_1'] - 1, 3)
                odd_2 = round((data_2['odd_draw'] * data_2['odd_2']) / (data_2['odd_draw'] + data_2['odd_2']), 3)
                save_to_database_list.append((0, data_1['event'], ' ', event_id['event_id'], '竞彩',
                                              odd_1, odd_2, 888, 0,
                                              data_1['start_time'], datetime.now(), 3.5, "足球", data_1['league']))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__jc_convert()
        save_data_for_jc_to_asia(save_to_database_list)
