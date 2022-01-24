#!/bin/bash

aws s3 sync ./_site/ s3://dev.mtnfog.com/ --delete
