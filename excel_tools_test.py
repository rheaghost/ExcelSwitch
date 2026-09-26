from excel_tools import list_tasks, execute

# 1. Discovery
print(list_tasks("clean"))   # should return 002, 003, 010, 014

# 2. Execution
result = execute("002", {
    "input": "templates/002_remove_duplicates/sample_data/sample.xlsx",
    "output": "templates/002_remove_duplicates/sample_data/test_out.xlsx",
})
print(result)