from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import platform
import datetime
from io import StringIO
import sqlite3
import pandas as pd
from constants import finance_indicator_names
import tushare as ts
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import delete_data_from_db


def get_chormedriver_path():
    os_name = platform.system()
    if os_name.lower() == 'windows':
        path = r"D:\newocr\chromedriver-win64\chromedriver.exe"
    elif os_name.lower() == 'linux':
        path = r"./chromedriver-win64/chromedriver_linux"
    else:
        raise Exception("当前操作系统不支持")
    return path


executable_path = get_chormedriver_path()

pro = ts.pro_api("f88e93f91c79cdb865f22f40cac23a2907da36b53fa9aa150228ed27")
# Setting up the webdriver
# 设置ChromeOptions，启用无界面模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
service = webdriver.ChromeService(executable_path=executable_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Connecting to the database

conn = sqlite3.connect('fina.db')





def code_transform(code):
    '''
    将600000.SH转换为SH600000
    :param code:
    :return:
    '''
    res = code.split('.')
    return res[1] + res[0]


def get_en_name(cn_name,names):
    '''
    获取英文名称
    :param cn_name:
    :param names: 来自contants.py finance_indicator_names
    :return:
    '''
    for name in names:
        if name["display"] == cn_name:
            return name["en"]
    return None


def handle_table(df_1,ts_code):
    '''
    处理表格数据
    :param df_1:
    :param ts_code:
    :return:
    '''
    unexpected_values = ['成长能力指标', '盈利能力指标', '收益质量指标', '财务风险指标', '营运能力指标']
    df_1_new = df_1[~df_1['每股指标'].isin(unexpected_values)]
    df_1_new = df_1_new.copy()
    df_1_new["en_name"] = df_1_new["每股指标"].apply(lambda x: get_en_name(x, finance_indicator_names))
    df_1_new = df_1_new.drop(columns=['每股指标'])
    df_1_new = df_1_new.set_index("en_name")
    df_1_new = df_1_new.T
    df_1_new.reset_index(inplace=True)
    df_1_new["index"] = "20" + df_1_new["index"]
    df_1_new.rename(columns={'index': 'end_date'}, inplace=True)
    df_1_new["ts_code"] = ts_code
    return df_1_new


def get_fina_from_dc(ts_code):
    '''
    从东方财富获取最新财报数据
    :param ts_code:
    :return:
    '''
    code = code_transform(ts_code)
    # Setting up the url
    url = f"https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={code}&color=b#/cwfx"

    # Opening the url
    driver.get(url)

    # Waiting for the page to load
    time.sleep(3)     # 等待页面加载完毕

    # Finding the table containing the financial data
    cwfx = driver.find_element(By.CSS_SELECTOR, '.cwfx')
    # 查找标签
    tab = cwfx.find_element(By.CSS_SELECTOR, '.tab')
    ul = tab.find_element(By.TAG_NAME, 'ul')
    lis = ul.find_elements(By.TAG_NAME, 'li')

    if len(lis) != 2:
        return None
    else:
        # 获取最新财务报告数据
        lis[1].click()
        time.sleep(3)  # 等待页面加载完毕

        cwfx = driver.find_element(By.CSS_SELECTOR, '.cwfx')
        zyzb_table = cwfx.find_element(By.CLASS_NAME, 'zyzb_table')
        table1 = zyzb_table.find_element(By.CLASS_NAME, 'table1')
        table3 = zyzb_table.find_element(By.CLASS_NAME, 'table3')
        # 获取报告期数据

        df_1 = pd.read_html(StringIO(str(table1.get_attribute('outerHTML'))), displayed_only=False, header=0)[0]
        df_1_new = handle_table(df_1,ts_code)

        # 获取单季度数据
        df_2 = pd.read_html(StringIO(str(table3.get_attribute('outerHTML'))), displayed_only=False, header=0)[0]
        df_2_new = handle_table(df_2,ts_code)
        return df_1_new,df_2_new


def download_stock_basic():
    '''
    每日下载一次股票基本信息
    获取股票基本信息
    :return:
    '''
    data = pro.stock_basic(exchange='', list_status='L',fields='ts_code,symbol,name,area,industry,list_date,market,exchange,is_hs,act_name,act_ent_type')
    data.to_sql('stock_basic', con=conn, if_exists='replace')


def get_stock_basic():
    '''
    获取股票基本信息
    名称	类型	默认显示	描述
    ts_code	str	Y	TS代码
    symbol	str	Y	股票代码
    name	str	Y	股票名称
    area	str	Y	地域
    industry	str	Y	所属行业
    fullname	str	N	股票全称
    enname	str	N	英文全称
    cnspell	str	Y	拼音缩写
    market	str	Y	市场类型（主板/创业板/科创板/CDR）
    exchange	str	N	交易所代码
    curr_type	str	N	交易货币
    list_status	str	N	上市状态 L上市 D退市 P暂停上市
    list_date	str	Y	上市日期
    delist_date	str	N	退市日期
    is_hs	str	N	是否沪深港通标的，N否 H沪股通 S深股通
    act_name	str	Y	实控人名称
    act_ent_type	str	Y	实控人企业性质
    :return:
    '''
    data = pd.read_sql_query('SELECT * FROM stock_basic WHERE exchange = "SSE" OR exchange = "SZSE"', conn)
    return data


def check_quarter_revenue_increase(df,limit_percent=10.0):
    '''
    检查季度营业收入是否有增长
    :return:
    '''
    yoy_total_operating_revenue = float(df.iloc[0]["yoy_total_operating_revenue"])
    if yoy_total_operating_revenue > limit_percent:
        return True,yoy_total_operating_revenue
    else:
        return False,yoy_total_operating_revenue


# TODO:增加对金融类指标的处理600816.SH
def update_new_fina(ts_code,end_date,pre_date):
    '''
    检查是否有新的财报数据，如果有则更新数据库
    :param ts_code:
    :param end_date:
    :param pre_date:预披露日期
    :return:
    '''
    df = pd.read_sql("SELECT end_date FROM indicator_quarter WHERE ts_code = '{}' ORDER BY end_date DESC LIMIT 1".format(ts_code), conn)
    df1,df2 = get_fina_from_dc(ts_code)

    if df.empty:
        '''
        数据库中没有该股票的财报数据，则插入数据
        检查最新季度营业收入是否有增长10%以上
        如果最新季度营业收入有增长，并且最新季度是要查询的截止日，则插入quarter_revenue_increase表
        '''
        df1.to_sql("indicator_report", conn, if_exists='append', index=False)
        df2.to_sql("indicator_quarter", conn, if_exists='append', index=False)
        has_new,yoy_total_operating_revenue = check_quarter_revenue_increase(df2)
        new_end_date = datetime.datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
        if (new_end_date in df2["end_date"].tolist()) and has_new:
            df_news = pd.DataFrame({'ts_code': [ts_code],"end_date": [new_end_date], 'yoy_total_operating_revenue': [yoy_total_operating_revenue], 'pre_date': [pre_date]})
            df_news.to_sql("quarter_revenue_increase", conn, if_exists='append', index=False)
    else:
        if df1.iloc[0]["end_date"] != df.iloc[0]["end_date"]:
            delete_data_from_db(conn, "indicator_report", ts_code)
            df1.to_sql("indicator_report", conn, if_exists='append', index=False)

            delete_data_from_db(conn, "indicator_quarter", ts_code)
            df2.to_sql("indicator_quarter", conn, if_exists='append', index=False)
            has_new,yoy_total_operating_revenue = check_quarter_revenue_increase(df2)
            if has_new:
                df_news = pd.DataFrame({'ts_code': [ts_code],"end_date": [df2.iloc[0]["end_date"]], 'yoy_total_operating_revenue': [yoy_total_operating_revenue], 'pre_date': [pre_date]})
                df_news.to_sql("quarter_revenue_increase", conn, if_exists='append', index=False)
        else:
            print("No new data")


def get_data_by_date():
    '''
    获取指定日期的财报数据
    :return:
    '''
    # 获取当前日期前后3天的日期，用于查询这段时间内是否存在披露
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    next_day = now + datetime.timedelta(days=3)
    next_day_str = next_day.strftime("%Y%m%d")
    pre_day = now - datetime.timedelta(days=3)
    pre_day_str = pre_day.strftime("%Y%m%d")
    # 获取当前要查询的截止日期
    if month in [1,2,3]:
        search_end_dates = [str(year-1) + '1231']
    elif month == 4:
        search_end_dates = [str(year) + '0331', str(year-1) + '1231']
    elif month in [5,6]:
        search_end_dates = [ str(year) + '0331']
    elif month in [7,8,9]:
        search_end_dates = [str(year) + '0630']
    elif month in [10,11,12]:
        search_end_dates = [str(year) + '0930']
    else:
        raise ValueError("Invalid month")
    # 查询截止日对应的披露情况
    for end_date in search_end_dates:
        # 获取截止日对应的预披露情况
        data = pro.disclosure_date(end_date=end_date)
        # 筛选出今天之前3天和今天之后3天的披露情况
        data = data[(data["pre_date"] >= pre_day_str) & (data["pre_date"] <= next_day_str)]
        # ts_codes = data["ts_code"].tolist()
        # 在此范围内存在披露的股票，逐个获取最新财报数据
        for index,row in data.iterrows():
            print(row["ts_code"])
            try:
                update_new_fina(row["ts_code"],end_date,row["pre_date"])
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    schedule = BlockingScheduler()
    schedule.add_job(get_data_by_date, 'interval', days=1, id='my_job_id')
    schedule.start()
    # print(get_chormedriver_path())
