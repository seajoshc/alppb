# Alpaca
If your AWS Lambda Python project has C extension modules (or dependencies that do), Alpaca will use AWS CodeBuild to build them on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package into your deployment bundle and upload to the AWS Lambda service.

# TODO
- [X] Foundation - create a CodeBuild project with hardcoded build that puts an artifact in s3
- [ ] Fix artifact so its a zip of the contents (excluding parent dir)
- [ ] Download the module locally
- [ ] Move codebuild stuff to a library?
- [ ] Allow user specification of the module to be built
- [ ] Delete the artifact from s3 as part of cleanup
- [ ] Add creation of IAM role for CodeBuild instead of using hardcoded, pre-built role
- [ ] Add deletion of IAM role as part of cleanup
- [ ] Add some randomness to the name of the build project and IAM role to prevent any potential name collisions on the off chance
- [ ] Exception handling - retry for delete and create, and any control flow necessary
- [ ] Default behavior is to create an s3 bucket and IAM role, but also allow user to optionally specify a bucket and/or policy
    - [ ] s3 bucket
    - [ ] IAM role
- [ ] One or more modules can be specified in one invocation of alpaca
- [ ] Allow specification of a requirements.txt file to use as a list of all modules to build
- [ ] Unit tests
- [ ] Integration tests
- [ ] Submit to PyPi and make into an executable
- [ ] Dockerize and submit to Dockerhub

## Exceptions
ResourceAlreadyExistsException
* https://stackoverflow.com/questions/33068055/boto3-python-and-how-to-handle-errors/33663484#33663484

# FAQs
1) Where does the name Alpaca come from?

When I was first thinking about this project, I was caling it the "Amazon Linux Python Application Compiler". I immediately noticed the acronym for that, ALPAC, was pretty close to Alpaca. It stuck with me, so I decided to keep it :)