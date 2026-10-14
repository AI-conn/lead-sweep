---
name: lead-sweep
description: Collect structured business leads from the live web with TinyFish Search and Fetch. Use when the user wants a lead list for a business type in a location, with website, email, phone, and address where the business itself publishes them, each lead tied to its source page.
---

# Lead Sweep

Build a lead list from the live web. TinyFish Search finds candidate businesses and TinyFish Fetch reads their real pages. You structure what the pages actually say.

## Rules that never bend

- Fill a field only from text a fetched page returned. If a business does not publish a phone, email, or address on the fetched page, record null. Never infer, guess, or complete a value from memory.
- Every lead carries the URL it came from. A lead without a source is not a lead.
- Prefer the business's own site over directories and social pages. Directories are discovery evidence, not contact evidence.
- Dedupe by business website before fetching. Fetch each unique site once.

## Workflow

1. Clarify the target if it is vague: business type, location, and how many leads. Default to 10.
2. Plan three searches: "<type> in <location> official website", "best independent <type> in <location>", "<type> in <location> contact".
3. Run the searches with the helper script or the TinyFish Search API and merge the results.
4. Dedupe by normalized URL and rank the business's own sites first, directories and social pages last.
5. Fetch the top candidates with the helper script or the TinyFish Fetch API, at most twice the requested lead count.
6. Extract per lead: name, website, email, phone, address, source URL, and a completeness score from 0 to 1 based on how many of name, email, phone, and address are present. Use the schema in references/output-schema.md.
7. Present the leads as a table plus a JSON block in the schema shape. Call out which fields were not published instead of hiding the gaps.

## Helper script

The script at scripts/sweep.py runs the searches and fetches and prints the raw TinyFish JSON for you to structure. It reads the API key from the TINYFISH_API_KEY environment variable.

```bash
python3 scripts/sweep.py --target "coffee shops" --location "Austin, TX" --limit 10
```

## Failure handling

- A search that returns nothing is a result, not an error. Report zero candidates and suggest a broader target or location.
- A fetch error on one page skips that page. Never let one bad page fail the sweep.
- An API error payload means stop and report it. Do not retry the same call unchanged more than once.
