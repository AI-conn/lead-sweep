#!/usr/bin/env python3
"""Lead sweep helper: runs TinyFish Search and Fetch for a target business
type and location, then prints the raw JSON for the agent to structure.

Reads the API key from the TINYFISH_API_KEY environment variable and sends
it only as the X-API-Key header to TinyFish hosts.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SEARCH_URL = "https://api.search.tinyfish.ai"
FETCH_URL = "https://api.fetch.tinyfish.ai"


def call(method, url, payload=None, timeout=120):
    headers = {}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    key = os.environ.get("TINYFISH_API_KEY")
    if key:
        headers["X-API-Key"] = key
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"error": f"HTTP {exc.code}"}
    except urllib.error.URLError as exc:
        return {"error": f"unreachable: {exc.reason}"}


def main(argv=None):
    parser = argparse.ArgumentParser(description="TinyFish lead sweep raw collector.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    queries = [
        f"{args.target} in {args.location} official website",
        f"best independent {args.target} in {args.location}",
        f"{args.target} in {args.location} contact",
    ]
    searches = []
    urls = []
    for query in queries:
        result = call("GET", SEARCH_URL + "?query=" + urllib.parse.quote(query))
        searches.append({"query": query, "result": result})
        for item in result.get("results") or []:
            if item.get("url") and item["url"] not in urls:
                urls.append(item["url"])
    fetched = call("POST", FETCH_URL, payload={"urls": urls[: args.limit * 2]}) if urls else {"results": [], "errors": []}
    print(json.dumps({"queries": queries, "searches": searches, "fetched": fetched}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
