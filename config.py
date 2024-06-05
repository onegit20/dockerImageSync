class Config:
    # 会话密钥
    SECRET_KEY = '5JXWUv39aVJ5xUqR1k9OzXsGc0XlM6sYg4Qq4u6ga2q1Xe8N2vz0BKO1Yh0C2f32'

    # session过期时间，单位秒，默认31天
    # PERMANENT_SESSION_LIFETIME = 86400  # 24小时

    # # 使用基于服务器内存的会话存储
    # SESSION_TYPE = 'filesystem'

    # 登录用户
    LOGIN_USERS = {
        'admin': 'password',  # 用户名： 密码
        # 可添加多个用户
    }

    # 镜像仓库
    IMAGE_REPOSITORIES = {
        'harbor-1': {
            'name': 'Harbor-1',
            'url': 'harbor-1.example.com',
            'projects': ['library', 'project1', 'project2'],
            'username': 'user',
            'password': 'password'
        },
        'harbor-2': {
            'name': 'Harbor-2',
            'url': 'harbor-2.example.com',
            'projects': ['library', 'project1'],
            'username': 'user',
            'password': 'password'
        },
        # 添加更多仓库
    }

    # 模板配置
    HTML_CONST = {
        'heading': '镜像仓库同步系统',  # 标题
        'placeholder':  # 镜像地址栏提示占位符
        [
            'harbor.example.com/library/example:v1',
            'alpine'
        ]
    }
