from my_util import get_top_region

# Sample result for testing
result = {
    "North America": {"total_count": 10, "country": {"United States": 5, "Canada": 5}},
    "Oceania": {"total_count": 6, "country": {"Australia": 6}},
    "unknown": {"total_count": 2, "country": {}}
}
top_country, top_continent = get_top_region(result)
print(f"Top Country: {top_country}, Top Continent: {top_continent}")
