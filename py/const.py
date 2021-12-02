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


def getReForIntegerOrFloat():
    return "(?=.)([+-]?([0-9]*)(\\.([0-9]+))?)"


# For each regex:
#   $1 = The whole number
#   $2 = Integer part
#   $3 = Fractional part with leading period
#   $4 = Fractional part
def getReStringWindows():
    return ''.join([
          "Minimum = ", getReForIntegerOrFloat(), "ms, ",
          "Maximum = ", getReForIntegerOrFloat(), "ms, ",
          "Average = ", getReForIntegerOrFloat(), "ms"
      ])


# For each regex:
#   $1 = The whole number
#   $2 = Integer part
#   $3 = Fractional part with leading period
#   $4 = Fractional part
def getReStringNix():
    return ''.join([
        "min/avg/max/mdev = ", getReForIntegerOrFloat(), "/",
        getReForIntegerOrFloat(), "/",
        getReForIntegerOrFloat(), "/",
        getReForIntegerOrFloat(), " ms"
    ])
