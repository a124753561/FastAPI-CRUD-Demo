# FastAPI 用户 CRUD API 示例

[English](./README-en.md)

基于 FastAPI + SQLAlchemy + MySQL 的用户增删改查 API 示例项目。

## 项目结构

```
fastapi-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 应用工厂 & lifespan
│   ├── config.py                # pydantic-settings 配置（读取 .env）
│   ├── database.py              # SQLAlchemy 引擎 / 会话 / Base / get_db
│   ├── api/v1/
│   │   ├── router.py            # v1 路由聚合
│   │   └── users.py             # 用户 CRUD 端点
│   ├── models/user.py           # SQLAlchemy User ORM 模型
│   ├── schemas/user.py          # Pydantic v2：UserCreate / UserUpdate / UserResponse
│   ├── services/user.py         # 业务逻辑层
│   └── exceptions/
│       └── handlers.py          # 自定义异常 & 全局异常处理器
├── pyproject.toml               # 项目元数据 & 依赖
├── .env                         # 环境变量
└── README.md
```

## 技术栈

| 组件         | 选型               |
|-------------|-------------------|
| Web 框架     | FastAPI           |
| ORM         | SQLAlchemy 2.0    |
| 数据库       | MySQL（PyMySQL 驱动）|
| 数据校验     | Pydantic v2       |
| 配置管理     | pydantic-settings |

## 快速开始

### 环境要求

- Python >= 3.10
- MySQL 服务

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置数据库

编辑 `.env` 文件，填写 MySQL 连接信息：

```
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/数据库名
```

创建数据库（如果还未创建）：

```bash
mysql -u 用户名 -p -e "CREATE DATABASE IF NOT EXISTS 数据库名 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. 启动服务

```bash
python -m app.main
```

服务启动后访问：
- API 文档：http://127.0.0.1:3002/docs
- 备用文档：http://127.0.0.1:3002/redoc

### PyCharm 调试

1. 打开 PyCharm，点击右上角 **Add Configuration...** → **+** → **Python**
2. 配置如下：

| 配置项       | 值                              |
|-------------|---------------------------------|
| Name        | `FastAPI Debug`                 |
| Module name | `app.main`                      |
| Working dir | 项目根目录（fastapi-demo）       |

3. 在代码中打上断点，点击 **Debug** 按钮即可调试

> 确保 PyCharm 使用的 Python 解释器已安装项目依赖。

## API 接口

所有接口前缀：`/api/v1/users`

| 方法   | 路径          | 说明              | 参数                                |
|--------|-------------|-------------------|-------------------------------------|
| POST   | `/`          | 创建用户          | Body: UserCreate JSON              |
| GET    | `/`          | 用户列表          | Query: `skip`(默认0), `limit`(默认100)|
| GET    | `/{user_id}` | 获取用户          | Path: user_id                      |
| PUT    | `/{user_id}` | 更新用户（部分更新）| Path: user_id, Body: UserUpdate JSON|
| DELETE | `/{user_id}` | 删除用户          | Path: user_id                      |

## 请求示例

**创建用户：**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com", "age": 28}'
```

**用户列表（分页）：**
```bash
curl "http://127.0.0.1:3002/api/v1/users/?skip=0&limit=10"
```

**获取单个用户：**
```bash
curl "http://127.0.0.1:3002/api/v1/users/1"
```

**部分更新：**
```bash
curl -X PUT "http://127.0.0.1:3002/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "李四"}'
```

**删除用户：**
```bash
curl -X DELETE "http://127.0.0.1:3002/api/v1/users/1"
```

## 响应状态码

| 状态码 | 含义           |
|--------|----------------|
| 200    | 请求成功       |
| 201    | 创建成功       |
| 204    | 删除成功       |
| 400    | 请求参数错误   |
| 404    | 用户不存在     |
| 409    | 邮箱冲突       |
| 422    | 请求体校验失败 |
| 500    | 服务器内部错误 |

## 用户字段

| 字段       | 类型     | 说明                 |
|-----------|---------|----------------------|
| id        | int     | 主键，自增           |
| name      | string  | 姓名，1-100 字符      |
| email     | string  | 邮箱，唯一           |
| age       | int     | 年龄，0-150，可选     |
| created_at| datetime| 创建时间（自动生成）  |
| updated_at| datetime| 更新时间（自动更新）  |

## 架构设计

```
HTTP 请求
    │
    ▼
Router (app/api/v1/users.py)  —— 参数解析，调用服务
    │
    ▼
Service (app/services/user.py) —— 业务逻辑，事务管理
    │
    ▼
Model (app/models/user.py) —— SQLAlchemy ORM
    │
    ▼
MySQL
```

异常由 `app/exceptions/handlers.py` 统一捕获并返回标准 JSON 错误响应。

## License

[MIT](LICENSE)
