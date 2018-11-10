#!/usr/bin/env python
"""
Alpaca
Builds Python pip packages on Amazon Linux to ensure
compatability for programs using them on AWS Lambda.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "Apache2"
from __future__ import print_function
import boto3


def main():
    """ Main entry point of the app """
    print("blorp!")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
