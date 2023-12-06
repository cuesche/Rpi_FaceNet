import tkinter as tk
import tkinter.messagebox
import re
import webbrowser
import time

import recognize_face


class GUI:
    
    def __init__(self):
        
        self.person="X"
        #self.browser=webdriver.Chrome()
        
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
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="red", fg="black", command=self.lo_normal)
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
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="red", fg="black", command=self.lo_pers_cont)
        self.buttonYes.place(x=62, y=30)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="white", fg="black")
        self.buttonNO.place_forget() 
                
        return
    
    def should_show_pers_cont(self):
        
        self.root.geometry("430x120+700+350")
        
        #labels
        self.labelBig.config(text="Willst du deinen eigenen Inhalt sehen?", font=("Arial Bold", 12), bg="white", fg="black")
        self.labelBig.place(x=50, y=30)
        
        self.labelSmall.config( font=("Arial Bold", 15), bg="white", fg="black") 
        self.labelSmall.place(x=50, y=0)
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="green", fg="black",command=self.lo_should_show_pers_cont)
        self.buttonYes.place(x=360, y=70)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="red", fg="black",command=self.normal)
        self.buttonNO.place(x=50, y=70)
        return
    
    def no_pers_detected(self):
        
        self.root.geometry("430x100+700+350")
        
        #labels
        self.labelBig.config(text="Keine Person erkannt, wiederholen?", font=("Arial Bold", 15), bg="white", fg="black")
        self.labelBig.place(x=50, y=0)
        
        self.labelSmall.config(text="Zurück?", font=("Arial Bold", 10), bg="white", fg="black") 
        self.labelSmall.place_forget()
        

        #buttons
        self.buttonYes.config(text="JA", font=("Arial Bold", 10), bg="green", fg="black",command=self.lo_normal)
        self.buttonYes.place(x=360, y=50)
        
        self.buttonNO.config(text="NEIN", font=("Arial Bold", 10), bg="red", fg="black",command=self.normal)
        self.buttonNO.place(x=50, y=50)
        return 
    
########### Logik ###########
        
        
    def lo_normal(self):
        '''
        gesichtserkennung wird auufgerufen
        person wird gespeichert
        Kontrolle ob Person in Datenbank
        '''
    
        labels=load_labels("people_labels.txt")
        
        self.person=recognize_face.main()
        
        if self.person in labels.values() and self.person!="unknown":
            #weiterleitung frage persöhnlicher inhalt
            self.should_show_pers_cont()
            text="Hallo "+self.person
            self.labelSmall.config(text=text)
            
            
        else: 
            #weiterleitung frage nochmal
            self.no_pers_detected()
            #self.person="Monika Müller" ##################entfernen
   
        return
    
    def lo_should_show_pers_cont(self):
        #Persöhnlicher Inhalt anzeigen
        self.pers_cont()
        persöhnlicherInhalt=load_labels("persöhnlicher_inhalt.txt")
        print(persöhnlicherInhalt.keys(),"\n",self.person)
        
        if str(self.person) in persöhnlicherInhalt.keys():
            #self.browser.get(persöhnlicherInhalt[self.person])
            webbrowser.open(persöhnlicherInhalt[self.person])
            
        else:
            print("Kein Persöhnlicher Inhalt")
        
        return
    
    def lo_pers_cont(self):
        #persöhnlicher content schliessen
        #self.browser.quit()
        webbrowser.close()
        print("dashboard schliessen")
        self.normal()
        self.person="X"
        return
    
    
        
def load_labels(path):
    dict = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split('::')  # Annahme, dass der Separator ein Tabulator ist
            dict[key] = value
        
    return dict
    
        

if __name__ == "__main__":
    gui = GUI()
    
    
    
    
        
