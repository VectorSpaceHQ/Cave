#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65
MYSQL=`which mysql`

Q1="CREATE DATABASE IF NOT EXISTS hvac;"
Q2="GRANT USAGE ON *.* TO $1@localhost IDENTIFIED BY '$2';"
Q3="GRANT ALL PRIVILEGES ON hvac.* TO $1@localhost;"
Q4="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}${Q4}"

if [ $# -ne $EXPECTED_ARGS ]
then
    echo "Usage: $0 dbuser dbpass"
    exit $E_BADARGS
fi

$MYSQL -uroot -p -e "$SQL"
mysql -u root -p hvac < database-schema.sql
