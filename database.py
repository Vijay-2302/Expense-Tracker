import ibm_db,datetime

import db_conn

db2 = db_conn.DbConn()

class Database:

    def __init__(self):
        self.conn = db2.connect()
        create_query = """CREATE TABLE  IF NOT EXISTS "GSN72184"."CREDENTIALS"(
                        User_ID INTEGER NOT NULL,
                        first_name CHAR(20),
                        last_name CHAR(20),
                        email VARCHAR(200),
                        pwd VARCHAR(20),
                        PRIMARY KEY(User_ID)
                        )"""
        stmt = ibm_db.prepare(self.conn,create_query)
        result=ibm_db.execute(stmt)

        create_query2 = f"""CREATE TABLE  IF NOT EXISTS "GSN72184"."EXPENSE"(
                        User_ID INTEGER ,
                        Expense_Amt INTEGER,
                        Expense_name VARCHAR(200),
                        Expense_Date DATE,
                        CONSTRAINT FK_PersonOrder FOREIGN KEY (User_ID)
                        REFERENCES "GSN72184"."CREDENTIALS"(User_ID)
                        )"""
        stmt2 = ibm_db.prepare(self.conn,create_query2)
        result2=ibm_db.execute(stmt2)

    def insert(self,uid,fname,lname,email,pwd):
        
        insert_query = f"""insert  into "GSN72184"."CREDENTIALS" values('{uid}','{fname}','{lname}','{email}','{pwd}')"""
        insert_table = ibm_db.exec_immediate(self.conn,insert_query)
        print("Inserted Successfull")

    def wallet_insert(self,uid,expense_amt,expense_name,expense_date):
        insert_query = f"""INSERT
                        INTO  "GSN72184"."EXPENSE" ("USER_ID","EXPENSE_AMT","EXPENSE_NAME","EXPENSE_DATE")
                        VALUES('{uid}',{expense_amt},'{expense_name}','{expense_date}');"""
        insert_table = ibm_db.exec_immediate(self.conn,insert_query)

    def length_view(self):
        length_query = ibm_db.exec_immediate(self.conn,'SELECT COUNT(*) FROM "GSN72184"."CREDENTIALS"')
        length = ibm_db.fetch_tuple(length_query)[0]
        
        return length
    
    def view(self,email):

        view_query = f"""SELECT email FROM "GSN72184"."CREDENTIALS" WHERE email = '{email}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        result = ibm_db.fetch_row(view_db)

        return result
        
    def lg_view(self,email):
        view_query = f"""SELECT pwd  FROM "GSN72184"."CREDENTIALS" WHERE email = '{email}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        result = ibm_db.fetch_tuple(view_db)

        return result

    def uid_view(self,email):
        view_query = f"""SELECT USER_ID FROM "GSN72184"."CREDENTIALS" WHERE email = '{email}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        result = ibm_db.fetch_tuple(view_db)
        
        return result[0]
    
    def expense_view(self,uid):
        result_lst = []
        view_query = f"""SELECT * FROM "GSN72184"."EXPENSE" WHERE USER_ID = '{uid}'"""
        view_db = ibm_db.exec_immediate(self.conn,view_query)
        s_no = 1
        while ibm_db.fetch_row(view_db) != False:
            
            amount = ibm_db.result(view_db, "EXPENSE_AMT")
            expense_name = ibm_db.result(view_db, "EXPENSE_NAME")
            expense_date = ibm_db.result(view_db,"EXPENSE_DATE")

            day = expense_date.strftime('%d')
            month = expense_date.strftime('%B')
            year = expense_date.strftime('%Y')
            date_tuple = (day,month,year)
            expense_date = "-".join(date_tuple)

            result_lst.append([s_no,expense_name,amount,expense_date])
            s_no += 1
        
        return result_lst
    
    def chart(self,dates,uid):
        expenses = []
        for i in dates:
            # i = i.replace('/','-')
            # print(i)
            view_query = f"""SELECT SUM(Expense_Amt) FROM "GSN72184"."EXPENSE" WHERE Expense_Date = '{i}' AND USER_ID = '{uid}'"""
            view_db = ibm_db.exec_immediate(self.conn,view_query)
            result = ibm_db.fetch_tuple(view_db)
            expenses.append(result [0])
        for i in range(len(expenses)):
            if expenses[i] == None:
                expenses[i] = 0       

        return expenses

    def pie_chart(self,uid,dates):
        
        results = {}
        
        for i in dates:
            view_query = f"""SELECT Expense_name,SUM(EXPENSE_AMT) FROM EXPENSE WHERE Expense_Date = '{i}' AND USER_ID = '{uid}' GROUP BY EXPENSE_NAME"""
            view_db = ibm_db.exec_immediate(self.conn,view_query)
            result = ibm_db.fetch_tuple(view_db)

            if result != False:
                results[result[0]] = result[1]
        
        return results