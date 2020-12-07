-- BUG跟踪标签表
CREATE TABLE "main"."bug_type" (
  "type_id" INTEGER NOT NULL,
  "type_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("type_id")
);


-- BUG类型表
CREATE TABLE "main"."bug_category" (
  "category_id" INTEGER NOT NULL,
  "category_name" NVARCHAR(16) NOT NULL,
  PRIMARY KEY ("category_id")
);


-- 开发类型表
CREATE TABLE "main"."develop_type" (
	"type_id" INTEGER NOT NULL,
	"type_name" NVARCHAR(16) NOT NULL,
	PRIMARY KEY ("type_id")
);


-- 测试人员表
CREATE TABLE "main"."tester" (
	"tester_id" INTEGER NOT NULL,
	"name" NVARCHAR(16) NOT NULL,
	PRIMARY KEY ("tester_id")
);


-- 策划人员表
CREATE TABLE "main"."planner" (
	"planner_id" INTEGER NOT NULL,
	"name" NVARCHAR(16) NOT NULL,
	PRIMARY KEY ("planner_id")
);


-- 开发人员表
CREATE TABLE "main"."developer" (
	"developer_id" INTEGER NOT NULL,
	"type_id" INTEGER NOT NULL,
	"name" NVARCHAR(16) NOT NULL,
	PRIMARY KEY ("developer_id"),
	CONSTRAINT "typeId" FOREIGN KEY ("type_id") REFERENCES "develop_type" ("type_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- 项目表
CREATE TABLE "main"."project" (
	"project_id" INTEGER NOT NULL,
	"planner_id" INTEGER NOT NULL,
	"project_name" NVARCHAR(255) NOT NULL,
	PRIMARY KEY ("project_id"),
	CONSTRAINT "plannerId" FOREIGN KEY ("planner_id") REFERENCES "planner" ("planner_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- 测试跟进表
CREATE TABLE "main"."test" (
	"tester_id" INTEGER NOT NULL,
	"project_id" INTEGER NOT NULL,
	CONSTRAINT "testerId" FOREIGN KEY ("tester_id") REFERENCES "tester" ("tester_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- 开发跟进表
CREATE TABLE "main"."develop" (
	"project_id" INTEGER NOT NULL,
	"developer_id" INTEGER NOT NULL,
	CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "developerId" FOREIGN KEY ("developer_id") REFERENCES "developer" ("developer_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- 测试计划表
CREATE TABLE "main"."test_plan" (
	"plan_id" INTEGER NOT NULL,
	"plan_name" NVARCHAR(16) NOT NULL,
	PRIMARY KEY ("plan_id")
);


-- 项目阶段表
CREATE TABLE "main"."project_phases" (
	"phases_id" INTEGER NOT NULL,
	"project_id" INTEGER NOT NULL,
	"plan_id" INTEGER NOT NULL,
	"start_time" TIMESTAMP,
	"end_time" TIMESTAMP,
	PRIMARY KEY ("phases_id"),
	CONSTRAINT "projectId" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "planId" FOREIGN KEY ("plan_id") REFERENCES "test_plan" ("plan_id") ON DELETE CASCADE ON UPDATE CASCADE
);


-- BUG信息表
CREATE TABLE "main"."bug" (
	"bug_id" INTEGER NOT NULL,
	"phases_id" INTEGER NOT NULL,
	"tester_id" INTEGER NOT NULL,
	"developer_id" INTEGER NOT NULL,
	"bug_type" INTEGER NOT NULL,
	"category" INTEGER NOT NULL,
	"title" NVARCHAR(255),
	"create_time" TIMESTAMP,
	"close_time" TIMESTAMP,
	"is_finished" BOOLEAN,
	"is_closed" BOOLEAN,
	"is_online" BOOLEAN,
	PRIMARY KEY ("bug_id"),
	CONSTRAINT "phasesId" FOREIGN KEY ("phases_id") REFERENCES "project_phases" ("phases_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "testerId" FOREIGN KEY ("tester_id") REFERENCES "tester" ("tester_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "developerId" FOREIGN KEY ("developer_id") REFERENCES "developer" ("developer_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "bugType" FOREIGN KEY ("bug_type") REFERENCES "bug_type" ("type_id") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "Category" FOREIGN KEY ("category") REFERENCES "bug_category" ("category_id") ON DELETE CASCADE ON UPDATE CASCADE
);


