import logging
import logging.config
import os
from logging.handlers import TimedRotatingFileHandler

import yaml


class LogManager:
    _instance = None

    def __new__(cls, logger_name='root', config_file='log_manager.yml'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(logger_name, config_file)
        return cls._instance

    def _init(self, logger_name, config_file):
        """
        # 设置日志文件路径
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, 'app.log')

        # 创建logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 创建formatter
        logging_format = '%(asctime)s %(levelname)s %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(fmt=logging_format, datefmt=date_format)

        # 创建文件处理器
        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # 给logger添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        """

        # 如果不存在logs目录则创建
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # # 配置日志记录器
        # logging.config.fileConfig(config_file)

        # 加载 YAML 配置文件
        with open(config_file, 'r') as file:
             config = yaml.safe_load(file)
        # 配置日志记录器
        logging.config.dictConfig(config)

        # 创建日志记录器
        self.logger = logging.getLogger(logger_name)
