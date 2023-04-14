import requests
import json
from datetime import datetime


# Define the GraphQL query
# query = """
# query ($cursor: String) {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100, after:$cursor) {
#       nodes {
#         id
#         createdAt
#         isLocked
#         lockedAt
#       }
#       pageInfo {
#         endCursor
#         hasNextPage
#       }
#     }
#   }
# }
# """

query = """
query ($cursor: String) {
  repository(owner: "sunbird-lern", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        id
        createdAt
        comments(first: 1) {
          nodes {
            createdAt
          }
        }
      }
    }
  }
}
"""


# Execute the GraphQL query

url = 'https://api.github.com/graphql'
token = "bearer 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"
headers = {"Authorization": "bearer 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", "Content-Type": "application/json"}

# Define the variables for the query
variables = {
  "cursor": None
}

# Initialize variables for calculating the average time to lock a discussion
total_time = 0
total_discussions = 0

# Make the initial request to the GraphQL API
response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers)
data = response.json()

# Loop through the discussions and calculate the average time to lock a discussion
while True:
  # Extract the data for each discussion
  discussions = data["data"]["repository"]["discussions"]["nodes"]
  for discussion in discussions:
    discussion_id = discussion["id"]
    discussion_created_at = discussion["createdAt"]
    comments = discussion["comments"]["nodes"]
    if comments:
      comment_created_at = comments[0]["createdAt"]

      # Calculate the time difference between the discussion creation time and the discussion lock time
      discussion_locked_time = datetime.fromisoformat(comment_created_at.replace("Z", "+00:00"))
      discussion_created_time = datetime.fromisoformat(discussion_created_at.replace("Z", "+00:00"))
      time_diff = (discussion_locked_time - discussion_created_time).total_seconds()

      # Add the time difference to the total time and increment the total number of discussions
      total_time += time_diff
      total_discussions += 1

  # Check if there are more pages of discussions
  if data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]:
    # Set the cursor to the endCursor of the current page
    variables["cursor"] = data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]

    # Make a new request to the GraphQL API with the updated cursor
    response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers)
    data = response.json()
  else:
    # All pages of discussions have been processed, so break out of the loop
    break


# Calculate the average time to lock a discussion
avg_time_to_lock = total_time / (total_discussions * 3600)

# Print the average time to lock a discussion
print(f"Average time to lock a discussion: {avg_time_to_lock} hours")




# cursor = None
# count = 0
# average_time_to_lock = 0
#
# while True:
#     variables = {'cursor': cursor}
#     response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
#     if response.status_code == 200:
#         json_data = json.loads(response.text)
#         discussions = json_data["data"]["repository"]["discussions"]["nodes"]
#         for d in discussions:
#             if d["comments"]["nodes"]:
#                 discussion_locked_time = datetime.strptime(d["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
#                 discussion_posted_time = datetime.strptime(d["comments"]["nodes"][0]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
#                 average_time_to_lock += (discussion_locked_time - discussion_posted_time)/discussions.total_seconds()
#                 count += 1
#         has_next_page = json_data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]
#         if has_next_page:
#             cursor = json_data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
#         else:
#             break
#     else:
#         print("Request failed with status code:", response.status_code)
#         break
#
# if count > 0:
#     avg_time = average_time_to_lock / count / 3600
#     print(f"Average time of first response: {avg_time:.2f} hours")
# else:
#     print("No discussions with comments found.")


# response = requests.post('https://api.github.com/graphql', json={'query': query}, headers={'Authorization': 'bearer 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'})
# response.raise_for_status()
# data = response.json()['data']
#
# # Calculate the average time to lock a discussion
# total_duration = 0
# num_discussions = 0
# for discussion in data['repository']['discussions']['nodes']:
#     if discussion['isLocked']:
#         locked_time = int(discussion['lockedAt'][:-1])  # Remove the 'Z' character from the end of the timestamp
#         created_time = int(discussion['createdAt'][:-1])
#         duration = locked_time - created_time
#         total_duration += duration
#         num_discussions += 1
# if num_discussions > 0:
#     avg_duration = total_duration / num_discussions
#     print(f'Average time to lock a discussion: {avg_duration} seconds')
# else:
#     print('No locked discussions found')
