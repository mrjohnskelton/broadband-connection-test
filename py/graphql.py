import requests
import json
import os
import inspect

#See https://stackoverflow.com/questions/50499/how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
baseDir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

with open(os.path.join(baseDir, '..', 'config.json')) as config_file:
    config = json.load(config_file)



"""
#See https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error
#found from: https://www.google.co.uk/search?hl=en&q=python+post+graphql+mutation&meta=
#
batchMutation = """
mutation batchCreate($createpingtestresultsarray: [CreatePingTestResultsInput]!) {
  batchCreatePingTestResults(input: $createpingtestresultsarray) {
    items {
      id
    }
  }
}
"""

# A simple function to use requests.post to make the API call. Note the json= section.
def __run_query(url, headers, query): 
  request = requests.post(url, json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def batchCreatePing(payload):
  try:
    #result = run_query(query) # Execute the query
    variable = {}
    variable['createpingtestresultsarray'] = payload
    request = requests.post(config['endpoint']['url'], json={'query': batchMutation, 'variables': variable}, headers=config['endpoint']['headers'])
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, mutation))

  except requests.exceptions.SSLError:
    print('No internet connection?')

