import tkinter as tk
import time,json
from tkinter import messagebox,ttk

# stop horloge
stop = False 
local = True
def stopHorloge():
    global stop
    
    if(not stop):
        btn_stop.config(text="Mettre en marche")
        stop =True
    else:
        btn_stop.config(text="Arreter l'horloge")
        stop = False
        misAjourHeur()
    return stop
# change de format
am_pm = False
def changeFormat():
    global am_pm
    if(not am_pm):
        formatTime.config(text="24h")
        am_pm = True
    else:
        formatTime.config(text="AM - PM")
        am_pm = False
    
    return am_pm
def enregistreAlarme():
    # recuperation des donnée du formulaire
    h = entry_heur.get()
    min = entry_minutes.get()
    sec = entry_secondes.get()
        
    try:
        h = int(h)
        min = int(min)
        sec = int(sec)
    except Exception:
        messagebox.showerror("Error","impossible d'avoir des heurs de cette format")
            
    if((h >=24 or h < 0) or (min >=60 or min < 0) or (sec >= 60 or sec < 0)):
        messagebox.showerror("Erorr","merci de bien vouloire rensseigner des valeur d'heur et/ou de minutes et/ou de seconde valide")
    else:
        try:
            with open("enregistreAlarme.json","r") as dataAlaram:
                data = json.load(dataAlaram)
        except:
            fichier = open("enregistreAlarme.json","w")
            data = []
            fichier.write(json.dumps(data))
            fichier.close()
        # verification de l'existance de l'alarme dans le fichier json
        exist = False 
        if data != []:
            for i in data:
                if(h == i["heur"] and min == i["minute"] and sec ==i["seconde"]):
                    exist = True
        if exist :
            messagebox.showerror("Error","cette alarme est dejà en registrez")
        else:
            obj = {
                "heur":h,
                "minute":min,
                "seconde":sec
            }
            data.append(obj)
            fichier = open("enregistreAlarme.json","w")
            fichier.write(json.dumps(data,indent=True))
            fichier.close()
            messagebox.showinfo("Success","l'Alarme a bien été enregistrez")
            block.destroy()
def Regle_heur():
    
    global local,heur,minute,seconde
    
    h = entry_heur.get()
    min = entry_minutes.get()
    sec = entry_secondes.get()
      
    try:
        h = int(h)
        min = int(min)
        sec = int(sec)
    except Exception:
        messagebox.showerror("Error","impossible d'avoir des heurs de cette format")
            
    if((h >=24 or h < 0) or (min >=60 or min < 0) or (sec >= 60 or sec < 0)):
        messagebox.showerror("Erorr","merci de bien vouloire rensseigner des valeur d'heur et/ou de minutes et/ou de seconde valide")
    else:
        heur = h
        minute = min
        seconde = sec
        local = False
# gestion des alarmes

def alarme():
    global block,entry_heur,entry_minutes,entry_secondes
    
    block = tk.Frame(fenetre,bg="#cdebff")
    block.place(x=25,y=250,width=340,height=130)
    
    lr_heur = tk.Label(block,fg="black",font=('calibrie',12),text="Hh",bg="#cdebff").place(x=10,y=40)
    
    entry_heur = ttk.Spinbox(block,from_=0,to=24,font=('calibrie',12))
    entry_heur.place(x=40,y=40,width=50,height=25)
    
    
    entry_minutes = ttk.Spinbox(block,from_=0,to=59,font=("calibire",12))
    entry_minutes.place(x=150,y=40,width=50,height=25)
    lr_minute = tk.Label(block,fg='black',font=("calibrie",12),text="Mm",bg="#cdebff").place(x=110,y=40)
    
    lr_seconde = tk.Label(block,fg="black",font=("calibrie",12),text="Sec",bg="#cdebff").place(x=210,y=40) 
    entry_secondes = ttk.Spinbox(block, from_=0,to=59,font=("calibrie",12))
    entry_secondes.place(x=250,y=40,width=50, height=25)
    
    btn_reglage = tk.Button(block,text="OK",fg='black', command=enregistreAlarme)
    btn_reglage.place(x=100,y=80,width=50)
    
    btn_reglage = tk.Button(block,text="Regler",fg='black', command=Regle_heur)
    btn_reglage.place(x=170,y=80,width=50)
    
