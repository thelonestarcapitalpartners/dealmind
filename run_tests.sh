#!/usr/bin/env bash
set -e
# Run backend unit tests from repo root
cd backend
python3 -m unittest -v tests/test_extraction_unittest.py
