
def delete_data_from_db(conn, table_name, ts_code):
    '''
    删除数据库中指定表的数据
    :param table_name:
    :param ts_code:
    :return:
    '''

    cursor = conn.cursor()
    cursor.execute("DELETE FROM {} where ts_code = '{}'".format(table_name, ts_code))
    conn.commit()
    # 关闭连接
    cursor.close()