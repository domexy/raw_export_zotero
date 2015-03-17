# -*- coding: utf-8 -*-
#!/usr/bin/python

import sqlite3
import os
from raw_export import exportMultipleItems 



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



if __name__ == '__main__':
    STORAGEPATH=os.getcwd()+"\\storage\\"
    EXPORTBASEPATH = raw_input("Enter the path you want to export to:\n")
    shutil.copy2("zotero.sqlite","zotero_workcopy.sqlite")
    conn = sqlite3.connect('zotero_workcopy.sqlite')
    cursor = conn.cursor()
    CollectionToExport = raw_input("Enter the name of the collection you would like to export:\n")
    sql = "SELECT collectionID FROM collections WHERE collectionName = \""+CollectionToExport+"\""
    cursor.execute(sql)
    startingCollection = cursor.fetchone()
    exportCollection(startingCollection,EXPORTBASEPATH,STORAGEPATH,cursor)
    conn.close()
    print("Export Complete")
