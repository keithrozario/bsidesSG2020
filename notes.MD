# Commands

To query location:

    sls invoke -f exfil_api --data '{"building": "LOC#WA | SEATTLE", "seat": "B01|f07|A27|R05"}'

To query confidential data:

    sls invoke -f exfil_api --data '{"building": "HRCONF#HR-EMPLOYEE1", "seat": "2005-11-08"}'

## Scoped

To query location

    sls invoke -f query_location --data '{"building": "LOC#WA | SEATTLE", "seat": "B01|f07|A27|R05"}'

To query confidential data (will fail):

    sls invoke -f query_location --data '{"building": "HRCONF#HR-EMPLOYEE1", "seat": "2005-11-08"}'

## Scoped 2

    sls invoke -f dynamo_query_scoped_2 --data '{"building": "LOC#WA | SEATTLE", "seat": "B01|f07|A27|R05"}'

    sls invoke -f dynamo_query_scoped_2 --data '{"building": "HRCONF#HR-EMPLOYEE1", "seat": "2005-11-08"}'

## Scoped 3

    sls invoke -f dynamo_query_scoped_3 --data '{"building": "LOC#WA | SEATTLE", "seat": "B01|f07|A27|R05"}'

    sls invoke -f dynamo_query_scoped_3 --data '{"building": "HRCONF#HR-EMPLOYEE1", "seat": "2005-11-08"}'