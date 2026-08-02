#!/bin/bash
set -e

echo "🚀 Initializing GameVault Database & User Privileges..."

sudo mariadb < "SQL FILES/01.database.sql"
sudo mariadb GameVault < "SQL FILES/02.tables.sql"
sudo mariadb GameVault < "SQL FILES/04.indexes.sql"
sudo mariadb GameVault < "SQL FILES/06.functions.sql"
sudo mariadb GameVault < "SQL FILES/07.procedures.sql"
sudo mariadb GameVault < "SQL FILES/08.triggers.sql"
sudo mariadb GameVault < "SQL FILES/05.views.sql"
sudo mariadb GameVault < "SQL FILES/03.sampledata.sql"
sudo mariadb < "SQL FILES/create_user.sql"

echo "✅ GameVault Database Initialized Successfully!"
