#!/usr/bin/env python
#
# Updated by kalendra456

import requests
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

timeout = 3
verbose = True
version = "1.0.6"
banner = """
---------------------------------
| s | u | b | a | l | i | v | e |
---------------------------------     

                      by kalendra456
                      version: {}
      Updated by kalendra456
""".format(version, sys.argv[0])

usage = "\n [SYNTAX]  python {} target.txt -o output.txt [-rm] [-http] [-https] [-subdir]".format(sys.argv[0])

def create_file(user_file):
    with open(user_file, "w") as output_file:
        output_file.close()

def check_subdomain(url, remove_redirects, avoid_subdir):
    results = []
    for protocol in ["http://", "https://"]:
        try:
            req = requests.get(protocol + url, timeout=timeout, allow_redirects=not remove_redirects)
            extra = "- {} {}".format(protocol.upper(), req.status_code) if verbose else ""
            print("[+] Domain is online! ({}{})".format(protocol + url, extra))
            if not remove_redirects or req.status_code < 300 or req.status_code >= 400:
                if avoid_subdir and urlparse(req.url).netloc != urlparse(protocol + url).netloc:
                    print("[-] Avoided redirection to subdir! ({})".format(req.url))
                    continue
                results.append(protocol + url)
            break  # Break the loop if successful request
        except requests.exceptions.RequestException:
            print("[-] Domain is offline! ({}{})".format(protocol + url, extra))
            continue
    return results

def main():
    parser = argparse.ArgumentParser(description="Check availability of subdomains and save all subdomains to a file.")
    parser.add_argument("input_file", help="Input file containing subdomains")
    parser.add_argument("-o", "--output", help="Output file to save all subdomains", default="alive.txt")
    parser.add_argument("-rm", "--remove_redirects", action="store_true", help="Remove URLs that result in redirections (HTTP 3xx)")
    parser.add_argument("-http", "--http_only", action="store_true", help="Check only HTTP URLs")
    parser.add_argument("-https", "--https_only", action="store_true", help="Check only HTTPS URLs")
    parser.add_argument("-subdir", "--avoid_subdir", action="store_true", help="Avoid redirections to subdir")
    args = parser.parse_args()

    if args.http_only and args.https_only:
        print("Error: -http and -https flags cannot be used together.")
        sys.exit(1)

    print(banner)

    with open(args.input_file, "r") as input_file:
        create_file(args.output)

        urls = [line.strip() for line in input_file if line.strip()]
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(lambda url: check_subdomain(url, args.remove_redirects, args.avoid_subdir), urls):
                results.extend(result)

        with open(args.output, "a") as output_file:
            for result in results:
                output_file.write("{}\n".format(result))

if __name__ == "__main__":
    main()
