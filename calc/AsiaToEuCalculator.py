import numpy
from db.utils import DatabaseForAsiaToEu, save_data_for_hedge


class AsiaToEu:
    """亚to欧计算程序"""
    @staticmethod
    def __matrix_calculate(odd_1, odd_draw, handicap, odd_2, pending_all):
        """矩阵计算，原理不懂(o_O)"""
        analyze_no = (handicap * 100) % 100  # 盘口解析值为盘口数值乘以100除以100之后的余数，取整数
        if analyze_no == 75:
            fix_no = 0.5 + 0 * odd_2
        elif analyze_no == 0:
            fix_no = 1 + 0 * odd_2
        elif analyze_no == 25:
            fix_no = 0.5 + 0.5 * odd_2
        elif analyze_no == 50:
            fix_no = 0 + 0 * odd_2
        else:
            fix_no = 0

        a = numpy.array([[1, 1, 0], [odd_1, 0, -odd_2],
                         [0, odd_draw, fix_no - odd_2]])
        b = numpy.array([[pending_all], [0], [0]])
        result = numpy.linalg.inv(a).dot(b)
        pending_a = float(result[0][0])
        pending_b = float(result[1][0])
        pending_c = float(result[2][0])
        result = {
            'pending_a': pending_a,
            'pending_b': pending_b,
            'pending_c': pending_c,
            'fix_no': fix_no}
        return result

    @staticmethod
    def __gain_calculate(result, odd_1, odd_draw, odd_2, pending_all):
        """最后的gain值计算"""
        gain_1 = odd_1 * result['pending_a'] - pending_all
        gain_2 = odd_2 * result['pending_b'] - pending_all
        gain_draw = odd_draw * result['pending_c'] + result['pending_a'] * result['fix_no'] - pending_all
        if int(gain_1) == int(gain_2) == int(gain_draw):
            return int(gain_1)
        return None

    @staticmethod
    def __check_data():
        """从数据库支持中提取需要的数据"""
        # 去重后的event_id列表
        # all_id_list = DatabaseForAsiaToEu.distinct_id_all()

        # 去重后的欧赔event_id列表
        eu_id_list = DatabaseForAsiaToEu.distinct_id_eu()

        # 需要的odds表中的数据
        odds_list = DatabaseForAsiaToEu.search_odds_list()

        # 创建以event_id为键的字典，值为同event_id的条目，进行数据归类
        # 避免暴力解造成效率低下
        odds_dict = {i: [] for i in eu_id_list}

        # 以欧赔的event_id为键进行索引，排除多余的数据，避免计算时多余的循环
        for odds in odds_list:
            try:
                odds_dict[odds['event_id']].append(odds)
            except KeyError:
                continue

        return odds_dict

    @classmethod
    def __search_and_calculate(cls):
        """提取数据并进行计算和返回"""
        pending_all = 10000
        odds_dict = cls.__check_data()
        save_to_database_list = []
        for event_id in odds_dict.keys():
            for odds_1 in odds_dict[event_id]:
                for odds_2 in odds_dict[event_id]:
                    if odds_1['dealer'] != odds_2['dealer']:
                        odd_1 = odds_1['odd_1'] + 1  # 非平竞彩赔率
                        odd_draw = odds_1['odd_draw'] + 1  # 平竞彩赔率
                        # 矩阵计算模块必须保证欧赔在前
                        # 否则亚盘的odd_draw=888会参与计算，影响结果
                        if odd_draw == 888:
                            continue
                        handicap = odds_2['handicap']  # 盘口数值
                        odd_2 = odds_2['odd_2'] + 1  # 亚盘对应盘口赔率
                        result = cls.__matrix_calculate(odd_1, odd_draw, handicap, odd_2, pending_all)
                        gain = cls.__gain_calculate(result, odd_1, odd_draw, odd_2, pending_all)
                        if gain is None:
                            continue
                        if gain > -3000 and (
                                result['pending_a'] > 0 and result['pending_b'] > 0 and result['pending_c'] > 0):
                            save_to_database_list.append((
                                0, odds_1['sports'], odds_1['league'], odds_1['event'], odds_2['event_en'],
                                odds_1['event_en'], odds_1['start_time'], odds_1['dealer'], odds_2['dealer'],
                                odds_1['dealer'], odds_1['handicap'], odds_2['handicap'], odds_1['handicap'],
                                odds_1['odd_1'], odds_2['odd_2'], odds_1['odd_draw'], result['pending_a'],
                                result['pending_b'], result['pending_c'], gain))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__search_and_calculate()
        save_data_for_hedge(save_to_database_list)


if __name__ == '__main__':
    AsiaToEu.save_data_to_database()
