import json
import requests
from collections import defaultdict
import time
import configparser
import sys
import os

#Mapping of country codes to country names (to be used in fetch_geolocation)
country_name_mapping = {
    "US": "United States of America",
    "CA": "Canada",
    "IN": "India",
    "CN": "China",
    "RU": "Russia",
    "BR": "Brazil",
    "AU": "Australia",
    "ZA": "South Africa",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "IT": "Italy",
    "JP": "Japan",
    "KR": "South Korea",
    "MX": "Mexico",
    "AR": "Argentina",
    "ID": "Indonesia",
    "NG": "Nigeria",
    "PK": "Pakistan",
    "SA": "Saudi Arabia",
    "EG": "Egypt",
    "PE": "Peru",
    "CL": "Chile",
    "CO": "Colombia",
    "PL": "Poland",
    "VN": "Vietnam",
    "TH": "Thailand",
    "BD": "Bangladesh",
    "MY": "Malaysia",
    "PH": "Philippines",
    "UA": "Ukraine",
    "KE": "Kenya",
    "KR": "South Korea",
    "SG": "Singapore",
    "TW": "Taiwan",
    "IR": "Iran",
    "SY": "Syria",
    "QA": "Qatar",
    "KW": "Kuwait",
    "JO": "Jordan",
    "TR": "Turkey",
    "EG": "Egypt",
    "IQ": "Iraq",
    "AE": "United Arab Emirates",
    "LV": "Latvia",
    "LT": "Lithuania",
    "EE": "Estonia",
    "FI": "Finland",
    "SE": "Sweden",
    "NO": "Norway",
    "BG": "Bulgaria",
    "RO": "Romania",
    "RS": "Serbia",
    "HR": "Croatia",
    "MK": "North Macedonia",
    "AL": "Albania",
    "BH": "Bahrain",
    "CY": "Cyprus",
    "MD": "Moldova",
    "BA": "Bosnia and Herzegovina",
    "ME": "Montenegro",
    "XK": "Kosovo",
    "AM": "Armenia",
    "BY": "Belarus",
    "GE": "Georgia",
    "MO": "Macao",
    "KZ": "Kazakhstan",
    "TJ": "Tajikistan",
    "UZ": "Uzbekistan",
    "TM": "Turkmenistan",
    "MN": "Mongolia",
    "KG": "Kyrgyzstan",
    "LA": "Laos",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
    "AF": "Afghanistan",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Democratic Republic of the Congo",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Cote d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IL": "Israel",
    "IM": "Isle of Man",
    "IT": "Italy",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KW": "Kuwait",
    "LA": "Laos",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libya",
    "MA": "Morocco",
    "MD": "Moldova",
    "ME": "Montenegro",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "MK": "Macedonia",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "Saint Pierre and Miquelon",
    "PR": "Puerto Rico",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Reunion",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russia",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "Saint Helena",
    "SI": "Slovenia",
    "SJ": "Svalbard",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "SS": "South Sudan",
    "ST": "São Tomé and Príncipe",
    "SV": "El Salvador",
    "SX": "Sint Maarten",
    "SY": "Syria",
    "SZ": "Swaziland",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TL": "Timor-Leste",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TR": "Turkey",
    "TT": "Trinidad and Tobago",
    "TV": "Tuvalu",
    "TZ": "Tanzania",
    "UA": "Ukraine",
    "UG": "Uganda",
    "US": "United States of America",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Vatican City",
    "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela",
    "VG": "British Virgin Islands",
    "VI": "United States Virgin Islands",
    "VN": "Vietnam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "YE": "Yemen",
    "YT": "Mayotte",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

# Mapping of country codes to continents (to be used in fetch_geolocation)
continent_mapping = {
    "US": "North America",
    "CA": "North America",
    "IN": "Asia",
    "CN": "Asia",
    "RU": "Europe",
    "BR": "South America",
    "AU": "Oceania",
    "ZA": "Africa",
    "GB": "Europe",
    "DE": "Europe",
    "FR": "Europe",
    "IT": "Europe",
    "JP": "Asia",
    "KR": "Asia",
    "MX": "North America",
    "AR": "South America",
    "ID": "Asia",
    "NG": "Africa",
    "PK": "Asia",
    "SA": "Asia",
    "EG": "Africa",
    "PE": "South America",
    "CL": "South America",
    "CO": "South America",
    "PL": "Europe",
    "VN": "Asia",
    "TH": "Asia",
    "BD": "Asia",
    "MY": "Asia",
    "PH": "Asia",
    "UA": "Europe",
    "KE": "Africa",
    "KR": "Asia",
    "SG": "Asia",
    "TW": "Asia",
    "IR": "Asia",
    "SY": "Asia",
    "PK": "Asia",
    "QA": "Asia",
    "KW": "Asia",
    "JO": "Asia",
    "TR": "Europe",
    "EG": "Africa",
    "KE": "Africa",
    "IQ": "Asia",
    "AE": "Asia",
    "LV": "Europe",
    "LT": "Europe",
    "EE": "Europe",
    "FI": "Europe",
    "SE": "Europe",
    "PL": "Europe",
    "NO": "Europe",
    "BG": "Europe",
    "RO": "Europe",
    "RS": "Europe",
    "HR": "Europe",
    "MK": "Europe",
    "AL": "Europe",
    "BH": "Asia",
    "CY": "Europe",
    "MD": "Europe",
    "BA": "Europe",
    "ME": "Europe",
    "XK": "Europe",
    "AM": "Asia",
    "BY": "Europe",
    "GE": "Asia",
    "MO": "Asia",
    "KZ": "Asia",
    "TJ": "Asia",
    "UZ": "Asia",
    "TM": "Asia",
    "MN": "Asia",
    "KG": "Asia",
    "LA": "Asia",
    "ZM": "Africa",
    "ZW": "Africa",
    "AF": "Asia",
    "AL": "Europe",
    "DZ": "Africa",
    "AS": "Oceania",
    "AD": "Europe",
    "AO": "Africa",
    "AI": "Caribbean",
    "AR": "South America",
    "AM": "Asia",
    "AW": "Caribbean",
    "AU": "Oceania",
    "AT": "Europe",
    "AZ": "Asia",
    "BS": "Caribbean",
    "BH": "Asia",
    "BD": "Asia",
    "BB": "Caribbean",
    "BY": "Europe",
    "BE": "Europe",
    "BZ": "Central America",
    "BJ": "Africa",
    "BM": "Caribbean",
    "BT": "Asia",
    "BO": "South America",
    "BA": "Europe",
    "BW": "Africa",
    "BR": "South America",
    "IO": "Oceania",
    "BN": "Asia",
    "BG": "Europe",
    "BF": "Africa",
    "BI": "Africa",
    "KH": "Asia",
    "CM": "Africa",
    "CA": "North America",
    "CV": "Africa",
    "KY": "Caribbean",
    "CF": "Africa",
    "TD": "Africa",
    "CL": "South America",
    "CN": "Asia",
    "CO": "South America",
    "KM": "Africa",
    "CG": "Africa",
    "CD": "Africa",
    "CK": "Oceania",
    "CR": "Central America",
    "CI": "Africa",
    "HR": "Europe",
    "CU": "Caribbean",
    "CY": "Europe",
    "CZ": "Europe",
    "DK": "Europe",
    "DJ": "Africa",
    "DM": "Caribbean",
    "DO": "Caribbean",
    "EC": "South America",
    "EG": "Africa",
    "SV": "Central America",
    "GQ": "Africa",
    "ER": "Africa",
    "EE": "Europe",
    "ET": "Africa",
    "FO": "Europe",
    "FJ": "Oceania",
    "FI": "Europe",
    "FR": "Europe",
    "GA": "Africa",
    "GM": "Africa",
    "GE": "Asia",
    "GH": "Africa",
    "GI": "Europe",
    "GR": "Europe",
    "GL": "North America",
    "GD": "Caribbean",
    "GP": "Caribbean",
    "GU": "Oceania",
    "GT": "Central America",
    "GN": "Africa",
    "GW": "Africa",
    "GY": "South America",
    "HT": "Caribbean",
    "HN": "Central America",
    "HK": "Asia",
    "HU": "Europe",
    "IS": "Europe",
    "IN": "Asia",
    "ID": "Asia",
    "IR": "Asia",
    "IQ": "Asia",
    "IE": "Europe",
    "IL": "Europe",
    "IM": "Europe",
    "IT": "Europe",
    "JM": "Caribbean",
    "JO": "Asia",
    "JP": "Asia",
    "KE": "Africa",
    "KG": "Asia",
    "KH": "Asia",
    "KI": "Oceania",
    "KM": "Africa",
    "KW": "Asia",
    "LA": "Asia",
    "LS": "Africa",
    "LT": "Europe",
    "LU": "Europe",
    "LV": "Europe",
    "LY": "Africa",
    "MA": "Africa",
    "MD": "Europe",
    "ME": "Europe",
    "MG": "Africa",
    "MH": "Oceania",
    "MK": "Europe",
    "ML": "Africa",
    "MM": "Asia",
    "MN": "Asia",
    "MO": "Asia",
    "MP": "Oceania",
    "MQ": "Caribbean",
    "MR": "Africa",
    "MS": "Caribbean",
    "MT": "Europe",
    "MU": "Africa",
    "MV": "Asia",
    "MW": "Africa",
    "MX": "North America",
    "MY": "Asia",
    "MZ": "Africa",
    "NA": "Africa",
    "NC": "Oceania",
    "NE": "Africa",
    "NF": "Oceania",
    "NG": "Africa",
    "NI": "Central America",
    "NL": "Europe",
    "NO": "Europe",
    "NP": "Asia",
    "NR": "Oceania",
    "NU": "Oceania",
    "NZ": "Oceania",
    "OM": "Asia",
    "PA": "Central America",
    "PE": "South America",
    "PF": "Oceania",
    "PG": "Oceania",
    "PH": "Asia",
    "PK": "Asia",
    "PL": "Europe",
    "PM": "North America",
    "PR": "Caribbean",
    "PT": "Europe",
    "PW": "Oceania",
    "PY": "South America",
    "QA": "Asia",
    "RE": "Africa",
    "RO": "Europe",
    "RS": "Europe",
    "RU": "Europe",
    "RW": "Africa",
    "SA": "Asia",
    "SB": "Oceania",
    "SC": "Africa",
    "SD": "Africa",
    "SE": "Europe",
    "SG": "Asia",
    "SH": "Africa",
    "SI": "Europe",
    "SJ": "Europe",
    "SK": "Europe",
    "SL": "Africa",
    "SM": "Europe",
    "SN": "Africa",
    "SO": "Africa",
    "SR": "South America",
    "SS": "Africa",
    "ST": "Africa",
    "SV": "Central America",
    "SX": "Caribbean",
    "SY": "Asia",
    "SZ": "Africa",
    "TC": "Caribbean",
    "TD": "Africa",
    "TF": "Oceania",
    "TG": "Africa",
    "TH": "Asia",
    "TJ": "Asia",
    "TK": "Oceania",
    "TL": "Asia",
    "TM": "Asia",
    "TN": "Africa",
    "TO": "Oceania",
    "TR": "Asia",
    "TT": "Caribbean",
    "TV": "Oceania",
    "TZ": "Africa",
    "UA": "Europe",
    "UG": "Africa",
    "US": "North America",
    "UY": "South America",
    "UZ": "Asia",
    "VA": "Europe",
    "VC": "Caribbean",
    "VE": "South America",
    "VG": "Caribbean",
    "VI": "Caribbean",
    "VN": "Asia",
    "VU": "Oceania",
    "WF": "Oceania",
    "WS": "Oceania",
    "YE": "Asia",
    "YT": "Africa",
    "ZA": "Africa",
    "ZM": "Africa",
    "ZW": "Africa"
}

def load_config(config_path="config.ini"):
    """
    Loads the API key and access log file path from the config file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: A dictionary with 'api_key' and 'log_file_path'.

    Raises:
        ValueError: If the API key or log file path is missing in the config file.
    """
    # Parse the config file
    config = configparser.ConfigParser()
    config.read(config_path)

    # Get API key
    api_key = config.get("API", "key", fallback=None)
    if not api_key:
        raise ValueError("Error: API key not found in the config file.")

    # Get access log file path
    log_file_path = config.get("LOGS", "access_log", fallback=None)
    if not log_file_path:
        raise ValueError("Error: Access log file path not found in the config file.")

    # Validate log file path (if necessary)
    if not os.path.isfile(log_file_path):
        raise ValueError(f"Error: The specified log file '{log_file_path}' does not exist.")

    return {"api_key": api_key, "log_file_path": log_file_path}

def parse_access_log(file_path):
    """
    Parse the access log file to extract distinct IPs.
    
    Args:
        file_path (str): Path to the access log file.

    Returns:
        list: List of distinct IP addresses.   
    """
    ip_set = set() # Use a set to store unique IP addresses
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.split()
                if parts:
                    ip_set.add(parts[0])  # Extract the source IP address
    except Exception as e:
        raise ValueError(f"Error reading the file '{file_path}': {e}")

    return list(ip_set)

def fetch_geolocation(ip_list, token):
    """
    Fetch geolocation data for a list of IP addresses from ipinfo.io.

    Args:
        ip_list (list): List of IP addresses.
        token (str): The API token for the IP geolocation service.

    Returns:
        list: List of dictionaries containing IP, country, and continent.
    """
    geo_data = []
    base_url = "https://ipinfo.io"

    for ip in ip_list:
        try:
            response = requests.get(f"{base_url}/{ip}?token={token}")
            
            if response.status_code == 200:
                data = response.json()
                country_code = data.get('country', 'unknown')

                # Get country name and continent from mappings
                country_name = country_name_mapping.get(country_code, 'Unknown')
                continent = continent_mapping.get(country_code, 'Unknown')

            elif response.status_code == 429:  # Too Many Requests
                print("Rate limit hit. Retrying after delay...")
                time.sleep(5)  # Wait before retrying
                continue  # Retry the same IP

            elif response.status_code in [401, 403]:  # Unauthorized
                sys.exit("Invalid API key or Lack of permission")  # End the program with an error code

            else:
                print(f"Warning: Received status code {response.status_code} when testing API key")
                country_name = continent = 'unknown'
        
        except Exception as e:
            print(f"Error fetching data for IP {ip}: {e}")
            country_name = continent = 'unknown'

        geo_data.append({
            'ip': ip,
            'country': country_name,
            'continent': continent
        })

    return geo_data

def count_by_region(geo_data):
    """
    Count IP addresses by continent and country.

    Args:
        geo_data (list): List of dictionaries containing IP, country, and continent.

    Returns:
        dict: Nested dictionary with counts per continent and country.
    """
    result = defaultdict(lambda: {"total_count": 0, "country": defaultdict(int)})

    for entry in geo_data:
        continent = entry['continent']
        country = entry['country']
        result[continent]['total_count'] += 1
        if country != 'unknown':
            result[continent]['country'][country] += 1

    # Convert defaultdict to regular dict for output
    for continent, data in result.items():
        data['country'] = dict(data['country'])
    return dict(result)

def get_top_region(result):
    """
    Get the continent and country with the highest number of requests.

    Args:
        result (dict): Nested dictionary with counts per continent and country.

    Returns:
        tuple: (country, continent) with the highest counts.
    """
    max_country = None
    max_continent = None
    max_country_count = 0
    max_continent_count = 0

    for continent, data in result.items():
        if data['total_count'] > max_continent_count:
            max_continent_count = data['total_count']
            max_continent = continent

        for country, count in data['country'].items():
            if count > max_country_count:
                max_country_count = count
                max_country = country

    return max_country, max_continent

def write_to_json(result, output_file):
    """
    Write the result to a JSON file.

    Args:
        result (dict): The data to write.
        output_file (str): Path to the output JSON file.
    """
    with open(output_file, 'w') as file:
        json.dump(result, file, indent=4)


