#!/bin/bash
src=/home/repoforge/hina-testing/
dsthost=naruh.com
dstdir=/var/www/html/naruh.com/htdocs/pub/hina-testing/el6/
rsync -avz --delete-excluded --rsync-path 'sudo -u nginx rsync' \
  $src $dsthost:$dstdir --include-from=- <<EOF
+ RPMS/
+ RPMS/**
+ SOURCES/
+ SOURCES/**
+ SPECS/
+ SPECS/**
+ SRPMS/
+ SRPMS/**
- *
EOF
