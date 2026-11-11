"""Fetches your GitHub contribution calendar and saves data/contributions.json.
Usage:  GITHUB_TOKEN=xxx python scripts/fetch_contributions.py [username]
In GitHub Actions the built-in GITHUB_TOKEN works (public contributions).
"""
import json, os, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
USER = sys.argv[1] if len(sys.argv) > 1 else "toufeeqahmed916"
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}"""

def main():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "readme-cards"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[{"date": d["date"], "count": d["contributionCount"], "wd": d["weekday"]}
              for d in w["contributionDays"]] for w in cal["weeks"]]
    out = ROOT / "data" / "contributions.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"total": cal["totalContributions"], "weeks": weeks}))
    print(f"ok: {cal['totalContributions']} contributions -> {out}")

if __name__ == "__main__":
    main()
