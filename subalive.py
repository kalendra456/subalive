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
            url = "http://{}".format(line.strip())
            try:
                req = requests.get(url, timeout=timeout)
                extra = "- HTTP {}".format(req.status_code) if verbose else ""
                print("[+] Domain is online! ({}) {}".format(url, extra))
                with open(args.output, "a") as output_file:
                    output_file.write("{}\n".format(url))
            except KeyboardInterrupt:
                print("\n[-] Saving progress and exiting...")
                with open(args.output, "a") as output_file:
                    output_file.write("{}\n".format(url))
                break
            except requests.exceptions.Timeout:
                print("[-] Domain timed out! ({})".format(url))
            except requests.exceptions.ConnectionError:
                print("[-] Domain may not exist! ({})".format(url))
            except requests.exceptions.TooManyRedirects:
                print("[-] Domain has too many redirects! ({})".format(url))

if __name__ == "__main__":
    main()

