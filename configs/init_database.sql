drop table if exists accounts;
create table accounts (
    uid integer primary key autoincrement,
    username text not null unique, 
    password text not null,
    phone text,
    realname text,
    gender numeric,
    age integer,
    job text
);

drop table if exists activities;
create table activities (
    aid integer primary key autoincrement,
    title text not null,
    content text not null,
    cover_url text
);

drop table if exists user_activity_join;
create table user_activity_join (
    id integer primary key autoincrement,
    uid integer,
    aid integer,
    time numeric,
    operation numeric,
    op_time numeric
);

drop table if exists user_activity_act;
create table user_activity_act (
    actid integer primary key autoincrement,
    uid integer,
    username text,
    aid integer,
    time numeric,
    act numeric,
    location string,
    latitude numeric,
    longitude numeric,
    content string
);
