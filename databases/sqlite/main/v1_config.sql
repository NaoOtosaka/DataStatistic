-- 开发类型配置
INSERT INTO "develop_type" ( "type_name" )
VALUES
	( "前端开发" ),
	( "服务端开发" ),
	( "Android开发" ),
	( "IOS开发" );
	
-- BUG跟踪标签配置
INSERT INTO "bug_type" ("type_name")
VALUES
	("前端BUG"),
	("服务端BUG"),
	("Android BUG"),
	("IOS BUG");
	
	
-- BUG类型配置
INSERT INTO "bug_category" ("category_name")
VALUES
	("功能缺失"),
	("功能阻塞"),
	("环境异常"),
	("用例缺失"),
	("兼容性异常"),
	("部署异常");
	
	
-- 测试计划配置
INSERT INTO "test_plan" ("plan_name")
VALUES
	("冒烟测试"),
	("冒烟测试复核"),
	("一轮测试"),
	("二轮测试"),
	("兼容性测试"),
	("回归测试"),
	("线上验收");

	
-- QA人员配置
INSERT INTO "tester" ("name")
VALUES
-- 	("皮镜文"),
-- 	("杨顺"),
-- 	("石伟"),
-- 	("蔺子芹"),
-- 	("陈凯文"),
	("测试_test");
	
	
-- 开发人员配置
INSERT INTO "developer" ("name", "type_id")
VALUES
-- 	(""),
	("开发_test", 1);
	
	
-- 策划人员配置
INSERT INTO "planner" ("name")
VALUES
-- 	(""),
	("策划_test");
	
	

	

