# Lead Sweep Skill

An Agent Skill that turns any compatible agent into a live-web lead collector using TinyFish Search and Fetch.

- lead-sweep/SKILL.md holds the skill itself: when to use it, the rules (never invent a field, every lead carries its source), and the seven-step workflow.
- lead-sweep/scripts/sweep.py is the helper the skill calls. It runs the searches and fetches and prints raw TinyFish JSON for the agent to structure. It reads the key from the TINYFISH_API_KEY environment variable.
- lead-sweep/references/output-schema.md defines the lead record, with a real example whose null fields demonstrate the no-invention rule.

Install by copying the lead-sweep folder into the agent's skills directory. Verified on 2026-10-13: the helper compiles, returns clean JSON error objects on a bad key instead of crashing, and the workflow it drives is the same pipeline the companion LeadScout app ran live against the real TinyFish API.
