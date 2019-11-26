from db.utils import DatabaseForOnBet, save_data_for_on_bet


class OnBetCalculator:
    @classmethod
    def __search_and_calculator(cls):
        save_to_database_list = []
        for event_id in DatabaseForOnBet.distinct_id():
            jc_asia_list = DatabaseForOnBet.search_data_from_jc_to_asia(event_id)
            odds_list = DatabaseForOnBet.search_data_from_odds(event_id)
            for jc_asia in jc_asia_list:
                for odds in odds_list:
                    if jc_asia['handicap'] == odds['handicap']:
                        balance1 = 0.92 / jc_asia['odd_1']
                        balance2 = 0.92 / jc_asia['odd_2']
                        diff_1 = balance1 - jc_asia['odd_2']
                        diff_2 = balance2 - jc_asia['odd_1']
                        save_to_database_list.append(
                            (0, '足球', odds['league'], odds['event'], odds['event_en'], ' ', jc_asia['event_id'],
                             odds['start_time'], odds['dealer'],
                             '竞彩转亚', '', odds['handicap'], jc_asia['handicap'], 0, odds['odd_1'],
                             jc_asia['odd_2'], 0, 0, 0, 0, 0, diff_1, diff_2, balance1, balance2, 0))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__search_and_calculator()
        save_data_for_on_bet(save_to_database_list)
