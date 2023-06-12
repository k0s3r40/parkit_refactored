# parkit_refactored

Create database
    
    CREATE USER parkit WITH password '123';
    CREATE DATABASE parkit;
    GRANT ALL PRIVILEGES ON DATABASE parkit TO parkit;
    \c parkit
    CREATE EXTENSION postgis;