#!/bin/bash

if [[ -n $1 ]]; then
    echo "param provided to script, deleting projects postfixed with $1"
    oc delete project cab-it-ci-cd$1 cab-it-dev$1 cab-it-test$1
else
    echo "no param provided to script, deleting default projects"
    oc delete project cab-it-ci-cd cab-it-dev cab-it-test
fi
