#!/bin/bash

aws s3 sync ./_site/ s3://stage.mtnfog.com/ --delete
