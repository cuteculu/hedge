import pymysql
from setting.settings import DATABASE


def create_db():
    db = pymysql.connect(host=DATABASE['HOST'], user=DATABASE['USER'], password=DATABASE['PASSWORD'],
                         db=DATABASE['NAME'], port=DATABASE['PORT'],
                         cursorclass=pymysql.cursors.DictCursor, charset='utf8')
    return db


def save_data_for_odds(save_to_database_list):
    """保存数据到odds表"""
    db = create_db()
    cursor = db.cursor()
    insert_many_sql = "insert into `odds` values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(insert_many_sql, save_to_database_list)
    db.commit()


def save_data_for_jc_to_asia(save_to_database_list):
    """保存数据到jc_to_asia表"""
    db = create_db()
    cursor = db.cursor()
    insert_many_sql = "insert into `jc_to_asia` values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(insert_many_sql, save_to_database_list)
    db.commit()


def save_data_for_hedge(save_to_database_list):
    """保存数据到hedge表"""
    db = create_db()
    cursor = db.cursor()
    insert_many_sql = "insert into `hedge` values " \
                      "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(insert_many_sql, save_to_database_list)
    db.commit()


def save_data_for_on_bet(save_to_database_list):
    """保存数据到on_bet表"""
    db = create_db()
    cursor = db.cursor()
    insert_many_sql = "insert into `on_bet` values " \
                      "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(insert_many_sql, save_to_database_list)
    db.commit()


def save_data_for_wy_hedge(save_to_database_list):
    """保存数据到wy_hedge表"""
    db = create_db()
    cursor = db.cursor()
    insert_many_sql = "insert into `wy_hedge` values " \
                      "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(insert_many_sql, save_to_database_list)
    db.commit()


class DatabaseForAsiaToAsia:
    """为亚to亚提供数据库服务支持"""
    __db = create_db()
    __cursor = __db.cursor()

    @classmethod
    def distinct_id(cls):
        """
        查询并去重odds表中status=0且odd_draw=888的数据的event_id，
        status为0表示为最新可使用的数据，888为自定义标识，表示该数据为亚盘。
        """
        select_distinct_id_for_odds = "SELECT DISTINCT `event_id` FROM `odds` " \
                                      "where `status`=0  and `odd_draw`=888;"
        cls.__cursor.execute(select_distinct_id_for_odds)
        id_tuple = cls.__cursor.fetchall()
        return [i['event_id'] for i in id_tuple]

    @classmethod
    def search_asia_odds_list(cls):
        """查询odds表中的亚盘数据"""
        # odd_draw=888为自定义的亚盘标识
        cls.__cursor.execute(
            "select * from `odds` where `status`=0 and `odd_draw`=888;")
        asia_odds_list = cls.__cursor.fetchall()
        return asia_odds_list


class DatabaseForAsiaToEu:
    """为亚to欧计算提供数据库支持"""
    __db = create_db()
    __cursor = __db.cursor()

    @classmethod
    def distinct_id(cls):
        """去重并返回odds表中的所有event_id"""
        cls.__cursor.execute(
            "SELECT DISTINCT `event_id` FROM `odds` where `status`=0;")
        id_tuple = cls.__cursor.fetchall()
        return [i['event_id'] for i in id_tuple]

    @classmethod
    def search_odds_list(cls):
        """
        查询并返回odds表中的亚盘与欧盘数据，handicap为0是欧盘，
        odd_draw=888为亚盘(自定义标识)
        :return: 返回两者相加的列表
        """
        cls.__cursor.execute(
            "select * from `odds` where `status`=0 and `handicap`=0 and `odd_draw`!=888;")
        odds_list_eu = cls.__cursor.fetchall()
        cls.__cursor.execute(
            "select * from `odds` where `status`=0 and `odd_draw`=888;")
        odds_list_asia = cls.__cursor.fetchall()
        # 亚欧列表整合并返回
        odds_list_asia.extend(odds_list_eu)
        return odds_list_asia


class DatabaseForJCConvert:
    """竞彩转亚数据库支持"""
    __db = create_db()
    __cursor = __db.cursor()

    @classmethod
    def distinct_id(cls):
        """提供去重后的event_id"""
        cls.__cursor.execute("select distinct `event_id` from `odds` where `dealer`='竞彩' and `status`=0;")
        event_id_list = cls.__cursor.fetchall()
        return event_id_list

    @classmethod
    def search_data_from_id(cls, event_id):
        """提供单event_id数据查询"""
        select_sql = "select * from `odds` where `event_id`=%s and `dealer`='竞彩' and `status`=0;"
        cls.__cursor.execute(select_sql, [event_id])
        results = cls.__cursor.fetchall()
        return results


class DatabaseForOnBet:
    """on_bet计算支持"""
    __db = create_db()
    __cursor = __db.cursor()

    @classmethod
    def distinct_id(cls):
        """竞彩转亚后的表中的event_id去重返回"""
        cls.__cursor.execute("SELECT DISTINCT `event_id` FROM `jc_to_asia` where `status`=0;")
        id_tuple = cls.__cursor.fetchall()
        return [i['event_id'] for i in id_tuple]

    @classmethod
    def search_data_from_odds(cls, event_id):
        """根据event_id从odds表查询数据"""
        select_sql = "select * from `odds` where `odd_draw`=888 and `event_id`=%s and `status`=0;"
        cls.__cursor.execute(select_sql, [event_id])
        results = cls.__cursor.fetchall()
        return results

    @classmethod
    def search_data_from_jc_to_asia(cls, event_id):
        """根据event_id从jc_to_asia表查询数据"""
        select_sql = "select * from `jc_to_asia` where `odd_draw`=888 " \
                     "and `event_id`=%s and `status`=0;"
        cls.__cursor.execute(select_sql, [event_id])
        results = cls.__cursor.fetchall()
        return results


class DatabaseForWYHedge:
    """王阳hedge表数据库支持"""
    __db = create_db()
    __cursor = __db.cursor()

    @classmethod
    def search_data_from_hedge(cls):
        """提取hedge表所有数据"""
        select_sql = "select * from `hedge`;"
        cls.__cursor.execute(select_sql)
        results = cls.__cursor.fetchall()
        return results

    @classmethod
    def search_data_from_rate(cls):
        """
        提取rate表中dealer对应的返点率
        :return: 字典，dealer为键，rate为值
        """
        select_sql = "select * from `dealer_rate`;"
        cls.__cursor.execute(select_sql)
        results = cls.__cursor.fetchall()
        return {r['dealer']: r['rate'] for r in results}


if __name__ == '__main__':
    # print(DatabaseForWYHedge.search_data_from_rate())
    db = create_db()
