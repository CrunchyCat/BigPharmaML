import pickle
import requests
import sys
import csv
import re
from functools import lru_cache

# Configuration
USPS_API_KEY = "" #TODO: PUT API KEY HERE
ZIPCODE_PICKLE_LOCATION = "./Tools/zipcodes.pkl"

# Constants
ENDPOINT_USPS_ZIP = "https://secure.shippingapis.com/ShippingAPI.dll?API= CityStateLookup&XML="
ENDPOINT_USPS_ADD = "https://secure.shippingapis.com/ShippingAPI.dll?API= ZipCodeLookup&XML="
zipcodes: dict[str, tuple[str, str]] = {}

# Get Info from USPS API using ZipCode
@lru_cache(maxsize=None)
def usps_get_zip_info(zipcode: str) -> tuple[str, str]:
    if zipcode in zipcodes:
        return zipcodes[zipcode]
    print('Fetching City/State for {}...'.format(zipcode))
    request = f"<CityStateLookupRequest USERID=\"{USPS_API_KEY}\"><ZipCode ID='0'><Zip5>{zipcode}</Zip5></ZipCode></CityStateLookupRequest>"
    response = requests.get(ENDPOINT_USPS_ZIP + request)
    split = re.search("<Zip5>(.*)</Zip5><City>(.*)</City><State>(.*)</State>", response.text)
    if split is None:
        print('Failed to fetch info for {}'.format(zipcode))
        return ('', '')
    else:
        print('Found: City={} State={}'.format(split.group(2), split.group(3)))
        zipcodes[zipcode] = (split.group(2), split.group(3))
        with open (ZIPCODE_PICKLE_LOCATION, 'wb') as f:
            pickle.dump(zipcodes, f, protocol=pickle.HIGHEST_PROTOCOL)
    return (split.group(2), split.group(3))

# Get Info from USPS API using ZipCode
@lru_cache(maxsize=None)
def usps_get_add_info(addr: str, city: str, state: str) -> tuple[str, str, str]:
    # print('Fetching ZipCode for {}, {}, {}...'.format(addr, city, state))
    request = f"<ZipCodeLookupRequest USERID=\"{USPS_API_KEY}\"><Address ID=\"1\"><Address2>{addr}</Address2><City>{city}</City><State>{state}</State></Address></ZipCodeLookupRequest>"
    response = requests.get(ENDPOINT_USPS_ADD + request)
    split = re.search("<Address2>(.*)</Address2><City>(.*)</City><State>(.*)</State><Zip5>(.*)</Zip5>", response.text)
    if split is None:
        print('Failed to fetch info for {}, {}, {}'.format(addr, city, state))
        return (city, state, '')
    else:
        print('Found: Addr={}, City={} State={} ZipCode={}'.format(split.group(1), split.group(2), split.group(3), split.group(4)))
    return (split.group(2), split.group(3), split.group(4))

# Fill in Data
if __name__ == "__main__":
    # Check for Missing Arguments
    if len(sys.argv) < 2:
        print("Missing Command-Line Arguments\n" +
        "Usage: python3 fill_data.py <Input File: CSV> <Output File: CSV>")
        sys.exit("Exiting...")
    
    with open(ZIPCODE_PICKLE_LOCATION, 'rb') as f:
        zipcodes = pickle.load(f)

    # Initialize Writer to stdout
    with open(sys.argv[2], 'w') as f_out:
        writer = csv.writer(f_out, dialect='unix')

        # Read CSV & Fill in Data from USPS API
        with open(sys.argv[1], 'r') as f_in:
            for i, row in enumerate(csv.reader(f_in)):
                if len(''.join(row).strip()) < 5:   # Skip Empty/Too Small Lines
                    continue
                if i == 0:              # Write First Header
                    header = row
                    writer.writerow(row)
                    continue
                if row == header or row[0].lower() == 'state':      # Skip Duplicate Headers
                    continue

                csv_state = row[0]      # State
                csv_addr = row[2]       # Address 1
                csv_addr2 = row[3]      # Address 2
                csv_city = row[4]       # City
                csv_zip = row[5]        # ZipCode

                if csv_addr2 in csv_addr:                           # Remove Duplicate Address 2
                    csv_addr2 = ''
                if len(csv_city) > 9 and csv_city[-4:].isdigit():   # City has ZipCode in it
                    split_city = csv_city.split(' ')
                    csv_zip = split_city[-1].split('-')[0]
                    csv_city = ' '.join(x for x in split_city if not x.isdigit() and len(x) > 2)
                    csv_state = ''.join(x for x in split_city if len(x) == 2)[:2]
                if len(csv_zip) < 4:                                # If Zipcode is Too Short/Missing, use Address
                    csv_city, csv_state, csv_zip = usps_get_add_info(csv_addr, csv_city, csv_state)
                else:
                    if len(csv_zip) == 4:                               # ZipCode needs Extra 0
                        csv_zip = '0' + csv_zip
                    if len(csv_zip) > 4:                                # Get City/State from ZipCode
                        csv_city, csv_state = usps_get_zip_info(csv_zip[:5])

                writer.writerow([csv_state, row[1], csv_addr, csv_addr2, csv_city, csv_zip, row[6], row[7]])