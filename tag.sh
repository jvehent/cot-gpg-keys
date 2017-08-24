#!/bin/bash -e
PREFIX="~~~~~"

git pull --ff-only --tags
PREVIOUS_TAG=`git describe --abbrev=0`
# check the signature of the previous tag
echo
echo "$PREFIX Checking signature of $PREVIOUS_TAG ..."
echo
git tag -v "$PREVIOUS_TAG"
echo
echo "$PREFIX Good."
# check the commit logs between the previous tag and HEAD
echo "$PREFIX Log since $PREVIOUS_TAG ..."
echo
PAGER= git log "$PREVIOUS_TAG"..HEAD
echo
echo -n "$PREFIX does that log look good? (y/n) "
read input
if [ $input != 'y' ]; then
    exit 1
fi
# check the diff between the previous tag and HEAD
echo
echo "$PREFIX Diff since $PREVIOUS_TAG ..."
echo
PAGER= git diff "$PREVIOUS_TAG"
echo -n "$PREFIX does that log look good? (y/n) "
read input
if [ $input != 'y' ]; then
    exit 1
fi
# if that all looks good, tag
DATE=`python -c "from __future__ import print_function; import datetime; d=datetime.datetime.utcnow(); print('%04d%02d%02d%02d%02d%02d'%(d.year,d.month,d.day,d.hour,d.minute,d.second))"`
echo
echo "$PREFIX Date string is $DATE"
if [ ".$DATE" = "" ] ; then
    echo "$PREFIX bad date $DATE!"
    exit 1
fi
echo "$PREFIX Good."
echo
git tag -s -m "production-$DATE" production-$DATE
echo
echo "$PREFIX tagged with production-$DATE ."
echo "$PREFIX now use |git push --tags| to push the tag to the repo."
