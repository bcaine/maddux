#!/bin/sh

git checkout --orphan gh-pages
git fetch
git rebase origin/master
exit

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
