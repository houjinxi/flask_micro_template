# Flask微服务框架模版v1.0
整理的Flask web框架，仅供学习用。
## 框架功能
- 模块化框架结构，使用mvc设计模式分层处理业务逻辑
- 使用 flask_restplus 处理restful接口，及接口文档
- 配置支持本地配置和远程配置中心配置
- 框架使用SQLAlchemy进行数据库操作
- 业务逻辑处理可以使用peewee进行数据库操作
- 提供自封装的工具包

## 部署启动（Windows）
- **Python版本 v3.8**
- **安装依赖包**
```
pip install -r requirements.txt
```
- **create_app** 开启修复注释
```
app -> main-> __init__.py ->create_app
# fix_flask_restplus()

flask_restplus很久没维护，会导致werkzeug包引用报错
old = "from werkzeug import cached_property"
new = "from werkzeug.utils import cached_property"
```
- **项目启动**

```
flask run
```
##### **常见错误：**

**1. werkzeug与flask版本兼容问题 from werkzeug.wrappers.json import JSONMixin as _JSONMixin**
```
ModuleNotFoundError: No module named 'werkzeug.wrappers.json'; 'werkzeug.wrappers' is not a package
```
- **解决办法：werkzeug升级到0.15.4以上版本**
```
pip install werkzeug==0.15.4
```
**2. Python3.8不再支持time.clock**

```
AttributeError: module 'time' has no attribute 'clock' 
```
- **解决办法：Mako升级到1.1.2以上版本**
```
pip install Mako==1.1.2
```

## 部署启动（Docker）
后续更新

##  数据库版本管理（Flask-Migrate）
```
# 初始化数据库版本管理
flask db init
# 生成版本文件
flask db migrate -m "Initial migration."
# 升级版本文件
flask db upgrade
# 降级版本文件
flask db downgrade
# 帮助文档
flask db --help
# 生成迁移sql
flask db upgrade 版本号 --sql > migration.sql
```
## 计划更新模块
1. 用户鉴权管理
2. Docker框架部署和持续集成


