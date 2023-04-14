import requests
import json

import configparser

config = configparser.ConfigParser(interpolation=None)
config.read("/home/rashmi/PycharmProjects/Sunbird-lern overall/Community_disscusion/Discussions/config.ini")

name_of_community = config.get("COMMUNITY_NAME", "name")

def get_discussions(page_cursor=None):
    query = """
    query($cursor: String) {
      repository(owner: "%s", name: "community") {
        discussions(first: 100, after: $cursor) {
          totalCount
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            category {
              slug
            }
            comments(first: 1) {
              totalCount
              nodes{
                isAnswer
              }
            }
          }
        }
      }
    }
    """ % name_of_community
    token_details = config.get("BEARER", "token")


    url = 'https://api.github.com/graphql'
    headers = {"Authorization": "bearer " + token_details}
    variables = {'cursor': page_cursor}
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        json_data = json.loads(response.text)
        discussions = json_data["data"]["repository"]["discussions"]
        nodes = discussions["nodes"]
        has_next_page = discussions["pageInfo"]["hasNextPage"]
        end_cursor = discussions["pageInfo"]["endCursor"]
        if page_cursor is not None:
            nodes = filter_duplicate_discussions(nodes)
        if has_next_page:
            next_nodes, next_end_cursor = get_discussions(end_cursor)
            nodes.extend(next_nodes)
            end_cursor = next_end_cursor
        return nodes, end_cursor
    else:
        raise Exception("Request failed with status code:", response.status_code)


def filter_duplicate_discussions(discussions):
    ids = set()
    filtered_discussions = []
    for discussion in discussions:
        if discussion["id"] not in ids:
            ids.add(discussion["id"])
            filtered_discussions.append(discussion)
    return filtered_discussions


nodes, end_cursor = get_discussions()
bug_discussions = [d for d in nodes if d["category"]["slug"] == "issues"]
answered_bugs = [d for d in bug_discussions if d["comments"]["totalCount"] > 0]
num_answered_bugs = len(answered_bugs)
print("Number of answered bugs:", num_answered_bugs)

# import requests
# import json
#
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
#           createdAt
#           isAnswerable
#         }
#         comments(first: 1) {
#           totalCount
#           nodes{
#             isAnswer
#           }
#         }
#       }
#     }
#   }
# }
# """
#
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
#
# has_next_page = True
# end_cursor = None
# num_answered_bugs = 0
#
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
#         answered_bugs = [d for d in bug_discussions if d["comments"]["totalCount"] > 0]
#         num_answered_bugs += len(answered_bugs)
#     else:
#         print("Request failed with status code:", response.status_code)
#         break
#
# print("Number of answered bugs:", num_answered_bugs)






# import requests
# import json
#
# query = """
# query {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100) {
#       totalCount
#       nodes {
#         category {
#           slug
#           createdAt
#           isAnswerable
#         }
#         comments(first: 1) {
#           totalCount
#           nodes{
#             isAnswer
#           }
#         }
#       }
#     }
#   }
# }
# """
#
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
# response = requests.post(url, headers=headers, json={'query': query})
#
# if response.status_code == 200:
#     json_data = json.loads(response.text)
#     discussions = json_data["data"]["repository"]["discussions"]["nodes"]
#     bug_discussions = [d for d in discussions if d["category"]["slug"] == "bugs"]
#     answered_bugs = [d for d in bug_discussions if d["comments"]["totalCount"] > 0]
#     num_answered_bugs = len(answered_bugs)
#     print("Number of answered bugs:", num_answered_bugs)
# else:
#     print("Request failed with status code:", response.status_code)





# import requests
#
# url = 'https://api.github.com/graphql'
# headers = {'Authorization': 'Bearer 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'}
#
# query = """
# query {
#   repository(owner: "sunbird-ed", name: "community") {
#     issues(first: 100, labels: ["bug"]) {
#       nodes {
#         closedAt
#         timelineItems(last: 1, itemTypes: [CLOSED_EVENT]) {
#           nodes {
#             ... on ClosedEvent {
#               closer {
#                 ... on PullRequest {
#                   merged
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#   }
# }
# """
#
# response = requests.post(url, headers=headers, json={'query': query})
#
# if response.status_code == 200:
#   data = response.json()
#   bugs_answered = sum(1 for issue in data['data']['repository']['issues']['nodes'] if issue['closedAt'] and issue['timelineItems']['nodes'][0]['closer'] and issue['timelineItems']['nodes'][0]['closer']['merged'])
#   print(f'Number of bugs answered: {bugs_answered}')
# else:
#   print(f'Request failed with status code {response.status_code}: {response.text}')
