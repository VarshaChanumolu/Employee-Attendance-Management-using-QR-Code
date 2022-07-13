#Required libraries
import mysql.connector #for mysql connection
from tkinter import * #for GUI
import qrcode #for QR generation
from PIL import Image,ImageTk #for reading and working with images
from resizeimage import resizeimage #for resizing image
import cv2 #for camera access and reading QR code
from pyzbar.pyzbar import decode
import time
from datetime import date

#Database connectivity and creating tables
db=mysql.connector.connect(host="localhost",user='root',passwd="akash@05",database="sl_project")
if(db):
    print("Connection to Database established")
else:
    print("Could not connect to database")
mycursor=db.cursor()
key=0 #set it to 1 to create tables in the database
if(key==1):
    mycursor.execute("create table emp_details(PRN int primary key auto_increment,Name varchar(30),Gender varchar(7),contact_no varchar(20),Designation varchar(20),login_time time,logout_time time)")
    mycursor.execute("create table address(PRN int,Door_no varchar(10) not null,Street varchar(20)not null,City varchar(20)not null,State varchar(20)not null,PIN int not null,foreign key(PRN) references emp_details(PRN) on delete set null)")

    string_1="create table absentees (Date date primary key,absentee_1 int,absentee_2 int,absentee_3 int,absentee_4 int,absentee_5 int,attendees int,"
    string_2="foreign key(absentee_1) references emp_details(PRN) on delete set null,foreign key(absentee_2) references emp_details(PRN) on delete set null"
    string_3=",foreign key(absentee_3) references emp_details(PRN) on delete set null,foreign key(absentee_4) references emp_details(PRN) on delete set null,foreign key(absentee_5) references emp_details(PRN) on delete set null)"
    string_1=string_1+string_2+string_3
    mycursor.execute(string_1)


#CLASS FOR QR CODE GENERATION
class QR_code_gen:
    def __init__(self,root):
#variables to store data from text boxes
        self.PRN=StringVar()
        self.name=StringVar()
        self.gender=StringVar()
        self.contact=StringVar()
        self.designation=StringVar()
        self.door_no=StringVar()
        self.street=StringVar()
        self.city=StringVar()
        self.state=StringVar()
        self.PIN=StringVar()
#//////////////////////////////////////window properties///////////////////////////
        self.root=root #full window
        self.root.geometry("1100x680+200+50") #setting window dimensions
        self.root.title("GENERATE AND REGISTER WINDOW") #giving title to the window
        self.root.resizable(False,False) #to avoid resize of width and height
        title=Label(self.root,text="QR GENERATOR",font=("times new roman",40),bg='#008000',anchor='w')
        title.place(x=0,y=0,relwidth=1)

