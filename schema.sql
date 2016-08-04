drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  username string not null,
  password string not null
);
