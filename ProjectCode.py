from tkinter import *
import tkinter as tk
from PIL import ImageTk,Image
import sqlite3
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from tkinter import ttk
import matplotlib.pyplot as plt
root=Tk()
root.title("Reviewing System")
root.iconbitmap()
root.geometry("200x200")
global ward
ward=0
#create a database or connect to one
conn=sqlite3.connect('Details.db')

#create cursor
c=conn.cursor()

root.geometry("500x600")  
frame = Frame(root,bg='red')  
frame.grid(row=20,column=20)  

msg = Label(text = "MULTI REVIEWING SYSTEM",font = ("Algerian",30),bg = 'LightSkyBlue2')
msg.place(x=500,y=10)

#function for displaying result
def final_ward():
    global resulter
    resulter=Tk()
    resulter.title("Fetch Result")
    resulter.iconbitmap()
    resulter.geometry("400x250")
    global res_label
    global res_box
    res_label=Label(resulter,text="Enter Name ")
    res_label.place(relx=0.3,rely=0.4)
    res_box=Entry(resulter,width=30)
    res_box.place(relx=0.5,rely=0.4)
    res_btn=Button(resulter,text="Fetch",command=final_searchward,fg="Green",activebackground = "black")
    res_btn.place(relx=0.45,rely=0.85)
def final_searchward():
    global res_res
    res_res=res_box.get()
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    query_res= f"SELECT * FROM Wardrobe WHERE name='{res_res}';"
    c.execute(query_res)
    res_record=c.fetchone()
    global res_zero
    global res_one
    global res_two
    res_zero=res_record[4]
    res_one=res_record[3]
    res_two=res_record[5]
    slices=[res_two,res_one,res_zero]#the final neutral,positive,negative value shoud be passed here
    outputs=['negative','positive','neutral']
    cols=['c','m','b']
    plt.pie(slices,labels=outputs,colors=cols,startangle=90,shadow=True,explode=(0,0.1,0),autopct='%1.1f%%')
    plt.title("Final result")
    plt.show()
    global pier
    pier=Tk()
    pier.title("PIE")
    pier.iconbitmap()
    tk.Label(pier, text='Pie Chart').pack()
    c =tk.Canvas(width=154, height=154)
    c.grid(row=5,column=5)
    c.create_arc((2,2,152,152), fill="#FAF402", outline="#FAF402", start=prop(0), extent = prop(res_zero))
    c.create_arc((2,2,152,152), fill="#2BFFF4", outline="#2BFFF4", start=prop(res_zero), extent = prop(res_one))
    c.create_arc((2,2,152,152), fill="#E00022", outline="#E00022", start=prop(res_zero+res_one), extent = prop(res_two))

    pier.mainloop()
def prop(n):
    return 360.0 * n / 1000


#function for uploading image into db for client side
def ward_upload():
    global ward_editor_upload
    ward_editor_upload=Tk()
    ward_editor_upload.title("To Upload Wardrobe Image")
    ward_editor_upload.iconbitmap()
    ward_editor_upload.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global val_label_1
    global val_box_1
    global name_label_1
    global name_box_1
    global image_address_1
    name_label_1=Label(ward_editor_upload,text="Enter name :")
    name_label_1.grid(row=1,column=3)
    name_box_1=Entry(ward_editor_upload,width=30)
    name_box_1.grid(row=1,column=5)
    val_label_1=Label(ward_editor_upload,text="Enter location image present:")
    val_label_1.grid(row=3,column=3)
    val_box_1=Entry(ward_editor_upload,width=30)
    val_box_1.grid(row=3,column=5)
    image_address_1=val_box_1.get()
    print(image_address_1)
    '''
    #image_name_1=name_box_1.get("1.0","end-1c")
    ttk.Label(ward_editor_upload, text="Enter your Review :",
                  font=("Times New Roman", 15)).place(relx=0.15,rely=0.75)
    # Text Widget
    global tl
    tl = Text(ward_editor_upload, width=100, height=6)
    tl.place(relx=0.3,rely=0.7)
    tl.focus()'''
    upld_btn=Button(ward_editor_upload,text="UPLOAD",command=retrieve_input_1,fg="Green",activebackground = "black")
    upld_btn.grid(row=5,column=4)
#function to retrive input from client
def retrieve_input_1():
    #image_address_1=tl.get("1.0","end-1c")
    global image_name_1
    global image_address_1
    image_name_1=name_box_1.get()
    image_address_1=val_box_1.get()
    print(image_name_1)
    print(image_address_1)
    upld_2_btn=Button(ward_editor_upload,text="Confirm UPLOAD ",command=insertWard(image_name_1,image_address_1),fg="Green",activebackground = "black")
    upld_2_btn.grid(row=6,column=5)
# Function for Convert Binary Data 
# to Human Readable Format
def convertToBinaryData(filename):
      
    # Convert binary format to images 
    # or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
  