#//////////////////////////////employee frame in window root/////////////////
        emp_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        emp_frame.place(x=50,y=100,width=550,height=680)
        emp_frame_title=Label(emp_frame,text="Employee Details",font=("times new roman",20),bg='blue')
        emp_frame_title.place(x=0,y=0,relwidth=1)
    #required field labels
        #For PRN field
        lbl_emp_PRN=Label(emp_frame,text="PRN",font=("times new roman",15),bg="white")
        lbl_emp_PRN.place(x=20,y=60)
        #For Name field
        lbl_emp_name=Label(emp_frame,text="Name",font=("times new roman",15),bg="white")
        lbl_emp_name.place(x=20,y=100)
        #for gender feild
        lbl_emp_name=Label(emp_frame,text="Gender",font=("times new roman",15),bg="white")
        lbl_emp_name.place(x=20,y=140)
        #For contact field
        lbl_emp_contact=Label(emp_frame,text="Contact No",font=("times new roman",15),bg="white")
        lbl_emp_contact.place(x=20,y=180)
        #For designation field
        lbl_emp_designation=Label(emp_frame,text="Designation",font=("times new roman",15),bg="white")
        lbl_emp_designation.place(x=20,y=220)
        #For door no field
        lbl_emp_door=Label(emp_frame,text="Door No",font=("times new roman",15),bg="white")
        lbl_emp_door.place(x=20,y=260)
         #For street field
        lbl_emp_street=Label(emp_frame,text="Street",font=("times new roman",15),bg="white")
        lbl_emp_street.place(x=20,y=300)
        #For city field
        lbl_emp_city=Label(emp_frame,text="City",font=("times new roman",15),bg="white")
        lbl_emp_city.place(x=20,y=340)
        #For state field
        lbl_emp_state=Label(emp_frame,text="State",font=("times new roman",15),bg="white")
        lbl_emp_state.place(x=20,y=380)
        #For PIN field
        lbl_emp_PIN=Label(emp_frame,text="PIN",font=("times new roman",15),bg="white")
        lbl_emp_PIN.place(x=20,y=420)
    #required entry boxes for each feild
        #For PRN field
        lbl_emp_PRN=Entry(emp_frame,textvariable=self.PRN,font=("times new roman",15),bg="light yellow")
        lbl_emp_PRN.place(x=200,y=60)
        #For Name field
        txt_emp_name=Entry(emp_frame,textvariable=self.name,font=("times new roman",15),bg="light yellow")
        txt_emp_name.place(x=200,y=100)
        #for gender feild
        txt_emp_name=Entry(emp_frame,textvariable=self.gender,font=("times new roman",15),bg="light yellow")
        txt_emp_name.place(x=200,y=140)
        #For contact field
        txt_emp_contact=Entry(emp_frame,textvariable=self.contact,font=("times new roman",15),bg="light yellow")
        txt_emp_contact.place(x=200,y=180)
        #For designation field
        txt_emp_designation=Entry(emp_frame,textvariable=self.designation,font=("times new roman",15),bg="light yellow")
        txt_emp_designation.place(x=200,y=220)
        #For door no field
        txt_emp_door=Entry(emp_frame,textvariable=self.door_no,font=("times new roman",15),bg="light yellow")
        txt_emp_door.place(x=200,y=260)
         #For street field
        txt_emp_street=Entry(emp_frame,textvariable=self.street,font=("times new roman",15),bg="light yellow")
        txt_emp_street.place(x=200,y=300)
        #For city field
        txt_emp_city=Entry(emp_frame,textvariable=self.city,font=("times new roman",15),bg="light yellow")
        txt_emp_city.place(x=200,y=340)
        #For state field
        txt_emp_state=Entry(emp_frame,textvariable=self.state,font=("times new roman",15),bg="light yellow")
        txt_emp_state.place(x=200,y=380)
        #For PIN field
        txt_emp_PIN=Entry(emp_frame,textvariable=self.PIN,font=("times new roman",15),bg="light yellow")
        txt_emp_PIN.place(x=200,y=420)
    #Buttons
        #Register button
        Qr_generate_btn=Button(emp_frame,text="Register",command=self.register,font=("times new roman",18,"bold"),bg="Green")
        Qr_generate_btn.place(x=60,y=490)
        #Generate QR button
        register_btn=Button(emp_frame,text="Generate QR",command=self.generate,font=("times new roman",18,"bold"),bg="#FFA500")
        register_btn.place(x=190,y=490)
        #Reset button
        reset_btn=Button(emp_frame,text="Reset",command=self.reset,font=("times new roman",18,"bold"),bg="Red")
        reset_btn.place(x=370,y=490)
    #Display message/feedback message
        self.msg="Fill the feilds to continue"
        self.msg_lbl=Label(emp_frame,text=self.msg,font=("times new roman",20,"bold"),bg="white",fg="blue")
        self.msg_lbl.place(x=100,y=540)
