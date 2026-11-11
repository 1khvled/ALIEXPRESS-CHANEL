# AWS Lambda container for the DealScout publisher runtime.
#
# Build from the repository root:
#   docker build -f infra/aws/Dockerfile -t dealscout-runtime .
#
# The base image already contains the Lambda Runtime Interface Client and
# boto3; the publisher scripts are copied unchanged so local, CI and AWS runs
# execute exactly the same code.

FROM public.ecr.aws/lambda/python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Africa/Algiers

COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY app ${LAMBDA_TASK_ROOT}/app
COPY api ${LAMBDA_TASK_ROOT}/api
COPY scripts ${LAMBDA_TASK_ROOT}/scripts
COPY assets ${LAMBDA_TASK_ROOT}/assets
COPY storage ${LAMBDA_TASK_ROOT}/storage
COPY infra/aws/lambda_handler.py ${LAMBDA_TASK_ROOT}/lambda_handler.py
COPY infra/aws/state_sync.py ${LAMBDA_TASK_ROOT}/state_sync.py

CMD ["lambda_handler.handler"]
