#!/bin/bash

# Find and delete all __pycache__ directories in the current directory and its subdirectories
find . -type d -name "__pycache__" -exec rm -rf {} +
