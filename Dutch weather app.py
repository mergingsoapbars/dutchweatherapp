#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import math
import tkinter.font as tkfont
import sqlite3
import json
import requests
import re


# In[2]:


root = Tk()


# In[3]:


app_wdth = 1025
app_hght = 700

scrn_wdth = root.winfo_screenwidth()
scrn_hght = root.winfo_screenheight()

x = (scrn_wdth / 2) - (app_wdth / 2)
y = (scrn_hght / 2) - (app_hght / 2)


# In[4]:


root.title("Het weer in Nederland")
root.geometry(f"{app_wdth}x{app_hght}+{int(x)}+{int(y)}")
root.configure(bg='#cfcfcf')
root.iconbitmap("icon.ico")


# In[5]:


root.columnconfigure(0, weight=1000)
root.columnconfigure(1, weight=1000)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1000)
root.rowconfigure(2, weight=0)


# In[6]:


helv = tkfont.Font(family="Helvetica", size=12)


# In[7]:


loc_e = Entry(root)
loc_e.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky="NESW")
loc_e['font'] = helv


# In[8]:


ans_e = Text(root,bg="#cfcfcf",relief=SUNKEN)
ans_e.grid(row=1,column=0,columnspan=2,ipady=30,ipadx=150,sticky="NESW")
ans_e['font'] = helv


# In[9]:


