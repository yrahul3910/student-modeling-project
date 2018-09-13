#!/bin/sh
echo '-----------------------------------'
echo 'Installing packages'
echo '-----------------------------------'
yarn

echo '-----------------------------------'
echo 'Linting Python code'
echo '-----------------------------------'
pycodestyle server/server.py

echo '-----------------------------------'
echo 'Creating dist files'
echo '-----------------------------------'
ng build

echo '-----------------------------------'
echo 'Starting Flask server'
echo '-----------------------------------'
FLASK_APP=server/server.py flask run