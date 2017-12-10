# -*- coding:UTF-8 -*-
# coding=utf-8

import pymysql


# 入口
def chk_result(api_content, chk_level=1, db_sql=';'):
    #   参数说明：
    #   api_content 接口返回的包体
    #   chk_level <> 1 不检查data，没有db_sql
    #   chk_level = 1 检查data，有db_sql
    #   db_sql 数据库脚本 chk_level = 1时才看

    state = {}  # 检查结果，例： {'message':'success'}, {'succeed':'success'},{'data':'fail'}
    true = 'true'
    false = 'false'
    api_dict = eval(api_content)  # 接口返回的包体，转换成字典
    check_level = int(chk_level.encode('utf-8'))  # 传来的参数是unicode的，转换成int类型。

    message = api_dict['message']  # 对应包体中的message
    print("message is:" + message)
    succeed = api_dict['succeed']  # 对应包体中的succeed
    print("succeed is:" + succeed)
    data = api_dict['data']  # 对应包体中的data
    print(type(data))
    print("data is:")
    print(data)

    if message == '操作成功':
        print('Check message successfully')
        state['message'] = 'success'
    else:
        print('Check message fail')
        state['message'] = 'fail'

    if succeed == 'true':
        print('Check succeed successfully')
        state['succeed'] = 'success'
    else:
        print('Check succeed fail')
        state['succeed'] = 'fail'

    if check_level == 1:
        # 判断 如果data是字典，不需要排序，如果是list，进行排序
        if isinstance(data,dict):
            data_stored = []
            data_stored.append(data)
        else:
            data_stored = sorted(data, key=lambda s: s['id'], reverse=False)

        db_result = get_db_result(db_sql)
        print(data_stored)
        print(db_result)
        if db_result == data_stored:
            print('Check data successfully')
            state['data'] = 'success'
        else:
            print('Check data fail')
            state['data'] = 'fail'
    else:  # 不需要检查data时，直接置success
        print('Need not check data')
        state['data'] = 'success'

    print("state is:" + str(state))

    if state['message'] and state['succeed'] and state['data'] == 'success':
        result = 'success'
    else:
        result = 'false'

    return result


# 入口2 针对两个sql的接口 (childrenWithParent)
def chk_result2(api_content, chk_level=1, db_sql1=';',db_sql2=';'):
    #   参数说明：
    #   api_content 接口返回的包体
    #   chk_level <> 1 不检查data，没有db_sql
    #   chk_level = 1 检查data，有db_sql
    #   db_sql 数据库脚本 chk_level = 1时才看

    state = {}  # 检查结果，例： {'message':'success'}, {'succeed':'success'},{'data':'fail'}
    true = 'true'
    false = 'false'
    api_dict = eval(api_content)  # 接口返回的包体，转换成字典
    check_level = int(chk_level.encode('utf-8'))  # 传来的参数是unicode的，转换成int类型。

    message = api_dict['message']  # 对应包体中的message
    print("message is:" + message)
    succeed = api_dict['succeed']  # 对应包体中的succeed
    print("succeed is:" + succeed)
    data = api_dict['data']  # 对应包体中的data
    print(type(data))
    print("data is:")
    print(data)

    if message == '操作成功':
        print('Check message successfully')
        state['message'] = 'success'
    else:
        print('Check message fail')
        state['message'] = 'fail'

    if succeed == 'true':
        print('Check succeed successfully')
        state['succeed'] = 'success'
    else:
        print('Check succeed fail')
        state['succeed'] = 'fail'

    if check_level == 1:
        # 判断 如果data是字典，不需要排序，如果是list，进行排序
        if isinstance(data,dict):
            data_stored = []
            data_stored.append(data)
        else:
            data_stored = sorted(data, key=lambda s: s['id'], reverse=False)

        db_result1 = get_db_result(db_sql1)
        db_result2 = get_db_result(db_sql2)
        db_result3 = db_result1 + db_result2
        db_result = sorted(db_result3, key=lambda s: s['id'], reverse=False)

        print(data_stored)
        print(db_result)
        if db_result == data_stored:
            print('Check data successfully')
            state['data'] = 'success'
        else:
            print('Check data fail')
            state['data'] = 'fail'
    else:  # 不需要检查data时，直接置success
        print('Need not check data')
        state['data'] = 'success'

    print("state is:" + str(state))

    if state['message'] and state['succeed'] and state['data'] == 'success':
        result = 'success'
    else:
        result = 'false'

    return result







# 从数据库获取内容，返回字典
def get_db_result(sql):
    conn = pymysql.connect(host='120.76.85.35', port=13307, user='linklaws', passwd='linklaws_123', db='linklaws_test')
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 游标设置为字典类型
    cursor.execute(sql)

    # 获取剩余结果的第一行数据
    # row_1 = cursor.fetchone()
    # 获取剩余结果前n行数据
    # row_2 = cursor.fetchmany(3)
    # 获取剩余结果所有数据
    row_all = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return row_all


if __name__ == '__main__':
    true = 'true'
    api_content = str({"message": "操作成功", "level": "DEBUG", "errorCode": "0", "curtime": 1512373874971,
                       "data": [{"id": 1, "name": "民事部"}, {"id": 2, "name": "人格权纠纷"}, {"id": 3003, "name": "无因管理纠纷"},
                                {"id": 3333, "name": "民事"}], "succeed": true})
    chk_level = 1
    db_sql = "select id,name from t_tool_cause where type=0 and state='enable' order by id;"

    result = chk_result(api_content, chk_level, db_sql)
    print(result)
