import pynamodb

from src.utils.handlers.models import Plans


test_plan = Plans(name="test", conditions=["test1", "test2"])
print(test_plan.id)
print(test_plan.name)
print(test_plan.conditions)
print(test_plan.last_updated)

print("PLAN CREATE")
Plans.create(name="test-create5", conditions=["test-create-3", "test-create-2"])

print("PLAN UPDATE BY ID (CREATE FUNCTION)")
Plans.create(id_="b12fff30-957b-409e-a6b8-50a9e7f26f90", name="test-create5", conditions=["test-create-3", "test-create-2"])

print("ALL PLANS SCAN")
plan_records, total_records = Plans.get_records()
print(total_records)
for plan in plan_records:
    print(plan.to_dict())

print("PLANS QUERY BY ID")
plan_by_id = Plans.get_record_by_id(id_="8e46f619-610e-4e65-812a-d42b884197f4")
for plan in plan_by_id:
    print(plan.to_dict())