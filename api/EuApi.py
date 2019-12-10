import requests
import time
from db.utils import EVENT_DICT
from setting import settings
from datetime import datetime
from db.utils import save_data_for_odds


class EuApi:
    @classmethod
    def __read_eu_from_api(cls):
        """
        从odds_api获取欧赔的数据
        :return:list，欧赔数据列表
        """
        url = 'http://api.the-odds-api.com/v3/odds'
        params = {
            'apiKey': 'c88c0e2403bad7ce3397eb6571f9f599',
            'sport': 'soccer',
            'region': 'uk',
            'mkt': 'h2h'
        }

        response = requests.get(url, params=params)
        results = response.json()['data']
        return results

    @classmethod
    def __extract_data(cls):
        """
        欧赔原始数据整合处理清洗
        :return: list，元素为数据库对应字段组成的元组，
        """
        save_to_database_list = []
        results = cls.__read_eu_from_api()
        for r in results:
            for site in r['sites']:
                if r['home_team'].strip() == r['teams'][0].strip():
                    try:
                        event = EVENT_DICT[r['teams'][0].strip()] + ' vs ' + EVENT_DICT[r['teams'][1].strip()]
                    except KeyError:
                        continue
                else:
                    try:
                        event = EVENT_DICT[r['teams'][1].strip()] + ' vs ' + EVENT_DICT[r['teams'][0].strip()]
                    except KeyError:
                        continue
                if event not in settings.EVENT_ID_DICT:
                    settings.EVENT_ID_DICT[event] = settings.EVENT_ID
                    settings.EVENT_ID += 1
                event_id = settings.EVENT_ID_DICT[event]
                save_to_database_list.append(
                    (0, event, ' ', event_id, site['site_nice'], site['odds']['h2h'][0],
                     site['odds']['h2h'][1], site['odds']['h2h'][2], 0,
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r['commence_time'])),
                     datetime.now(), 0, '足球', r['sport_nice'], ))
        return save_to_database_list

    @classmethod
    def save_data_to_database(cls):
        save_to_database_list = cls.__extract_data()
        save_data_for_odds(save_to_database_list)


if __name__ == '__main__':
    EuApi.save_data_to_database()
