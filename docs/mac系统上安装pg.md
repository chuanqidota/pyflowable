```shell
brew install postgresql@14
brew services start postgresql@14

# 进入 PostgreSQL 命令行
psql postgres

CREATE DATABASE flowable;
CREATE USER flowable WITH PASSWORD 'flowable123';
GRANT ALL PRIVILEGES ON DATABASE flowable TO flowable;
\q 
```