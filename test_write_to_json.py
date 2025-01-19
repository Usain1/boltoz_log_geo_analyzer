from my_util import write_to_json

# Sample result for testing
result = {
    "North America": {"total_count": 10, "country": {"United States": 5, "Canada": 5}},
    "Oceania": {"total_count": 5, "country": {"Australia": 5}},
    "unknown": {"total_count": 2, "country": {}}
}
output_file = "test_result.json"
write_to_json(result, output_file)
print(f"Result written to {output_file}.")
