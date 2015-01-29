#! /bin/bash -ex

git checkout production
git rebase master
git push -f prod production:master
ssh root@bftapp dokku run teebr.co make "PYBABEL=pybabel" babel-compile
git checkout @{-1}
