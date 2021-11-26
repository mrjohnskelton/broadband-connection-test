# The GraphQL query (with a few aditional bits included)
# itself defined as a multi-line string.
def getGraphQLQuery():
    return """
        {
          query: listPingTestResults {
            items {
              id
              countryCode
              postalCode
              failed
              min
              avg
              max
              mdev
              datetime
            }
          }
        }
        """


# See https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error
# found from: https://www.google.co.uk/search?hl=en&q=python+post+graphql+mutation&meta=
def getGraphQLMutation():
    return """
        mutation create(
            $createpingtestresultsinput: CreatePingTestResultsInput!
            ) {
          createPingTestResults(input: $createpingtestresultsinput) {
            id
            countryCode
            postalCode
            failed
            min
            avg
            max
            mdev
            datetime
          }
        }"""
