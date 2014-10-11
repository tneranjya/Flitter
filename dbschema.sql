drop table if exists users;
create table users (
  username text primary key not null,
  fullname text not null,
  password text not null
);

drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  post_content text not null ,
  posted_timestamp datetime default current_timestamp,
  posted_by text not null,
  foreign key(posted_by) references users(username)
);

select * from users;