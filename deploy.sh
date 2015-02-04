#! /bin/bash -ex

git checkout production
git rebase master
git push -f prod production:master
echo "run 'make PYBABEL=pybabel babel-compile' on the app now"
#ssh root@bftapp dokku run teebr.co make "PYBABEL=pybabel" babel-compile
git checkout master
