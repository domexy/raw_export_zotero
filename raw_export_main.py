# -*- coding: utf-8 -*-d 
#!/usr/bin/python

import sqlite3
import os
import shutil
from raw_export_base import exportMultipleItems 



def exportCollection(currentCollection,exportPath,storagePath,cursor):
    #get starting collection
    if currentCollection == "":
            validinput = False
            while validinput == False:
                CollectionToExport = raw_input("Enter the name of the collection you would like to export:\n")
                sql = "SELECT collectionID FROM collections WHERE collectionName = \""+CollectionToExport+"\""
                cursor.execute(sql)
                startingCollection = cursor.fetchone()
                if startingCollection != None:
                    print ("WARNING: Collection does not exist!")
                else:
                    validinput == True
                    exportCollection(startingCollection,exportPath,storagePath,cursor)
        
    else:    
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


def exportByTags(EXPORTBASEPATH,STORAGEPATH,cursor):

    validinput = False
            while validinput == False:
                RawTagsToExport = raw_input("Enter the Tags you would like to export by (separated by , ):\n")
                TagsToExport =
                for Tag in TagsToExport:
                    #get tagIDs
                    sql = "SELECT tagID FROM tags WHERE name = \""+Tag+"\""
                    cursor.execute(sql)
                    TagID = cursor.fetchone()

                    #get itemIDs with corresponding tagIDs
                    sql = "SELECT itemID FROM itemtags WHERE tagID = \""+TagID+"\""
                    cursor.execute(sql)
                    ItemIDs = cursor.fetchall()

                    #only reprompt input if all tags are invalid
                    if startingCollection != None:
                        print ("WARNING: Tag \""+Tag+"\" does not exist!")
                    else:
                        validinput == True
                        raw_export.exportMultipleItems(ItemIDs)
            

    #Mockup:
    #Let user input Tags
    #Query Tags to validate existence
    #Query Files associated with Tags

    raw_export.exportMultipleItems(itemIDs)



if __name__ == '__main__':    
    validinput = False
    while validinput == False:
        STORAGEPATH=os.getcwd()+"\\storage\\"
        EXPORTBASEPATH = raw_input("Enter the path you want to export to: (default = current path)\n")
        if EXPORTBASEPATH == "":
            EXPORTBASEPATH = os.getcwd()
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
            exportCollection("",EXPORTBASEPATH,STORAGEPATH,cursor)
        elif exporttype == "2":
            validinput = True
            exportByTags(EXPORTBASEPATH,STORAGEPATH,cursor)
        else:
            print ("WARNING: Invalid Input!")
        
    conn.close()
    print("Export Complete")
