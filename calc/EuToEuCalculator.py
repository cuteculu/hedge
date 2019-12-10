from db.utils import save_data_for_hedge
from db.utils import DatabaseForEuToEu


class EuToEu:
    """欧to欧计算程序"""

    @classmethod
    def __search_data(cls):
        odds_list = DatabaseForEuToEu.search_eu_from_odds()
        return odds_list

    @classmethod
    def __eu_calculate(cls):
        odds_list = cls.__search_data()
        save_to_database_list = []
        for odds_1 in odds_list:
            for odds_2 in odds_list:
                if odds_1['event_id'] == odds_2['event_id'] and odds_1['dealer'] != odds_2['dealer']:
                    pending_a = 10000
                    # 计算逻辑
                    # 1胜
                    pending_b = pending_a * odds_1['odd_1'] / odds_2['odd_2']
                    pending_c = pending_a * odds_1['odd_1'] / odds_2['odd_draw']
                    gain = pending_a * odds_1['odd_1'] + pending_b * odds_2['odd_2'] + pending_c * odds_2['odd_draw']
                    gain = gain / 3 - pending_a - pending_b - pending_c
                    save_to_database_list.append((
                        0, odds_1['sports'], odds_1['league'], odds_1['event'], ' ', ' ', odds_1['start_time'],
                        odds_1['dealer'], odds_2['dealer'], odds_2['dealer'], 99, 77, 88, odds_1['odd_1'],
                        odds_2['odd_2'], odds_2['odd_draw'], pending_a, pending_b, pending_c, gain
                    ))

                    # 1负
                    pending_b = pending_a * odds_1['odd_2'] / odds_2['odd_1']
                    pending_c = pending_a * odds_1['odd_2'] / odds_2['odd_draw']
                    gain = pending_a * odds_1['odd_2'] + pending_b * odds_2['odd_1'] + pending_c * odds_2['odd_draw']
                    gain = gain / 3 - pending_a - pending_b - pending_c
                    save_to_database_list.append((
                        0, odds_1['sports'], odds_1['league'], odds_1['event'], ' ', ' ', odds_1['start_time'],
                        odds_1['dealer'], odds_2['dealer'], odds_2['dealer'], 77, 99, 88, odds_1['odd_2'],
                        odds_2['odd_1'], odds_2['odd_draw'], pending_a, pending_b, pending_c, gain
                    ))

                    # 1平
                    pending_b = pending_a * odds_1['odd_draw'] / odds_2['odd_1']
                    pending_c = pending_a * odds_1['odd_draw'] / odds_2['odd_2']
                    gain = pending_a * odds_1['odd_draw'] + pending_b * odds_2['odd_1'] + pending_c * odds_2[
                        'odd_2']
                    gain = gain / 3 - pending_a - pending_b - pending_c
                    save_to_database_list.append((
                        0, odds_1['sports'], odds_1['league'], odds_1['event'], ' ', ' ', odds_1['start_time'],
                        odds_1['dealer'], odds_2['dealer'], odds_2['dealer'], 88, 99, 77, odds_1['odd_draw'],
                        odds_2['odd_1'], odds_2['odd_2'], pending_a, pending_b, pending_c, gain
                    ))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__eu_calculate()
        save_data_for_hedge(save_to_database_list)


if __name__ == '__main__':
    EuToEu.save_data_to_database()
