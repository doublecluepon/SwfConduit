#!/bin/bash

if [ -d $1/_static ]; then
    rm -rf $1/static
    mv $1/_static $1/static
fi

if [ -d $1/_modules ]; then
    rm -rf $1/modules
    mv $1/_modules $1/modules
fi

if [ -d $1/_sources ]; then
    rm -rf $1/sources
    mv $1/_sources $1/sources
fi

find $1 -name '*.html' -exec perl -p -i -e"s/_static/static/g" '{}' ';'
find $1 -name '*.html' -exec perl -p -i -e's/_modules/modules/g' {} \;
find $1 -name '*.html' -exec perl -p -i -e's/_sources/sources/g' {} \;
find $1 -name '*.js' -exec perl -p -i -e's/_sources/sources/g' {} \;
