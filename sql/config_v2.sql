-- BUG类别配置
INSERT INTO "bug_category" ("category_name")
VALUES
	("功能缺失"),
	("功能阻塞"),
	("环境异常"),
	("用例缺失"),
	("兼容性异常"),
	("部署异常");
	
	
-- BUG跟踪标签配置
INSERT INTO "bug_type" ("type_name")
VALUES
	("前端BUG"),
	("服务端BUG"),
	("Android BUG"),
	("IOS BUG");
	
	
-- 开发类别配置
INSERT INTO "develop_type" ("type_name")
VALUES
	("前端开发"),
	("服务端开发"),
	("Android开发"),
	("IOS开发");
	

-- 测试阶段配置
INSERT INTO "test_plan" ("plan_name")
VALUES
	("冒烟测试"),
	("冒烟测试复核"),
	("一轮测试"),
	("二轮测试"),
	("兼容性测试"),
	("弱网测试"),
	("压力测试"),
	("灵敏度测试"),
	("性能测试"),
	("单元测试"),
	("回归测试"),
	("线上验收");
	
	
