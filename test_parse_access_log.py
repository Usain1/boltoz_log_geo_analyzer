from my_util import parse_access_log

# Test parse_access_log
log_file = "access.log"  # Ensure this file exists with sample data
ip_list = parse_access_log(log_file)
print(f"Distinct IPs: {ip_list}")
