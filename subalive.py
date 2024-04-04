#!/usr/bin/env python
#
# Updated by kalendra456

import requests
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor

timeout = 3
verbose = True
version = "1.0.5"
banner = """
---------------------------------
| s | u | b | a | l | i | v | e |
---------------------------------     

                      by kalendra456
                      version: {}
      Updated by kalendra456
""".format(version, sys.argv[0])

usage = "\n [SYNTAX]  python {} target.txt -o output.txt [-rm]".format(sys.argv[0])

def create_file(user_file):
    with open(user_file, "w") as output_file:
        output_file.close()

def check_subdomain(url, remove_redirects):
    try:
        req = requests.get(url, timeout=timeout, allow_redirects=not remove_redirects)
        extra = "- HTTP {}".format(req.status_code) if verbose else ""
        print("[+] Domain is online! ({}) {}".format(url, extra))
        return url if not remove_redirects or req.status_code < 300 or req.status_code >= 400 else None
    except requests.exceptions.RequestException:
        print("[-] Domain is offline! ({})".format(url))
        return None

def main():
    parser = argparse.ArgumentParser(description="Check availability of subdomains and save all subdomains to a file.")
    parser.add_argument("input_file", help="Input file containing subdomains")
    parser.add_argument("-o", "--output", help="Output file to save all subdomains", default="alive.txt")
    parser.add_argument("-rm", "--remove_redirects", action="store_true", help="Remove URLs that result in redirections (HTTP 3xx)")
    args = parser.parse_args()

    print(banner)

    with open(args.input_file, "r") as input_file:
        create_file(args.output)

        urls = ["http://{}".format(line.strip()) for line in input_file if line.strip()]

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(lambda url: check_subdomain(url, args.remove_redirects), urls)

        with open(args.output, "a") as output_file:
            for result in results:
                if result:
                    output_file.write("{}\n".format(result))

if __name__ == "__main__":
    main()
