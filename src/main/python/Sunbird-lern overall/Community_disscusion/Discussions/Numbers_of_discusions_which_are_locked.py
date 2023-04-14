import requests
import json

import configparser

config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")

name_of_community = config.get("COMMUNITY_NAME", "name")

query = """
query ($cursor: String) {
  repository(owner: "%s", name: "community") {
    discussions(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        locked
      }
    }
  }
}
""" % name_of_community
token_details = config.get("BEARER", "token")

url = 'https://api.github.com/graphql'
headers = {"Authorization": "bearer " +token_details}

cursor = None
count = 0

while True:
    variables = {'cursor': cursor}
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        json_data = json.loads(response.text)
        discussions = json_data["data"]["repository"]["discussions"]["nodes"]
        count += len([d for d in discussions if d["locked"] is True])
        has_next_page = json_data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]
        if has_next_page:
            cursor = json_data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
        else:
            break
    else:
        print("Request failed with status code:", response.status_code)
        break

print(f"Total count of locked discussions: {count}")





# import requests
#
# query1 = """
# query {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100) {
#       nodes {
#         locked
#       }
#     }
#   }
# }
# """
#
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
# r = requests.post(url, headers=headers, json={'query': query1})
#
# if r.status_code == 200:
#     data = r.json()
#     count = 0
#     for node in data['data']['repository']['discussions']['nodes']:
#         if node['locked'] is True:
#             count += 1
#     print(f"Total count of locked discussions: {count}")
# else:
#     print(f"Request failed with status code {r.status_code}")


# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
# r = requests.post(url, headers=headers, json={'query': query1})
# print(r.status_code)
# print(r.text)




# import requests
# query = """query {
#   repository(owner: "sunbird-ed", name: "community") {
#     discussions(first: 100 isLocked:true) {
#       # type: DiscussionConnection
#       totalCount # Int!
#
#       pageInfo {
#         # type: PageInfo (from the public schema)
#         isLocked
#         # startCursor
#         # endCursor
#         # hasNextPage
#         # hasPreviousPage
#       }
#
#       edges {
#         # type: DiscussionEdge
#         cursor
#         node {
#           # type: Discussion
#           id
#         }
#       }
#
#       nodes {
#         # type: Discussion
#         id
#       }
#     }
#   }
# }"""
#
# url = 'https://api.github.com/graphql'
# headers = {"Authorization": "bearer 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"}
# r = requests.post(url, headers=headers, json={'query': query})
# print(r.status_code)
# print(r.text)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import json
# #
# # import requests
# #
# # query = """query {
# #   repository(owner: "sunbird-ed", name: "community") {
# #     discussions(first: 100, locked: true) {
# #       edges {
# #         node {
# #           createdAt
# #           locked
# #         }
# #       }
# #     }
# #   }
# # }
# #
# # }"""
# #
# # query1 = """fragment FullType on __Type {
# #   kind
# #   name
# #   fields(includeDeprecated: true) {
# #     name
# #     args {
# #       ...InputValue
# #     }
# #     type {
# #       ...TypeRef
# #     }
# #     isDeprecated
# #     deprecationReason
# #   }
# #   inputFields {
# #     ...InputValue
# #   }
# #   interfaces {
# #     ...TypeRef
# #   }
# #   enumValues(includeDeprecated: true) {
# #     name
# #     isDeprecated
# #     deprecationReason
# #   }
# #   possibleTypes {
# #     ...TypeRef
# #   }
# # }
# # fragment InputValue on __InputValue {
# #   name
# #   type {
# #     ...TypeRef
# #   }
# #   defaultValue
# # }
# # fragment TypeRef on __Type {
# #   kind
# #   name
# #   ofType {
# #     kind
# #     name
# #     ofType {
# #       kind
# #       name
# #       ofType {
# #         kind
# #         name
# #         ofType {
# #           kind
# #           name
# #           ofType {
# #             kind
# #             name
# #             ofType {
# #               kind
# #               name
# #               ofType {
# #                 kind
# #                 name
# #               }
# #             }
# #           }
# #         }
# #       }
# #     }
# #   }
# # }
# # query IntrospectionQuery {
# #   __schema {
# #     queryType {
# #       name
# #     }
# #     mutationType {
# #       name
# #     }
# #     types {
# #       ...FullType
# #     }
# #     directives {
# #       name
# #       locations
# #       args {
# #         ...InputValue
# #       }
# #     }
# #   }
# # }"""
# #
# # # res = requests.post('https://api.github.com/graphql',header)
# # url = 'https://api.github.com/graphql'
# # headers = {"Authorization": "bearer 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"}
# # r = requests.post(url, headers=headers, json={'query': query})
# #
# # if r.status_code == 200:
# #     response_data = json.loads(r.text)
# #
# #     with open('output.json', 'w') as outfile:
# #         json.dump(response_data, outfile, indent=4)
# #
# #     print("Data saved to output.json")
# # else:
# #     print("Error: ", r.status_code)
# #
# # print(r.status_code)
# # print(r.text)