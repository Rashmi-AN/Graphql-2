import requests
import json
import datetime

# GraphQL query to retrieve the bug discussions and their first responses
query = """
query($cursor: String) {
  repository(owner: "sunbird-ed", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        category {
          slug
        }
        comments(first: 1) {
          totalCount
          nodes {
            createdAt
          }
        }
        createdAt
      }
    }
  }
}
"""

# Set up the GraphQL API endpoint and headers
url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer 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"}

# Send the GraphQL query and retrieve the JSON response
has_next_page = True
end_cursor = None
total_response_time = datetime.timedelta(0)
num_bugs = 0

while has_next_page:
    variables = {"cursor": end_cursor} if end_cursor else {}
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        json_data = json.loads(response.text)
        discussions = json_data["data"]["repository"]["discussions"]["nodes"]
        bug_discussions = [d for d in discussions if d["category"]["slug"] == "bugs"]
        num_bugs += len(bug_discussions)

        for discussion in bug_discussions:
            # Convert the createdAt timestamp to a datetime object
            bug_posted_time = datetime.datetime.strptime(discussion["createdAt"], '%Y-%m-%dT%H:%M:%SZ')

            # Calculate the time difference between the bug posted time and the first response time
            if discussion["comments"]["totalCount"] > 0:
                first_response_time = datetime.datetime.strptime(discussion["comments"]["nodes"][0]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
                response_time = first_response_time - bug_posted_time
                total_response_time += response_time

        end_cursor = json_data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
        has_next_page = json_data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]
    else:
        print("Request failed with status code:", response.status_code)
        break

if num_bugs > 0:
    avg_response_time = total_response_time / num_bugs
    avg_response_time_hours = avg_response_time.total_seconds() / 3600
    print(f"Average time of first response for {num_bugs} bug discussions: {avg_response_time_hours:.2f} hours")
else:
    print("No bug discussions found.")







# import requests
# import json
# import datetime
#
# # GraphQL query to retrieve the bug discussions and their first responses
# query = """
# query($cursor: String) {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100, after: $cursor) {
#       pageInfo {
#         endCursor
#         hasNextPage
#       }
#       nodes {
#         category {
#           slug
#         }
#         comments(first: 1) {
#           totalCount
#           nodes {
#             createdAt
#           }
#         }
#         createdAt
#       }
#     }
#   }
# }
# """
#
# # Set up the GraphQL API endpoint and headers
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
#
# # Initialize variables
# has_next_page = True
# end_cursor = None
# num_bugs = 0
# total_response_time = datetime.timedelta(0)
#
# # Loop through all pages of bug discussions and calculate the average time of the first response
# while has_next_page:
#     variables = {"cursor": end_cursor}
#     response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
#
#     if response.status_code == 200:
#         json_data = json.loads(response.text)
#         discussions = json_data["data"]["repository"]["discussions"]
#         end_cursor = discussions["pageInfo"]["endCursor"]
#         has_next_page = discussions["pageInfo"]["hasNextPage"]
#         bug_discussions = [d for d in discussions["nodes"] if d["category"]["slug"] == "bugs"]
#         num_bugs += len(bug_discussions)
#
#         # Calculate the total response time of the first response for bug discussions
#         for discussion in bug_discussions:
#             # Convert the createdAt timestamp to a datetime object
#             bug_posted_time = datetime.datetime.strptime(discussion["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
#
#             # Calculate the time difference between the bug posted time and the first response time
#             if discussion["comments"]["totalCount"] > 0:
#                 first_response_time = datetime.datetime.strptime(discussion["comments"]["nodes"][0]["createdAt"],
#                                                                  '%Y-%m-%dT%H:%M:%SZ')
#                 response_time = first_response_time - bug_posted_time
#                 total_response_time += response_time
#
#     else:
#         print("Request failed with status code:", response.status_code)
#         break
#
# if num_bugs > 0:
#     avg_response_time = total_response_time / num_bugs /3600
#     print(f"Average time of first response for {num_bugs} bug discussions: {avg_response_time}")
# else:
#     print("No bug discussions found.")


