# Speed Testing

A package of code and config to run background tests on actual broadband speeds experienced by the consumer.

The author's set up is as follows:

- a Raspberry Pi connected by ethernet cable to my Broadband router
  - runs the 'test' code as cron jobs
  - seperately picks up the files containing test results and posts them to an AWS back-end
- the AWS back end consists of:
  - an AppSync/GraphQL API which stores the results in an AWS DynamoDB table
