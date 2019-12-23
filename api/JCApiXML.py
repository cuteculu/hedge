import collections
import xmltodict
import requests
from datetime import datetime
from db.utils import save_data_for_odds, DatabaseForJCConvert, save_data_for_jc_to_asia, EVENT_DICT
from setting import settings


class JC:
    @staticmethod
    def __read_odds_id_from_xml():
        """
        获取并解析xml文件
        """
        response = requests.get('http://interface.win007.com/zq/JcZqOdds.aspx').content.decode('utf8')
        tree = xmltodict.parse(response)['list']['match']
        # with open(BASE_DIR + 'JcZqOdds_aspx.xml', 'r', encoding='utf8') as f:
        #     tree = xmltodict.parse(f.read())['list']['match']
        # 如果tree只有一条数据，类型就不是list，会导致后面遍历出错
        if isinstance(tree, collections.OrderedDict):
            tree = [tree]
        return tree

    @classmethod
    def __extract_data(cls):
        """
        遍历比赛赔率列表，以字符id进行匹配，提取对应的通用matchId，
        与数据库字段进行对应处理，将所有结果保存为列表，其中每一条结果为元组。
        """
        # 待存入数据库的元组临时存储列表
        save_to_database_list = []

        char_id_list = cls.__read_odds_id_from_xml()

        for char_id in char_id_list:
            # 飞鲸数据中竞彩的赔率0盘和其他盘在同一条json字典中，需要两次提取。
            try:
                event = EVENT_DICT[char_id['Home']] + ' vs ' + EVENT_DICT[char_id['Away']]
            except KeyError:
                continue
            if event not in settings.EVENT_ID_DICT:
                settings.EVENT_ID_DICT[event] = settings.EVENT_ID
                settings.EVENT_ID += 1
            match_id = settings.EVENT_ID_DICT[event]
            if char_id['rq']['stop'] == 'False':
                save_to_database_list.append((0, event, ' ',
                                              match_id, '竞彩', char_id['rq']['rq3'], char_id['rq']['rq0'],
                                              char_id['rq']['rq1'], 0,
                                              char_id['MatchTime'], datetime.now(),
                                              char_id['rq']['goal'], "足球", char_id['league']))
            if char_id['sf']['stop'] == 'False':
                save_to_database_list.append((0, event, ' ',
                                              match_id, '竞彩', char_id['sf']['sf3'], char_id['sf']['sf0'],
                                              char_id['sf']['sf1'], 0,
                                              char_id['MatchTime'], datetime.now(), 0, "足球", char_id['league']))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__extract_data()
        save_data_for_odds(save_to_database_list)


class JCConvert:
    """竞彩转换亚盘"""

    @staticmethod
    def __jc_single_convert(result):
        """
        竞彩单条数据转亚盘
        :param result:dict，event_id对应的单条数据
        :return: list，元素为转换完成后的数据库字段对应结果组成的tuple
        """
        # 返回结果列表
        save_to_database_list = []
        if result['handicap'] == -1.0:
            # 1.5盘
            odd_1 = round(result['odd_1'] - 1, 3)
            odd_2 = round((result['odd_draw'] * result['odd_2']) / (result['odd_draw'] + result['odd_2']) - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩', odd_1,
                                          odd_2, 888, 0, result['start_time'], datetime.now(), 1.5,
                                          "足球", result['league']))
        elif result['handicap'] == 1.0:
            # -1.5盘
            odd_1 = round(
                (result['odd_1'] * result['odd_draw']) / (result['odd_1'] + result['odd_draw']) - 1
                , 3)
            odd_2 = round(result['odd_2'] - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩', odd_1,
                                          odd_2, 888, 0, result['start_time'], datetime.now(), -1.5,
                                          "足球", result['league']))
        elif result['handicap'] == -2.0:
            # 1.5盘
            odd_1 = round((result['odd_1'] * result['odd_draw']) / (result['odd_1'] + result['odd_draw']), 3)
            odd_2 = round(result['odd_2'] - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩', odd_1,
                                          odd_2, 888, 0, result['start_time'], datetime.now(), 1.5,
                                          "足球", result['league']))
            # 1.75盘
            odd_1 = round(
                ((1200 * result['odd_1'] * result['odd_draw'] - 1200 * result['odd_draw'] - 1176 * result[
                    'odd_1']) / 25) / (48 * result['odd_draw'] + 24 * result['odd_1']), 3)
            odd_2 = round(result['odd_2'] - ((12 * result['odd_2']) / (25 * result['odd_draw'])) - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩', odd_1,
                                          odd_2, 888, 0, result['start_time'], datetime.now(), 1.75,
                                          "足球", result['league']))
        elif result['handicap'] == -3.0:
            # 2.5盘
            odd_1 = round((result['odd_1'] * result['odd_draw']) / (result['odd_1'] + result['odd_draw']), 3)
            odd_2 = round(result['odd_2'] - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩',
                                          odd_1, odd_2, 888, 0,
                                          result['start_time'], datetime.now(), 2.5, "足球", result['league']))

            # 2.75盘
            odd_1 = round(
                ((1200 * result['odd_1'] * result['odd_draw'] - 1200 * result['odd_draw'] - 1176 * result[
                    'odd_1']) / 25) / (48 * result['odd_draw'] + 24 * result['odd_1']), 3)
            odd_2 = round(result['odd_2'] - ((12 * result['odd_2']) / (25 * result['odd_draw'])) - 1, 3)
            save_to_database_list.append((0, result['event'], ' ', result['event_id'], '竞彩',
                                          odd_1, odd_2, 888, 0,
                                          result['start_time'], datetime.now(), 2.75, "足球", result['league']))
        return save_to_database_list

    @classmethod
    def __jc_convert(cls):
        """竞彩转亚，两条数据转换"""
        event_id_list = DatabaseForJCConvert.distinct_id()
        save_to_database_list = []
        for event_id in event_id_list:
            results = DatabaseForJCConvert.search_data_from_id(event_id['event_id'])
            try:
                data_1 = results[1]
                data_2 = results[0]
            except IndexError:
                # 如果results中没有两条数据，说明此event_id对应只有单条数据
                # 传入单条转换方法中进行转换并返回结果
                save_to_database_list.extend(cls.__jc_single_convert(results[0]))
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


if __name__ == '__main__':
    JC.save_data_to_database()
    JCConvert.save_data_to_database()
