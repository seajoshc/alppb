# Alpaca
If your AWS Lambda Python project has C extension modules (or dependencies that do), Alpaca will use AWS CodeBuild to build them on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package into your deployment bundle and upload to the AWS Lambda service.

# TODO
## 0.1.0
- [X] Foundation - create a CodeBuild project with hardcoded build that puts an artifact in s3
- [X] Fix artifact so its a zip of the contents (excluding parent dir)
- [X] Download the module locally to dir alpaca was run from
- [X] Move codebuild stuff to a module
- [X] Delete the artifact from s3 as part of cleanup
- [X] Add creation of IAM role for CodeBuild instead of using hardcoded, pre-built role
- [X] Add deletion of IAM role as part of cleanup
- [X] Move aws-cli stuff to boto3
- [X] Allow user specification of the desired module to be built using alpaca
- [X] Cleanup existing docstrings
- [X] Remove base64 stuff in iam.py as it obscures whats happening
- [X] Axe the examples dir
- [X] Allow user specification of the bucket
## 1.0.0
- [ ] Exception handling
    - [X] Update and overwrite if resources already exist
    - [X] pre-req checking
    - [ ] Valid PyPi package
    - [X] Bucket and CodeBuild need to be in same region
- [ ] Unit tests
- [ ] Integration tests
- [ ] Submit to PyPi and make into an executable
- [ ] Dockerize and submit to Dockerhub
## v1.1
- [ ] Create an s3 bucket when an arg is specified
- [ ] Allow user to optionally specify an IAM role
- [ ] One or more modules can be specified in one invocation of alpaca
- [ ] Allow specification of a requirements.txt file to use as a list of all modules to build
- [ ] Specify download location of the artifact


## Exceptions
ResourceAlreadyExistsException
* https://stackoverflow.com/questions/33068055/boto3-python-and-how-to-handle-errors/33663484#33663484

For role not having the trust relationship: InvalidInputException

from botocore.exceptions import ClientError

# FAQs
1) Where does the name Alpaca come from?

When I was first thinking about this project, I was caling it the "Amazon Linux Python Application Compiler". I immediately noticed the acronym for that, ALPAC, was pretty close to Alpaca. It stuck with me, so I decided to keep it :)