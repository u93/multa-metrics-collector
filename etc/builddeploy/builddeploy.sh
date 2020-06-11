#!/bin/bash

ENVIRONMENT=${1}

cdk deploy BackendBaseStack-${ENVIRONMENT} && \
cdk deploy UserOrganizationStack-${ENVIRONMENT} && \
cdk deploy UserApisBackend-${ENVIRONMENT} && \
cdk deploy AnalyticsStack-${ENVIRONMENT}