-- BUG类型表
DROP TABLE IF EXISTS "bug_category";
CREATE TABLE "bug_category" (
  "category_id" INTEGER NOT NULL,
  "category_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("category_id")
);


-- BUG跟踪标签
DROP TABLE IF EXISTS "bug_type";
CREATE TABLE "bug_type" (
  "type_id" INTEGER NOT NULL,
  "type_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("type_id")
);


-- 测试阶段表
DROP TABLE IF EXISTS "test_plan";
CREATE TABLE "test_plan" (
  "plan_id" INTEGER NOT NULL,
  "plan_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("plan_id")
);


-- 开发标签表
DROP TABLE IF EXISTS "develop_type";
CREATE TABLE "develop_type" (
  "type_id" INTEGER NOT NULL,
  "type_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("type_id")
);


-- 策划表
DROP TABLE IF EXISTS "planner";
CREATE TABLE "planner" (
  "planner_id" INTEGER NOT NULL,
  "name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("planner_id")
);


-- 开发表
DROP TABLE IF EXISTS "developer";
CREATE TABLE "developer" (
  "developer_id" INTEGER NOT NULL,
  "type_id" INTEGER NOT NULL,
  "name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("developer_id"),
  CONSTRAINT "typeId" FOREIGN KEY ("type_id") REFERENCES "develop_type" ("type_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- QA表
DROP TABLE IF EXISTS "tester";
CREATE TABLE "tester" (
  "tester_id" INTEGER NOT NULL,
  "name" NVARCHAR(16) NOT NULL,
	"email" VARCHAR(255) NOT NULL,
  PRIMARY KEY ("tester_id")
);


-- 项目表
DROP TABLE IF EXISTS "project";
CREATE TABLE "project" (
  "project_id" INTEGER NOT NULL,
  "planner_id" INTEGER NOT NULL,
  "project_name" NVARCHAR(255) NOT NULL,
  PRIMARY KEY ("project_id"),
  CONSTRAINT "plannerId" FOREIGN KEY ("planner_id") REFERENCES "planner" ("planner_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- 项目进度表
DROP TABLE IF EXISTS "project_phases";
CREATE TABLE "project_phases" (
	"phase_id" INTEGER NOT NULL,
	"project_id" INTEGER NOT NULL,
	"plan_id" INTEGER NOT NULL,
	"start_time" TIMESTAMP,
	"end_time" TIMESTAMP,
	PRIMARY KEY ("phase_id"),
	CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "planId" FOREIGN KEY ("plan_id") REFERENCES "test_plan" ("plan_id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- 开发跟进表
DROP TABLE IF EXISTS "develop";
CREATE TABLE "develop" (
  "project_id" INTEGER NOT NULL,
  "developer_id" INTEGER NOT NULL,
  CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "developerId" FOREIGN KEY ("developer_id") REFERENCES "developer" ("developer_id") ON DELETE CASCADE ON UPDATE CASCADE
);



-- 测试跟进表
DROP TABLE IF EXISTS "test";
CREATE TABLE "test" (
  "tester_id" INTEGER NOT NULL,
  "project_id" INTEGER NOT NULL,
  CONSTRAINT "testerId" FOREIGN KEY ("tester_id") REFERENCES "tester" ("tester_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- BUG表
DROP TABLE IF EXISTS "bug";
CREATE TABLE "bug" (
  "bug_id" INTEGER NOT NULL,
  "tester_id" INTEGER NOT NULL,
  "developer_id" INTEGER NOT NULL,
	"phase_id" INTEGER NOT NULL,
	"bug_type" INTEGER NOT NULL,
  "category" INTEGER NOT NULL,
  "title" NVARCHAR(255),
  "create_time" TIMESTAMP,
  "close_time" TIMESTAMP,
  "is_finished" BOOLEAN,
  "is_closed" BOOLEAN,
  "is_online" BOOLEAN,
  PRIMARY KEY ("bug_id"),
  CONSTRAINT "testerId" FOREIGN KEY ("tester_id") REFERENCES "tester" ("tester_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "developerId" FOREIGN KEY ("developer_id") REFERENCES "developer" ("developer_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "phaseId" FOREIGN KEY ("phase_id") REFERENCES "project_phases" ("phase_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "bugType" FOREIGN KEY ("bug_type") REFERENCES "bug_type" ("type_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "Category" FOREIGN KEY ("category") REFERENCES "bug_category" ("category_id") ON DELETE CASCADE ON UPDATE CASCADE
);
