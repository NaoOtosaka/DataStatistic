import flask
import json
import logging
from flask import request

from lib.Database import db

import api.config.config as API_CONFIG

from api.lib.project import get_bug_list_with_project


# 声明服务
server = flask.Flask(__name__)


def get_develop_type_with_type_id(type_id):
    """
    根据开发类型id获取对应类型名称
    :param type_id:
    :return: string
    """
    sql = """
        SELECT
        develop_type.type_name
        FROM
        develop_type
        WHERE
        develop_type.type_id = "%i"
    """ % type_id

    result = db(sql)
    print(result)
    if result:
        return result[0][0]
    else:
        return []


def select_develop_type_exist(type_id):
    """
    查询开发类型是否存在
    :return:  boolean
    """
    sql = """
            SELECT
            *
            FROM
            develop_type
            WHERE
            develop_type.type_id =  "%i"
        """ % type_id

    result = db(sql)
    print(result)
    if result:
        return True
    else:
        return False


if __name__ == '__main__':
    print(get_develop_type_with_type_id(1))