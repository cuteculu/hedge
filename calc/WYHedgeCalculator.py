from db.utils import DatabaseForWYHedge, save_data_for_wy_hedge


class WYHedge:
    @classmethod
    def __search_and_calculate(cls):
        """
        通过数据库支持提取数据进行计算以及结果整合。
        :return: list，元素为计算结果对应数据库的元组。
        """
        hedge_data_list = DatabaseForWYHedge.search_data_from_hedge()
        dealer_rate_dict = DatabaseForWYHedge.search_data_from_rate()

        # 返回结果
        save_to_database_list = []

        for hedge in hedge_data_list:
            try:
                gain = hedge['pending_a'] * dealer_rate_dict[hedge['dealer_1']] + \
                       hedge['pending_b'] * dealer_rate_dict[hedge['dealer_2']] + \
                       hedge['pending_c'] * dealer_rate_dict[hedge['dealer_3']] + hedge['gain']
            except KeyError:
                continue
            if gain > 0:
                hedge['id'] = 0
                hedge['gain'] = int(gain)
                save_to_database_list.append(tuple(hedge.values()))

        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__search_and_calculate()
        save_data_for_wy_hedge(save_to_database_list)


if __name__ == '__main__':
    WYHedge.save_data_to_database()