#QR code window
        qr_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        qr_frame.place(x=650,y=100,width=400,height=550)
        qr_frame_title=Label(qr_frame,text="QR Code",font=("times new roman",20),bg="blue")
        qr_frame_title.place(x=0,y=0,relwidth=1)
        #image need to be label
        self.qr_code=Label(qr_frame,text="Previw Not Available",font=("times new roman",15),bg="dark green",fg="white")
        self.qr_code.place(x=40,y=100,width=300,height=300)
    
 #Methods
    #Method 1 to generate a QR code
    def generate(self):
        ans=0
        if(self.PRN.get()=='' or self.name.get()=='' or self.contact.get()=='' or self.designation.get()=='' or self.door_no.get()=='' or self.street.get()=='' or self.city.get()=='' or self.state.get()=='' or self.PIN.get()=='' or self.gender.get()==''):
            self.msg="Mandatory to fill all the fields"
            self.msg_lbl.config(text=self.msg,fg="red")
        else:
            #qr generation code
            data={"PRN:":self.PRN.get(),"Name:":self.name.get(),"Gender:":self.gender.get(),"Contact_No:":self.contact.get(),"Designation:":self.designation.get()}
            #data=(f"PRN:{self.PRN.get()}\nName:{self.name.get()}\nGender:{self.gender.get()}\nContact_No:{self.contact.get()}\nDesignation:{self.designation.get()}\n") #string which gets converted to QR code
            QRcode=qrcode.make(data) #main statement which makes QR code
            #saving and resizing QR codes in a folder
            QRcode=resizeimage.resize_cover(QRcode,[300,300])
            QRcode.save("QR codes/EMP_"+self.PRN.get()+".png")
            #updating image label in window
            self.image=ImageTk.PhotoImage(QRcode)
            self.qr_code.config(image=self.image)
            self.msg="QR code generated successfully"
            self.msg_lbl.config(text=self.msg,fg="green")   
    #Method 2 to reset all the entry feilds
    def reset(self):
        self.PRN.set('')
        self.name.set('') 
        self.contact.set('')
        self.designation.set('') 
        self.door_no.set('')
        self.street.set('')
        self.city.set('')
        self.state.set('')
        self.PIN.set('')
        self.gender.set('')
        self.qr_code.config(image='')
        self.msg="Fields resetted successfully"
        self.msg_lbl.config(text=self.msg,fg="green")  
    #Method 3 to register where details entered are being stored in database
    def register(self):
        ans=1
        mycursor.execute(f"select PRN from emp_details where PRN={self.PRN.get()}")
        check=mycursor.fetchone()
        if (str(type(check))[8:16])=="NoneType":
            if(self.PRN.get()=='' or self.name.get()=='' or self.contact.get()=='' or self.designation.get()=='' or self.door_no.get()=='' or self.street.get()=='' or self.city.get()=='' or self.state.get()=='' or self.PIN.get()=='' or self.gender.get()==''):
                self.msg="Fill all the feilds to register"
                self.msg_lbl.config(text=self.msg,fg="red")
            else:
                mycursor.execute(f"insert into emp_details(PRN,Name,Gender,contact_no,Designation) values({self.PRN.get()},'{self.name.get()}','{self.gender.get()}','{self.contact.get()}','{self.designation.get()}')")
                mycursor.execute(f"insert into address values({self.PRN.get()},'{self.door_no.get()}','{self.street.get()}','{self.city.get()}','{self.state.get()}','{self.PIN.get()}')")
                db.commit()
                self.msg="Employee Registered successfully"
                self.msg_lbl.config(text=self.msg,fg="green")
        else:
            self.msg="Exsisting user's cannot register again"
            self.msg_lbl.config(text=self.msg,fg="red") 


#window 2 with register,generate and reset options
def generate(): #func to open window 2
    window2=Toplevel(window1) #object of Tk
    gen_obj=QR_code_gen(window2) 
    window2.mainloop()


