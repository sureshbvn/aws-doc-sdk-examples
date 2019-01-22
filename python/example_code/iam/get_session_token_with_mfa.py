# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of
# the License is located at
# 
# http://aws.amazon.com/apache2.0/
# 
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

# snippet-sourcedescription:[get_session_token_with_mfa.py demonstrates how to call GetSessionToken and pass MFA authentication information. The temporary security credentials returned by the GetSessionToken operation are then used to list all S3 buckets in the account.]
# snippet-service:[iam]
# snippet-keyword:[Python]
# snippet-keyword:[AWS Identity and Access Management (IAM)]
# snippet-keyword:[Code Sample]
# snippet-keyword:[GetSessionToken]
# snippet-sourcetype:[full-example]
# snippet-sourcedate:[2019-01-22]
# snippet-sourceauthor:[stephswo (AWS)]
# snippet-start:[iam.python.get_session_token_with_mfa.complete]

import boto
from boto.s3.connection import S3Connection
from boto.sts import STSConnection

# Prompt for MFA time-based one-time password (TOTP)
mfa_TOTP = raw_input("Enter the MFA code: ")

# The calls to AWS STS GetSessionToken must be signed with the access key ID and secret
# access key of an IAM user. The credentials can be in environment variables or in 
# a configuration file and will be discovered automatically
# by the STSConnection() function. For more information, see the Python SDK 
# documentation: http://boto.readthedocs.org/en/latest/boto_config_tut.html

sts_connection = STSConnection()

# Use the appropriate device ID (serial number for hardware device or ARN for virtual device). 
# Replace ACCOUNT-NUMBER-WITHOUT-HYPHENS and MFA-DEVICE-ID with appropriate values.

tempCredentials = sts_connection.get_session_token(
    duration=3600,
    mfa_serial_number="&region-arn;iam::ACCOUNT-NUMBER-WITHOUT-HYPHENS:mfa/MFA-DEVICE-ID",
    mfa_token=mfa_TOTP
)

# Use the temporary credentials to list the contents of an S3 bucket
s3_connection = S3Connection(
    aws_access_key_id=tempCredentials.access_key,
    aws_secret_access_key=tempCredentials.secret_key,
    security_token=tempCredentials.session_token
)

# Replace BUCKET-NAME with an appropriate value.
bucket = s3_connection.get_bucket(bucket_name="BUCKET-NAME")
objectlist = bucket.list()
for obj in objectlist:
    print obj.name

# snippet-end:[iam.python.get_session_token_with_mfa.complete]
