-- SELECT * 
-- FROM bug, tester, developer, bug_type, bug_category 
-- WHERE
-- bug.tester_id = tester.tester_id AND bug.developer_id = developer.developer_id AND bug.bug_type = bug_type.type_id AND bug.category = bug_category.category_id;


SELECT * 
FROM bug, project_phases, project, test_plan
WHERE
bug.phases_id = project_phases.phases_id AND project_phases.project_id = project.project_id AND project_phases.plan_id = test_plan.plan_id
AND bug_id = 1;