def insertWard(name, photo):
    try:
          
        # Using connect method for establishing
        # a connection
        sqliteConnection = sqlite3.connect('Details.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
          
        # insert query
        sqlite_insert_blob_query = """ INSERT INTO Wardrobe
                                  (name,image,ones,zeros,twos) VALUES (?,?,0,0,0)"""
          
        # Converting human readable file into 
        # binary data
        empPhoto = convertToBinaryData(photo)
          
        # Convert data into tuple format
        data_tuple = (name, empPhoto)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        global success_label
        success_label=Label(ward_editor_upload,text="Image and file inserted successfully ..")
        success_label.grid(row=9,column=7)
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        global fail_label
        fail_label=Label(ward_editor_upload,text="Failed to insert")
        fail_label.grid(row=9,column=7)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
#insertBLOB("Smith", "D:\Internship Tasks\GFG\images\One.png")

#function for reviewer side wardrobe 
def ward_list_items():
    global ward_editor
    ward_editor=Tk()
    ward_editor.title("To Review Wardrobe List")
    ward_editor.iconbitmap()
    ward_editor.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global n
    
    global val_label
    global val_box
    val_label=Label(ward_editor,text="Enter location where you want to download:")
    val_label.place(relx=0.15,rely=0.35)
    val_box=Entry(ward_editor,width=30)
    val_box.place(relx=0.35,rely=0.35)
    n=val_box.get()
    down_btn=Button(ward_editor,text="DOWNLOAD",command=ward_list,fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.4)

def ward_list():
    try:
	
        # Using connect method for establishing
        # a connection
        con = sqlite3.connect('Details.db')
        cursor = con.cursor()
        print("Connected Successfully")
        
        query2=f"SELECT ward_image from Login_details WHERE userid='{username}' AND passcode ='{password}';"
        
        cursor.execute(query2)
        global last_image_ward
        global ward_oid
        last_image_ward=cursor.fetchone()
        print(last_image_ward)
        global last_ward
        last_ward=int(last_image_ward[0])
        last_ward+=1
        # Search from table query
        query = f"SELECT * FROM Wardrobe WHERE oid={last_ward}"

        # using cursor object executing our query
        cursor.execute(query)
        
        # fectching all records from cursor object
        records = cursor.fetchall()
        ward_oid=last_ward
        # using for loop retrieving one by one
        # rows or data
        
        for row in records:
		
            # storing row[0] in name variable
            name = row[0]
            #print(row)
            #present_ones=row[3]
            # printing name variable
            print("Image Name = ", name)
            
            # storing image (currently in binary format)
            image = row[1]
		
            # calling above convert_data() for converting
            # binary data to human readable
            convert_data(image, n + name + ".png")
            print("Yeah!! We have successfully retrieved values from database")

            # If we don't have any records in our database,
            # then print this
            if len(records) == 0:
                print("Sorry! Please Insert some data before reading from the database.")
        

        # print exception if found any during program
    # is running
    except sqlite3.Error as error:
        print(format(error))

    # using finally, closing the connection
    # (con) object
    finally:
        if con:
            con.close()
            print("SQLite connection is closed")

    #ward_list_items()
    global ward_num
    limit=0
    ward_num=0
    global val1_label
    val1_label=Label(ward_editor,text="IMAGE "+name)
    val1_label.place(relx=0.3,rely=0.6)
    ttk.Label(ward_editor, text="Enter your Review :",
                  font=("Times New Roman", 15)).place(relx=0.15,rely=0.75)
    # Text Widget
    global t
    t = Text(ward_editor, width=100, height=6)
    t.place(relx=0.3,rely=0.7)
    t.focus()
    down_btn=Button(ward_editor,text="Submit",command=lambda:retrieve_input(),fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.85)
#command=lambda: retrieve_input()

def retrieve_input():
    #print("hello")
    n=val_box.get()
    #print(n)
    inputValue=t.get("1.0","end-1c")
    result=senti(inputValue)
    global final_ward_label
    
    final_ward_label=Label(ward_editor,text="Review Has been saved , click on close ")
    final_ward_label.place(relx=0.5,rely=0.9)
    #we need to add data after creating wardrobe table
    t.delete(1.0,END)
    if(result==1):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT ones FROM Wardrobe WHERE oid={ward_oid}"
        c.execute(query1)
        present_ones=c.fetchone()
        print(present_ones)
        present_one=int(present_ones[0])
        present_one+=1
        print(present_one)
        c.execute(f"""UPDATE Wardrobe SET
            ones=:ones
            WHERE oid={ward_oid}""",
                    {
                        'ones':present_one
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==0):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT zeros FROM Wardrobe WHERE oid={ward_oid}"
        c.execute(query1)
        global present_zeros
        present_zeros=c.fetchone()
        print(present_zeros)
        present_zero=int(present_zeros[0])
        present_zero+=1
        print(present_zero)
        c.execute(f"""UPDATE Wardrobe SET
            zeros=:zeros

            WHERE oid={ward_oid}""",
                    {
                        'zeros':present_zero
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==2):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT twos FROM Wardrobe WHERE oid={ward_oid}"
        c.execute(query1)
        global present_twos
        present_twos=c.fetchone()
        print(present_twos)
        present_two=int(present_twos[0])
        present_two+=1
        print(present_two)
        c.execute(f"""UPDATE Wardrobe SET
            twos=:twos
            WHERE oid={ward_oid}""",
                    {
                        'twos':present_two
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')

    #create cursor
    c=conn.cursor()
    c.execute(f"""UPDATE Login_details SET
        ward_image=:ward_image

        WHERE userid={username} AND passcode={password}""",
                {
                    'ward_image':last_ward
                }
                )
    #commit changes
    conn.commit()

    #close connection
    conn.close()
    ward_editor.mainloop()
    
    
    #ward_editor.destroy()
    #ward_editor.destroy()
#function to upload image into database
# Function for Convert Binary
# Data to Human Readable Format
def convert_data(data, file_name):
	
	# Convert binary format to
	# images or files data
	with open(file_name, 'wb') as file:
		file.write(data)
	img = Image.open(file_name)
	print(img)

#sentimental analysis

def senti(inputvalue):
    data=inputvalue
    stop_words = set(stopwords.words('english'))
    stop_words.remove("not")
    data.lower()
    dat=list(data.split())
    #word_tokens = word_tokenize(data)
    corpus=[]
    ps = PorterStemmer()
    print(data)
    for i in range(0,len(dat)):
        review = re.sub('[^a-zA-Z]',' ', dat[i])
        if(review not in set(stop_words)):
            corpus.append(review)
    #print(corpus)
    sid = SentimentIntensityAnalyzer()
    pos_word_list=[]
    neu_word_list=[]
    neg_word_list=[]

    for word in corpus:
        #print(sia.polarity_scores(word))
        if (sid.polarity_scores(word)['compound']) >= 0.4:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.4:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)                
            
    if(len(pos_word_list)>len(neu_word_list)):
        return 1
    elif(len(pos_word_list)<len(neu_word_list)):
        return 0
        
    else:
        return 2

def update():
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor() 
    
    #record_id=user.get()
    c.execute("""UPDATE Login_details SET
        userid=:userid,
        passcode=:passcode,
        name=:name,
        phone=:phone,
        address=:address
        
        WHERE userid=:userid AND passcode=:passcode""",
              {
                  'userid':userid_editor1.get(),
                  'passcode':passcode_editor1.get(),
                  'name':name_editor1.get(),
                  'phone':phone_editor1.get(),
                  'address':address_editor1.get()
              }
             )
    
    
    #commit changes
    conn.commit()
    #close connection
    conn.close()
    editor.destroy()
    #delete_box.delete(0,END)

def edit_details():
    global name_login_box
    global passcode_login_box
    #create textboxes
    name_login_box=Entry(root,width=30)
    name_login_box.place(relx=0.4,rely=0.4)
    #passcode text code
    passcode_login_box=Entry(root,width=30,show='*')
    passcode_login_box.place(relx=0.4,rely=0.5)
    
    #label for userid
    name_login_label=Label(root,text="USER ID")
    name_login_label.place(relx=0.3,rely=0.4)
    #label for passcode in login
    passcode_login_label=Label(root,text="passcode")
    passcode_login_label.place(relx=0.3,rely=0.5)
    
    #create Login button
    login_btn2=Button(root,text="submit",command=edit)
    login_btn2.place(relx=0.47,rely=0.55)
    name_login_box.delete(0,END)
    passcode_login_box.delete(0,END)
#create an edit function to update a record
def edit():
    global record_id
    global record_passcode
    record_id=name_login_box.get()
    record_passcode=passcode_login_box.get()
    global editor
    editor=Tk()
    editor.title("Update A Record")
    editor.iconbitmap()
    editor.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')

    #create cursor
    c=conn.cursor()
    
    #Query the database
    statement=f"SELECT * FROM Login_details WHERE userid='{record_id}' AND passcode = '{record_passcode}'"
    c.execute(statement)
    records=c.fetchall()
    #print("hi")
    
    #create global variables for text box names
    global name_editor1
    global phone_editor1
    global address_editor1
    global userid_editor1
    global passcode_editor1
    
    #create text boxes
    userid_editor1=Entry(editor,width=30)
    userid_editor1.grid(row=1,column=1)
    passcode_editor1=Entry(editor,width=30)
    passcode_editor1.grid(row=2,column=1)
    name_editor1=Entry(editor,width=30)
    name_editor1.grid(row=3,column=1,padx=20,pady=(10,0))
    phone_editor1=Entry(editor,width=30)
    phone_editor1.grid(row=4,column=1)
    address_editor1=Entry(editor,width=30)
    address_editor1.grid(row=5,column=1)
  

    #create TextBox Labels
    userid_label=Label(editor,text="User id")
    userid_label.grid(row=1,column=0)
    passcode_label=Label(editor,text="passcode")
    passcode_label.grid(row=2,column=0)
    name_label=Label(editor,text="Name")
    name_label.grid(row=3,column=0,pady=(10,0))
    phone_label=Label(editor,text="Phone Number")
    phone_label.grid(row=4,column=0)
    address_label=Label(editor,text="Address")
    address_label.grid(row=5,column=0)
    #create a Save button to save edited record
    
     #Loop thru results
    for record in records:
        userid_editor1.insert(0,record[0])
        passcode_editor1.insert(0,record[1])
        name_editor1.insert(0,record[2])
        phone_editor1.insert(0,record[3])
        address_editor1.insert(0,record[4])
    
    edit_btn=Button(editor,text="Save Record",command=update)
    edit_btn.grid(row=14,column=1,columnspan=2,pady=10,padx=10,ipadx=145)
    #name_login_box.delete(0,END)
    #passcode_login_box.delete(0,END)
    #commit changes
    conn.commit()
    #close connection
    conn.close()
 

#function for adding record into database
def submit():
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    #insert into table
    c.execute("INSERT INTO Login_details VALUES (:userid,:passcode,:name,:phone,:address,:ward_image,:design_image,:new_image)",
    {
        
        'userid': userid_editor.get(),
        'passcode':passcode_editor.get(),
        'name':name_editor.get(),
        'phone':phone_editor.get(),
        'address':address_editor.get(),
        'ward_image':'0',
        'design_image':'0',
        'new_image':'0'
    })
    
    #commit changes
    conn.commit()
    #close connection
    conn.close()
    
    #clear the text boxes
    userid_editor.delete(0,END)
    passcode_editor.delete(0,END)
    name_editor.delete(0,END)
    phone_editor.delete(0,END)
    address_editor.delete(0,END)
    adder.destroy()

def final_design():
    global resulter1
    resulter1=Tk()
    resulter1.title("Fetch Result")
    resulter1.iconbitmap()
    resulter1.geometry("400x250")
    global res_label
    global res_box
    res_label=Label(resulter1,text="Enter Name ")
    res_label.place(relx=0.3,rely=0.4)
    res_box=Entry(resulter1,width=30)
    res_box.place(relx=0.5,rely=0.4)
    res_btn=Button(resulter1,text="Fetch",command=final_searchdesign,fg="Green",activebackground = "black")
    res_btn.place(relx=0.45,rely=0.85)
def final_searchdesign():
    global res_res
    res_res=res_box.get()
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    query_res= f"SELECT * FROM Design WHERE name='{res_res}';"
    c.execute(query_res)
    res_record=c.fetchone()
    global res_zero
    global res_one
    global res_two
    res_zero=res_record[4]
    res_one=res_record[3]
    res_two=res_record[5]
    slices=[res_two,res_one,res_zero]#the final neutral,positive,negative value shoud be passed here
    outputs=['negative','positive','neutral']
    cols=['c','m','b']
    plt.pie(slices,labels=outputs,colors=cols,startangle=90,shadow=True,explode=(0,0.1,0),autopct='%1.1f%%')
    plt.title("Final result")
    plt.show()
    global pier
    pier=Tk()
    pier.title("PIE")
    pier.iconbitmap()
    tk.Label(pier, text='Pie Chart').pack()
    c =tk.Canvas(width=154, height=154)
    c.grid(row=5,column=5)
    c.create_arc((2,2,152,152), fill="#FAF402", outline="#FAF402", start=prop(0), extent = prop(res_zero))
    c.create_arc((2,2,152,152), fill="#2BFFF4", outline="#2BFFF4", start=prop(res_zero), extent = prop(res_one))
    c.create_arc((2,2,152,152), fill="#E00022", outline="#E00022", start=prop(res_zero+res_one), extent = prop(res_two))

    pier.mainloop()

def prop(n):
    return 360.0 * n / 1000


#function for uploading image into db for client side
def design_upload():
    global design_editor_upload
    design_editor_upload=Tk()
    design_editor_upload.title("To Upload Wardrobe Image")
    design_editor_upload.iconbitmap()
    design_editor_upload.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global val_label_12
    global val_box_12
    global name_label_12
    global name_box_12
    global image_address_12
    name_label_12=Label(design_editor_upload,text="Enter name :")
    name_label_12.grid(row=1,column=3)
    name_box_12=Entry(design_editor_upload,width=50)
    name_box_12.grid(row=1,column=5)
    val_label_12=Label(design_editor_upload,text="Enter location image present:")
    val_label_12.grid(row=3,column=3)
    val_box_12=Entry(design_editor_upload,width=50)
    val_box_12.grid(row=3,column=5)
    image_address_12=val_box_12.get()
    print(image_address_12)
    '''
    #image_name_1=name_box_1.get("1.0","end-1c")
    ttk.Label(ward_editor_upload, text="Enter your Review :",
                  font=("Times New Roman", 15)).place(relx=0.15,rely=0.75)
    # Text Widget
    global tl
    tl = Text(ward_editor_upload, width=100, height=6)
    tl.place(relx=0.3,rely=0.7)
    tl.focus()'''
    upld_btn=Button(design_editor_upload,text="UPLOAD",command=retrieve_input_12,fg="Green",activebackground = "black")
    upld_btn.grid(row=5,column=4)
#function to retrive input from client
def retrieve_input_12():
    #image_address_1=tl.get("1.0","end-1c")
    global image_name_12
    global image_address_12
    image_name_12=name_box_12.get()
    image_address_12=val_box_12.get()
    print(image_name_12)
    print(image_address_12)
    upld_2_btn=Button(design_editor_upload,text="Confirm UPLOAD ",command=insertdesign(image_name_12,image_address_12),fg="Green",activebackground = "black")
    upld_2_btn.grid(row=6,column=5)
    
def insertdesign(name, photo):
    try:
          
        # Using connect method for establishing
        # a connection
        sqliteConnection = sqlite3.connect('Details.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
          
        # insert query
        sqlite_insert_blob_query = """ INSERT INTO Design
                                  (name,image,ones,zeros,twos) VALUES (?,?,0,0,0)"""
          
        # Converting human readable file into 
        # binary data
        empPhoto = convertToBinaryData(photo)
          
        # Convert data into tuple format
        data_tuple = (name, empPhoto)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        global success_label_1
        success_label_1=Label(design_editor_upload,text="Image and file inserted successfully ..")
        success_label_1.grid(row=9,column=7)
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        global fail_label_1
        fail_label_1=Label(design_editor_upload,text="Failed to insert")
        fail_label_1.grid(row=9,column=7)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
#insertBLOB("Smith", "D:\Internship Tasks\GFG\images\One.png")

#function for reviewer side wardrobe 
def design_list_items():
    global design_editor
    design_editor=Tk()
    design_editor.title("To Review Art And Design")
    design_editor.iconbitmap()
    design_editor.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global n
    
    global val_label
    global val_box
    val_label=Label(design_editor,text="Enter location where you want to download:")
    val_label.place(relx=0.15,rely=0.35)
    val_box=Entry(design_editor,width=30)
    val_box.place(relx=0.35,rely=0.35)
    n=val_box.get()
    down_btn=Button(design_editor,text="DOWNLOAD",command=design_list,fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.4)

def design_list():
    try:
	
        # Using connect method for establishing
        # a connection
        con = sqlite3.connect('Details.db')
        cursor = con.cursor()
        print("Connected Successfully")
        
        query2=f"SELECT design_image from Login_details WHERE userid='{username}' AND passcode ='{password}';"
        
        cursor.execute(query2)
        global last_image_design
        global design_oid
        last_image_design=cursor.fetchone()
        print(last_image_design)
        global last_design
        last_design=int(last_image_design[0])
        last_design+=1
        # Search from table query
        query = f"SELECT * FROM Design WHERE oid={last_design}"

        # using cursor object executing our query
        cursor.execute(query)
        
        # fectching all records from cursor object
        records = cursor.fetchall()
        design_oid=last_design
        # using for loop retrieving one by one
        # rows or data
        
        for row in records:
		
            # storing row[0] in name variable
            name = row[0]
            #print(row)
            #present_ones=row[3]
            # printing name variable
            print("Image Name = ", name)
            
            # storing image (currently in binary format)
            image = row[1]
		
            # calling above convert_data() for converting
            # binary data to human readable
            convert_data(image, n + name + ".png")
            print("Yeah!! We have successfully retrieved values from database")

            # If we don't have any records in our database,
            # then print this
            if len(records) == 0:
                print("Sorry! Please Insert some data before reading from the database.")
        

        # print exception if found any during program
    # is running
    except sqlite3.Error as error:
        print(format(error))

    # using finally, closing the connection
    # (con) object
    finally:
        if con:
            con.close()
            print("SQLite connection is closed")

    #ward_list_items()
    global design_num
    limit=0
    design_num=0
    global val1_label
    val1_label=Label(design_editor,text="Art And Design IMAGE")
    val1_label.place(relx=0.3,rely=0.6)
    ttk.Label(design_editor, text="Enter your Review :",
                  font=("Times New Roman", 15)).place(relx=0.15,rely=0.75)
    # Text Widget
    global t1
    t1= Text(design_editor, width=100, height=6)
    t1.place(relx=0.3,rely=0.7)
    t1.focus()
    down_btn=Button(design_editor,text="Submit",command=lambda:retrieve_input_design(),fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.85)
#command=lambda: retrieve_input()

def retrieve_input_design():
    #print("hello")
    n=val_box.get()
    #print(n)
    inputValue=t1.get("1.0","end-1c")
    result=senti(inputValue)
    global final_design_label
    
    final_design_label=Label(design_editor,text="Review Has been saved , click on close ")
    final_design_label.place(relx=0.5,rely=0.9)
    #we need to add data after creating wardrobe table
    t1.delete(1.0,END)
    if(result==1):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT ones FROM Design WHERE oid={design_oid}"
        c.execute(query1)
        present_ones_1=c.fetchone()
        print(present_ones_1)
        present_one_1=int(present_ones_1[0])
        present_one_1+=1
        print(present_one_1)
        c.execute(f"""UPDATE Design SET
            ones=:ones
            WHERE oid={design_oid}""",
                    {
                        'ones':present_one_1
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==0):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT zeros FROM Design WHERE oid={design_oid}"
        c.execute(query1)
        global present_zeros_1
        present_zeros_1=c.fetchone()
        print(present_zeros_1)
        present_zero_1=int(present_zeros_1[0])
        present_zero_1+=1
        print(present_zero_1)
        c.execute(f"""UPDATE Design SET
            zeros=:zeros

            WHERE oid={design_oid}""",
                    {
                        'zeros':present_zero_1
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==2):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT twos FROM Design WHERE oid={design_oid}"
        c.execute(query1)
        global present_twos_1
        present_twos_1=c.fetchone()
        print(present_twos_1)
        present_two_1=int(present_twos_1[0])
        present_two_1+=1
        print(present_two_1)
        c.execute(f"""UPDATE Design SET
            twos=:twos
            WHERE oid={design_oid}""",
                    {
                        'twos':present_two_1
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')

    #create cursor
    c=conn.cursor()
    c.execute(f"""UPDATE Login_details SET
        design_image=:design_image

        WHERE userid={username} AND passcode={password}""",
                {
                    'design_image':last_design
                }
                )
    #commit changes
    conn.commit()

    #close connection
    conn.close()
    design_editor.mainloop()
    
def final_new():
    global resulter2
    resulter2=Tk()
    resulter2.title("Fetch Result")
    resulter2.iconbitmap()
    resulter2.geometry("400x250")
    global res_label
    global res_box
    res_label=Label(resulter2,text="Enter Name ")
    res_label.place(relx=0.3,rely=0.4)
    res_box=Entry(resulter2,width=30)
    res_box.place(relx=0.5,rely=0.4)
    res_btn=Button(resulter2,text="Fetch",command=final_searchnew,fg="Green",activebackground = "black")
    res_btn.place(relx=0.45,rely=0.85)
def final_searchnew():
    global res_res
    res_res=res_box.get()
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    query_res= f"SELECT * FROM PRODUCT WHERE name='{res_res}';"
    c.execute(query_res)
    res_record=c.fetchone()
    global res_zero
    global res_one
    global res_two
    res_zero=res_record[4]
    res_one=res_record[3]
    res_two=res_record[5]
    slices=[res_two,res_one,res_zero]#the final neutral,positive,negative value shoud be passed here
    outputs=['negative','positive','neutral']
    cols=['c','m','b']
    plt.pie(slices,labels=outputs,colors=cols,startangle=90,shadow=True,explode=(0,0.1,0),autopct='%1.1f%%')
    plt.title("Final result")
    plt.show()
    global pier
    pier=Tk()
    pier.title("PIE")
    pier.iconbitmap()
    tk.Label(pier, text='Pie Chart').pack()
    c =tk.Canvas(width=154, height=154)
    c.grid(row=5,column=5)
    c.create_arc((2,2,152,152), fill="#FAF402", outline="#FAF402", start=prop(0), extent = prop(res_zero))
    c.create_arc((2,2,152,152), fill="#2BFFF4", outline="#2BFFF4", start=prop(res_zero), extent = prop(res_one))
    c.create_arc((2,2,152,152), fill="#E00022", outline="#E00022", start=prop(res_zero+res_one), extent = prop(res_two))
    pier.mainloop()

#function for uploading image into db for client side
def new_upload():
    global new_editor_upload
    new_editor_upload=Tk()
    new_editor_upload.title("To Upload PRODUCT Image")
    new_editor_upload.iconbitmap()
    new_editor_upload.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global val_label_13
    global val_box_13
    global name_label_13
    global name_box_13
    global image_address_13
    name_label_13=Label(new_editor_upload,text="Enter name :")
    name_label_13.grid(row=1,column=3)
    name_box_13=Entry(new_editor_upload,width=30)
    name_box_13.grid(row=1,column=5)
    val_label_13=Label(new_editor_upload,text="Enter location image present:")
    val_label_13.grid(row=3,column=3)
    val_box_13=Entry(new_editor_upload,width=30)
    val_box_13.grid(row=3,column=5)
    image_address_13=val_box_13.get()
    print(image_address_13)
    '''
    #image_name_1=name_box_1.get("1.0","end-1c")
    ttk.Label(ward_editor_upload, text="Enter your Review :",
                  font=("Times New Roman", 15)).place(relx=0.15,rely=0.75)
    # Text Widget
    global tl
    tl = Text(ward_editor_upload, width=100, height=6)
    tl.place(relx=0.3,rely=0.7)
    tl.focus()'''
    upld_btn=Button(new_editor_upload,text="UPLOAD",command=retrieve_input_13,fg="Green",activebackground = "black")
    upld_btn.grid(row=5,column=4)
#function to retrive input from client
def retrieve_input_13():
    #image_address_1=tl.get("1.0","end-1c")
    global image_name_13
    global image_address_13
    image_name_13=name_box_13.get()
    image_address_13=val_box_13.get()
    print(image_name_13)
    print(image_address_13)
    upld_2_btn=Button(new_editor_upload,text="Confirm UPLOAD ",command=insertnew(image_name_13,image_address_13),fg="Green",activebackground = "black")
    upld_2_btn.grid(row=6,column=5)
    
def insertnew(name, photo):
    try:
          
        # Using connect method for establishing
        # a connection
        sqliteConnection = sqlite3.connect('Details.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
          
        # insert query
        sqlite_insert_blob_query = """ INSERT INTO PRODUCT
                                  (name,image,ones,zeros,twos) VALUES (?,?,0,0,0)"""
          
        # Converting human readable file into 
        # binary data
        empPhoto = convertToBinaryData(photo)
          
        # Convert data into tuple format
        data_tuple = (name, empPhoto)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        global success_label_2
        success_label_2=Label(new_editor_upload,text="Image and file inserted successfully ..")
        success_label_2.grid(row=9,column=7)
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        global fail_label_2
        fail_label_2=Label(new_editor_upload,text="Failed to insert")
        fail_label_2.grid(row=9,column=7)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
#insertBLOB("Smith", "D:\Internship Tasks\GFG\images\One.png")

#function for reviewer side wardrobe 
def new_list_items():
    global new_editor
    new_editor=Tk()
    new_editor.title("To Review Newly Launching Products List")
    new_editor.iconbitmap()
    new_editor.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global n
    
    global val_label
    global val_box
    val_label=Label(new_editor,text="Enter location where you want to download:")
    val_label.place(relx=0.15,rely=0.35)
    val_box=Entry(new_editor,width=30)
    val_box.place(relx=0.35,rely=0.35)
    n=val_box.get()
    down_btn=Button(new_editor,text="DOWNLOAD",command=new_list,fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.4)

def new_list():
    try:
	
        # Using connect method for establishing
        # a connection
        con = sqlite3.connect('Details.db')
        cursor = con.cursor()
        print("Connected Successfully")
        
        query2=f"SELECT new_image from Login_details WHERE userid='{username}' AND passcode ='{password}';"
        
        cursor.execute(query2)
        global last_image_new
        global new_oid
        last_image_new=cursor.fetchone()
        print(last_image_new)
        global last_new
        last_new=int(last_image_new[0])
        last_new+=1
        # Search from table query
        query = f"SELECT * FROM PRODUCT WHERE oid={last_new}"

        # using cursor object executing our query
        cursor.execute(query)
        
        # fectching all records from cursor object
        records = cursor.fetchall()
        new_oid=last_new
        # using for loop retrieving one by one
        # rows or data
        
        for row in records:
		
            # storing row[0] in name variable
            name = row[0]
            #print(row)
            #present_ones=row[3]
            # printing name variable
            print("Student Name = ", name)
            
            # storing image (currently in binary format)
            image = row[1]
		
            # calling above convert_data() for converting
            # binary data to human readable
            convert_data(image, n + name + ".png")
            print("Yeah!! We have successfully retrieved values from database")

            # If we don't have any records in our database,
            # then print this
            if len(records) == 0:
                print("Sorry! Please Insert some data before reading from the database.")
        

        # print exception if found any during program
    # is running
    except sqlite3.Error as error:
        print(format(error))

    # using finally, closing the connection
    # (con) object
    finally:
        if con:
            con.close()
            print("SQLite connection is closed")

    #ward_list_items()
    global new_num
    limit=0
    new_num=0
    global val2_label
    val2_label=Label(new_editor,text="Newly Launching Product")
    val2_label.place(relx=0.3,rely=0.6)
    ttk.Label(new_editor, text="Enter your Review :",
                  font=("Times New Roman", 20)).place(relx=0.15,rely=0.75)
    # Text Widget
    global t2
    t2= Text(new_editor, width=100, height=6)
    t2.place(relx=0.3,rely=0.7)
    t2.focus()
    down_btn=Button(new_editor,text="Submit",command=lambda:retrieve_input_2(),fg="Green",activebackground = "black")
    down_btn.place(relx=0.45,rely=0.85)
#command=lambda: retrieve_input()

def retrieve_input_2():
    #print("hello")
    n=val_box.get()
    #print(n)
    inputValue=t2.get("1.0","end-1c")
    result=senti(inputValue)
    global final_new_label
    
    final_new_label=Label(new_editor,text="Review Has been saved , click on close ")
    final_new_label.place(relx=0.5,rely=0.9)
    #we need to add data after creating wardrobe table
    t2.delete(1.0,END)
    if(result==1):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT ones FROM PRODUCT WHERE oid={new_oid}"
        c.execute(query1)
        present_ones_2=c.fetchone()
        print(present_ones_2)
        present_one_2=int(present_ones_2[0])
        present_one_2+=1
        print(present_one_2)
        c.execute(f"""UPDATE PRODUCT SET
            ones=:ones
            WHERE oid={new_oid}""",
                    {
                        'ones':present_one_2
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==0):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT zeros FROM PRODUCT WHERE oid={new_oid}"
        c.execute(query1)
        global present_zeros_2
        present_zeros_2=c.fetchone()
        print(present_zeros_2)
        present_zero_2=int(present_zeros_2[0])
        present_zero_2+=1
        print(present_zero_2)
        c.execute(f"""UPDATE PRODUCT SET
            zeros=:zeros

            WHERE oid={new_oid}""",
                    {
                        'zeros':present_zero_2
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    elif(result==2):
        #present_ones+=1
        conn=sqlite3.connect('Details.db')

        #create cursor
        c=conn.cursor()
        query1= f"SELECT twos FROM PRODUCT WHERE oid={new_oid}"
        c.execute(query1)
        global present_twos_2
        present_twos_2=c.fetchone()
        print(present_twos_2)
        present_two_2=int(present_twos_2[0])
        present_two_2+=1
        print(present_two_2)
        c.execute(f"""UPDATE PRODUCT SET
            twos=:twos
            WHERE oid={new_oid}""",
                    {
                        'twos':present_two_2
                    }
                    )
        #commit changes
        conn.commit()

        #close connection
        conn.close()
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')

    #create cursor
    c=conn.cursor()
    c.execute(f"""UPDATE Login_details SET
        new_image=:new_image

        WHERE userid={username} AND passcode={password}""",
                {
                    'new_image':last_new
                }
                )
    #commit changes
    conn.commit()

    #close connection
    conn.close()
    new_editor.mainloop() 

#function for sign in
def addintodb():
    global adder
    adder=Tk()
    adder.title("Create A Record")
    adder.iconbitmap()
    adder.geometry("400x250")
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    
    #create global variables for text box names
    global name_editor
    global phone_editor
    global address_editor
    global userid_editor
    global passcode_editor
    #create text boxes
    userid_editor=Entry(adder,width=30)
    userid_editor.grid(row=7,column=1)
    passcode_editor=Entry(adder,width=30)
    passcode_editor.grid(row=8,column=1)
    name_editor=Entry(adder,width=30)
    name_editor.grid(row=4,column=1,padx=20,pady=(10,0))
    phone_editor=Entry(adder,width=30)
    phone_editor.grid(row=5,column=1)
    address_editor=Entry(adder,width=30)
    address_editor.grid(row=6,column=1)

    #create TextBox Labels
    userid_label=Label(adder,text="User id")
    userid_label.grid(row=7,column=0)
    passcode_label=Label(adder,text="passcode")
    passcode_label.grid(row=8,column=0)
    name_label=Label(adder,text="Name")
    name_label.grid(row=4,column=0,pady=(10,0))
    phone_label=Label(adder,text="Phone Number")
    phone_label.grid(row=5,column=0)
    address_label=Label(adder,text="Address")
    address_label.grid(row=6,column=0)
    userid_label=Label(adder,text="User id")
    userid_label.grid(row=7,column=0)
    passcode_label=Label(adder,text="passcode")
    passcode_label.grid(row=8,column=0)
    
    #create a Save button to save edited record
    
    #create button
    submit_btn=Button(adder,text="Add Record to Database",command=submit)
    submit_btn.grid(row=9,column=1,columnspan=2,pady=10,padx=10,ipadx=100)
    
    #commit changes
    conn.commit()
    #close connection
    conn.close()
#function for differnt items list
def item_list_res():
    wadrobe_btn=Button(root,text="of WADROBE LIST",command=final_ward)
    wadrobe_btn.place(relx=0.45,rely=0.75)
    design_btn=Button(root,text="of ART AND DESIGN",command=final_design)
    design_btn.place(relx=0.4455,rely=0.85)
    prod_btn=Button(root,text="of NEWLY LAUNCHING PRODUCTS",command=final_new)
    prod_btn.place(relx=0.425,rely=0.95)
    
#function for differnt items list
def item_list():
    wadrobe_btn=Button(root,text="WADROBE LIST",command=ward_upload)
    wadrobe_btn.place(relx=0.45,rely=0.75)
    design_btn=Button(root,text="ART AND DESIGN",command=design_upload)
    design_btn.place(relx=0.4455,rely=0.85)
    prod_btn=Button(root,text="NEWLY LAUNCHING PRODUCTS",command=new_upload)
    prod_btn.place(relx=0.425,rely=0.95)

def item_list_give():
    wadrobe_btn=Button(root,text="For WADROBE LIST",command=ward_list_items)
    wadrobe_btn.place(relx=0.45,rely=0.75)
    design_btn=Button(root,text="For ART AND DESIGN",command=design_list_items)
    design_btn.place(relx=0.4455,rely=0.85)
    prod_btn=Button(root,text="For NEWLY LAUNCHING PRODUCTS",command=new_list_items)
    prod_btn.place(relx=0.425,rely=0.95)
#function for entering details
def login_details():
    global name_login_box
    global passcode_login_box
    #create textboxes
    name_login_box=Entry(root,width=30)
    name_login_box.place(relx=0.4,rely=0.4)
    #passcode text code
    passcode_login_box=Entry(root,width=30,show='*')
    passcode_login_box.place(relx=0.4,rely=0.5)
    #label for userid
    name_login_label=Label(root,text="USER ID")
    name_login_label.place(relx=0.3,rely=0.4)
    #label for passcode in login
    passcode_login_label=Label(root,text="passcode")
    passcode_login_label.place(relx=0.3,rely=0.5)
    
    #create Login button
    login_btn2=Button(root,text="submit",command=login)
    login_btn2.place(relx=0.47,rely=0.55)

    #print("hel",username,password)
    #name_login_box.delete(0,END)
    #passcode_login_box.delete(0,END)
#function for login
def login():
    #create a database or connect to one
    conn=sqlite3.connect('Details.db')
    #create cursor
    c=conn.cursor()
    global username
    global password
    username=name_login_box.get()
    password=passcode_login_box.get()
    #print("hel",username,password)
    statement = f"SELECT userid from Login_details WHERE userid='{username}' AND passcode ='{password}';"
    c.execute(statement)
    record=c.fetchone()
    if not record:  # An empty result evaluates to False.
        fail=Label(text="Enter valid details...")
        fail.place(relx=0.37,rely=0.6)
        name_login_box.delete(0,END)
        passcode_login_box.delete(0,END)
    else:
        #print("Welcome")
        passed_label=Label(text="Logged in successfully..")
        passed_label.place(relx=0.37,rely=0.6)
        login3_btn=Button(root,text="GIVE REVIEW",command=item_list_give)
        login3_btn.place(relx=0.35,rely=0.65)
        login3_1_btn=Button(root,text="GET REVIEW",command=item_list)
        login3_1_btn.place(relx=0.45,rely=0.65)
        login3_2_btn=Button(root,text="GET RESULT",command=item_list_res)
        login3_2_btn.place(relx=0.55,rely=0.65)
        name_login_box.delete(0,END)
        passcode_login_box.delete(0,END)
    #commit changes
    conn.commit()

    #close connection
    conn.close()
    #name_login_box.delete(0,END)
    #passcode_login_box.delete(0,END)    
    
    
'''
#create table
c.execute("""CREATE TABLE Login_details(
            userid text,
            passcode text,
            name text,
            phone text,
            address text,
            ward_image text,
            design_image text,
            new_image text
        )""")
'''
#frame 1

login1_btn=Button(root,text="LOGIN",command=login_details,fg="blue",activebackground = "black")
#login1_btn.grid(row=20,column=90)
login1_btn.place(relx=0.45, rely=0.25, anchor=CENTER)

sign_btn=Button(root,text="SIGN UP",command=addintodb,fg="Green",activebackground = "black")
sign_btn.place(relx=0.55, rely=0.25, anchor=CENTER)

makechange_btn=Button(root,text="EDIT INFORMATION",command=edit_details,fg="indigo",activebackground = "red")
makechange_btn.place(relx=0.5, rely=0.3, anchor=CENTER)



#commit changes
conn.commit()

#close connection
conn.close()

root.mainloop()