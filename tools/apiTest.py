import flask
import json
from flask import request

from tools.DBTest import db

server = flask.Flask(__name__)


# 声明接口路径
# 需要多种请求方式时，methods中增加即可，例['get', 'post']
# GET类型接口测试
@server.route('/index', methods=['get'])
# 接口主逻辑
def index():
    """
    测试用GET接口
    :return:
    """
    res = {'msg': '测试用借口', 'status': 1}
    return json.dumps(res, ensure_ascii=False)


# GET类型接口测试
@server.route('/api/v1/project', methods=['get'])
def show_project():
    """
    GET类型接口测试
    展示项目详细信息
    :return:{
        'msg': string,
        'data': {
            'projectId': int,
            'projectName': string,
            'planner': string,
            'developer': Developer_info_list,
            'tester': Tester_info_list,
            'projectPhase': Phase_info_list
        },
        'status': 1
        }
    """
    project_id = request.values.get('projectId')

    if project_id:
        base_info = get_project_base_info(project_id)
        # 项目信息是否存在
        if base_info:
            # 获取开发人员信息
            developer_info = get_developer_with_project(project_id)

            # 获取测试人员信息
            tester_info = get_tester_with_project(project_id)

            # 获取项目进度信息
            phase_info = get_phase_info_with_project(project_id)

            res = {
                'msg': "成功",
                'data': {
                    'projectId': base_info['projectId'],
                    'projectName': base_info['projectName'],
                    'planner': base_info['planner'],
                    'developer': developer_info,
                    'tester': tester_info,
                    'projectPhase': phase_info
                },
                'status': 1
            }
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def get_project_base_info(project_id):
    """
    根据项目ID获取项目基础信息
    :param project_id:  项目ID
    :return:
    {
        'projectId': int,
        'projectName': string,
        'planner': string,
    }
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name,
        planner.name
        FROM
        project
        INNER JOIN planner ON project.planner_id = planner.planner_id
        WHERE
        project.project_id = "%s";
    """ % project_id

    temp = {}

    # 获取项目基础信息
    result = db(sql)
    if result:
        print(result)
        temp = {
                'projectId': result[0][0],
                'projectName': result[0][1],
                'planner': result[0][2],
            }
        return temp
    else:
        return []


def get_developer_with_project(project_id):
    """
    根据项目ID获取与之关联的开发人员列表
    :param project_id:  项目ID
    :return: developer list
    {
        'developerId': int,
        'name': string,
        'developType': string
    }
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.name,
        develop_type.type_name
        FROM
        developer
        INNER JOIN develop_type ON developer.type_id = develop_type.type_id
        INNER JOIN develop ON develop.developer_id = developer.developer_id
        WHERE
        develop.project_id = "%s";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)
        print(len(result))
        for i in range(len(result)):
            temp.append(
                {
                    'developerId': result[i][0],
                    'name': result[i][1],
                    'developType': result[i][2]
                }
            )
        return temp
    else:
        return []


def get_tester_with_project(project_id):
    """
    根据项目ID获取与之关联的测试人员列表
    :param project_id:  项目ID
    :return: developer list
    {
        'testerId': int,
        'name': string
    }
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name
        FROM
        test
        INNER JOIN tester ON test.tester_id = tester.tester_id
        WHERE
        test.project_id = "%s";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)
        print(len(result))
        for i in range(len(result)):
            temp.append(
                {
                    'testerId': result[i][0],
                    'name': result[i][1],
                }
            )
        return temp
    else:
        return []


def get_phase_info_with_project(project_id):
    """
    根据项目ID获取对应项目进度
    :param project_id:  项目ID
    :return: developer list
    {
        'phaseId': int,
        'name': string,
        'startTime' timestamp,
        'endTime' timestamp
    }
    """
    sql = """
        SELECT
        project_phases.phase_id,
        test_plan.plan_name,
        project_phases.start_time,
        project_phases.end_time
        FROM
        project
        INNER JOIN project_phases ON project_phases.project_id = project.project_id
        INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
        WHERE
        project.project_id = "%s";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'phaseId': result[i][0],
                    'name': result[i][1],
                    'startTime': result[i][2],
                    'endTime': result[i][3]
                }
            )
        return temp
    else:
        return []


# 数据库挂载测试
# POST类型接口测试
# 接收path参数时使用 request.arg
# 接收json参数时使用 request.json
# 接收k-v参数时使用 request.values
@server.route('/api/v1//project/add', methods=['post'])
def add_project():
    """
    测试用POST接口
    :return:
    """
    # 接收入参
    planner_id = request.json.get('plannerId')
    print(planner_id)
    print(type(planner_id))
    project_name = request.json.get('projectName')

    if project_name and planner_id:
        sql = 'SELECT * FROM project WHERE project_name = "%s";' % project_name
        if db(sql):
            res = {'msg': '项目已存在', 'status': 2001}
        else:
            insert_sql = 'INSERT INTO project ("planner_id", "project_name") VALUES (%i, "%s")' \
                         % (planner_id, project_name)
            status = db(insert_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


# PUT类型接口测试
@server.route('/api/v1//project/edit', methods=['put'])
def edit_project():
    """
    测试用PUT接口
    :return:
    """
    # 接收入参
    project_id = request.json.get('projectId')
    planner_id = request.json.get('plannerId')
    project_name = request.json.get('projectName')

    if project_id and planner_id and project_name:
        sql = 'SELECT * FROM project WHERE project_id = "%i";' % project_id
        if db(sql):
            update_sql = 'UPDATE project SET planner_id="%i", project_name="%s" WHERE project_id="%i"'\
                         % (planner_id, project_name, project_id)
            status = db(update_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


# DELETE类型接口测试
@server.route('/api/v1//project/delete', methods=['delete'])
def delete_project():
    """
    测试用DELETE接口
    :return:
    """
    # 接收入参
    project_id = request.json.get('projectId')

    if project_id:
        sql = 'SELECT * FROM project WHERE project_id = "%i";' % project_id
        if db(sql):
            delete_sql = 'DELETE FROM project WHERE project_id="%i";' % project_id
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


# 启动服务
# debug=True时，修改代码后会自动重启服务
server.run(port=9222, debug=True, host="0.0.0.0")
