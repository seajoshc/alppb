# Alpaca
If your AWS Lambda Python project has C extension modules (or dependencies that do), Alpaca will use AWS CodeBuild to compile them on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package into your deployment bundle and upload to the AWS Lambda service.