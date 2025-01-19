from my_util import count_by_region

# Sample geo_data for testing
geo_data = [
    {'ip': '140.206.225.232', 'country': 'China', 'continent': 'Asia'},
    {'ip': '54.230.10.84', 'country': 'United Kingdom', 'continent': 'Europe'},
    {'ip': '213.215.224.186', 'country': 'Italy', 'continent': 'Europe'}
]
result = count_by_region(geo_data)
print(f"Count by Region: {result}")
