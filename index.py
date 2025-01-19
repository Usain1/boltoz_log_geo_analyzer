from my_util import (
    parse_access_log,
    fetch_geolocation,
    count_by_region,
    get_top_region,
    write_to_json,
    load_config,
)

def main():

    # Step 1: Load configuration (in this case, API Key and Log File Path)
    config = load_config()

    # Step 2: Parse the access log and get a set of distinct source ip addresses 
    ip_list = parse_access_log(config["log_file_path"])
    print(f"Found {len(ip_list)} distinct IP addresses.")

    # Step 3:  Fetch geolocation data
    geo_data = fetch_geolocation(ip_list, config["api_key"])
    print(f"Geolocation data fetched for {len(geo_data)} IP addresses.")

    # Step 4: Count by region
    result = count_by_region(geo_data)

    # Step 5: Write result to JSON
    output_file = "geoip.json"
    write_to_json(result, output_file)
    print(f"Result written to {output_file}.")

    # Step 6: Get and print the top region
    top_country, top_continent = get_top_region(result)
    print(f"The country with the highest number of clients is {top_country}, while the continent is {top_continent}.")

if __name__ == "__main__":
    main()
