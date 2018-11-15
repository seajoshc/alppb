# Alpaca
If your AWS Lambda Python project has C extension modules (or dependencies that do), Alpaca will use AWS CodeBuild to build them on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package into your deployment bundle and upload to the AWS Lambda service.

# TODO
## Development
- [X] Foundation - create a CodeBuild project with hardcoded build that puts an artifact in s3
- [X] Fix artifact so its a zip of the contents (excluding parent dir)
- [X] Download the module locally to dir alpaca was run from
- [X] Move codebuild stuff to a module
- [X] Delete the artifact from s3 as part of cleanup
- [ ] Add creation of IAM role for CodeBuild instead of using hardcoded, pre-built role
- [ ] Add deletion of IAM role as part of cleanup
- [ ] Move aws-cli stuff to boto3
- [ ] Add some randomness to the name of the build project to prevent any potential name collision on the off chance
- [ ] Allow user specification of the desired module to be built using alpaca
## MVP
- [ ] Exception handling - retry for delete and create, and any control flow necessary
- [ ] Default behavior is to create an s3 bucket and IAM role, but also allow user to optionally specify a bucket and/or policy
    - [ ] s3 bucket
    - [ ] IAM role
- [ ] One or more modules can be specified in one invocation of alpaca
- [ ] Allow specification of a requirements.txt file to use as a list of all modules to build
- [ ] Specify download location of the artifact
- [ ] Unit tests
- [ ] Integration tests
- [ ] Submit to PyPi and make into an executable
- [ ] Dockerize and submit to Dockerhub

## Exceptions
ResourceAlreadyExistsException
* https://stackoverflow.com/questions/33068055/boto3-python-and-how-to-handle-errors/33663484#33663484

from botocore.exceptions import ClientError

# FAQs
1) Where does the name Alpaca come from?

When I was first thinking about this project, I was caling it the "Amazon Linux Python Application Compiler". I immediately noticed the acronym for that, ALPAC, was pretty close to Alpaca. It stuck with me, so I decided to keep it :)