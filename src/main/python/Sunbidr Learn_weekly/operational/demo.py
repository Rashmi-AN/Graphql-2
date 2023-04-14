import requests
import json

# define the GraphQL query
query = """
query ($cursor: String) {
  repository(owner: "sunbird-lern", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        createdAt
        locked
      }
    }
  }
}
"""

# set up HTTP headers
url = "https://api.github.com/graphql"
headers = {"Authorization": "Bearer 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"}

# set up GraphQL variables
variables = {"cursor": None}

# initialize counter
count = 0

# loop through paginated GraphQL responses
while True:
    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    json_response = json.loads(response.text)
    discussions = json_response['data']['repository']['discussions']['nodes']
    for discussion in discussions:
        if not discussion['locked']:
            count += 1
    if not json_response['data']['repository']['discussions']['pageInfo']['hasNextPage']:
        break
    variables["cursor"] = json_response['data']['repository']['discussions']['pageInfo']['endCursor']

# display total count
print(f"Total number of open discussions: {count}")
