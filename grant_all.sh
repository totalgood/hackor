
#!/usr/bin/env sh

if [ -n "$1" ]; then
   export DATABASE_NAME="$1"
fi
if [ -n "$2" ]; then
   export DATABASE_USER="$2"
fi

sudo su postgres
for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" $DATABASE_NAME` ; do  psql -c "alter table \"$tbl\" owner to $DATABASE_USER" $DATABASE_NAME ; done
psql "$DATABASE_NAME" -c "GRANT ALL ON ALL TABLES IN SCHEMA public to ${DATABASE_USER};"
for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" $DATABASE_NAME` ; do  psql -c "alter table \"$tbl\" owner to $DATABASE_USER" $DATABASE_NAME ; done
psql "$DATABASE_NAME" -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ${DATABASE_USER};"
for tbl in `psql -qAt -c "select table_name from information_schema.views where table_schema = 'public';" $DATABASE_NAME` ; do  psql -c "alter table \"$tbl\" owner to $DATABASE_USER" $DATABASE_NAME ; done
psql "$DATABASE_NAME" -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ${DATABASE_USER};"

