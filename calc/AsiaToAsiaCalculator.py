from db.utils import DatabaseForAsiaToAsia
from db.utils import save_data_for_hedge


class AsiaToAsia:
    @staticmethod
    def __check_data_():
        """
        通过数据库支持，提取所需的亚盘数据，进行清洗匹配，
        将结果存为字典并返回
        """
        # 亚盘数据的列表
        asia_odds_list = DatabaseForAsiaToAsia.search_asia_odds_list()

        # 去重后的亚盘event_id
        id_list = DatabaseForAsiaToAsia.distinct_id()

        # 创建一个字典，以event_id为键，值为列表，将event_id相同的条目进行归类
        asia_odds_dict = {i: [] for i in id_list}

        # 同类的条目存入对应的列表中，在进行计算的时候能有效避免使用暴力解法造成效率低下
        for odds in asia_odds_list:
            asia_odds_dict[odds['event_id']].append(odds)

        return asia_odds_dict

    @classmethod
    def __search_and_calculate(cls):
        """
        通过数据库支持查询并计算数据，将结果整合为元组并存入临时的列表中并返回这个列表。
        """
        # 最终结果元组的存放列表
        save_to_database_list = []

        asia_odds_dict = cls.__check_data_()
        for event_id in asia_odds_dict.keys():
            for odds_1 in asia_odds_dict[event_id]:
                for odds_2 in asia_odds_dict[event_id]:
                    if odds_1 != odds_2 and odds_1['handicap'] == odds_2['handicap']:
                        pending_a = 10000
                        pending_b = pending_a * odds_1['odd_1'] / odds_2['odd_2']
                        s = pending_a + pending_b
                        gain = (pending_a * (odds_1['odd_1']) + pending_b * (odds_2['odd_2'])) / 2 - s
                        if gain > -3000 and (odds_1['dealer'] != odds_2['dealer']):
                            save_to_database_list.append((
                                odds_1['sports'], odds_1['league'], odds_1['event'], odds_2['event_en'],
                                odds_1['event_en'], odds_1['start_time'], odds_1['dealer'], odds_2['dealer'],
                                odds_1['dealer'], odds_1['handicap'], odds_2['handicap'], odds_1['handicap'],
                                odds_1['odd_1'], odds_2['odd_2'], odds_1['odd_draw'],
                                pending_a, pending_b, 0, gain))

        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__search_and_calculate()
        save_data_for_hedge(save_to_database_list)
