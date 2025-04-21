USE mysql;
UPDATE user SET Grant_priv='Y' WHERE User='root' AND Host='%';
FLUSH PRIVILEGES;

CREATE USER 'flaskuser'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON prj_404error.* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;

-- SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:1234@서버IP:3306/prj_404error'