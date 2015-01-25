# -*- coding: utf-8 -*-
#!/usr/bin/python

import sqlite3
import os
import shutil



def init():
    print("enter the name of the collection you would like to export:")
    CollectionToExport = raw_input()
    sql = "SELECT collectionID FROM collections WHERE collectionName = \""+CollectionToExport+"\""
    cursor.execute(sql)
    startingCollection = cursor.fetchone()
    exportCollection(startingCollection,EXPORTBASEPATH)
    conn.close()
    print("Export Complete")



def exportCollection(currentCollection,exportpath):
    #get name of collection and create directory
    sql = "SELECT collectionName FROM collections WHERE collectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    CollectionName = cursor.fetchone()
    exportpath = exportpath+"\\"+str(CollectionName[0])
    os.mkdir(exportpath)
    print(exportpath)
    #get IDs and Keys for Items in current directory then export them
    getItemsToExport(currentCollection,exportpath)
    #repeat for child Collections
    getChildCollections(currentCollection,exportpath)



def getItemsToExport(currentCollection,path):
    sql = "SELECT itemID FROM collectionitems WHERE collectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    itemIDs = cursor.fetchall()

    if itemIDs != []:
        for item in itemIDs:
            sql = "SELECT key FROM items WHERE itemID = "+str(item[0])
            cursor.execute(sql)
            itemKey = cursor.fetchone()
            exportItem(item,itemKey,path)
    


def exportItem(itemID,itemKey,exportPath):
    if os.access(STORAGEPATH+"\\"+str(itemKey[0]), os.F_OK):
        #remove Zotero based files
        directoryFiles = os.listdir(STORAGEPATH+str(itemKey[0]))
        if ".zotero-ft-cache" in directoryFiles:
            directoryFiles.remove(".zotero-ft-cache")
        if ".zotero-ft-info" in directoryFiles:
            directoryFiles.remove(".zotero-ft-info")
        
        #copy remaining files
        if len(directoryFiles) > 1:
            exportPath = makeExtraDirectory(itemID,exportPath)          
        for fileName in directoryFiles:
            shutil.copy2(STORAGEPATH+str(itemKey[0])+"\\"+fileName,exportPath)
        print("Copying "+ fileName)
    else:
        getSourceItemKeys(itemID,itemKey,exportPath)


        
def makeExtraDirectory(itemID,oldPath):
    sql = "SELECT valueID FROM itemData WHERE ItemID = "+str(itemID[0])+" AND fieldID = 110"
    cursor.execute(sql)
    valueID = cursor.fetchone()
    sql = "SELECT value FROM itemDataValues WHERE valueID = "+str(valueID[0])
    cursor.execute(sql)
    title = cursor.fetchone()
    newPath = oldPath +"\\"+ adjustName(title[0])
    os.mkdir(newPath)
    print (newPath)
    return newPath



def getSourceItemKeys(itemID,itemKey,path):
    sql = "SELECT itemID FROM itemAttachments WHERE sourceItemID = "+str(itemID[0])
    cursor.execute(sql)
    SourceItemIDs = cursor.fetchall()
    if len(SourceItemIDs) > 1:
        path = makeExtraDirectory(itemID,path)   
    for item in SourceItemIDs:
            sql = "SELECT key FROM items WHERE itemID = "+str(item[0])
            cursor.execute(sql)
            itemKey = cursor.fetchone()
            exportItem(item,itemKey,path)



def adjustName(name):
    if os.name == "nt":
        name = name.translate(None, '<>:"\/|?*').encode('cp1252')
    elif os.name == "posix":
        name = name.translate(None, '<>:"\/|?*').encode('utf-8')
    return name



def getChildCollections(currentCollection,exportPath):
    sql = "SELECT collectionID FROM collections WHERE parentCollectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    childCollectionIDs = cursor.fetchall()

    if childCollectionIDs != []:
        for childCollection in childCollectionIDs:
            exportCollection(childCollection,exportPath)
            

        
conn = sqlite3.connect('zotero.sqlite')
cursor = conn.cursor()
STORAGEPATH=os.getcwd()+"\\storage\\"
EXPORTBASEPATH = raw_input("Enter the path you want to export to:\n")
init()
