#!/bin/sh

git branch -D gh-pages
git push origin --delete gh-pages
git checkout --orphan gh-pages

mv docs/source/index.rst docs/source/index.rst.bak

rm docs/source/maddux* docs/source/modules*
sphinx-apidoc -o docs/source/ maddux/

mv docs/source/index.rst.bak docs/source/index.rst

cd docs
make html
cd ..

touch .nojekyll
cp -r docs/build/html/* .

git add -A
git commit -m "Updating Github Pages"
git push origin gh-pages
git checkout master
