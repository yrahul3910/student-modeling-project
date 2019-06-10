#!/bin/sh
echo '-----------------------------------'
echo 'Installing packages'
echo '-----------------------------------'
npm i
sudo npm i -g @angular/cli@6.2.0

echo '-----------------------------------'
echo 'Linting Python code'
echo '-----------------------------------'
pycodestyle server/server.py

echo '-----------------------------------'
echo 'Linting Angular code'
echo '-----------------------------------'
ng lint

echo '-----------------------------------'
echo 'Creating dist files'
echo '-----------------------------------'
ng build

echo '-----------------------------------'
echo 'Starting Flask server'
echo '-----------------------------------'
FLASK_APP=server/server.py flask run
