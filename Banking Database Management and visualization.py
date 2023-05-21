import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector as mysql

mycon=mysql.connect(host="127.0.0.1",user="root",passwd="Rashi@2003",database="priyanshi")
print(mycon)
MY=mycon.cursor()

MY.execute('CREATE TABLE IF NOT EXISTS customers (Id INT AUTO_INCREMENT PRIMARY KEY,Name varchar(50), Balance float(9), Pin int(4),City varchar(50), State varchar(50),  Created_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

deposition = 0
withdrawal = 0
balance = 0
counter_1 = 1
counter_2 = 7
i = 0


while True:
   
    print("=====================================")
    print(" ----Welcome to Soni Bank----       ")
    print(" ---Project By Priyanshi Soni---       ")
    print("=====================================")
    print("*************")
    print("=<< 1. Open a new account         >>=")
    print("=<< 2. Withdraw Money             >>=")
    print("=<< 3. Deposit Money              >>=")
    print("=<< 4. Account Details            >>=")
    print("=<< 5. Check Customers & Balance  >>=")
    print("=<< 6. Statistics               >>=")
    print("=<< 7. Exit/Quit                  >>=")
    print("*************")
   
    # now to take input from user .
    if mycon.is_connected():
        choiceNumber = input("Select your choice number from the above menu : ")
        if choiceNumber == "1":
            print("Choice number 1 is selected by the customer")
            # this will take the no:of customers from the user.

            NOC = eval(input("Number of Customers : "))
 
            i = i + NOC
            #  if condition will restrict the number of new account to 5.
            if i > 5:
                print("\n")
                print("Customer registration exceed reached or Customer registration too low")
                i = i - NOC
            else:
                # The while loop will run according to the no:of customers.
                while counter_1 <= i:
                    # This will take information from customer and then append them to the list.
                   
                    name = input("Input Fullname : ")
                   
                    pin = str(input("Please input a pin of your choice : "))
                    city = input("Input City : ")
                    state = input("Input State : ")
                   
                    deposition = input("Please input a value to deposit to start an account : ")
                    sql = " INSERT INTO customers (Name,Balance,Pin, City, State) VALUES (%s, %s, %s, %s, %s)" #for string input use %s for number we use %d for %f
                    val = (name,deposition,pin, city, state)
                    MY.execute(sql, val)
                    mycon.commit()

                    sql1= "select id from customers where Name='"+name+"'";
                    MY.execute(sql1);
                    print("\nName=", end=" ")
                    print(name)
                    print("\nCity=", end=" ")
                    print(city)
                    print("\nState=", end=" ")
                    print(state)
                    print("Pin=", end=" ")
                    print(MY.fetchall()[0][0])
                    print("Balance=", end=" ")
                    print(deposition, end=" ")
                    print("-/DT")
                    counter_1 = counter_1 + 1
                    counter_2 = counter_2 + 1
                    print("\nYour name is added to customers system")
                    print("Your pin is added to customer system")
                    print("Your balance is added to customer system")
                    print("----New account created successfully !----")
                    print("\n")
                    print("Your name is avalilable on the customers list now : ")
                    print(name)
                    print("\n")
                    print("Note! Please remember the Name and Pin")
                    print("========================================")
                    # This will help the user to go back to the start of the program (main menu).
            mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
        elif choiceNumber == "2":
            print("Choice number 2 is selected by the customer")
            # This while loop will prevent the user using the account if the username or pin is wrong.
            customerID = input("Please input customer Id : ")
            pin = input("Please input pin : ")
            query= 'select * FROM CUSTOMERS where id='+ str(customerID)+' and Pin='+str(pin)
            MY.execute(query)
            record=MY.fetchall()
            if len(record)>0:
                customerData = record[0] #it will give tuple from list
                existing_balance = customerData[2] # it will give 3 element of 2 index in tuple
                withdrawal = eval(input("Input value to Withdraw, your current balance is "+str(existing_balance)+" : "))
                if existing_balance<withdrawal:
                    print("Transaction cannot happen")
                else:
                    new_balance=existing_balance-withdrawal
                    update_query='update customers set balance='+str(new_balance)+' where id='+ str(customerID)
                    MY.execute(update_query)
                    mycon.commit()
                    fetchQuery= 'select * from customers where id='+ str(customerID)
                    MY.execute(fetchQuery);
                    updated_record=MY.fetchall()
                    if len(updated_record)>0:
                        print("your available balance is:",updated_record[0][2]) # if record not found then it will throw index exception, that why handling this
                    else:
                        print("opps something went wrong")      
            else:
                print("Your customer id and pin does not match!\n")
           
            # This will help the user to go back to the start of the program (main menu).
            mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
        elif choiceNumber == "3":
            print("Choice number 3 is selected by the customer")
            customerID = input("Please input customer Id : ")
            pin = input("Please input pin : ")
            query= 'select * FROM CUSTOMERS where id='+ str(customerID)+' and Pin='+str(pin)
            MY.execute(query)
            record=MY.fetchall()

            if len(record)>0:
                customerData = record[0]
                existing_balance = customerData[2]
                deposit=eval(input("Input value to deposit, your current balance is "+str(existing_balance)+" : "))
                new_balance=existing_balance+deposit
                update_query='update customers set balance='+str(new_balance)+' where id='+ str(customerID)
                MY.execute(update_query)
                mycon.commit()
                fetchQuery= 'select * from customers where id='+ str(customerID)
                MY.execute(fetchQuery);
                updated_record=MY.fetchall()
                if len(updated_record)>0:
                    print("your available balance is:",updated_record[0][2]) # if record not found then it will throw index exception, that why handling this
                else:
                    print("opps something went wrong")      
            else:
                print("Your customer id and pin does not match!\n")

        elif choiceNumber == "4":
            print("Choice number 4 is selected by the customer")
            customerID = input("Please input customer Id : ")
            print("\n")
            df=pd.read_sql("select Id,Name,Balance,City,State,Created_On  from customers  where Id="+ str(customerID),mycon)
            print(df)


           
        elif choiceNumber == "5":
            print("Choice number 5 is selected by the customer")
            print("Customer balances mentioned below : ")
            print("\n")
            """query= 'select * FROM CUSTOMERS'
            MY.execute(query)
            record=MY.fetchall()
            print("+----+-------+---------+---------+-------+---------------------+")
            print("| Id | Name  | Balance |  City   | State | Created_On          |");
            print("+----+-------+---------+---------+-------+---------------------+")
            if len(record)>0:
                for i in record:
                    print( str(i[0])," | "+ str(i[1])," | "+ str(i[2])," | "+str(i[4])," | "+str(i[5])," | "+str(i[6]))
            print("+----+-------+---------+---------+-------+---------------------+")
            print("| Total record:",  len(record));
            print("+----+-------+---------+---------+-------+---------------------+\n")
            else:
                print("currently we don't have any customers")
            """
            df=pd.read_sql("select Id,Name,Balance,City,State,Created_On  from customers;",mycon)
            print(df)
         
        elif choiceNumber == "6":
            print("Choice number 6 is selected by the customer")
            print("\n")
            distinct_cities="SELECT DISTINCT CITY FROM CUSTOMERS ORDER BY City"
            count_per_city= "SELECT count(Id) from  customers group by City order by City"
            MY.execute(distinct_cities)
            citiesRecords=MY.fetchall()
            MY.execute(count_per_city)
            countRecords=MY.fetchall()
            plt.bar([x[0] for x in citiesRecords],[x[0] for x in countRecords])
            plt.xlabel("Cities")
            plt.ylabel("no. of Customers")
            plt.title("No of customers per cities")
            plt.show()


            distinct_states="SELECT DISTINCT STATE FROM CUSTOMERS ORDER BY STATE"
            count_per_STATE= "SELECT count(Id) from  customers group by STATE order by STATE"
            MY.execute(distinct_states)
            stateRecords=MY.fetchall()
            MY.execute(count_per_STATE)
            countRecords=MY.fetchall()
            plt.pie([x[0] for x in countRecords], labels=[x[0] for x in stateRecords],autopct="%5.2f%%")
            plt.title("No of customers per states")
            plt.show()

 
            # This  helps the user to go back to the start of the program (main menu).
            mainMenu = input("Please press enter key to go back to main menu to perform another fuction or exit ...")
        elif choiceNumber == "7":
        # This  would be just showed to the customer.
            print("Choice number 5 is selected by the customer")
            print("Thank you for using our banking system!")
            print("\n")
            print("Come again")
            print("Bye bye")
            break    
        else:
        # This else function  would work when a wrong function is chosen.
            print("Invalid option selected by the customer")
            print("Please Try again!")
        # This  helps the user to go back to the start of the program (main menu).
            mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
