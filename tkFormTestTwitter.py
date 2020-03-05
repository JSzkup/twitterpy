from tkinter import *
import geocoder

def build_query(entries):

    search_query = []

    locWords = str(entries['At this location'].get())
    geoLoc = geocoder.osm(locWords)
    if locWords == "":
        #geoLoc= ""
        pass
    else:
        geoLoc = ("geocode:" + str(geoLoc.lat) + "," + str(geoLoc.lng) + ",138km,")
        search_query.append(geoLoc)
    
    allWords = str(entries['All of these words'].get())
    if allWords == "":
        pass
    else:
        search_query.append(allWords)

    exaWords = str(entries['This exact phrase'].get())
    if exaWords == "":
        pass
    else:
        exaWords = ("\"" + exaWords +"\"")
        search_query.append(exaWords)

    anyWords = str(entries['Any of these words'].get())
    if anyWords == "":
        pass
    else:
        anyWords = (anyWords.replace(" ", " OR "))
        search_query.append(anyWords)

    nonWords = str(entries['None of these words'].get())
    if nonWords == "":
        pass
    else:
        nonWords = ("-" + nonWords.replace(" ", " -"))
        search_query.append(nonWords)

    hasWords = str(entries['These hashtags'].get())
    if hasWords == "":
        pass
    else:
        search_query.append(hasWords)


    menWords = str(entries['Mentioning these accounts'].get())
    if menWords == "":
        pass
    else:
        search_query.append(menWords)

    for i in search_query:
        print(i)

    #return search_query
    
def makeform(root, fields):

   entries = {}

   for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row)

        row.pack(side = TOP, fill = X, padx = 10 , pady = 5)
        lab.pack(side = LEFT)
        ent.pack(side = RIGHT, expand = YES, fill = X)

        entries[field] = ent

   return entries

if __name__ == '__main__':
    root = Tk()
    # creates the form based off the fields in the fields tuple
    fields = ('At this location', 'All of these words', 'This exact phrase', 'Any of these words', 'None of these words', 'These hashtags', 'Mentioning these accounts')
    ents = makeform(root, fields)

    # binds the enter key to the submit button
    root.bind('<Return>', (lambda event, e = ents: build_query(e)))

    b1 = Button(root, text = 'Submit',
       command=(lambda e = ents: build_query(e)))
    b1.pack(side = LEFT, padx = 5, pady = 5)

    b2 = Button(root, text = 'Quit', command = root.quit)
    b2.pack(side = LEFT, padx = 5, pady = 5)

    root.mainloop()
