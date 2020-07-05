import pynamodb

from src.utils.handlers.models import Plans

print("PLAN CREATE")
Plans.create(name="test-create7", conditions=["test-create-3", "test-create-2"])

print("PLAN UPDATE BY ID (CREATE FUNCTION)")
Plans.create(name="test-create6", conditions=["test-create-3", "test-create-2"])

print("ALL PLANS SCAN")
plan_records, total_records, last_evaluated_key = Plans.get_records()
print(total_records)
print(last_evaluated_key)
for plan in plan_records:
    print(plan.to_dict())
    # plan.delete_record()

print("PLANS QUERY BY ID")
plan_by_id = Plans.get_record_by_id(id_="8e46f619-610e-4e65-812a-d42b884197f4")
for plan in plan_by_id:
    print(plan.to_dict())
