import sys
from datetime import datetime

from docker import from_env
from docker.errors import DockerException, APIError

from utils.image_parser import flatten


class DockerHandler:
    def __init__(self, logger, username=None, password=None, registry=None):
        self.username = username
        self._password = password
        self.registry = registry
        self.callback = None
        self.logger = logger

        try:
            self.client = from_env()
            self.client.login(username=self.username, password=self._password, registry=self.registry)
        except APIError as e:
            # print(f'[ERROR] {e}')
            self.logger.exception(e)
            sys.exit(1)
        except DockerException as e:
            # print(f'[ERROR] {e}')
            self.logger.exception(e)
            sys.exit(1)

    def set_callback(self, callback):
        self.callback = callback

    def login(self, username, password, registry=None):
        try:
            self.client.login(username=username, password=password, registry=registry)
        except APIError as e:
            self.callback(format_msg(f'[ERROR] {e}'), True)
            self.logger.exception(e)
            sys.exit(1)

    def sync(self, source_images, target_repository, project, flatten_level):
        self.callback(format_msg('开始同步......'), False)

        target_name_list = []
        for image in source_images:

            target_image = flatten(image, target_repository, project, flatten_level)
            target_name_list.append(target_image)

            try:
                # 拉取镜像
                resp = self.client.api.pull(image, stream=True, decode=True)
                for line in resp:
                    self.callback(str(line), False)
                    self.logger.info(str(line))

                # 打tag
                self.client.api.tag(image, target_image)

                # 推送镜像
                resp = self.client.api.push(target_image, stream=True, decode=True)
                for line in resp:
                    self.callback(str(line), False)
                    self.logger.info(str(line))

                # 清理镜像
                self.client.images.remove(target_image)
                self.client.images.remove(image)

            except APIError as e:
                self.callback(format_msg(f'[ERROR] {e}'), True)
                self.logger.exception(e)
                sys.exit(1)

            self.callback(format_msg(f'镜像成功推送到：{target_image}'), False)

        self.client.close()
        self.callback(format_msg('同步完成!'), False)
        for target in target_name_list:
            self.callback(target, True)


def format_msg(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'[{now}] {message}'
