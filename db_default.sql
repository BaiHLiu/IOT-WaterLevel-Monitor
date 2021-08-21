/*
 Navicat Premium Data Transfer

 Source Server         : pycharm
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 21/08/2021 21:36:27
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alarm_log
-- ----------------------------
DROP TABLE IF EXISTS "alarm_log";
CREATE TABLE "alarm_log" (
"alarm_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
"sensor_id" integer,
"dev_id" integer,
"type" integer,
"water_level" integer,
"datetime" date
);

-- ----------------------------
-- Table structure for dev_info
-- ----------------------------
DROP TABLE IF EXISTS "dev_info";
CREATE TABLE "dev_info" (
  "dev_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "dev_name" TEXT(50) NOT NULL,
  "dev_port" TEXT(6),
  "last_upload_datetime" DATE NOT NULL DEFAULT '',
  "alarm_params" TEXT(200) NOT NULL DEFAULT '',
  "upload_count" integer(20) NOT NULL DEFAULT 0,
  "interval_time" integer(6) DEFAULT 5,
  "distance_query_arg" TEXT NOT NULL DEFAULT '',
  "temperature_query_arg" TEXT NOT NULL DEFAULT ''
);

-- ----------------------------
-- Table structure for sensor_info
-- ----------------------------
DROP TABLE IF EXISTS "sensor_info";
CREATE TABLE "sensor_info" (
  "sensor_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "sensor_name" TEXT,
  "bind_dev_id" INTEGER NOT NULL,
  "distance_offset" integer(5),
  "hex_address" TEXT(10) NOT NULL,
  "home_graph" integer,
  "ground_level" integer DEFAULT 0
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Table structure for upload_log
-- ----------------------------
DROP TABLE IF EXISTS "upload_log";
CREATE TABLE "upload_log" (
  "upload_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "dev_id" INTEGER,
  "dev_ip" TEXT(20) NOT NULL,
  "sensor_id" INTEGER,
  "sensor_distance" integer(5) NOT NULL,
  "sensor_temperature" integer(5,2) NOT NULL,
  "datetime" date NOT NULL
);

-- ----------------------------
-- Auto increment value for alarm_log
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 9 WHERE name = 'alarm_log';

-- ----------------------------
-- Auto increment value for dev_info
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 13 WHERE name = 'dev_info';

-- ----------------------------
-- Auto increment value for sensor_info
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 11 WHERE name = 'sensor_info';

-- ----------------------------
-- Auto increment value for upload_log
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 49429 WHERE name = 'upload_log';

PRAGMA foreign_keys = true;
