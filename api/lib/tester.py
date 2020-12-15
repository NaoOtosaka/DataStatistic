import flask
import json
import logging
from flask import request

from lib.Database import db

import api.config.config as API_CONFIG

from api.lib.project import get_bug_list_with_project

# 声明服务
server = flask.Flask(__name__)


@server.route('/api/v1/tester/list', methods=['GET'])
def tester_list():
    """
    返回测试人员列表
    :return:
    """
    return json.dumps(show_tester_list(), ensure_ascii=False)


@server.route('/api/v1/tester', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tester():
    if request.method == 'GET':
        return show_tester_info()
    elif request.method == 'POST':
        return add_tester()
    elif request.method == 'PUT':
        return edit_tester()
    elif request.method == 'DELETE':
        return delete_tester()


def show_tester_list():
    """
    获取测试人员列表
    :return:{
        'msg': string,
        'data': {
            'testerId': int,
            'testerName': string,
            'testerEmail': string
        },
        'status': 1
        }
    """
    result = get_tester_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无测试人员信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def show_tester_info():
    """
    展示测试人员详细信息
    :return: {
        'msg': string,
        'data': {
            'testerId': int,
            'testerName': string,
            'testerEmail': string,
            'project': project_info_list
        },
        'status': 1
    }
    """
    tester_id = request.values.get('testerId')

    if tester_id:
        base_info = get_tester_base_info(tester_id)
        if base_info:
            project_info = get_project_info_with_tester(tester_id)

            res = {
                'msg': "成功",
                'data': {
                    'testerId': base_info['testerId'],
                    'testerName': base_info['testerName'],
                    'testerEmail': base_info['testerEmail'],
                    'project': project_info
                },
                'status': 1
            }
        else:
            res = {'msg': '测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_tester():
    """
    新增测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    tester_name = request.json.get('testerName')
    tester_email = request.json.get('testerEmail')
    logging.log(1, tester_email)
    print(tester_name)
    print(tester_email)

    if tester_name and tester_email:
        sql = 'SELECT * FROM tester WHERE tester.email = "%s";' % tester_email
        if db(sql):
            res = {'msg': '该测试人员已存在', 'status': 2001}
        else:
            insert_sql = 'INSERT INTO "tester" ("name", "email") VALUES ("%s", "%s");' \
                         % (tester_name, tester_email)
            status = db(insert_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_tester():
    """
    编辑测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    tester_id = request.json.get('testerId')
    tester_name = request.json.get('testerName')
    tester_email = request.json.get('testerEmail')
    print(tester_id)
    print(tester_name)
    print(tester_email)

    if tester_name and tester_email and tester_id:
        sql = 'SELECT * FROM tester WHERE tester.tester_id = "%i";' % tester_id
        if db(sql):
            sql = 'SELECT * FROM tester WHERE tester.email = "%s";' % tester_email
            if db(sql):
                update_sql = 'UPDATE tester SET name="%s", email="%s" WHERE tester_id="%i"' \
                             % (tester_name, tester_email, tester_id)
                status = db(update_sql)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '邮箱不可重复', 'status': 2001}
        else:
            res = {'msg': '该测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_tester():
    """
    删除测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    tester_id = request.json.get('testerId')

    if tester_id:
        sql = 'SELECT * FROM tester WHERE tester_id = "%i";' % tester_id
        if db(sql):
            delete_sql = 'DELETE FROM tester WHERE tester_id="%i";' % tester_id
            status = db(delete_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def get_tester_base_info(tester_id):
    """
    根据测试人员id获取测试人员基础信息
    :param tester_id:   测试人员ID
    :return: tester_info_list
    {
        'testerId': int,
        'testerName': string,
        'testerEmail':string
    }
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name
        FROM
        tester
        WHERE
        tester.tester_id = "%i"
    """ % tester_id

    # 获取测试基础信息
    result = db(sql)
    if result:
        print(result)
        temp = {
                'testerId': result[0][0],
                'testerName': result[0][1],
                'testerEmail': result[0][2]
            }
        return temp
    else:
        return []


def get_tester_list():
    """
    获取测试人员列表
    :return:
    [
        {
            'testerId': int,
            'testerName': string,
            'testerEmail': string
        }
    ]
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name,
        tester.email
        FROM
        tester
        """
    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'testerId': result[i][0],
                    'testerName': result[i][1],
                    'testerEmail': result[i][2]
                }
            )
        return temp
    else:
        return []


def get_project_info_with_tester(tester_id):
    """
    根据测试人员获取其负责的项目列表及项目下bug数量（总数，测试人员负责数）
    :param tester_id:   测试人员ID
    :return: project_info_list
    [
        {
            'projectId': int,
            'projectName': string,
            'total': int,
            'testerCount': int
        }
    ]
    """
    temp = []

    project_list = get_project_list_with_tester(tester_id)
    if project_list:
        for i in project_list:
            # 获取项目对应bug总数
            project_id = i['projectId']
            project_name = i['projectName']

            total = len(get_bug_list_with_project(project_id))
            tester_count = len(get_bug_with_tester_and_project(tester_id, project_id))
            temp.append(
                {
                    'projectId': project_id,
                    'projectName': project_name,
                    'total': total,
                    'testerCount': tester_count
                }
            )

        return temp
    else:
        return []


def get_project_list_with_tester(tester_id):
    """
    根据测试人员获取其负责的项目列表
    :return: project_info_list
    [
        {
            'projectId': int,
            'projectName': string
        }
    ]
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name
        FROM
        tester
        INNER JOIN test ON test.tester_id = tester.tester_id
        INNER JOIN project ON test.project_id = project.project_id
        WHERE
        test.tester_id = "%i"
    """ % tester_id

    temp = []

    # 获取项目id列表
    result = db(sql)

    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'projectId': result[i][0],
                    'projectName': result[i][1]
                }
            )
        return temp
    else:
        return []


def get_bug_with_tester_and_project(tester_id, project_id):
    """
    根据项目人员负责的项目获取项目中该测试人员负责的Bug
    :return: bug_id_list
    [int]
    """
    sql = """
        SELECT
        bug.bug_id
        FROM
        bug
        INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
        INNER JOIN project ON project_phases.project_id = project.project_id
        INNER JOIN tester ON bug.tester_id = tester.tester_id
        WHERE
        tester.tester_id = "%i" AND
        project.project_id = "%i"
    """ % (tester_id, project_id)

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []


def setup():
    server.run(port=9222, debug=True, host="0.0.0.0")


if __name__ == '__main__':
    setup()