# -*- coding: utf-8 -*-
#!/usr/bin/python

import sqlite3
import os
import shutil




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
    if itemIDs != []:
        for item in itemIDs:
            sql = "SELECT key FROM items WHERE itemID = "+str(item[0])
            cursor.execute(sql)
            itemKey = cursor.fetchone()

            #export the Item
            exportItem(item,itemKey,exportPath,storagePath,cursor)

    #repeat for child Collections
    sql = "SELECT collectionID FROM collections WHERE parentCollectionID = "+str(currentCollection[0])
    cursor.execute(sql)
    childCollectionIDs = cursor.fetchall()

    if childCollectionIDs != []:
        for childCollection in childCollectionIDs:
            exportCollection(childCollection,exportPath,storagePath,cursor)



def exportItem(itemID,itemKey,exportPath,storagePath,cursor):
    if os.access(storagePath+"\\"+str(itemKey[0]), os.F_OK): #This effectively checks if the Item is a single file or a Zotero object (eg. Book )
        #remove Zotero based files
        directoryFiles = os.listdir(storagePath+str(itemKey[0]))
        if ".zotero-ft-cache" in directoryFiles:
            directoryFiles.remove(".zotero-ft-cache")
        if ".zotero-ft-info" in directoryFiles:
            directoryFiles.remove(".zotero-ft-info")
        
        #copy remaining files
        if len(directoryFiles) > 1:
            exportPath = makeExtraDirectory(itemID,exportPath,cursor)          
        for fileName in directoryFiles:
            shutil.copy2(storagePath+str(itemKey[0])+"\\"+fileName,exportPath)
        print("Copying "+ fileName)
    else:
        #get SourceItemKeys
        sql = "SELECT itemID FROM itemAttachments WHERE sourceItemID = "+str(itemID[0])
        cursor.execute(sql)
        SourceItemIDs = cursor.fetchall()
        if len(SourceItemIDs) > 1:
            newExportPath = makeExtraDirectory(itemID,exportPath,cursor)
            for item in SourceItemIDs:
                sql = "SELECT key FROM items WHERE itemID = "+str(item[0])
                cursor.execute(sql)
                itemKey = cursor.fetchone()
                exportItem(item,itemKey,newExportPath,storagePath,cursor)
        else:
            for item in SourceItemIDs:
                    sql = "SELECT key FROM items WHERE itemID = "+str(item[0])
                    cursor.execute(sql)
                    itemKey = cursor.fetchone()
                    exportItem(item,itemKey,exportPath,storagePath,cursor)


        
def makeExtraDirectory(itemID,oldPath,cursor):
    sql = "SELECT valueID FROM itemData WHERE ItemID = "+str(itemID[0])+" AND fieldID = 110"
    cursor.execute(sql)
    valueID = cursor.fetchone()
    sql = "SELECT value FROM itemDataValues WHERE valueID = "+str(valueID[0])
    cursor.execute(sql)
    title = cursor.fetchone()
    if os.name == "nt":
        newTitle = title[0].translate('<>:"\/|?*').encode('cp1252')
    elif os.name == "posix":
        newTitle = title[0].translate('<>:"\/|?*').encode('utf-8')
    newPath = oldPath +"\\"+ newTitle
    os.mkdir(newPath)
    print (newPath)
    return newPath



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
