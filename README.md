# HTTP Access Log Geolocation

This Python script processes an HTTP access log file to identify unique client IPs, fetch their geolocation data, and generate a JSON summary of the results. It also identifies the country and continent with the highest number of requests.

## Features: 
- Parse an access log file to extract unique IP addresses.
- Fetch geolocation data for each IP using the IPinfo API.
- Handle rate-limiting errors from the API gracefully.
- Summarize the number of requests by continent and country.
- Output results as a JSON file.
- Highlight the country and continent with the highest number of requests.

## Requirements:
- `Python 3.7` or later
- `requests` library
- `configparser` library (standard in Python)

## Usage: 
Run the script: `python3 index.py`

## Output
The script will output the number of distinct IPs and write the JSON summary to result.json:
```json
{
   "Europe": {
      "total_count": 10,
      "country": {
         "Italy": 8,
         "France": 2
      }
   },
   ...
   "unknown": {
      "total_count": 7
   }
}
```
The script will also display:
```csharp
The country with the highest number of requests is Italy, while the continent is Europe.
```

## Notes:
- If the API key is missing, it prints an error message and stops the program using sys.exit(1). 
- Ensure the API key provided has sufficient quota for the requests.
- Handle rate-limiting errors by ensuring the script retries after a wait period.
