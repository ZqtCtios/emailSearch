import sqlite3
import datetime
def main():
    db=sqlite3.connect('db.sqlite3')
    cursor=db.cursor()
    cursor.execute('select id,remainder from verify_usermessage where isVerified =1')
    data=cursor.fetchall()
    for line in data:
        cid=line[0]
        remainder=int(line[1])
        print(cid,remainder)
        if remainder==0:
            continue
        else:
            remainder=remainder-1
            cursor.execute('update verify_usermessage set remainder={} where id={}'.format(remainder,cid))
            if remainder==0:
                cursor.execute('update verify_usermessage set isVerified=0 where id={}'.format(cid))
    db.commit()
            
        
        
        
if __name__ == "__main__":
    main()
