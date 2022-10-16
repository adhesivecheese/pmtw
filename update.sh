#!/usr/bin/env sh

python -m build
twine upload --repository pmtw dist/*