def heur_local():
    
    global tim,heur,minute,seconde
    
    tim = time.localtime()
    heur = tim.tm_hour
    minute = tim.tm_min
    seconde = tim.tm_sec
    label_am_pm = tk.Label(div,font=('calibri',15,'bold'),fg="black")
    label_am_pm.place(x=235, y=30, width=65,height=50)
    if(am_pm):
        if(heur > 12):
            heur -= 12
            label_am_pm.config(text="PM")
        else:
            label_am_pm.config(text="AM")    

def regalge_heur():
    global heur,minute,seconde
    if(heur <=23):
        if minute <= 59:
            if seconde <=59:
                seconde +=1
            else:
                seconde = 0
                minute +=1
        else:
            minute = 0
            heur += 1
    else:
        heur = 0
        minute = 0
        seconde = 0
    

#Actualiser Heur 
def misAjourHeur():
    
    if(local):
        heur_local()
    else:
        regalge_heur()
        
    label_heur.config(text=heur)
    label_minute.config(text=minute)
    label_seconde.config(text=seconde)
    
    try:
        with open("enregistreAlarme.json","r") as dataAlarme:
            alarmes = json.load(dataAlarme)
    except Exception:
        alarmes = []
        pass
    if(alarmes !=[]):
        for i in alarmes:
            if(heur == i["heur"] and minute == i["minute"] and seconde == i["seconde"]):
                txt = "Votre Alert de : {}h {}min {}sec est arrivée"
                messagebox.showinfo("success",txt.format(heur,minute,seconde))
    if(stop):
        pass
    else:
        div.after(1000,misAjourHeur)
    
    

# fenetre principale
fenetre = tk.Tk()
fenetre.geometry("600x400")
fenetre.title("Horloge")
fenetre.iconbitmap("images/horloge.ico")
fenetre.resizable(width=False,height=False)

# block d'affichage de l'horloge
div = tk.Frame(fenetre)
div.place(x=175,y=100,width=500,height=200)

# heur
label_heur = tk.Label(div,bg="grey",font=('calibrie',15,'bold'),fg="black")
label_heur.place(x=10, y=30, width=65,height=50)
name_heur = tk.Label(div,text="Heur",bg="grey",font=('calibrie',10,'bold'),fg="black").place(x=10, y=100, width=65,height=25)

# Minutes
label_minute = tk.Label(div,bg='grey',font=('calibrie',15,'bold'),fg="black")
label_minute.place(x=85, y=30, width=65,height=50)
name_minunte = tk.Label(div,text="Minute",bg="grey",font=('calibrie',10,'bold'),fg="black").place(x=85, y=100, width=65,height=25)

# Secondes
label_seconde = tk.Label(div,font=('calibri',15,'bold'),fg="black",bg='grey')
label_seconde.place(x=160, y=30, width=65,height=50)
name_seconde = tk.Label(div,text="Seconde",bg="grey",font=('calibrie',10,'bold'),fg="black").place(x=160, y=100, width=65,height=25)


# button d'alarme
btn_stop = tk.Button(fenetre, text="Alarme", bg="#ff4e0f",fg="white",font=('calibrie',10,'bold'),command=alarme)
btn_stop.place(x=450,y=20,width=130,height=30)

# button de reglage
btn_regleHeur = tk.Button(fenetre, text="Reglage", bg="grey",fg="white",font=('calibrie',10,'bold'),command=alarme)
btn_regleHeur.place(x=450,y=60,width=130,height=30)

# format horloge
formatTime = tk.Button(fenetre, text="AM - PM", bg="grey",fg="white",font=('calibrie',10,'bold'),command=changeFormat)
formatTime.place(x=10,y=20,width=70,height=30)

# supenssion time 
btn_stop = tk.Button(fenetre, text="Arreter l'horloge", bg="#ff4e0f",fg="white",font=('calibrie',10,'bold'),command=stopHorloge)
btn_stop.place(x=230,y=80,width=140,height=30)

# supenssion time 
btn_close= tk.Button(fenetre, text="Quiter", bg="grey",fg="white",font=('calibrie',10,'bold'),command=fenetre.quit)
btn_close.place(x=400,y=340,width=140,height=30)
# affichage de l'horloge
misAjourHeur()

fenetre.mainloop()
