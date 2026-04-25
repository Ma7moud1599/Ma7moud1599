import requests
import re
import os

token = os.environ['GH_PAT']
headers = {'Authorization': f'bearer {token}'}

query = """
{
  user(login: "Ma7moud1599") {
    pullRequests(states: [OPEN, CLOSED, MERGED]) { totalCount }
    issues(states: [OPEN, CLOSED]) { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PRIVATE) { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalRepositoryContributions
    }
  }
}
"""

r = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
data = r.json()['data']['user']

prs     = data['pullRequests']['totalCount']
issues  = data['issues']['totalCount']
cc      = data['contributionsCollection']
commits = cc['totalCommitContributions'] + cc['restrictedContributionsCount']

print(f"PRs={prs} Commits={commits} Issues={issues}")

with open('README.md', 'r') as f:
    content = f.read()

content = re.sub(r'(PRs-)\d+(-)', lambda m: f"{m.group(1)}{prs}{m.group(2)}", content)
content = re.sub(r'(Commits-)\d+\+-', lambda m: f"{m.group(1)}{commits}+-", content)
content = re.sub(r'(Issues-)\d+(-)', lambda m: f"{m.group(1)}{issues}{m.group(2)}", content)

with open('README.md', 'w') as f:
    f.write(content)
