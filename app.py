from os import linesep
from copy import deepcopy
import re

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO
# from flask_session import Session

from config import Config
# from dev.config_dev import Config
import utils


# 创建实例
app = Flask(__name__)
# 加载配置
app.config.from_object(Config)

# Session(app)
# socketio = SocketIO(app, manage_session=False)

# SocketIO对象
socketio = SocketIO(app)

# 使用flask_login管理用户登录
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 登录页名称

# 获取登录用户
users = app.config['LOGIN_USERS']


# 用户类，继承UserMixin
class User(UserMixin):
    def __init__(self, username):
        self.id = username  # 设置属性id的话就不用重写get_id()方法


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    return User(username)  # 返回用户对象


# 获取镜像仓库
repositories = app.config['IMAGE_REPOSITORIES']

# 获取模板配置
html_const = app.config['HTML_CONST']

# 删除用户名和密码敏感信息
repositories_copy = deepcopy(repositories)
for key in repositories_copy.keys():
    repositories_copy.get(key).pop('username')
    repositories_copy.get(key).pop('password')


@app.route('/')
@login_required
def index():
    # 模板渲染
    return render_template('index.html', html_const=html_const, repositories=repositories_copy)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not current_user.is_authenticated:  # 如果没登录
            return render_template('login.html', html_const=html_const)
        return redirect(url_for('index'))

    username = request.form['username']
    password = request.form['password']
    if username in users and password == users.get(username):
        user = User(username)
        login_user(user)
        return redirect(url_for('index'))

    flash('用户名或密码错误，请重新登录。', 'error')  # 传递消息
    # return redirect(url_for('login'))
    return render_template('login.html', html_const=html_const, username=username, password=password)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/sync', methods=['post'])
@login_required
def sync():
    # # 获取表单数据，如果镜像是私有的，需要登录授权
    # private_registry = request.form['private_registry']
    # private_user = request.form['private_user']
    # private_passwd = request.form['private_passwd']
    #
    # # 获取表单数据，列表推导，去掉前后空白符，空行，空白行
    # source_images = [s.strip() for s in request.form.get('source_images').split(linesep) if re.search(r'\S', s)]  # List Comprehensions
    # repository_key = request.form.get('repository_key_value')
    # project = request.form.get('project_value')  # harbor仓库中的项目名
    #
    # # 获取表单数据，仓库扁平化选项值
    # flatten_level = int(request.form['flatten_level_value'])

    # 获取表单数据
    data = request.get_json()
    private_registry = data['private_registry']
    private_user = data['private_user']
    private_passwd = data['private_passwd']
    source_images_string = data['source_images']
    source_images = [s.strip() for s in source_images_string.split(linesep) if re.search(r'\S', s)]
    repository_key = data['repository_key_value']
    project = data['project_value']
    flatten_level = int(data['flatten_level_value'])

    session_id = (data['sid'])

    # 判断填写镜像地址是否合法
    pass

    # 仓库账号/密码/url等信息
    username = repositories.get(repository_key).get('username')
    password = repositories.get(repository_key).get('password')
    registry = repositories[repository_key]['url']

    logger = utils.LogManager('appLogger', 'log_manager.yml').logger
    handler = utils.DockerHandler(logger=logger, username=username, password=password, registry=registry)

    # 日志回调函数
    def send_sync_log(msg, done):
        socketio.emit('log', {'log': msg, 'done_flag': done}, to=session_id)
    handler.set_callback(send_sync_log)

    # 如果镜像是私有的，需要登录授权
    if private_user and private_passwd:
        handler.login(username=private_user, password=private_passwd, registry=private_registry)

    # 开始同步
    handler.sync(source_images=source_images, target_repository=registry, project=project, flatten_level=flatten_level)

    return 'Done!'


# @socketio.on('message')
# def handle_response(data):
#     print('1:')
#     print(data['sid'])
#
#
# @socketio.on('connect')
# def handle_connect():
#     print('2:')
#     print(request.sid)
#
#
# @socketio.on('disconnect')
# def handle_disconnect():
#     print('3:')
#     print('断开连接')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
