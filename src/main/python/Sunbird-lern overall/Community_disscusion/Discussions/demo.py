from datetime import datetime
# import requests
#
# # Set up the GraphQL API request
# url = "https://api.github.com/graphql"
# headers = {"Authorization": "Bearer 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"}
#
# # Set up the GraphQL query
# query = """
# query ($cursor: String) {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100, after: $cursor) {
#       pageInfo {
#         hasNextPage
#         endCursor
#       }
#       nodes {
#         id
#         createdAt
#         comments(first: 1) {
#           nodes {
#             createdAt
#           }
#         }
#       }
#     }
#   }
# }
# """
#
# # Set up the variables for the GraphQL query
# variables = {"cursor": None}
#
# # Initialize variables to track the total time and number of discussions
# total_time = 0
# total_discussions = 0
#
# # Loop through the discussions and calculate the average time to lock a discussion
# while True:
#   # Extract the data for each discussion
#   discussions = data["data"]["repository"]["discussions"]["nodes"]
#   for discussion in discussions:
#     discussion_id = discussion["id"]
#     discussion_created_at = discussion["createdAt"]
#     comments = discussion["comments"]["nodes"]
#     if comments:
#       comment_created_at = comments[0]["createdAt"]
#
#       # Calculate the time difference between the discussion creation time and the discussion lock time
#       discussion_locked_time = datetime.fromisoformat(comment_created_at.replace("Z", "+00:00"))
#       discussion_created_time = datetime.fromisoformat(discussion_created_at.replace("Z", "+00:00"))
#       time_diff = (discussion_locked_time - discussion_created_time).total_seconds()
#
#       # Add the time difference to the total time and increment the total number of discussions
#       total_time += time_diff
#       total_discussions += 1
#
#   # Check if there are more pages of discussions
#   if data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]:
#     # Set the cursor to the endCursor of the current page
#     variables["cursor"] = data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
#
#     # Make a new request to the GraphQL API with the updated cursor
#     response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers)
#     data = response.json()
#   else:
#     # All pages of discussions have been processed, so break out of the loop
#     break
#
# # Calculate the average time to lock a discussion in hours
# average_time = total_time / (total_discussions * 3600)
#
# # Print the result
# print(f"Average time to lock a discussion: {average_time:.2f} hours")




import requests

# Set up the GraphQL API request
url = "https://api.github.com/graphql"
headers = {"Authorization": "Bearer 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"}

# Set up the GraphQL query
query = """query($cursor: String) {
  organization(login: "Sunbird-ED") {
    repositories(first: 100, after: $cursor) {
      nodes{
        discussions(first:100){
          totalCount
        }
      }
      totalCount
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}"""

# Initialize variables to track the total count of discussions
total_discussions = 0
has_next_page = True
end_cursor = None

# Loop through the repositories and sum the totalCount of discussions for each repository
while has_next_page:
    # Set up the variables for the GraphQL query
    variables = {"cursor": end_cursor}

    # Make a request to the GraphQL API with the query and variables
    response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers)
    data = response.json()

    # Extract the data for each repository
    repositories = data["data"]["organization"]["repositories"]["nodes"]
    for repo in repositories:
        total_discussions += repo["discussions"]["totalCount"]

    # Check if there are more pages of repositories
    has_next_page = data["data"]["organization"]["repositories"]["pageInfo"]["hasNextPage"]
    if has_next_page:
        end_cursor = data["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]

# Print the total count of discussions
print(f"Total count of discussions: {total_discussions}")
