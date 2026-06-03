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
│   ├── api/
│   │   ├── response_route.py    # 自定义 APIRoute，统一 ApiResponse 包装
│   │   └── v1/
│   │       ├── auth.py           # 认证端点（登录）
│   │       ├── router.py        # v1 路由聚合
│   │       ├── users.py         # 用户 CRUD 端点
│   │       └── roles.py         # 角色 CRUD 端点
│   ├── models/
│   │   ├── __init__.py          # 模型导入（供 create_all）
│   │   ├── user.py              # SQLAlchemy User ORM 模型
│   │   └── role.py              # SQLAlchemy Role ORM 模型
│   ├── schemas/
│   │   ├── response.py          # ApiResponse 通用响应模型
│   │   ├── user.py              # Pydantic v2：UserCreate/UserUpdate/UserResponse/UserFilter
│   │   └── role.py              # Pydantic v2：RoleCreate/RoleUpdate/RoleResponse/RoleFilter
│   ├── services/
│   │   ├── auth.py              # JWT 认证逻辑
│   │   ├── user.py              # 用户业务逻辑层
│   │   └── role.py              # 角色业务逻辑层
│   └── exceptions/
│       └── handlers.py          # 自定义异常 & 全局异常处理器
├── init.sql                     # 数据库初始化脚本
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

### 2. 初始化数据库

**方式一：使用 SQL 脚本（推荐）**

```bash
mysql -u 用户名 -p < init.sql
```

**方式二：手动建库建表**

编辑 `.env` 文件，填写 MySQL 连接信息：

```
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/数据库名
```

创建数据库（如果还未创建）：

```bash
mysql -u 用户名 -p -e "CREATE DATABASE IF NOT EXISTS 数据库名 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

> 如果表还未创建，应用启动时会自动建表（`create_all`），无需手动执行。

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

### SQL 日志

开发时将 `.env` 中 `DEBUG` 设为 `true`，重启后终端会打印所有 SQL 语句。

### JWT 密钥

生产环境务必将 `.env` 中 `SECRET_KEY` 改为随机字符串：

```
SECRET_KEY=your-random-secret-key
```

## API 接口

### 认证接口

所有接口前缀：`/api/v1/auth`

| 方法 | 路径       | 说明              | 参数                   |
|------|-----------|-------------------|------------------------|
| POST | `/login`  | 邮箱密码登录       | Body: LoginRequest JSON |
| POST | `/refresh`| 刷新 token        | Body: RefreshRequest JSON |

> 登录成功返回 `access_token`（30 分钟有效）和 `refresh_token`（7 天有效）。调用其他接口时在请求头加上 `Authorization: Bearer <access_token>`。
> access_token 过期后用 `refresh_token` 调用 `/auth/refresh` 获取新 token。
> 创建用户接口无需登录（注册），其余所有接口均需 token 鉴权。

### 用户接口

所有接口前缀：`/api/v1/users`

| 方法   | 路径          | 说明              | 参数                                                  |
|--------|-------------|-------------------|------------------------------------------------------|
| POST   | `/`          | 创建用户          | Body: UserCreate JSON                                |
| GET    | `/`          | 用户列表          | Query: `skip`(默认0), `limit`(默认100), `name`(模糊), `age`(精确) |
| GET    | `/{user_id}` | 获取用户          | Path: user_id                                        |
| PUT    | `/{user_id}` | 更新用户（部分更新）| Path: user_id, Body: UserUpdate JSON                  |
| DELETE | `/{user_id}` | 删除用户          | Path: user_id                                        |

### 角色接口

所有接口前缀：`/api/v1/roles`

| 方法   | 路径          | 说明              | 参数                                                  |
|--------|-------------|-------------------|------------------------------------------------------|
| POST   | `/`          | 创建角色          | Body: RoleCreate JSON                                |
| GET    | `/`          | 角色列表          | Query: `skip`(默认0), `limit`(默认100), `name`(模糊)  |
| GET    | `/{role_id}` | 获取角色          | Path: role_id                                        |
| PUT    | `/{role_id}` | 更新角色          | Path: role_id, Body: RoleUpdate JSON                 |
| DELETE | `/{role_id}` | 删除角色          | Path: role_id                                        |

## 请求示例

**登录获取 token：**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "zhangsan@example.com", "password": "123456"}'
```

响应:
```json
{"code":200, "message":"操作成功", "data":{"access_token":"...", "refresh_token":"...", "token_type":"bearer"}}
```

**刷新 token：**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your-refresh-token"}'
```

**创建用户（注册）：**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com", "password": "123456", "age": 28}'
```

**用户列表（分页+过滤，需登录）：**
```bash
TOKEN="your-token-here"
curl "http://127.0.0.1:3002/api/v1/users/?skip=0&limit=10&name=张&age=28" \
  -H "Authorization: Bearer $TOKEN"
```

**获取单个用户：**
```bash
curl "http://127.0.0.1:3002/api/v1/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

**部分更新：**
```bash
curl -X PUT "http://127.0.0.1:3002/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "李四"}'
```

**创建角色：**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/roles/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "管理员", "description": "系统管理员"}'
```

**角色列表：**
```bash
curl "http://127.0.0.1:3002/api/v1/roles/?name=管理"
```

**删除用户：**
```bash
curl -X DELETE "http://127.0.0.1:3002/api/v1/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

## 响应状态码

| 状态码 | 含义           |
|--------|----------------|
| 200    | 请求成功       |
| 201    | 创建成功       |
| 204    | 删除成功       |
| 400    | 请求参数错误   |
| 401    | 未登录或 token 无效 |
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
| password  | string  | 密码，bcrypt 哈希存储 |
| age       | int     | 年龄，0-150，可选     |
| role_id   | int     | 角色 ID，可选         |
| created_at| datetime| 创建时间（自动生成）  |
| updated_at| datetime| 更新时间（自动更新）  |

## 角色字段

| 字段        | 类型     | 说明                 |
|------------|---------|----------------------|
| id         | int     | 主键，自增           |
| name       | string  | 角色名，1-50 字符，唯一|
| description| string  | 描述，0-200 字符，可选 |
| created_at | datetime| 创建时间（自动生成）  |
| updated_at | datetime| 更新时间（自动更新）  |

## 响应格式

所有接口统一返回以下 JSON 结构：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

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
