# -*- coding: utf-8 -*-d 
#!/usr/bin/python

import sqlite3
import os
import shutil
from raw_export_base import exportMultipleItems 



def exportCollection(currentCollection,exportPath,storagePath,cursor):
    #get name of collection and create directory
    sql = "SELECT collectionName FROM collections WHERE collectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    CollectionName = cursor.fetchone()
    exportPath = exportPath+"\\"+str(CollectionName[0])
    os.mkdir(exportPath)
    print(exportPath)

    #get IDs and Keys for Items in current directory then export them
    sql = "SELECT itemID FROM collectionitems WHERE collectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    itemIDs = cursor.fetchall()
    raw_export.exportMultipleItems(itemIDs)

    #repeat for child Collections
    sql = "SELECT collectionID FROM collections WHERE parentCollectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    childCollectionIDs = cursor.fetchall()

    if childCollectionIDs != []:
        for childCollection in childCollectionIDs:
            exportCollection(childCollection,exportPath,storagePath,cursor)


def exportByTags():
    print("I DO STUFF")



if __name__ == '__main__':
    #TODO: Collection needs to be validatedadd a
    #TODO: implement preset default export path
    
    validinput = False
    while validinput == False:
        STORAGEPATH=os.getcwd()+"\\storage\\"
        EXPORTBASEPATH = raw_input("Enter the path you want to export to:\n")
        if os.path.isdir(EXPORTBASEPATH):
            validinput = True
        else:
            print ("WARNING: Invalid Path!")
            
    shutil.copy2("zotero.sqlite","zotero_workcopy.sqlite")
    conn = sqlite3.connect('zotero_workcopy.sqlite')
    cursor = conn.cursor()
            
    validinput = False
    while validinput == False:
        print("1: Collection")
        print("2: Tags")
        exporttype = raw_input("Enter the type of export:")
        
        if exporttype == "1":
            validinput = True
            CollectionToExport = raw_input("Enter the name of the collection you would like to export:\n")
            sql = "SELECT collectionID FROM collections WHERE collectionName = \""+CollectionToExport+"\""
            cursor.execute(sql)
            startingCollection = cursor.fetchone()
            exportCollection(startingCollection,EXPORTBASEPATH,STORAGEPATH,cursor)
        elif exporttype == "2":
            validinput = True
            exportByTags() #TODO: Add Parameters
        else:
            print ("WARNING: Invalid Input!")
        
    conn.close()
    print("Export Complete")
