#!/bin/bash

set -e

# Initialize GaiaNet with the specified configuration
gaianet init --config https://raw.githubusercontent.com/getcto/gaianet/main/docker_02.json

exec gaianet start & tail -f /dev/null
