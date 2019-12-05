from api.JCApiXML import JC, JCConvert
from api.AsiaApiXML import Asia
from db.utils import DB_CURSOR
from db.utils import DB_CONNECTOR
from calc.AsiaToAsiaCalculator import AsiaToAsia
from calc.AsiaToEuCalculator import AsiaToEu
from calc.OnBetCalculator import OnBetCalculator
from calc.WYHedgeCalculator import WYHedge


def init_database():
    """进行数据库的初始化"""
    # 清空hedgelist表
    DB_CURSOR.execute("delete from `hedge`;")
    # 清空odds表
    DB_CURSOR.execute("delete from `odds`;")
    # 清空onbet表
    DB_CURSOR.execute("delete from `on_bet`;")
    # 清空jc_to_asia表
    DB_CURSOR.execute("delete from `jc_to_asia`;")
    # 清空wy_hedge
    DB_CURSOR.execute("delete from `wy_hedge`;")
    DB_CONNECTOR.commit()


def main():
    """主入口函数"""
    # 初始化
    print('初始化...')
    init_database()
    print('初始化完成！')

    # 数据提取与存储
    print('提取竞彩数据并存储...')
    JC.save_data_to_database()
    print('完成竞彩提取！')
    print('开始竞彩转亚...')
    JCConvert.save_data_to_database()
    print('完成！')
    print('提取亚盘数据并存储...')
    Asia.save_data_to_database()
    print('完成亚盘提取！')

    # 进行数据计算
    print('开始on_bet计算...')
    OnBetCalculator.save_data_to_database()
    print('完成！')
    print('开始亚对亚计算...')
    AsiaToAsia.save_data_to_database()
    print('完成！')
    print('开始亚对欧计算...')
    AsiaToEu.save_data_to_database()
    print('完成！')
    print('开始wy_hedge计算...')
    WYHedge.save_data_to_database()
    print('完成！')
    DB_CURSOR.close()
    DB_CONNECTOR.close()


if __name__ == '__main__':
    import time
    st = time.time()
    main()
    print('用时：{}s'.format(round(time.time() - st, 2)))
