CREATE TABLE IF NOT EXISTS population (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    일시 VARCHAR(20),
    시간대구분 VARCHAR(10),
    자치구 VARCHAR(20),
    총생활인구수 FLOAT,
    남자미성년자 FLOAT,
    남자청년 FLOAT,
    남자중년 FLOAT,
    남자노년 FLOAT,
    여자미성년자 FLOAT,
    여자청년 FLOAT,
    여자중년 FLOAT,
    여자노년 FLOAT
);
CREATE TABLE IF NOT EXISTS weather (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    일시 VARCHAR(20),
    평균기온 FLOAT,
    최저기온 FLOAT,
    최고기온 FLOAT,
    강수_계속시간 FLOAT,
    일강수량 FLOAT
);
CREATE TABLE IF NOT EXISTS train (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    일시 VARCHAR(20),
    자치구 VARCHAR(20),
    승차총승객수 FLOAT,
    하차총승객수 FLOAT
);
CREATE TABLE IF NOT EXISTS bus (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    일시 VARCHAR(20),
    자치구 VARCHAR(20),
    승차총승객수 FLOAT,
    하차총승객수 FLOAT
);

describe population;
describe weather;
describe train;
describe bus;
