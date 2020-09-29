# These are the notes for the talk

## Query for the Cloudtrail logs on Cloudwatch

    {$.userIdentity.type = "AssumedRole" && $.eventName = "GetParameter"}