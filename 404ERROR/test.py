from werkzeug.security import generate_password_hash

hash_pw = generate_password_hash('1234')
print(hash_pw)