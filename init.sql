-- FastAPI Demo 数据库初始化脚本
-- 数据库需要先手动创建，本脚本只建表

CREATE DATABASE IF NOT EXISTS fastapi_demo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fastapi_demo;

-- 角色表
CREATE TABLE IF NOT EXISTS fastapi_roles (
    id          INT          NOT NULL AUTO_INCREMENT  PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL,
    description VARCHAR(200) DEFAULT NULL,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户表
CREATE TABLE IF NOT EXISTS fastapi_users (
    id          INT          NOT NULL AUTO_INCREMENT  PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL,
    age         INT          DEFAULT NULL,
    role_id     INT          DEFAULT NULL,
    password    VARCHAR(255) NOT NULL,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_email (email),
    INDEX       idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 请求日志表
CREATE TABLE IF NOT EXISTS fastapi_request_logs (
    id               INT           NOT NULL AUTO_INCREMENT  PRIMARY KEY,
    url              VARCHAR(2048) NOT NULL,
    method           VARCHAR(10)   NOT NULL,
    query_params     TEXT          DEFAULT NULL,
    request_body     TEXT          DEFAULT NULL,
    response_body    TEXT          DEFAULT NULL,
    status_code      INT           NOT NULL,
    response_time_ms INT           NOT NULL,
    client_ip        VARCHAR(45)   DEFAULT NULL,
    user_agent       VARCHAR(512)  DEFAULT NULL,
    request_headers  TEXT          DEFAULT NULL,
    user_id          INT           DEFAULT NULL,
    trace_id         CHAR(32)   DEFAULT NULL,
    created_at       DATETIME      DEFAULT CURRENT_TIMESTAMP,
    INDEX            idx_log_created_at (created_at),
    INDEX            idx_log_user_id (user_id),
    INDEX            idx_log_status_code (status_code),
    INDEX            idx_log_method_url (method, url(255)),
    INDEX            idx_log_trace_id (trace_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
