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


# 数据库挂载测试
# POST类型接口测试
# 接收path参数时使用 request.arg
# 接收json参数时使用 request.json
# 接收k-v参数时使用 request.values
@server.route('/project/add', methods=['post'])
def project():
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


# 启动服务
# debug=True时，修改代码后会自动重启服务
server.run(port=9222, debug=True)
