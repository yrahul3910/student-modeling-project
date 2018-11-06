#!/bin/sh
echo '-----------------------------------'
echo 'Installing packages'
echo '-----------------------------------'
yarn

echo '-----------------------------------'
echo 'Linting code'
echo '-----------------------------------'
pycodestyle server/server.py
npm run lint

echo '-----------------------------------'
echo 'Creating dist files'
echo '-----------------------------------'
npm run build

echo '-----------------------------------'
echo 'Starting Flask server'
echo '-----------------------------------'
FLASK_APP=server/server.py flask run 6000