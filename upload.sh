#!/bin/bash

aws s3 sync ./_site/ s3://mtnfog-websites/mtnfog.com/ --delete
