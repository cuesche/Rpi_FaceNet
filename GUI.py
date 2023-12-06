import tkinter as tk
import tkinter.messagebox

import time

import recognize_face as rec_face 

class GUI:
    
    def __init__(self):
        
        #init  
        self.root = tk.Tk()
        self.root.title("Persöhnlicher Inhalt")
        self.root.geometry("140x60+10+10")
        self.root.configure(background="white")
        
        #labels
        self.labelBig = tk.Label(self.root, text="Willst du deinen eigenen Inhalt sehen", font=("Arial Bold", 10), bg="white", fg="black")
        self.labelBig.place_forget()
        
        self.labelSmall = tk.Label(self.root, text="Persöhnicher Inhalt?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place(x=7, y=0)
        

        #buttons
        self.buttonYes = tk.Button(self.root, text="JA", font=("Arial Bold", 10), bg="red", fg="black", command=self.lo_normal)
        self.buttonYes.place(x=62, y=30)
        
        self.buttonNO = tk.Button(self.root, text="NEIN", font=("Arial Bold", 10), bg="white", fg="black")
        self.buttonNO.place()
        self.buttonNO.place_forget()
        
        
        
        self.root.mainloop()
        
    def normal(self):       
        
        self.root.geometry("140x60+10+10")
        
        #labels
        self.labelBig.config(text="Willst du deinen eigenen Inhalt sehen", font=("Arial Bold", 10), bg="white", fg="black")
        self.labelBig.place_forget()
        
        self.labelSmall.config(text="Persöhnicher Inhalt?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place(x=7, y=0)   
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="red", fg="black")
        self.buttonYes.place(x=62, y=30)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="white", fg="black")
        self.buttonNO.place_forget()

        return
        
    def pers_cont(self):
        
        self.root.geometry("140x60+10+10")
        
        #labels
        self.labelBig.config(text="Willst du deinen eigenen Inhalt sehen", font=("Arial Bold", 10), bg="white", fg="black")
        self.labelBig.place_forget()
        
        self.labelSmall.config(text="Zurück?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place(x=50, y=0)   
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="red", fg="black")
        self.buttonYes.place(x=62, y=30)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="white", fg="black")
        self.buttonNO.place_forget() 
                
        return
    
    def should_show_pers_cont(self):
        
        self.root.geometry("430x100+700+350")
        
        #labels
        self.labelBig.config(text="Willst du deinen eigenen Inhalt sehen?", font=("Arial Bold", 15), bg="white", fg="black")
        self.labelBig.place(x=50, y=0)
        
        self.labelSmall.config(text="Zurück?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place_forget()
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="green", fg="black")
        self.buttonYes.place(x=360, y=50)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="red", fg="black")
        self.buttonNO.place(x=50, y=50)
        
        return
    
    def no_pers_detected(self):
        
        self.root.geometry("430x100+700+350")
        
        #labels
        self.labelBig.config(text="Keine Person erkannt, wiederholen?", font=("Arial Bold", 15), bg="white", fg="black")
        self.labelBig.place(x=50, y=0)
        
        self.labelSmall.config(text="Zurück?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place_forget()
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="green", fg="black")
        self.buttonYes.place(x=360, y=50)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="red", fg="black")
        self.buttonNO.place(x=50, y=50)
        return 
    
########### Logik ###########
        
        # 0 = normal
        # 1 = pers_cont
        # 2 = should_show_pers_cont
        # 3 = no_pers_detected
        
    def lo_normal(self):
        person=rec_face.main()
        
        if person==True:
            self.should_show_pers_cont()
            
        if person==False:
            self.no_pers_detected()       
        return
    
    def state_one(self):
        
        self.pers_cont()
        self.state = 1
        return
    
    def state_two(self):
        
        self.should_show_pers_cont()
        self.state = 2
        return
    
    def state_three(self):
        
        self.no_pers_detected()
        self.state = 3
        return
        

    
        

if __name__ == "__main__":
    gui = GUI()
    
    
    
    
        
