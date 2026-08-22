#!/usr/bin/env bash
# Source AWS client environment variables for fakecloud-backed tests.
FAKECLOUD_PORT="${FAKECLOUD_PORT:-4566}"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://127.0.0.1:${FAKECLOUD_PORT}}"
