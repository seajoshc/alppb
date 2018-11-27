# Build
# docker build . -t alppb

# Run
# docker run --rm -it -v ~/.aws:/home/someuser/.aws \
#     -v $(pwd):/alppb alppb pypi_package s3_bucket

FROM python:3.6-alpine3.8

ENV PATH=/home/someuser/.local/bin/:$PATH

RUN adduser --disabled-password --gecos "" someuser
USER someuser

WORKDIR /alppb
RUN pip install alppb --user

ENTRYPOINT [ "alppb" ]
