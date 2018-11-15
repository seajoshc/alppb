# Alpaca
If your AWS Lambda Python project has C extension modules (or dependencies that do), Alpaca will use AWS CodeBuild to compile them on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package into your deployment bundle and upload to the AWS Lambda service.

# TODO
- [ ] Move codebuild stuff to a library
- [ ] Allow user specification of the module to be built
- [ ] Download the module locally
- [ ] Delete the module from s3 as part of cleanup
- [ ] Create IAM role
- [ ] Add deletion of IAM role as part of cleanup
- [ ] Add some randomness to the name of the build project and IAM role to prevent any potential name collisions on the off chance
- [ ] Exception handling - retry for delete and create, and any control flow necessary
- [ ] Default behavior is to create an s3 bucket, but also allow user to optionally specify a bucket
- [ ] One or more modules can be specified in one invocation
- [ ] Allow specification of a requirements.txt file to use as a list of all modules to build
- [ ] Unit tests
- [ ] Integration tests
- [ ] Submit to PyPi


## Exceptions
ResourceAlreadyExistsException
* https://stackoverflow.com/questions/33068055/boto3-python-and-how-to-handle-errors/33663484#33663484