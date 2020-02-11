import hashlib, uuid
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='mrbartucz.com',
                             user='rk6239hx',
                             password='us10interstate39',
                             db='rk6239hx_salthash',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# ask the user to store the password
user = input("What is your name? ")
password = input("What is your password? ")

# this creates a brand new guaranteed unique salt every time you run it
salt = uuid.uuid4().hex

passwordSalt = password + str(salt)

# this is an open-source method to ONE-WAY hash a password
hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

try:
    with connection.cursor() as cursor:
        # Update the record in the database
        sql = "INSERT INTO SaltHash (User, Salt, Hash) VALUES (%s, %s, %s)"
        val = (user, salt, hashed_password)
        
        # execute the sql command
        cursor.execute(sql, val)
        
        # commit to save the changes
        connection.commit()
        
        verificationPassword = input("Enter password again for verification: ")
        
        # Search for the password previously entered for verification
        sql = "SELECT Salt FROM SaltHash WHERE User = %s"
        
        # execute the sql command
        cursor.execute(sql, user)
        result = cursor.fetchone()
        
        returnSalt = result['Salt']
        
        verificationSalt = verificationPassword + returnSalt
        
        if verificationSalt == passwordSalt:
            print("The password is correct.")
        else:
            print("The password is incorrect.")

finally:
    connection.close()