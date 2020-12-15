import flask
import json
from flask import request

from lib.Database import db

from api.lib.developType import get_develop_type_with_type_id, select_develop_type_exist
from api.lib.project import get_bug_list_with_project


# 声明服务
server = flask.Flask(__name__)


@server.route('/api/v1/developer/list', methods=['GET'])
def developer_list():
    """
    返回开发者列表
    :return:
    """
    return json.dumps(get_developer_list(), ensure_ascii=False)


@server.route('/api/v1/developer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def developer():
    if request.method == 'GET':
        return show_developer_info()
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass


def show_developer_info():
    """
    展示开发人员详细信息
    :return:{
        'msg': "成功",
        'data': {
            'developerId': int,
            'developerName': string,
            'developerType': string,
            'developerEmail': string,
            'project': project_info_list
        },
        'status': 1
    }
    """
    developer_id = int(request.values.get('developerId'))

    if developer_id:
        base_info = get_developer_base_info(developer_id)
        if base_info:
            develop_type = get_develop_type_with_type_id(base_info['typeId'])
            project_info = get_project_info_with_developer(developer_id)

            res = {
                'msg': "成功",
                'data': {
                    'developerId': base_info['developerId'],
                    'developerName': base_info['developerName'],
                    'developerType': develop_type,
                    'developerEmail': base_info['developerEmail'],
                    'project': project_info
                },
                'status': 1
            }
        else:
            res = {'msg': '开发人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_developer():
    """
    新增开发人员
    :return:
    """
    # 接受入参
    developer_name = request.json.get('developerName')
    developer_email = request.json.get('developerEmail')
    develop_type = request.json.get('developType')

    if developer_name and developer_email:
        sql = 'SELECT * FROM developer WHERE developer.email = "%s";' % developer_email
        if db(sql):
            res = {'msg': '该开发人员已存在', 'status': 2001}
        else:
            if select_develop_type_exist(develop_type):
                insert_sql = 'INSERT INTO "developer" ("type_id", "name", "email") VALUES ("%i", "%s", "%s");' \
                             % (develop_type, developer_name, developer_email)
                status = db(insert_sql)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '开发类型不存在', 'status': 4001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_developer():
    """
    编辑开发人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    developer_id = request.json.get('developerId')
    developer_name = request.json.get('developerName')
    developer_email = request.json.get('developerEmail')
    develop_type = request.json.get('developType')
    print(developer_id)
    print(developer_name)
    print(developer_email)

    if developer_name and developer_email and developer_id:
        sql = 'SELECT * FROM developer WHERE developer.developer_id = "%s";' % developer_id
        if db(sql):
            res = {'msg': '该开发人员已存在', 'status': 2001}
        else:
            if select_develop_type_exist(develop_type):
                update_sql = 'UPDATE developer SET type_id = "%i", name="%s", email="%s" WHERE developer_id="%i"' \
                             % (develop_type, developer_name, developer_email, developer_id)
                status = db(update_sql)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '开发类型不存在', 'status': 4001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_developer():
    """
    删除开发人员
    :return:
    """
    developer_id = request.json.get('developerId')

    if developer_id:
        sql = 'SELECT * FROM developer WHERE developer_id = "%i";' % developer_id
        if db(sql):
            delete_sql = 'DELETE FROM developer WHERE developer_id="%i";' % developer_id
            status = db(delete_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def get_developer_base_info(developer_id):
    """
    根据测试人员id获取测试人员基础信息
    :param developer_id:   测试人员ID
    :return: developer_info_list
    {
        'developerId': int,
        'typeId': int,
        'developerName': string,
        'developerEmail': string
    }
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.type_id,
        developer.name,
        developer.email
        FROM
        developer
        WHERE
        developer.developer_id = "%i"
    """ % developer_id

    # 获取测试基础信息
    result = db(sql)
    if result:
        print(result)
        temp = {
                'developerId': result[0][0],
                'typeId': result[0][1],
                'developerName': result[0][2],
                'developerEmail': result[0][3]
            }
        return temp
    else:
        return []


def get_developer_list():
    """
    获取开发人员列表
    :return:
    [
        {
            'developerId': int,
            'typeId': int,
            'developerName': string,
            'developerEmail': string
        }
    ]
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.type_id,
        developer.name,
        developer.email
        FROM
        developer
    """
    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'developerId': result[i][0],
                    'typeId': result[i][1],
                    'developerName': result[i][2],
                    'developerEmail': result[i][3]
                }
            )
        return temp
    else:
        return []


def get_project_info_with_developer(developer_id):
    """
    根据开发人员获取获取其负责的项目列表及项目下bug数量（总数，开发人员负责数）
    :param developer_id:
    :return:project_info_list
    [
        {
            'projectId': int,
            'projectName': string,
            'total': int,
            'developerCount': int
        }
    ]
    """
    temp = []

    project_list = get_project_list_with_developer(developer_id)

    if project_list:
        for i in project_list:
            project_id = i['projectId']
            project_name = i['projectName']

            total = len(get_bug_list_with_project(project_id))
            developer_count = len(get_bug_with_developer_and_project(developer_id, project_id))
            temp.append(
                {
                    'projectId': project_id,
                    'projectName': project_name,
                    'total': total,
                    'testerCount': developer_count
                }

            )
        return temp
    else:
        return []


def get_project_list_with_developer(developer_id):
    """
    根据开发人员获取其负责的项目列表
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
        project
        INNER JOIN develop ON develop.project_id = project.project_id
        INNER JOIN developer ON develop.developer_id = developer.developer_id
        WHERE
        developer.developer_id = "%s"
    """ % developer_id

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


def get_bug_with_developer_and_project(developer_id, project_id):
    """
    根据项目人员负责的项目获取项目中该开发人员负责的Bug
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
        INNER JOIN developer ON bug.developer_id = developer.developer_id
        WHERE
        developer.developer_id = "%i" AND
        project.project_id = "%i"
    """ % (developer_id, project_id)

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