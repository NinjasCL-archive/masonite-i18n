#!/usr/bin/env sh
flake8 .
pydocstyle . -e -s | more
