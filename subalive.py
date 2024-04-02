#!/usr/bin/env python
#
# Updated by kalendra456

import requests
import sys
import argparse

timeout = 3
verbose = True
version = "1.0.2"
banner = """
---------------------------------
| s | u | b | a | l | i | v | e |
---------------------------------     

                      by kalendra456
                      version: {}
      Updated by kalendra456
""".format(version, sys.argv[0])

usage = "\n [SYNTAX]  python {} target.txt -o output.txt".format(sys.argv[0])

def create_file(user_file):
    with open(user_file, "w") as output_file:
        output_file.close()

def main():
    parser = argparse.ArgumentParser(description="Check availability of subdomains and save all subdomains to a file.")
    parser.add_argument("input_file", help="Input file containing subdomains")
    parser.add_argument("-o", "--output", help="Output file to save all subdomains", default="alive.txt")
    args = parser.parse_args()

    print(banner)

    with open(args.input_file, "r") as input_file:
        create_file(args.output)

        for line in input_file:
            url_http = "http://{}".format(line.strip())
            url_https = "https://{}".format(line.strip())
            
            try:
                req_http = requests.get(url_http, timeout=timeout)
                extra_http = "- HTTP {}".format(req_http.status_code) if verbose else ""
                print("[+] Domain is online! ({}) {}".format(url_http, extra_http))
                with open(args.output, "a") as output_file:
                    output_file.write("{}\n".format(url_http))
            except requests.exceptions.RequestException:
                try:
                    req_https = requests.get(url_https, timeout=timeout)
                    extra_https = "- HTTPS {}".format(req_https.status_code) if verbose else ""
                    print("[+] Domain is online! ({}) {}".format(url_https, extra_https))
                    with open(args.output, "a") as output_file:
                        output_file.write("{}\n".format(url_https))
                except requests.exceptions.RequestException:
                    print("[-] Domain is offline! ({})".format(line.strip()))
            except KeyboardInterrupt:
                print("\n[-] Saving progress and exiting...")
                with open(args.output, "a") as output_file:
                    output_file.write("{}\n".format(url_http))
                break

if __name__ == "__main__":
    main()
