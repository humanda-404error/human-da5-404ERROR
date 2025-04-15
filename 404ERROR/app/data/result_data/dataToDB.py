import csv
import pymysql
import io

# DB 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='prj_404error',
    charset='utf8mb4'
)

cursor = conn.cursor()

population_columns = [
    '일시', '시간대구분', '자치구', 
    '총생활인구수', '남자미성년자', '남자청년', '남자중년', '남자노년', 
    '여자미성년자', '여자청년', '여자중년', '여자노년'
]


with open('SHS_population.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=',')
    
   
    reader.fieldnames = [field.replace('\ufeff', '').strip() for field in reader.fieldnames]
    
    for row in reader:
        print(row) #test

       
        row = {key.strip(): value for key, value in row.items()}
        
        
        values = [row[col] for col in population_columns]

        sql = """
            INSERT INTO population ({})
            VALUES ({})
        """.format(
            ', '.join(population_columns),
            ', '.join(['%s'] * len(values))
        )
        cursor.execute(sql, values)


weather_columns = [
    '일시','평균기온','최저기온','최고기온','강수_계속시간','일강수량'
]
with open('SHS_weather.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=',')
    
   
    reader.fieldnames = [field.replace('\ufeff', '').strip() for field in reader.fieldnames]
    
    for row in reader:
        print(row)  #test
        
        
        row = {key.strip(): value for key, value in row.items()}
        
        values = [row[col] for col in weather_columns]
        
        sql = """
            INSERT INTO weather ({})
            VALUES ({})
        """.format(
            ', '.join(weather_columns),  
            ', '.join(['%s'] * len(values))
        )
        cursor.execute(sql, values)


bus_columns = [
    '일시','자치구','승차총승객수','하차총승객수'
]
with open('LHK_bus.csv', 'r', encoding='euc-kr') as f:
    reader = csv.DictReader(f, delimiter=',')
    
    
    reader.fieldnames = [field.replace('\ufeff', '').strip() for field in reader.fieldnames]
    
    for row in reader:
        print(row)  #test
        
        
        row = {key.strip(): value for key, value in row.items()}
        
        values = [row[col] for col in bus_columns]
        
        sql = """
            INSERT INTO bus ({})
            VALUES ({})
        """.format(
            ', '.join(bus_columns), 
            ', '.join(['%s'] * len(values))
        )
        cursor.execute(sql, values)


train_columns = [
    '일시','자치구','승차총승객수','하차총승객수'
]
with open('JSC_train.csv', 'r', encoding='euc-kr') as f:
    reader = csv.DictReader(f, delimiter=',')
    
    
    reader.fieldnames = [field.replace('\ufeff', '').strip() for field in reader.fieldnames]
    
    for row in reader:
        print(row)  #test
        
   
        row = {key.strip(): value for key, value in row.items()}
        
        values = [row[col] for col in train_columns]
        
        sql = """
            INSERT INTO train ({})
            VALUES ({})
        """.format(
            ', '.join(train_columns), 
            ', '.join(['%s'] * len(values))
        )
        cursor.execute(sql, values)

#commit
conn.commit()

cursor.close()
conn.close()

print('fin')
