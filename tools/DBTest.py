import sqlite3


def db(sql=None):
    """
    数据库操作
    :param sql:
    :return:
    """
    # 挂载链接
    connect = connect_database()
    # 传入查询时
    if sql:
        # 执行SQL
        result = query(connect, sql)

        connect.close()
        return result
    # 关闭链接
    connect.close()


def connect_database():
    """
    挂载数据库
    :return: 链接对象
    """
    # 挂载链接
    connect = sqlite3.connect('../data.db')
    # 强制启动外键约束
    connect.execute("PRAGMA foreign_keys=1;")

    return connect


def query(connect, sql):
    """
    执行SQL
    :type connect: sqlite3.Connection
    :type sql: string
    """
    sql = sql.strip()

    if sql.lstrip().upper().startswith("SELECT"):
        # 创建游标
        cursor = connect.cursor()
        # 查询
        result = select(cursor, sql)
        # 关闭游标
        cursor.close()
        return result
    elif sql.lstrip().upper().startswith("INSERT"):
        result = insert(connect, sql)
        return result
    elif sql.lstrip().upper().startswith("UPDATE"):
        result = update(connect, sql)
        return result
    elif sql.lstrip().upper().startswith("DELETE"):
        result = delete(connect, sql)
        return result
    else:
        pass


def select(cursor, sql):
    """
    SELECT语句
    :param sql:
    :param cursor:
    :return:
    """
    # 执行SQL
    cursor.execute(sql)
    # 获取结果
    result = cursor.fetchall()

    return result


def insert(connect, sql):
    """
    INSERT语句
    :param sql:
    :param connect:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        print(sqlite3.Error)

    return result


def update(connect, sql):
    """
    UPDATE语句
    :param connect:
    :param sql:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        print(sqlite3.Error)

    return result


def delete(connect, sql):
    """
    DELETE语句
    :param connect:
    :param sql:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        print(sqlite3.Error)

    return result


if __name__ == '__main__':
    conn = sqlite3.connect('../data.db')

    print(type(conn))

    cur = conn.cursor()

    print(type(cur))

    # c.execute("select * from user")
    #
    # print(c.fetchone())

    buffer = ''

    while True:
        line = input()
        if line == "":
            break
        buffer += line
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()
                cur.execute(buffer)
                print(cur.fetchall())
                # if buffer.lstrip().upper().startswith("SELECT"):
                #     print(cur.fetchall())
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])
            buffer = ""

    conn.close()

