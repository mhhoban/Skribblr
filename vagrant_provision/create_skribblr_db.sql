CREATE DATABASE skribblr;

CREATE USER skribblr_admin WITH PASSWORD 'secret';

ALTER ROLE skribblr_admin SET client_encoding TO 'utf8';
ALTER ROLE skribblr_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE skribblr_admin SET timezone to 'UTC';
ALTER ROLE skribblr_admin WITH CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE skribblr TO skribblr_admin;
