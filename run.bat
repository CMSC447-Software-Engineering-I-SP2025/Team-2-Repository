@echo off
SETLOCAL
start java -jar .\target\CookbookApp-0.0.1-SNAPSHOT.jar
npm --prefix .\recipe-app\ run dev