#window 3 which is bascically camera app to read QR code
#here a small text box for scanning message
def camera():
    local_time = time.localtime() #for local time
    #detector=cv2.QRCodeDetector() #method to detect a QR code
    cap=cv2.VideoCapture(0, cv2.CAP_DSHOW) #variable to store a vedio and passing 0 would record a vedio using camera
    cap.set(3,640) #width-3;height-4
    cap.set(4,480) #dimensions of the camera window
    camera=True
    while (camera==True):
        sucess,frame=cap.read() #sucess boolean,frame is a snapshot
        cv2.imshow("Code scan",frame) #to open camera window
        cv2.waitKey(1) #to show window for 1ms and loop repeats to form a vedio
        for code in decode(frame):
            decoded=code.data.decode('utf-8').split(",") 
            PRN_list=decoded[0].split(":") 
            PRN_list1=PRN_list[2].split("'")
            PRN=int(PRN_list1[1]) #final extracted PRN of the employee
            current_time = time.strftime("%H:%M:%S", local_time) #to store local time
            if(str(code.type)=='QRCODE'):
                time.sleep(1) #to freeze window for 5 seconds to confirm that the code is read
                camera=False #to stop camera from making a vedio display
                cv2.destroyAllWindows() # to close the camera window
            mycursor.execute(f"select login_time from emp_details where PRN={PRN}") #to extract login time
            check=mycursor.fetchone()
            if (str(type(check))[8:16])!="NoneType":
                for i in check:
                    ans=i
                    if(str(ans)=='None'): #to update login time for fresh login
                        mycursor.execute(f" update emp_details set login_time='{current_time}' where PRN={PRN}") #to update login time
                        message="Employee logged in successful"
                        msg_label.configure(text=message,fg="green")
                    else:
                        mycursor.execute(f"select logout_time from emp_details where PRN={PRN}") #to extract login time
                        check=mycursor.fetchone()
                        for i in check:
                            ans=i
                            if(str(ans)=='None'): #to update login time for fresh login
                                mycursor.execute(f" update emp_details set logout_time='{current_time}' where PRN={PRN}") #to update login time
                                message="Employee logged out successful"
                                msg_label.configure(text=message,fg="green")

                db.commit()
            else:
                message="Invalid user Unable to login/logout"
                msg_label.configure(text=message,fg="red")


            
