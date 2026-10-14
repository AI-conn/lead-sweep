# Lead record schema

One JSON object per lead. Every field comes from a fetched page or is null.

| Field | Type | Meaning |
|---|---|---|
| name | string or null | Business name as the business presents it, usually the page title's first segment |
| website | string | The business page that was fetched |
| email | string or null | First email address published in the page text |
| phone | string or null | First phone number published in the page text |
| address | string or null | First street address published in the page text |
| source_url | string | Final URL after any redirect, the evidence link |
| discovery_snippet | string | The search snippet that surfaced this business, up to 200 characters |
| completeness | number 0 to 1 | Share of name, email, phone, and address that are present |

Example:

```json
{
  "name": "Bennu Coffee",
  "website": "https://www.bennucoffee.com/",
  "email": null,
  "phone": null,
  "address": null,
  "source_url": "https://www.bennucoffee.com/",
  "discovery_snippet": "Bennu Coffee is an independently owned 24-hour coffee shop in Austin.",
  "completeness": 0.25
}
```

The example is real output shape from a 2026-10-13 run. The nulls are the point: the homepage did not publish those details, so the record says so instead of inventing them.
