#!/bin/bash

# MySQL 접속 정보 설정
DB_USER="root"
DB_PASSWORD="Snowcountry12~"
DB_NAME="stock_db"

# SQL 파일 경로 설정
SQL_FILE="/Users/juwon/Desktop/won-data_crawling/stock_tables.sql"

# MySQL 명령어를 사용하여 SQL 파일 실행
mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" <<EOF
source $SQL_FILE;
EOF

# 실행이 완료되었는지 확인
if [ $? -eq 0 ]; then
    echo "Tables created successfully."
else
    echo "Error occurred while creating tables."
fi