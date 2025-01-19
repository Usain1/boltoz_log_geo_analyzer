from my_util import fetch_geolocation

# Replace with real IPs and your API key for testing
ip_list = ["140.206.225.232", "54.230.10.84","213.215.224.186"]
token = "f7d715493d0baa"
geo_data = fetch_geolocation(ip_list, token)
print(f"Geolocation Data: {geo_data}")