# import requests
# import json
# import datetime
#
# # GraphQL query to retrieve the bug discussions and their first responses
# query = """
# query {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100) {
#       totalCount
#       nodes {
#         category {
#           slug
#         }
#         comments(first: 1) {
#           totalCount
#           nodes {
#             createdAt
#           }
#         }
#         createdAt
#       }
#     }
#   }
# }
# """
#
# # Set up the GraphQL API endpoint and headers
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
#
# # Send the GraphQL query and retrieve the JSON response
# response = requests.post(url, headers=headers, json={'query': query})
#
# if response.status_code == 200:
#     json_data = json.loads(response.text)
#     discussions = json_data["data"]["repository"]["discussions"]["nodes"]
#     bug_discussions = [d for d in discussions if d["category"]["slug"] == "bugs"]
#     num_bugs = len(bug_discussions)
#
#     # Calculate the average time of the first response for bug discussions
#
#     total_response_time = datetime.timedelta(0)
#     for discussion in bug_discussions:
#     # Convert the createdAt timestamp to a datetime object
#         bug_posted_time = datetime.datetime.strptime(discussion["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
#     # Calculate the time difference between the bug posted time and the first response time
#     if discussion["comments"]["totalCount"] > 0:
#         first_response_time = datetime.datetime.strptime(discussion["comments"]["nodes"][0]["createdAt"],
#                                                          '%Y-%m-%dT%H:%M:%SZ')
#     response_time = first_response_time - bug_posted_time
#     total_response_time += response_time
#
#     if num_bugs > 0:
#         avg_response_time = total_response_time / num_bugs
#     print(f"Average time of first response for {num_bugs} bug discussions: {avg_response_time}")
# else:
#     print("No bug discussions found.")





    # total_response_time = datetime.timedelta(0)
    # for discussion in bug_discussions:
    #     # Convert the createdAt timestamp to a datetime object
    #     bug_posted_time = datetime.datetime.strptime(discussion["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    #     # Calculate the time difference between the bug posted time and the first response time
    #     if discussion["comments"]["totalCount"] > 0:
    #         first_response_time = datetime.datetime.strptime(discussion["comments"]["nodes"][0]["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    #         response_time = first_response_time - bug_posted_time
    #         total_response_time += response_time
    # average_response_time = total_response_time / num_bugs
    #
    # print("Total number of bugs:", num_bugs)
    # print("Average time: ",average_response_time)


# import requests
# import json
# import datetime
#
# # GraphQL query to retrieve the bug discussions and their first responses
# query = """
# query {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100) {
#       totalCount
#       nodes {
#         category {
#           slug
#         }
#         comments(first: 1) {
#           totalCount
#           nodes {
#             createdAt
#           }
#         }
#         createdAt
#       }
#     }
#   }
# }
# """
#
# # Set up the GraphQL API endpoint and headers
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
#
# # Send the GraphQL query and retrieve the JSON response
# response = requests.post(url, headers=headers, json={'query': query})
#
# if response.status_code == 200:
#     json_data = json.loads(response.text)
#     discussions = json_data["data"]["repository"]["discussions"]["nodes"]
#     bug_discussions = [d for d in discussions if d["category"]["slug"] == "bugs"]
#     num_bugs = len(bug_discussions)
#
#     # Calculate the average time of the first response for bug discussions
#     total_response_time = datetime.timedelta(0)
#     for discussion in bug_discussions:
#         # Convert the createdAt timestamp to a datetime object
#         bug_posted_time = datetime.datetime.fromisoformat(discussion["createdAt"])
#         # Calculate the time difference between the bug posted time and the first response time
#         if discussion["comments"]["totalCount"] > 0:
#             first_response_time = datetime.datetime.fromisoformat(discussion["comments"]["nodes"][0]["createdAt"])
#             response_time = first_response_time - bug_posted_time
#             total_response_time += response_time
#     average_response_time = total_response_time / num_bugs
#
#     print("Total number of bugs:", num_bugs)
#     print("Average time of first response:", average_response_time)
# else:
#     print("Request failed with status code:", response.status_code)
