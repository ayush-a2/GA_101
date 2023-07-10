employees = [
    {"name": "john", "salary": 3000, "designation": "developer"},
    {"name": "Emma", "salary": 4000, "designation": "manager"},
    {"name": "sonu", "salary": 55000, "designation": "tester"}
 
]

max_salary = 0
max_salary_employee = {}

for employee in employees:
    if employee["salary"] > max_salary:
        max_salary = employee["salary"]
        max_salary_employee = employee

print("maximum salary:")
print(max_salary_employee)