municipalities = ['Almelo', 'Veere', 'Coevorden', 'Aalsmeer', 'Haarlemmermeer', 'Zaltbommel', 'Noardeast-Fryslân', 'Aalten', 'Nieuwkoop', 'Assen', 'Sluis', 'Alphen aan den Rijn', 'Laarbeek', 'Opmeer', 'Súdwest-Fryslân', 'Medemblik', 'Nissewaard', 'Haarlemmermeer', 'De Ronde Venen', 'Waadhoeke', 'Barneveld', 'Leusden', 'Goeree-Overflakkee', 'Zundert', 'West Betuwe', 'Het Hogeland', 'Westerkwartier', 'Bloemendaal', 'Zevenaar', 'Druten', 'Bergen (L.)', 'Dinkelland', 'Castricum', 'Heerenveen', 'De Fryske Marren', 'Tubbergen', 'Alblasserdam', 'Leeuwarden', 'Heerenveen', 'Tytsjerksteradiel', 'Maasdriel', 'Alkmaar', 'Súdwest-Fryslân', 'Almelo', 'Lochem', 'Almere', 'Altena', 'West Maas en Waal', 'Alphen-Chaam', 'Alphen aan den Rijn', 'Noordenveld', 'Stadskanaal', 'De Wolden', 'Hoogeveen', 'West Maas en Waal', 'Hof van Twente', 'Vijfheerenlanden', 'Aa en Hunze', 'Horst aan de Maas', 'Utrechtse Heuvelrug', 'Amersfoort', 'Krimpenerwaard', 'Maasdriel', 'De Ronde Venen', 'Amstelveen', 'Beekdaelen', 'Amsterdam', 'Ouder-Amstel', 'Altena', 'Het Hogeland', 'Overbetuwe', 'Aa en Hunze', 'Medemblik', 'Hardenberg', 'Hardenberg', 'Hardenberg', 'Lingewaard', 'Zevenaar', 'Noardeast-Fryslân', 'Wijdemeren', 'Aa en Hunze', 'Hollands Kroon', 'Aa en Hunze', 'Aa en Hunze', 'Westerveld', 'De Wolden', 'Westerwolde', 'Apeldoorn', 'Westerwolde', 'Ooststellingwerf', 'West Maas en Waal', 'Appingedam', 'Venlo', 'Molenlanden', 'Middelburg', 'Arnhem', 'Ommen', 'Súdwest-Fryslân', 'Buren', 'West Betuwe', 'Assen', 'Zaanstad', 'Asten', 'Noardeast-Fryslân', 'Achtkarspelen', 'Zeist', 'Koggenland', 'Terneuzen', 'Montferland', 'Terschelling', 'Waadhoeke', 'Bronckhorst', 'De Ronde Venen', 'Leeuwarden', 'Borsele', 'Baarle-Nassau', 'Peel en Maas', 'Steenwijkerland', 'Baarn', 'Steenwijkerland', 'Zevenaar', 'Altena', 'Oldambt', 'Haarlemmermeer', 'Leudal', 'Het Hogeland', 'Gemert-Bakel', 'De Fryske Marren', 'Opsterland', 'Wijchen', 'Midden-Drenthe', 'De Fryske Marren', 'Hardenberg', 'Aa en Hunze', 'Aa en Hunze', 'Ameland', 'Simpelveld', 'Eijsden-Margraten', 'Noordoostpolder', 'De Fryske Marren', 'Lochem', 'Barendrecht', 'Emmen', 'Barneveld', 'Hollands Kroon', 'Steenwijkerland', 'Wijchen', 'Deventer', 'Breda', 'Alphen-Chaam', 'Leeuwarden', 'Het Hogeland', 'Maasgouw', 'Montferland', 'Beek', 'Berg en Dal', 'Laarbeek', 'Apeldoorn', 'Apeldoorn', 'Cuijk', 'Oldambt', 'Ommen', 'Ommen', 'West Betuwe', 'Beesel', 'Edam-Volendam', 'Opsterland', 'Midden-Drenthe', 'Haarlemmermeer', 'Venlo', 'Westerwolde', 'Berkelland', 'Steenwijkerland', 'Eijsden-Margraten', 'Lingewaard', 'West Maas en Waal', 'Bloemendaal', 'Ede', 'Coevorden', 'Medemblik', 'Lopik', 'Hof van Twente', 'Alphen aan den Rijn', 'Zandvoort', 'Berg en Dal', 'Valkenburg aan de Geul', 'Krimpenerwaard', 'Bergeijk', 'Bergen (NH.)', 'Bergen (NH.)', 'Bergen (L.)', 'Bergen op Zoom', 'Hardenberg', 'Wijchen', 'Oss', 'Lansingerland', 'Peel en Maas', 'Lansingerland', 'Tilburg', 'Krimpenerwaard', 'Koggenland', 'Sint-Michielsgestel', 'Waadhoeke', 'Zaltbommel', 'Best', 'Boxmeer', 'Losser', 'Beuningen', 'Buren', 'Gulpen-Wittem', 'Beverwijk', 'Dronten', 'Delfzijl', 'Sluis', 'Terneuzen', 'Hilvarenbeek', 'Haaren', 'Veere', 'De Bilt', 'De Bilt', 'Beekdaelen', 'Waadhoeke', 'Waadhoeke', 'Bladel', 'Steenwijkerland', 'Blaricum', 'Oldambt', 'Súdwest-Fryslân', 'Lansingerland', 'Weststellingwerf', 'Molenlanden', 'Weststellingwerf', 'Waadhoeke', 'Noardeast-Fryslân', 'Westerwolde', 'Venray', 'Bloemendaal', 'Hoorn', 'Steenwijkerland', 'Súdwest-Fryslân', 'Simpelveld', 'Bodegraven-Reeuwijk', 'Boekel', 'Achtkarspelen', 'Waadhoeke', 'Groningen', 'Westerkwartier', 'Haarlemmermeer', 'Weststellingwerf', 'Waadhoeke', 'Súdwest-Fryslân', 'Goeree-Overflakkee', 'Heerenveen', 'Smallingerland', 'De Fryske Marren', 'Berkelland', 'Borger-Odoorn', 'Midden-Groningen', 'Veendam', 'Delfzijl', 'Sittard-Geleen', 'Borne', 'Almelo', 'Noardeast-Fryslân', 'Borsele', 'Zeist', 'Westerveld', 'Alphen aan den Rijn', 'Halderberge', 'Rotterdam', 'Westerwolde', 'Stede Broec', 'West Maas en Waal', 'Midden-Drenthe', 'Boxmeer', 'Boxtel', 'Montferland', 'Zaltbommel', 'Molenlanden', 'Noardeast-Fryslân', 'Breda', 'Aalten', 'Oude IJsselstreek', 'Hollands Kroon', 'Súdwest-Fryslân', 'Sluis', 'Stichtse Vecht', 'Wijdemeren', 'Brielle', 'Westerkwartier', 'Leeuwarden', 'Súdwest-Fryslân', 'De Fryske Marren', 'Waterland', 'Langedijk', 'Horst aan de Maas', 'Meppel', 'Horst aan de Maas', 'Raalte', 'Dantumadiel', 'Bronckhorst', 'Borger-Odoorn', 'Borger-Odoorn', 'Schouwen-Duiveland', 'Zaltbommel', 'Hardenberg', 'Hardenberg', 'Twenterand', 'Schouwen-Duiveland', 'Brummen', 'Brunssum', 'Midden-Drenthe', 'Sittard-Geleen', 'Cranendonck', 'Cranendonck', 'Cranendonck', 'Leudal', 'Borger-Odoorn', 'Borger-Odoorn', 'Haarlemmermeer', 'Achtkarspelen', 'Steenwijkerland', 'Meerssen', 'Tynaarlo', 'Bunnik', 'Bunschoten', 'Noardeast-Fryslân', 'Ameland', 'Buren', 'Texel', 'Schagen', 'Haarlemmermeer', 'Schouwen-Duiveland', 'Tytsjerksteradiel', 'Súdwest-Fryslân', 'Noardeast-Fryslân', 'Gooise Meren', 'West Betuwe', 'Buren', 'Eijsden-Margraten', 'Sluis', 'Schagen', 'Capelle aan den IJssel', 'Baarle-Nassau', 'Venray', 'Bladel', 'Castricum', 'Alphen-Chaam', 'Hulst', 'Texel', 'Coevorden', 'Noord-Beveland', 'Hardenberg', 'Deventer', 'Súdwest-Fryslân', 'Wijk bij Duurstede', 'Noordoostpolder', 'Vught', 'Haarlemmermeer', 'Cuijk', 'Culemborg', 'Hellendoorn', 'Hellendoorn', 'Gorinchem', 'Coevorden', 'Coevorden', 'Coevorden', 'Dalfsen', 'Ommen', 'Dantumadiel', 'Westerveld', 'Súdwest-Fryslân', 'Hardenberg', 'Súdwest-Fryslân', 'Ede', 'Druten', 'West Betuwe', 'Waadhoeke', 'Hof van Twente', 'Pijnacker-Nootdorp', 'De Fryske Marren', 'Delft', 'Delfzijl', 'Zaltbommel', 'Oss', 'Dinkelland', 'Deurne', 'Dinkelland', 'Oldenzaal', 'Oss', 'Aa en Hunze', 'Deventer', 'Montferland', 'Oss', 'Diemen', 'Hof van Twente', 'Deventer', 'Rheden', 'Hilvarenbeek', 'Westerveld', 'Westerveld', 'Hardenberg', 'De Fryske Marren', 'Steenbergen', 'Aalten', 'Coevorden', 'Schagen', 'Goeree-Overflakkee', 'Neder-Betuwe', 'Beekdaelen', 'Doesburg', 'Doetinchem', 'Heusden', 'Westerkwartier', 'Noardeast-Fryslân', 'Zeist', 'Westerveld', 'Veere', 'Tynaarlo', 'Dongen', 'Waadhoeke', 'De Fryske Marren', 'Ooststellingwerf', 'Utrechtse Heuvelrug', 'Lingewaard', 'Elburg', 'Renkum', 'Dordrecht', 'Oosterhout', 'Smallingerland', 'Opsterland', 'Smallingerland', 'Schouwen-Duiveland', 'Bronckhorst', 'West Maas en Waal', 'Utrechtse Heuvelrug', 'Oldambt', 'Bodegraven-Reeuwijk', 'Velsen', 'Alkmaar', 'Overbetuwe', 'Borsele', 'Dantumadiel', 'Midden-Drenthe', 'Drimmelen', 'Achtkarspelen', 'De Wolden', 'Altena', 'Waadhoeke', 'Dronten', 'Borger-Odoorn', 'Borger-Odoorn', 'Borger-Odoorn', 'Heusden', 'Druten', 'Duiven', 'Ouder-Amstel', 'Eersel', 'Sint-Michielsgestel', 'Altena', 'Westerveld', 'Leeuwarden', 'Tytsjerksteradiel', 'Súdwest-Fryslân', 'Leeuwarden', 'Tytsjerksteradiel', 'Súdwest-Fryslân', 'Echt-Susteren', 'Neder-Betuwe', 'De Wolden', 'De Fryske Marren', 'De Fryske Marren', 'Buren', 'Eijsden-Margraten', 'Edam-Volendam', 'Ede', 'Ede', 'Noardeast-Fryslân', 'Sluis', 'Lochem', 'Tynaarlo', 'Tynaarlo', 'Bunschoten', 'Eemnes', 'Het Hogeland', 'Noordenveld', 'Het Hogeland', 'Loppersum', 'Noordenveld', 'Brummen', 'Eersel', 'Borger-Odoorn', 'Borger-Odoorn', 'Borger-Odoorn', 'De Fryske Marren', 'Steenwijkerland', 'Altena', 'Aa en Hunze', 'Aa en Hunze', 'Aa en Hunze', 'Aa en Hunze', 'Peel en Maas', 'Bergen (NH.)', 'Bergen (NH.)', 'Bergen (NH.)', 'Berkelland', 'Eijsden-Margraten', 'Eindhoven', 'Sittard-Geleen', 'Aa en Hunze', 'De Fryske Marren', 'Elburg', 'Aa en Hunze', 'Aa en Hunze', 'Hoogeveen', 'Gulpen-Wittem', 'Leudal', 'Rheden', 'Schouwen-Duiveland', 'Borger-Odoorn', 'Borsele', 'Midden-Drenthe', 'Gemert-Bakel', 'Heusden', 'Stein', 'Ooststellingwerf', 'Nunspeet', 'Overbetuwe', 'Rhenen', 'Noordoostpolder', 'Emmen', 'Emmen', 'Brummen', 'Epe', 'Noardeast-Fryslân', 'Enkhuizen', 'Noordoostpolder', 'Enschede', 'West Betuwe', 'Wierden', 'Westerkwartier', 'Epe', 'Gulpen-Wittem', 'Het Hogeland', 'Lochem', 'Emmen', 'Buren', 'Berg en Dal', 'Coevorden', 'Ermelo', 'Meierijstad', 'Hilvarenbeek', 'Haaren', 'Grave', 'Noordoostpolder', 'West Betuwe', 'Oude IJsselstreek', 'Etten-Leur', 'Rotterdam', 'Midden-Drenthe', 'De Wolden', 'Vijfheerenlanden', 'Horst aan de Maas', 'Beuningen', 'Borger-Odoorn', 'Borger-Odoorn', 'Borger-Odoorn', 'Borger-Odoorn', 'Súdwest-Fryslân', 'Kerkrade', 'Gulpen-Wittem', 'Westerkwartier', 'Dantumadiel', 'Delfzijl', 'Dantumadiel', 'Westerkwartier', 'Leeuwarden', 'Noardeast-Fryslân', 'Súdwest-Fryslân', 'Moerdijk', 'Oldambt', 'Waadhoeke', 'Tubbergen', 'Hoogeveen', 'Ooststellingwerf', 'De Fryske Marren', 'Súdwest-Fryslân', 'Terschelling', 'Noardeast-Fryslân', 'Midden-Groningen', 'Noordenveld', 'Waadhoeke', 'Westerveld', 'Leeuwarden', 'Opsterland', 'Midden-Groningen', 'Doetinchem', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Alphen-Chaam', 'Zaltbommel', 'Veere', 'Barneveld', 'Groningen', 'Midden-Drenthe', 'Westerkwartier', 'Loppersum', 'Loppersum', 'Tytsjerksteradiel', 'Grave', 'Aa en Hunze', 'Aa en Hunze', 'Aa en Hunze', 'Cranendonck', 'Aa en Hunze', 'Súdwest-Fryslân', 'Aa en Hunze', 'Twenterand', 'Noord-Beveland', 'Geertruidenberg', 'Nissewaard', 'Coevorden', 'Coevorden', 'Berkelland', 'Tubbergen', 'Westerveld', 'Oss', 'Venray', 'West Betuwe', 'Zoeterwoude', 'Geldrop-Mierlo', 'Sittard-Geleen', 'West Betuwe', 'Berkelland', 'Gemert-Bakel', 'Sint-Michielsgestel', 'Altena', 'Oude IJsselstreek', 'Lingewaard', 'Zwartewaterland', 'Gennep', 'Achtkarspelen', 'Heerenveen', 'Meerssen', 'Zevenaar', 'Altena', 'Molenlanden', 'Aa en Hunze', 'Aa en Hunze', 'Ommen', 'Steenwijkerland', 'Gilze en Rijen', 'Noardeast-Fryslân', 'Losser', 'Groningen', 'Barneveld', 'Delfzijl', 'Goeree-Overflakkee', 'Súdwest-Fryslân', 'Smallingerland', 'Goes', 'De Fryske Marren', 'Goirle', 'Hof van Twente', 'Koggenland', 'Gorinchem', 'Opsterland', 'Lochem', 'Gouda', 'Krimpenerwaard', 'Molenlanden', 'Hoeksche Waard', 'Leeuwarden', 'Houten', 'Hulst', 'Kampen', 'Alkmaar', 'Hardenberg', 'Peel en Maas', 'Leudal', 'Grave', 'Wijdemeren', 'Hoeksche Waard', 's-Gravenhage', 'Dongen', 'Borsele', 'Westland', 'Súdwest-Fryslân', 'Sittard-Geleen', 'Horst aan de Maas', 'Westerkwartier', 'Veere', 'Sluis', 'De Bilt', 'Boxmeer', 'Oost Gelre', 'Berg en Dal', 'Duiven', 'Bergen (NH.)', 'Tynaarlo', 'Aa en Hunze', 'Groningen', 'Eijsden-Margraten', 'Molenlanden', 'Stede Broec', 'Westerkwartier', 'Alkmaar', 'Leeuwarden', 'Horst aan de Maas', 'Gulpen-Wittem', 'Sittard-Geleen', 'Tytsjerksteradiel', 'West Betuwe', 'Haaksbergen', 'Lingewaard', 'Coevorden', 'Haaren', 'Tubbergen', 'Hellendoorn', 'Haarlem', 'Haarlemmermeer', 'Berkelland', 'Heusden', 'Utrecht', 'Krimpenerwaard', 'Leudal', 'Vijfheerenlanden', 'Hilvarenbeek', 'Leudal', 'Haarlemmermeer', 'Brummen', 'Bronckhorst', 'Noardeast-Fryslân', 'Bergen op Zoom', 'Twenterand', 'Westerkwartier', 'Gemert-Bakel', 'Altena', 'Reimerswaal', 'Noardeast-Fryslân', 'Noardeast-Fryslân', 'Noardeast-Fryslân', 'Bladel', 'Cuijk', 'Tubbergen', 'Elburg', 'Hardenberg', 'Harderwijk', 'Hardinxveld-Giessendam', 'Oss', 'Groningen', 'Lochem', 'De Fryske Marren', 'Hollands Kroon', 'Achtkarspelen', 'Midden-Groningen', 'Groningen', 'Harlingen', 'Woerden', 'Oost Gelre', 'Ede', 'Súdwest-Fryslân', 'Heerenveen', 'De Fryske Marren', 'Zwartewaterland', 'Hattem', 'Oldebroek', 'Ooststellingwerf', 'Ooststellingwerf', 'Medemblik', 'Westerveld', 'Westerveld', 'Alphen aan den Rijn', 'Alphen aan den Rijn', 'Maasdriel', 'Heusden', 'Terschelling', 'Súdwest-Fryslân', 'Maasgouw', 'Renkum', 'Oude IJsselstreek', 'Hardenberg', 'Heemskerk', 'Heemstede', 'Steenbergen', 'Nissewaard', 'Borsele', 'Goes', 'Goes', 'Heerde', 'Montferland', 'Kampen', 'Borsele', 'Heerenveen', 'Maasdriel', 'Heerhugowaard', 'Zwijndrecht', 'Roosendaal', 'Heerlen', 'Heusden', 'Bernheze', 'West Betuwe', 'Bernheze', 'Raalte', 'Heeze-Leende', 'Noardeast-Fryslân', 'Horst aan de Maas', 'Vijfheerenlanden', 'Leudal', 'Venray', 'Súdwest-Fryslân', 'Westland', 'Gennep', 'Gulpen-Wittem', 'Moerdijk', 'Hulst', 'Berg en Dal', 'Oldambt', 'Heiloo', 'Hoeksche Waard', 'Borsele', 'Raalte', 'Nissewaard', 'Oudewater', 'Peel en Maas', 'Den Helder', 'Deurne', 'Hellendoorn', 'Hellevoetsluis', 'West Betuwe', 'Midden-Groningen', 'Helmond', 'Haaren', 'Drechterland', 'Súdwest-Fryslân', 'Overbetuwe', 'Leeuwarden', 'Opsterland', 'Hendrik-Ido-Ambacht', 'Hengelo', 'Bronckhorst', 'Hof van Twente', 'Hulst', 'Koggenland', 'Waadhoeke', 'Roerdalen', 'Goeree-Overflakkee', 'Wijchen', 'Oss', 'Heusden', 'Roermond', 'Borne', " 's-Hertogenbosch", 'Overbetuwe', 'Zevenaar', 'West Betuwe', 'Overbetuwe', 'Oisterwijk', 'West Betuwe', 'Heumen', 'Aalten', 'Heusden', 'Asten', 'Renkum', 'Leudal', 'Tubbergen', 'Noardeast-Fryslân', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Harderwijk', 'Súdwest-Fryslân', 'Midden-Drenthe', 'Leeuwarden', 'Leeuwarden', 'Hillegom', 'Hilvarenbeek', 'Hilversum', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Hollands Kroon', 'Waadhoeke', 'Edam-Volendam', 'Borsele', 'De Ronde Venen', 'Vijfheerenlanden', 'Terneuzen', 'Rotterdam', 'Apeldoorn', 'Ede', 'Heerlen', 'Maasdriel', 'Weststellingwerf', 'Nijkerk', 'Halderberge', 'Wierden', 'De Bilt', 'Hoogeveen', 'Ameland', 'Coevorden', 'Rijssen-Holten', 'Boxmeer', 'Hardenberg', 'Hardenberg', 'Sittard-Geleen', 'Noardeast-Fryslân', 'Delfzijl', 'Súdwest-Fryslân', 'Overbetuwe', 'Westland', 'Haarlemmermeer', 'Sluis', 'Apeldoorn', 'Molenlanden', 'Reusel-De Mierden', 'Drimmelen', 'Bladel', 'Hardenberg', 'Woensdrecht', 'Westerveld', 'Midden-Drenthe', 'Hoogeveen', 'Midden-Groningen', 'Midden-Drenthe', 'Drechterland', 'Bronckhorst', 'Amersfoort', 'Amersfoort', 'Kaag en Braassem', 'Rotterdam', 'Opmeer', 'Terschelling', 'Hoorn', 'Midden-Delfland', 'Texel', 'Molenlanden', 'Heerenveen', 'Leudal', 'Westerkwartier', 'Het Hogeland', 'Druten', 'Horst aan de Maas', 'Oosterhout', 'Houten', 'Smallingerland', 'Het Hogeland', 'Woensdrecht', 'Zeist', 'Noordenveld', 'Den Helder', 'Oss', 'Lingewaard', 'Huizen', 'Loppersum', 'Beekdaelen', 'Reusel-De Mierden', 'Nunspeet', 'Hulst', 'Gilze en Rijen', 'Bronckhorst', 'Leeuwarden', 'Leudal', 'Tytsjerksteradiel', 'Maasdriel', 'Leeuwarden', 'Súdwest-Fryslân', 'De Fryske Marren', 'Weststellingwerf', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Staphorst', 'Súdwest-Fryslân', 'Velsen', 'Steenwijkerland', 'Kampen', 'IJsselstein', 'Sluis', 'Neder-Betuwe', 'Landsmeer', 'Waterland', 'Súdwest-Fryslân', 'Gulpen-Wittem', 'Waadhoeke', 'Buren', 'Súdwest-Fryslân', 'Leudal', 'Lopik', 'Beekdaelen', 'Noardeast-Fryslân', 'Leeuwarden', 'Leeuwarden', 'Leeuwarden', 'Noardeast-Fryslân', 'Wormerland', 'Tytsjerksteradiel', 'Opsterland', 'Westerkwartier', 'Lochem', 'Leeuwarden', 'De Fryske Marren', 'Noardeast-Fryslân', 'Heerenveen', 'Den Helder', 'Súdwest-Fryslân', 'Kaag en Braassem', 'Terschelling', 'Loon op Zand', 'Steenwijkerland', 'Steenwijkerland', 'Woerden', 'Kampen', 'Noord-Beveland', 'Kampen', 'Het Hogeland', 'Tiel', 'Buren', 'Kapelle', 'Hulst', 'Heerenveen', 'Noord-Beveland', 'Goes', 'Katwijk', 'Cuijk', 'Waterland', 'Vijfheerenlanden', 'Oss', 'Bronckhorst', 'Berg en Dal', 'Leudal', 'Tiel', 'Buren', 'Maasdriel', 'De Wolden', 'Kerkrade', 'Schouwen-Duiveland', 'Zaltbommel', 'Peel en Maas', 'Neder-Betuwe', 'Coevorden', 'Midden-Groningen', 'Montferland', 'Súdwest-Fryslân', 'Molenlanden', 'Terschelling', 'Hoeksche Waard', 'Voorst', 'Apeldoorn', 'Emmen', 'Emmen', 'Zundert', 'Borger-Odoorn', 'Voerendaal', 'Kapelle', 'Goes', 'Ede', 'Waadhoeke', 'Het Hogeland', 'Hardenberg', 'Twenterand', 'Hulst', 'Moerdijk', 'Eersel', 'Heerenveen', 'Leeuwarden', 'Stichtse Vecht', 'Langedijk', 'Alkmaar', 'De Wolden', 'Terneuzen', 'De Fryske Marren', 'Midden-Groningen', 'Hollands Kroon', 'Noardeast-Fryslân', 'Noardeast-Fryslân', 'Noardeast-Fryslân', 'Westerkwartier', 'Echt-Susteren', 'Peel en Maas', 'Texel', 'Zaanstad', 'Achtkarspelen', 'Barneveld', 'Barneveld', 'Westerkwartier', 'Súdwest-Fryslân', 'Smallingerland', 'Wijdemeren', 'Noord-Beveland', 'Alphen aan den Rijn', 'Veere', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Reimerswaal', 'Noordoostpolder', 'Hollands Kroon', 'Delfzijl', 'Hardenberg', 'Krimpenerwaard', 'Krimpen aan den IJssel', 'Lochem', 'Zaanstad', 'Horst aan de Maas', 'Midden-Groningen', 'Reimerswaal', 'Steenbergen', 'Súdwest-Fryslân', 'Aalsmeer', 'Steenwijkerland', 'Hulst', 'Borsele', 'Edam-Volendam', 'Uithoorn', 'Westland', 'Raalte', 'Bronckhorst', 'Rheden', 'Reusel-De Mierden', 'Baarn', 'Drimmelen', 'Midden-Groningen', 'Groningen', 'Medemblik', 'Hulst', 'Terschelling', 'Landgraaf', 'Sint Anthonis', 'Landsmeer', 'Wijk bij Duurstede', 'Ooststellingwerf', 'Weststellingwerf', 'Noordenveld', 'Mill en Sint Hubert', 'Molenlanden', 'Tubbergen', 'Moerdijk', 'Opsterland', 'De Fryske Marren', 'Lochem', 'Laren', 'Zevenaar', 'Dinkelland', 'Het Hogeland', 'Westerkwartier', 'Sint Anthonis', 'Westerkwartier', 'Heeze-Leende', 'Het Hogeland', 'Vijfheerenlanden', 'Vijfheerenlanden', 'Loppersum', 'Utrechtse Heuvelrug', 'Leeuwarden', 'De Fryske Marren', 'Leiden', 'Leiderdorp', 'Leidschendam-Voorburg', 'Kaag en Braassem', 'Haarlemmermeer', 'Krimpenerwaard', 'Leeuwarden', 'Groningen', 'Lelystad', 'Ommen', 'Dalfsen', 'Vaals', 'De Fryske Marren', 'Montferland', 'Nijmegen', 'Leeuwarden', 'Bergen op Zoom', 'Westerkwartier', 'Deventer', 'Venray', 'Wijchen', 'Leusden', 'Berg en Dal', 'Noordenveld', 'Brummen', 'Nederweert', 'Borsele', 'Vijfheerenlanden', 'Noardeast-Fryslân', 'Oost Gelre', 'Boxtel', 'Buren', 'Westland', 'Raalte', 'Apeldoorn', 'Someren', 'Terschelling', 'Laarbeek', 'Deurne', 'Oost Gelre', 'Noordenveld', 'Haarlemmermeer', 'Sittard-Geleen', 'Castricum', 'De Wolden', 'Cuijk', 'Maasgouw', 'Montfoort', 'Noardeast-Fryslân', 'Opsterland', 'Lisse', 'Haarlemmermeer', 'Oss', 'Oss', 'Zevenaar', 'Lochem', 'Apeldoorn', 'Stichtse Vecht', 'Stichtse Vecht', 'Súdwest-Fryslân', 'Montferland', 'Súdwest-Fryslân', 'Venlo', 'Súdwest-Fryslân', 'Duiven', 'Lingewaard', 'Oldebroek', 'Assen', 'Loon op Zand', 'Bernheze', 'Wijdemeren', 'Hardenberg', 'Lopik', 'Lopik', 'Loppersum', 'Delfzijl', 'Losser', 'Horst aan de Maas', 'Westerkwartier', 'Midden-Groningen', 'Heerenveen', 'Ede', 'Stede Broec', 'Westerkwartier', 'Hollands Kroon', 'Losser', 'Noordoostpolder', 'Hardenberg', 'Raalte', 'Opsterland', 'Bergeijk', 'Súdwest-Fryslân', 'Cranendonck', 'Utrechtse Heuvelrug', 'Utrechtse Heuvelrug', 'Stichtse Vecht', 'De Bilt', 'West Maas en Waal', 'Maasgouw', 'Peel en Maas', 'Hoeksche Waard', 'Westland', 'Boxmeer', 'Midden-Delfland', 'Maassluis', 'Maastricht', 'Beek', 'Rotterdam', 'Oss', 'Drimmelen', 'Ooststellingwerf', 'Súdwest-Fryslân', 'Heumen', 'Tubbergen', 'Tubbergen', 'Leeuwarden', 'Midden-Drenthe', 'Oss', 'Eijsden-Margraten', 'Echt-Susteren', 'Laarbeek', 'Tubbergen', 'Hardenberg', 'Raalte', 'Oost Gelre', 'Steenwijkerland', 'Hof van Twente', 'Waterland', 'Alkmaar', 'Noordoostpolder', 'Olst-Wijhe', 'Noardeast-Fryslân', 'Waadhoeke', 'Westerkwartier', 'Aa en Hunze', 'Zwartewaterland', 'Kampen', 'Noordenveld', 'Buren', 'Gulpen-Wittem', 'Medemblik', 'Midden-Groningen', 'Delfzijl', 'Vijfheerenlanden', 'Horst aan de Maas', 'Utrecht', 'Meerssen', 'Groningen', 'Altena', 'Oude IJsselstreek', 'Oss', 'Peel en Maas', 'Horst aan de Maas', 'Roerdalen', 'Veere', 'Goeree-Overflakkee', 'Waadhoeke', 'Het Hogeland', 'Meppel', 'Coevorden', 'Beekdaelen', 'Venray', 'West Betuwe', 'Horst aan de Maas', 'Noardeast-Fryslân', 'Eijsden-Margraten', 'Mook en Middelaar', 'Middelburg', 'Goeree-Overflakkee', 'Edam-Volendam', 'Loppersum', 'Beemster', 'Hollands Kroon', 'Tynaarlo', 'Harlingen', 'Terschelling', 'Oldambt', 'Westerkwartier', 'Medemblik', 'Leeuwarden', 'Geldrop-Mierlo', 'De Ronde Venen', 'Hoeksche Waard', 'Heerenveen', 'Gemert-Bakel', 'Mill en Sint Hubert', 'Berg en Dal', 'Gennep', 'Waadhoeke', 'De Fryske Marren', 'Noardeast-Fryslân', 'Loon op Zand', 'Moerdijk', 'Oisterwijk', 'Zuidplas', 'Roosendaal', 'Molenlanden', 'Mook en Middelaar', 'Gilze en Rijen', 'Súdwest-Fryslân', 'Waterland', 'Westland', 'Montfoort', 'Roerdalen', 'Mook en Middelaar', 'Hoeksche Waard', 'Zuidplas', 'Meerssen', 'Noardeast-Fryslân', 'Gemert-Bakel', 'Gooise Meren', 'Gooise Meren', 'Tytsjerksteradiel', 'Weststellingwerf', 'Noardeast-Fryslân', 'Sittard-Geleen', 'Midden-Groningen', 'Stadskanaal', 'Stadskanaal', 'Westland', 'Gooise Meren', 'Noordoostpolder', 'Heumen', 'Zaltbommel', 'Wijdemeren', 'Steenwijkerland', 'Nederweert', 'Nederweert', 'Berkelland', 'Leudal', 'West Betuwe', 'Leudal', 'Deurne', 'Oss', 'Oss', 'Heerenveen', 'Ameland', 'Noardeast-Fryslân', 'Bladel', 'Oude IJsselstreek', 'Noardeast-Fryslân', 'Medemblik', 'Westerkwartier', 'Westerkwartier', 'Westerkwartier', 'Het Hogeland', 'Noordenveld', 'Aa en Hunze', 'Oldambt', 'Middelburg', 'Raalte', 'Hulst', 'Oldambt', 'Zaltbommel', 'Emmen', 'Midden-Drenthe', 'Hoeksche Waard', 'Borger-Odoorn', 'Emmen', 'Borsele', 'Hollands Kroon', 'Pekela', 'Kaag en Braassem', 'Heerenveen', 'Aa en Hunze', 'Nieuwegein', 'Heerenveen', 'Altena', 'Stichtse Vecht', 'Bodegraven-Reeuwijk', 'Schouwen-Duiveland', 'Zuidplas', 'Hoogeveen', 'Midden-Drenthe', 'Stichtse Vecht', 'Heerenveen', 'Goeree-Overflakkee', 'Nieuwkoop', 'Heusden', 'Vijfheerenlanden', 'Hoogeveen', 'Coevorden', 'Molenlanden', 'Dalfsen', 'Oldambt', 'Molenlanden', 'Noordenveld', 'Emmen', 'Echt-Susteren', 'Nieuwkoop', 'Haarlemmermeer', 'Sluis', 'Steenbergen', 'Emmen', 'Westerkwartier', 'Wijchen', 'Stichtse Vecht', 'Waadhoeke', 'Opsterland', 'Voorst', 'Ooststellingwerf', 'Smallingerland', 'De Fryske Marren', 'Weststellingwerf', 'Weststellingwerf', 'Weststellingwerf', 'De Fryske Marren', 'Westerveld', 'Weststellingwerf', 'Meppel', 'Súdwest-Fryslân', 'Nijkerk', 'Nijkerk', 'Súdwest-Fryslân', 'Aa en Hunze', 'Nijmegen', 'Hellendoorn', 'Roosendaal', 'Borsele', 'Bernheze', 'Tytsjerksteradiel', 'Aa en Hunze', 'Eijsden-Margraten', 'Beemster', 'Midden-Groningen', 'Alkmaar', 'Oldebroek', 'Molenlanden', 'Nieuwkoop', 'Schouwen-Duiveland', 'Moerdijk', 'Westerkwartier', 'Groningen', 'Langedijk', 'Hoogeveen', 'Coevorden', 'Schouwen-Duiveland', 'Westerkwartier', 'Noordwijk', 'Noordwijk', 'Het Hogeland', 'Weststellingwerf', 'Pijnacker-Nootdorp', 'Noordenveld', 'Wierden', 'Nuenen', 'Westerkwartier', " 's-Hertogenbosch", 'Hoeksche Waard', 'Leudal', 'Nunspeet', 'Beekdaelen', 'Dinkelland', 'Sittard-Geleen', 'Koggenland', 'Neder-Betuwe', 'Bunnik', 'Uden', 'Borger-Odoorn', 'Borger-Odoorn', 'Boxmeer', 'Oegstgeest', 'Epe', 'Tytsjerksteradiel', 'Hollands Kroon', 'Súdwest-Fryslân', 'Maasgouw', 'Oss', 'Venray', 'Beekdaelen', 'Oirschot', 'Oisterwijk', 'Deventer', 'Bronckhorst', 'Ooststellingwerf', 'Oldebroek', 'Weststellingwerf', 'Weststellingwerf', 'Westerkwartier', 'Westerkwartier', 'Weststellingwerf', 'Steenwijkerland', 'Oldenzaal', 'Het Hogeland', 'De Fryske Marren', 'Weststellingwerf', 'Olst-Wijhe', 'Opsterland', 'Asten', 'Ommen', 'Buren', 'Het Hogeland', 'Steenwijkerland', 'Groningen', 'Stadskanaal', 'Berg en Dal', 'Goeree-Overflakkee', 'Oirschot', 'Sluis', 'Reimerswaal', 'Oosterhout', 'Renkum', 'Waadhoeke', 'Drechterland', 'Terschelling', 'Texel', 'Coevorden', 'Overbetuwe', 'Oosterhout', 'Schouwen-Duiveland', 'Drechterland', 'Het Hogeland', 'Noardeast-Fryslân', 'Weststellingwerf', 'Vijfheerenlanden', 'Loppersum', 'Ooststellingwerf', 'Oldebroek', 'De Fryske Marren', 'Alkmaar', 'Súdwest-Fryslân', 'Edam-Volendam', 'Veere', 'Wormerland', 'Venray', 'Noardeast-Fryslân', 'Vlissingen', 'Westvoorne', 'Oldambt', 'Westerkwartier', 'Medemblik', 'Oostzaan', 'Dinkelland', 'Smallingerland', 'Westerkwartier', 'West Betuwe', 'Neder-Betuwe', 'West Betuwe', 'Sint Anthonis', 'Opmeer', 'Súdwest-Fryslân', 'Medemblik', 'Midden-Drenthe', 'Heerenveen', 'Midden-Drenthe', 'Nederweert', 'Oss', 'Woensdrecht', 'Hulst', 'Vijfheerenlanden', 'Steenwijkerland', 'Alkmaar', 'Ede', 'Gennep', 'Molenlanden', 'Kaag en Braassem', 'Aa en Hunze', 'Halderberge', 'Dinkelland', 'Stichtse Vecht', 'Molenlanden', 'Hoeksche Waard', 'Goeree-Overflakkee', 'Haarlemmermeer', 'Hollands Kroon', 'Pekela', 'Kaag en Braassem', 'Westerveld', 'Waadhoeke', 'Smallingerland', 'De Fryske Marren', 'Súdwest-Fryslân', 'De Fryske Marren', 'Heerenveen', 'Borsele', 'De Fryske Marren', 'Moerdijk', 'Tynaarlo', 'Halderberge', 'Koggenland', 'Hellevoetsluis', 'Ouder-Amstel', 'Krimpenerwaard', 'Westerwolde', 'Texel', 'Het Hogeland', 'Heerenveen', 'Schagen', 'Goeree-Overflakkee', 'Oudewater', 'Oldambt', 'Heusden', 'Schagen', 'Langedijk', 'Alkmaar', 'Tholen', 'Noardeast-Fryslân', 'Schouwen-Duiveland', 'De Fryske Marren', 'De Fryske Marren', 'Heumen', 'Utrechtse Heuvelrug', 'Losser', 'Oss', 'Boxmeer', 'Midden-Groningen', 'Terneuzen', 'Bloemendaal', 'Borsele', 'Steenwijkerland', 'Noardeast-Fryslân', 'Zevenaar', 'Peel en Maas', 'Oudewater', 'Papendrecht', 'Sittard-Geleen', 'Aa en Hunze', 'Súdwest-Fryslân', 'Tynaarlo', 'Noordenveld', 'Waadhoeke', 'Noordenveld', 'Weststellingwerf', 'Rotterdam', 'Berg en Dal', 'Westerveld', 'Hoogeveen', 'Schagen', 'Terneuzen', 'Súdwest-Fryslân', 'Hoeksche Waard', 'Het Hogeland', 'Waadhoeke', 'Westerkwartier', 'Pijnacker-Nootdorp', 'Súdwest-Fryslân', 'Mook en Middelaar', 'Zaltbommel', 'Westland', 'Steenwijkerland', 'Lopik', 'Albrandswaard', 'Tholen', 'Súdwest-Fryslân', 'Groningen', 'Roerdalen', 'Breda', 'Druten', 'Tynaarlo', 'Staphorst', 'Edam-Volendam', 'Waterland', 'Purmerend', 'Landsmeer', 'Beekdaelen', 'Woensdrecht', 'Putten', 'Hoeksche Waard', 'Raalte', 'Geertruidenberg', 'Geertruidenberg', 'Noardeast-Fryslân', 'Hardenberg', 'Apeldoorn', 'Súdwest-Fryslân', 'Overbetuwe', 'Voerendaal', 'Het Hogeland', 'Oss', 'Buren', 'Ooststellingwerf', 'Dantumadiel', 'Súdwest-Fryslân', 'Leeuwarden', 'Landerd', 'Bodegraven-Reeuwijk', 'Gulpen-Wittem', 'Noardeast-Fryslân', 'Berkelland', 'Schouwen-Duiveland', 'Renkum', 'Renswoude', 'Lingewaard', 'Sluis', 'Reusel-De Mierden', 'Tubbergen', 'Beesel', 'Bronckhorst', 'Rheden', 'Assen', 'Hardenberg', 'Hardenberg', 'Rhenen', 'West Betuwe', 'Albrandswaard', 'Ridderkerk', 'Waadhoeke', 'Goirle', 'Súdwest-Fryslân', 'Bergeijk', 'Berkelland', 'Gilze en Rijen', 'Boxmeer', 'Sint Anthonis', 'Kaag en Braassem', 'Katwijk', 'Alkmaar', 'Kaag en Braassem', 'De Fryske Marren', 'Zundert', 'Haarlemmermeer', 'Rijssen-Holten', 'Rijswijk', 'Buren', 'Altena', 'Reimerswaal', 'Dantumadiel', 'Gemert-Bakel', 'Vlissingen', 'Westvoorne', 'Noordenveld', 'Noordenveld', 'Noordenveld', 'Kaag en Braassem', 'Roermond', 'Meppel', 'Leudal', 'De Fryske Marren', 'Aa en Hunze', 'Het Hogeland', 'Roosendaal', 'Echt-Susteren', " 's-Hertogenbosch", 'Dinkelland', 'Maasdriel', 'Emmen', 'De Fryske Marren', 'De Fryske Marren', 'Rotterdam', 'Albrandswaard', 'Smallingerland', 'Het Hogeland', 'De Fryske Marren', 'Staphorst', 'Rotterdam', 'Haarlemmermeer', 'Rozendaal', 'Rucphen', 'De Fryske Marren', 'Westerveld', 'De Wolden', 'De Wolden', 'West Betuwe', 'Noordoostpolder', 'Berkelland', 'Tytsjerksteradiel', 'Westerkwartier', 'Dinkelland', 'Het Hogeland', 'Boxmeer', 'Súdwest-Fryslân', 'Velsen', 'Velsen', 'Midden-Groningen', 'Terneuzen', 'Teylingen', 'Het Hogeland', 'Schagen', 'Schagen', 'Landerd', 'Deventer', 'Houten', 'Waadhoeke', 'Edam-Volendam', 'Schouwen-Duiveland', 'Midden-Groningen', 'Súdwest-Fryslân', 'De Fryske Marren', 'Koggenland', 'Oldambt', 'Steenwijkerland', 'Drechterland', 'Molenlanden', 'Alkmaar', 'Tholen', 'Weststellingwerf', 'Scherpenzeel', 'Súdwest-Fryslân', 'Eijsden-Margraten', 'Schiedam', 'Schiermonnikoog', 'Rucphen', 'Meierijstad', 'Midden-Groningen', 'Beekdaelen', 'Valkenburg aan de Geul', 'Beekdaelen', 'Beekdaelen', 'Aa en Hunze', 'Haarlemmermeer', 'Haarlemmermeer', 'Meppel', 'Midden-Delfland', 'Noordoostpolder', 'Sluis', 'Emmen', 'Krimpenerwaard', 'Aa en Hunze', 'Coevorden', 'Vijfheerenlanden', 'Bergen (NH.)', 'Kapelle', 'Het Hogeland', 'Súdwest-Fryslân', 'Hardenberg', 'Westerkwartier', 'Westerwolde', 'Schouwen-Duiveland', 'Veere', 'Horst aan de Maas', 'Waadhoeke', 'Twenterand', 'Hardenberg', 'Súdwest-Fryslân', 'Dantumadiel', 'Midden-Groningen', 'Bergen (L.)', 'Opsterland', 'Medemblik', 'Oude IJsselstreek', 'Nissewaard', 'Simpelveld', 'Oude IJsselstreek', 'Cuijk', 'Groningen', 'Sint Anthonis', 'Eijsden-Margraten', 'Mill en Sint Hubert', 'Steenwijkerland', 'Hulst', 'Echt-Susteren', 'Sluis', 'Schagen', 'Schagen', 'Schagen', 'De Fryske Marren', 'Roerdalen', 'Langedijk', 'Tholen', 'Rucphen', 'Tholen', 'Waadhoeke', 'Waadhoeke', 'De Fryske Marren', 'Tholen', 'Sint-Michielsgestel', 'Meierijstad', 'Schouwen-Duiveland', 'Sittard-Geleen', 'Waadhoeke', 'Hardenberg', 'Waadhoeke', 'Coevorden', 'Altena', 'Gulpen-Wittem', 'Sliedrecht', 'Weststellingwerf', 'Overbetuwe', 'Midden-Groningen', 'Hollands Kroon', 'De Fryske Marren', 'Sluis', 'Terneuzen', 'Venray', 'Smallingerland', 'Súdwest-Fryslân', 'Midden-Drenthe', 'Leeuwarden', 'Súdwest-Fryslân', 'Oudewater', 'De Fryske Marren', 'Cranendonck', 'Soest', 'Soest', 'Someren', 'Goeree-Overflakkee', 'Son en Breugel', 'De Fryske Marren', 'Weststellingwerf', 'Haarlemmermeer', 'Haarlem', 'Opmeer', 'Weststellingwerf', 'Rheden', 'Waadhoeke', 'Beek', 'Midden-Drenthe', 'Westerveld', 'Koggenland', 'Zevenaar', 'Delfzijl', 'West Betuwe', 'Nissewaard', 'Aa en Hunze', 'Wormerland', 'Waalwijk', 'Rucphen', 'Terneuzen', 'Goeree-Overflakkee', 'Stadskanaal', 'Halderberge', 'Moerdijk', 'Staphorst', 'Alkmaar', 'Loppersum', 'Het Hogeland', 'Tholen', 'Súdwest-Fryslân', 'Loppersum', 'Rheden', 'Steenbergen', 'Noordenveld', 'Midden-Groningen', 'Bronckhorst', 'Voorst', 'Eersel', 'Steenwijkerland', 'Steenwijkerland', 'Ommen', 'Weststellingwerf', 'Stein', 'Goeree-Overflakkee', 'Heeze-Leende', 'Sint Anthonis', 'Maasgouw', 'Venlo', 'Coevorden', 'Leeuwarden', 'Het Hogeland', 'Montferland', 'Krimpenerwaard', 'Alkmaar', 'Leusden', 'Amersfoort', 'Weert', 'Molenlanden', 'Terschelling', 'Alphen-Chaam', 'Hoeksche Waard', 'Hoeksche Waard', 'Barneveld', 'Achtkarspelen', 'Midden-Drenthe', 'Hoogeveen', 'Tytsjerksteradiel', 'Achtkarspelen', 'Achtkarspelen', 'Echt-Susteren', 'Tytsjerksteradiel', 'Roermond', 'Beekdaelen', 'Leeuwarden', 'Dronten', 'Horst aan de Maas', 'Tynaarlo', 'Oss', 'Leeuwarden', 'Venlo', 'Heerenveen', 'Oude IJsselstreek', 'Drimmelen', 'De Fryske Marren', 'Hulst', 'De Fryske Marren', 'Delfzijl', 'Delfzijl', 'Noardeast-Fryslân', 'Terneuzen', 'De Fryske Marren', 'Barneveld', 'Súdwest-Fryslân', 'Opsterland', 'Voorst', 'Breda', 'Voorst', 'Groningen', 'Tholen', 'Maasgouw', 'Tiel', 'Hoogeveen', 'Midden-Drenthe', 'Stichtse Vecht', 'Vijfheerenlanden', 'Horst aan de Maas', 'Opsterland', 'Smallingerland', 'Tilburg', 'Dinkelland', 'Het Hogeland', 'Westvoorne', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Heerenveen', 'De Fryske Marren', 'Súdwest-Fryslân', 'Midden-Groningen', 'Westerkwartier', 'Bronckhorst', 'Zevenaar', 'Noordoostpolder', 'Brummen', 'Loppersum', 'West Betuwe', 'Noardeast-Fryslân', 'Midden-Groningen', 'Tubbergen', 'West Betuwe', 'Schagen', 'Steenwijkerland', 'Houten', 'Voorst', 'Achtkarspelen', 'Achtkarspelen', 'Medemblik', 'Tynaarlo', 'Tytsjerksteradiel', 'Waadhoeke', 'Waadhoeke', 'Assen', 'Berg en Dal', 'Apeldoorn', 'Uden', 'Tilburg', 'Westerveld', 'Apeldoorn', 'Waterland', 'Uitgeest', 'Uithoorn', 'Het Hogeland', 'Het Hogeland', 'Súdwest-Fryslân', 'Altena', 'Meerssen', 'Oude IJsselstreek', 'Baarle-Nassau', 'Het Hogeland', 'Breda', 'Alphen-Chaam', 'Opsterland', 'Urk', 'Stein', 'Alkmaar', 'Koggenland', 'Het Hogeland', 'Utrecht', 'Vaals', 'Epe', 'Overbetuwe', 'Katwijk', 'Valkenburg aan de Geul', 'Valkenswaard', 'Borger-Odoorn', 'Borger-Odoorn', 'Borger-Odoorn', 'West Betuwe', 'Oude IJsselstreek', 'Oude IJsselstreek', 'Tubbergen', 'Westerwolde', 'Altena', 'Veendam', 'Veenendaal', 'Smallingerland', 'Noordenveld', 'De Wolden', 'Noardeast-Fryslân', 'Emmen', 'Veere', 'Heerde', 'De Fryske Marren', 'Meierijstad', 'Hollands Kroon', 'Maasdriel', 'Hardenberg', 'Venlo', 'Veldhoven', 'Grave', 'Rheden', 'Velsen', 'Velsen', 'Velsen', 'Hardenberg', 'Boekel', 'Drechterland', 'Venlo', 'Venray', 'Gennep', 'Eersel', 'Montferland', 'Venray', 'Vijfheerenlanden', 'Cuijk', 'Bronckhorst', 'Nunspeet', 'Het Hogeland', 'Boxmeer', 'Brielle', 'Haarlemmermeer', 'Vaals', 'Ommen', 'Weststellingwerf', 'Bernheze', " 's-Hertogenbosch", 'Ommen', 'De Ronde Venen', 'Westerkwartier', 'Vlaardingen', 'Westerwolde', 'Westerveld', 'Westerveld', 'Stadskanaal', 'Utrecht', 'Vlieland', 'Deurne', 'Heusden', 'Vlissingen', 'Krimpenerwaard', 'Roerdalen', 'Voerendaal', 'Bloemendaal', 'Hulst', 'Edam-Volendam', 'Uden', 'Steenwijkerland', 'Rotterdam', 'Leidschendam-Voorburg', 'Teylingen', 'Voorschoten', 'Oude IJsselstreek', 'Voorst', 'Barneveld', 'Heerde', 'Bronckhorst', 'Bernheze', 'Boxmeer', 'Oost Gelre', 'Aa en Hunze', 'Venray', 'Stichtse Vecht', 'Tynaarlo', 'Westerwolde', 'Twenterand', 'Twenterand', 'Nieuwkoop', 'Waadhoeke', 'Veere', 'Vught', 'West Betuwe', 'Súdwest-Fryslân', 'Molenlanden', 'Texel', 'Waalre', 'Waalwijk', 'Oldambt', 'Reimerswaal', 'West Betuwe', 'Bodegraven-Reeuwijk', 'Altena', 'Schagen', 'Noardeast-Fryslân', 'Coevorden', 'Waddinxveen', 'Tiel', 'Drimmelen', 'Delfzijl', 'Wageningen', 'Valkenburg aan de Geul', 'Hulst', 'Dantumadiel', 'West Maas en Waal', 'Steenwijkerland', 'Sint Anthonis', 'Venray', 'Noardeast-Fryslân', 'Heerde', 'Westerveld', 'Westerveld', 'Edam-Volendam', 'Het Hogeland', 'Het Hogeland', 'Noardeast-Fryslân', 'Schagen', 'Teylingen', 'Súdwest-Fryslân', 'Zutphen', 'Leeuwarden', 'Leeuwarden', 'Ooststellingwerf', 'Waalwijk', 'Wassenaar', 'Westerveld', 'Waterland', 'Midden-Groningen', 'Westland', 'Sluis', 'De Ronde Venen', 'Westerwolde', 'Opmeer', 'Dinkelland', 'Weert', 'Weesp', 'Het Hogeland', 'Doetinchem', 'Leeuwarden', 'Emmen', 'Ede', 'Maasdriel', 'Bergen (L.)', 'Bergen (L.)', 'Olst-Wijhe', 'Kapelle', 'Apeldoorn', 'Leeuwarden', 'Altena', 'Bunnik', 'Zundert', 'Medemblik', 'Olst-Wijhe', 'Maasgouw', 'Beemster', 'De Bilt', 'Borger-Odoorn', 'Terneuzen', 'Oude IJsselstreek', 'Sint Anthonis', 'Midden-Drenthe', 'Midden-Groningen', 'Dantumadiel', 'Loppersum', 'Noardeast-Fryslân', 'Twenterand', 'Bergeijk', 'Hollands Kroon', 'Oldambt', 'Het Hogeland', 'Noordenveld', 'Westervoort', 'Loppersum', 'Alkmaar', 'Súdwest-Fryslân', 'Waadhoeke', 'Veere', 'Zaanstad', 'Hoeksche Waard', 'Terschelling', 'Drechterland', 'Zaanstad', 'Steenwijkerland', 'Haarlemmermeer', 'Noardeast-Fryslân', 'Het Hogeland', 'Beuningen', 'Oldebroek', 'Coevorden', 'Coevorden', 'Bronckhorst', 'Waadhoeke', 'Wierden', 'Hollands Kroon', 'Hollands Kroon', 'Noardeast-Fryslân', 'Wijchen', 'De Fryske Marren', 'Drechterland', 'Wormerland', 'Olst-Wijhe', 'De Wolden', 'Beverwijk', 'Wijk bij Duurstede', 'Altena', 'Gulpen-Wittem', 'Harlingen', 'Beekdaelen', 'Montferland', 'Molenlanden', 'Opsterland', 'Midden-Drenthe', 'Mill en Sint Hubert', 'Veendam', 'Smallingerland', 'Goes', 'Westerveld', 'Steenwijkerland', 'Moerdijk', 'De Ronde Venen', 'Voorst', 'Westerkwartier', 'Kampen', 'Tynaarlo', 'Sittard-Geleen', 'Hollands Kroon', 'Groningen', 'Oldambt', 'Beuningen', 'Waadhoeke', 'Het Hogeland', 'Eersel', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Winterswijk', 'Loppersum', 'Leeuwarden', 'Noord-Beveland', 'Ommen', 'Súdwest-Fryslân', 'Steenwijkerland', 'Westerveld', 'Gulpen-Wittem', 'Midden-Drenthe', 'Súdwest-Fryslân', 'Waadhoeke', 'Woensdrecht', 'Woerden', 'Nieuwkoop', 'Medemblik', 'Delfzijl', 'Renkum', 'Goes', 'Súdwest-Fryslân', 'Groningen', 'Weststellingwerf', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Wormerland', 'Zaanstad', 'Kaag en Braassem', 'Midden-Groningen', 'Castricum', 'Woudenberg', 'Altena', 'Súdwest-Fryslân', 'Roosendaal', 'Roosendaal', 'Tytsjerksteradiel', 'Leeuwarden', 'Tynaarlo', 'Reimerswaal', 'Súdwest-Fryslân', 'Súdwest-Fryslân', 'Venray', 'Terneuzen', 'Zaanstad', 'Zaanstad', 'Kampen', 'Zaltbommel', 'Schagen', 'Borger-Odoorn', 'Het Hogeland', 'Weststellingwerf', 'Emmen', 'Loppersum', 'Zandvoort', 'Montferland', 'Tynaarlo', 'Landerd', 'Loppersum', 'Zeewolde', 'Rucphen', 'Woerden', 'Tynaarlo', 'Assen', 'Assen', 'Zeist', 'Bronckhorst', 'Borne', 'Tiel', 'West Betuwe', 'Overbetuwe', 'Zevenaar', 'Moerdijk', 'Moerdijk', 'Drimmelen', 'Nieuwkoop', 'Zuidplas', 'Westerkwartier', 'Schouwen-Duiveland', 'Oost Gelre', 'Vijfheerenlanden', 'Hollands Kroon', 'Loppersum', 'Noordwijk', 'Buren', 'Buren', 'Zoetermeer', 'Zoeterwoude', 'Schouwen-Duiveland', 'Westerveld', 'Veere', 'Het Hogeland', 'Hoeksche Waard', 'Midden-Groningen', 'Terneuzen', 'Koggenland', 'Waterland', 'Westerkwartier', 'Tynaarlo', 'Nissewaard', 'Tynaarlo', 'Beemster', 'Langedijk', 'Alkmaar', 'Steenwijkerland', 'Midden-Drenthe', 'Noordenveld', 'Het Hogeland', 'De Wolden', 'Sluis', 'Zaltbommel', 'Wierden', 'Zundert', 'Súdwest-Fryslân', 'Zutphen', 'Het Hogeland', 'Hoorn', 'Medemblik', 'Medemblik', 'Haarlemmermeer', 'Noardeast-Fryslân', 'Alphen aan den Rijn', 'Haarlemmermeer', 'Barneveld', 'Emmen', 'Brielle', 'Zwartewaterland', 'Coevorden', 'Waadhoeke', 'Midden-Drenthe', 'Zwijndrecht', 'Coevorden', 'Zwolle']


# In[10]:


def loc_lookup(event=None):  
    api_request = requests.get("http://weerlive.nl/api/json-data-10min.php?key=025e2b1d6f&locatie="+str(loc_e.get()))
    api = json.loads(api_request.content)
    api_access = api["liveweer"]
    datastring = str(api_access)
    datalist = re.findall(r"'(.*?)'", datastring)
    
    if str(loc_e.get()) not in municipalities:
        ans_e.insert(END, "De gemeente "+str(loc_e.get())+" is niet gevonden.\n\n")
        
    else:                 
        def Convert(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct
            
        lst = datalist
        datadic = Convert(lst)
            
        plac = datadic["plaats"]
        temp = datadic["temp"]
        summ = datadic["samenv"]
        pros = datadic["verw"]
        mint = datadic["d0tmin"]
        maxt = datadic["d0tmax"]
        sunc = datadic["d0zon"]
        raic = datadic["d0neerslag"]

        text_today = "Momenteel is het in "+str(plac)+" "+str(temp)+" graden, en de verwachting voor de dag is als volgt: \n\n"+str(pros)+"\n"
        text_temp_today = "De minimumtemperatuur is "+str(mint)+" graden, en de maximumtemperatuur is "+str(maxt)+" graden. \n"
        text_rain_today = "Er is "+str(sunc)+"% kans op zon, en "+str(raic)+"% kans op regen. \n\n"
        
        ans_e.insert(END, text_today+text_temp_today+text_rain_today)


# In[11]:


def clearfields():
    ans_e.delete("1.0","end")
    loc_e.delete(0, END)


# In[12]:


loc_btn = Button(root, text="Vind het weer voor deze gemeente", command=loc_lookup)
loc_btn.grid(row=2,column=0,sticky="NESW")


# In[13]:


clr_btn = Button(root, text="Maak de velden leeg", command=clearfields)
clr_btn.grid(row=2,column=1,ipadx=40,sticky="NESW")


# In[14]:


root.bind('<Return>', loc_lookup)


# In[15]:


root.mainloop()