#class for admin activities
class admin:
    def __init__(self,root):
        #variables
        self.PRN=StringVar()
        self.date=StringVar()
        self.key=0 #key to prevent accessing attendence without storing absentees
        #window allignment commands
        self.root=root
        self.root.geometry("1100x680+200+50")
        self.root.title("ADMIN WINDOW")
        self.root.resizable(False,False)
        #commands to place objects in window
        title=Label(self.root,text="ADMIN",font=("times new roman",40),bg='#008000',anchor='w') #to place title in the window
        title.place(x=0,y=0,relwidth=1)

        menu_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        menu_frame.place(x=450,y=150,width=200,height=200)
        menu_frame_title=Label(menu_frame,text="MENU",font=("times new roman",18),bg='blue',anchor='w')
        menu_frame_title.place(x=0,y=0,relwidth=1)
        #Buttons
        attendence_btn=Button(menu_frame,text="Attendence",command=self.attendence,font=("times new roman",15,"bold"),bg="Green")
        attendence_btn.place(x=30,y=50)
        employee_btn=Button(menu_frame,text="Employee details",command=self.details,font=("times new roman",15,"bold"),bg="Green")
        employee_btn.place(x=30,y=100)
        #label to display PRN text
        display_lbl=Label(menu_frame,text="PRN: ",font=("times new roman",15,"bold"),bg="white")
        display_lbl.place(x=30,y=150)
        #text box to take employee PRN as input
        emp_PRN=Entry(menu_frame,textvariable=self.PRN,font=("times new roman",15),bg="light yellow",width=6)
        emp_PRN.place(x=100,y=150)

        output_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        output_frame.place(x=50,y=350,width=1000,height=250)
        output_frame_title=Label(output_frame,text="Result",font=("times new roman",18),bg="blue",anchor='w')
        output_frame_title.place(x=0,y=0,relwidth=1)

        self.msg="select a option to display result"
        self.msg_lbl=Label(output_frame,text=self.msg,font=("times new roman",15,"bold"),bg="green",fg="white")
        self.msg_lbl.place(x=10,y=35,width=980,height=280)

    def attendence(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if(self.key==0):
            mycursor.execute(f"select Date from absentees where Date='{date.today()}'")
            check=mycursor.fetchone()
            if (str(type(check))[8:16])=="NoneType":
                mycursor.execute("select count(PRN) from emp_details where login_time is not NULL and logout_time is not NULL")
                check1=mycursor.fetchone()
                for i in check1:
                    mycursor.execute(f"insert into absentees(Date,attendees) values('{date.today()}',{i})") #to store count of that day in absentees table
                self.msg=i
                self.msg_lbl.configure(text=f"Today'S Attendence : {i}")
                if(int(current_time[0:2])>=5 or int(current_time[0:2])<=9):
                    mycursor.execute("update emp_details set login_time=NULL")
                    mycursor.execute("update emp_details set logout_time=NULL")
                    db.commit()
                mycursor.execute("select PRN from emp_details where login_time is NULL and logout_time is NULL")
                check2=mycursor.fetchall()
                sample_list=[]
                for i in check2:
                    sample_list.append(i[0])
                for i in range(0,len(sample_list)):
                    val=i+1
                    mycursor.execute(f"update absentees set absentee_{val}={sample_list[i]} where Date='{date.today()}'")
                    db.commit()
                self.key=1
            else:
                self.msg_lbl.configure(text="Today's attendence is aldready been marked") 
        else:
            self.msg_lbl.configure(text="Use absentees button before attendence")


    def details(self):
        #PRN=self.PRN.get()
        mycursor.execute(f"select * from emp_details where PRN={self.PRN.get()}")
        check=mycursor.fetchone()
        final1=[]
        for i in check:
            final1.append(i)
        final_str=f"PRN:{final1[0]}\nName:{final1[1]}\nGender:{final1[2]}\nContact_no:{final1[3]}\nDesignation:{final1[4]}\n"
        mycursor.execute(f"select * from address where PRN={self.PRN.get()}")
        check1=mycursor.fetchone()
        final2=[]
        for i in check1:
            final2.append(i)
        final_str=final_str+f"Address: {final2[1]}, {final2[2]}, {final2[3]}, {final2[4]}, {final2[5]}."
        self.msg_lbl.config(text=final_str) 
            

#window4 for admin view
def admin_call_func():
    window3=Toplevel(window1)
    admin_obj=admin(window3)
    window3.mainloop()
    #window3.title("ADMIN WINDOW")


#Main window with admin,register and scan options or HOME PAGE
window1=Tk()
#window 1 properties like geometry and resize things
window1.geometry("1100x680+200+50")
window1.title("WELCOME WINDOW")
window1.resizable(False,False)
#Title of the window
title=Label(window1,text="HOME PAGE",font=("times new roman",40),bg="green",anchor="w")
title.place(x=0,y=0,relwidth=1)
#Frame in the window
opt_frame=Frame(window1,bd=3,relief=RIDGE,bg="white")
opt_frame.place(x=100,y=100,width=880,height=500)
#Buttons in opt_frame
#admin button
admin_btn=Button(opt_frame,text="ADMIN",command=lambda:admin_call_func(),font=("times new roman",15),bg="blue",)
admin_btn.place(x=100,y=380)
#generate button
gen_btn=Button(opt_frame,text="GENERATE",command=lambda:generate(),font=("times new roman",15),bg="blue")
gen_btn.place(x=350,y=380)
#scan button
scan_btn=Button(opt_frame,text="SCAN",command=camera,font=("times new roman",15),bg="blue")
scan_btn.place(x=650,y=380)
#image labels 
#admin image label
img_admin=Image.open(r"C:\Users\User\Documents\5th sem\SL_project\admin.png") #to load image
final1=ImageTk.PhotoImage(img_admin) #to pass to label
admin_img=Label(opt_frame,image=final1,bg="black") #passing image to label to display
admin_img.place(x=50,y=120)
#generate image label
img_gen=Image.open(r"C:\Users\User\Documents\5th sem\SL_project\QR_img.png") #to load image
img_gen=resizeimage.resize_cover(img_gen,[190,240])
final2=ImageTk.PhotoImage(img_gen) #to pass to label
gen_img=Label(opt_frame,image=final2,bg="black") #passing image to label to display
gen_img.place(x=310,y=120)
#scan image label
img_scn=Image.open(r"C:\Users\User\Documents\5th sem\SL_project\scan.jpg") #to load image
img_scn=resizeimage.resize_cover(img_scn,[190,240])
final3=ImageTk.PhotoImage(img_scn) #to pass to label
scn_img=Label(opt_frame,image=final3,bg="black") #passing image to label to display
scn_img.place(x=580,y=120)
message="Select a option to continue"
msg_label=Label(opt_frame,text=message,font=("times new roman",18),fg="dark green")
msg_label.place(x=280,y=440)
window1.mainloop()