# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 15:28
# @Author  : HoxHou
# @File    : model_generator.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows


import yaml

"""
数据model生成器：
1.根据环境生成 model 文件
2.生成器：getter、setter、deleter
"""


class PeeweeGenerator(object):

    def __init__(self, env, database):
        self.env = env
        self.database = database

    # 读取配置yaml
    # 生成peewee model语句
    # 生成方法

    def read_config(self, project_name="environments"):
        with open('peewee.yaml', encoding='UTF-8') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config[project_name][self.env] if self.env in config[project_name] else False

    def _command(self):
        config = self.read_config()
        DATABASE = self.database
        DB_FILE = f"{DATABASE}.py"
        DIALECT = config["DIALECT"]
        USERNAME = config["USERNAME"]
        PASSWORD = config["PASSWORD"]
        HOST = config["HOST"]
        PORT = config["PORT"]
        COMMAND = "python -m pwiz -e "
        PEEWEE_DATABASE_UR = f"{COMMAND}{DIALECT} -H {HOST} -p {PORT} -u {USERNAME} -P {PASSWORD} {DATABASE} > {DB_FILE}"
        print(PEEWEE_DATABASE_UR)
        return PEEWEE_DATABASE_UR

    def create_model(self):
        self._command()


if __name__ == '__main__':
    pg = PeeweeGenerator("local", "test_automation")
    pg.create_model()
