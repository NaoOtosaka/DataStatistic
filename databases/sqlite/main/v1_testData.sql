-- 创建项目
INSERT INTO "project" ("planner_id", "project_name")
VALUES
	( 1, "测试用项目" );
	
	
-- 生成测试阶段
INSERT INTO "project_phases" ("project_id", "plan_id", "start_time", "end_time")
VALUES
	( 1, 1, "1607081154936", "1607082154936");


-- 定义BUG
INSERT INTO "bug" ("phases_id", "tester_id", "developer_id", "bug_type", "category", "title", "create_time", "close_time", "is_finished", "is_closed", "is_online")
VALUES
	( 1, 1, 1, 1, 1, "测试用BUG", "1607081154936", NULL, "FALSE", "FALSE", "TRUE");