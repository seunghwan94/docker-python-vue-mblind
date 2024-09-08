const fs = require('fs');
const path = require('path');
const mariadb = require('mysql');

// 설정 파일의 경로
const configPath = path.join(__dirname, '..', 'config.json');

// 설정 파일 읽기
const configData = fs.readFileSync(configPath, 'utf8');
const config = JSON.parse(configData);

// 데이터베이스 설정 가져오기
const dbConfig = config.database;

// 데이터베이스 연결 설정
const conn = mariadb.createConnection({
    host: dbConfig.host,
    port: dbConfig.port,
    user: dbConfig.user,
    password: dbConfig.password,
    database: dbConfig.database
});

module.exports = conn;
