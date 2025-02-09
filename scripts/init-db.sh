#!/bin/bash
set -e

# Criar o banco de dados principal
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE ${POSTGRES_TEST_NAME};
EOSQL
