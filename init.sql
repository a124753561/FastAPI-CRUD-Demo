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
