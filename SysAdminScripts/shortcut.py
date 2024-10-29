#!/bin/python3
#Jake Paczkowski
#NSSA-221 Script 3
#The purpose of htis script is to allow suers to create symbolic links to a file
#and store those links in the users home directory, while also giving them the option to delete the links


#import modules
import os
import sys
import subprocess

#get_home_path will grab the path to the users home directory
def get_home_path():
    return os.path.join(os.path.expanduser("~"),"Desktop")

#create_symlink will be used to create symbolic links and add them to the users home directory
def create_symlink(targetFile):
    homePath = get_home_path()
    linkName = os.path.basename(targetFile) + "_shortcut"
    linkPath = os.path.join(homePath, linkName)

    try:
        subprocess.run(["ls", "-s", targetFile, linkPath])
        print(f"Symbolic link created: {linkPath} --> {targetFile}")
    except FileExistsError:
        print("Symbolic Link already exists!")


#Delete_symlink will allow a user to delete a symbolic link that was created
def delete_symlink():
    homePath = get_home_path()
    linkName = input("Enter the name of the symbolic link you wish to remove")
    linkPath = os.path.join(homePath, linkName)

    if os.path.islink(linkPath):
        os.remove(linkPath)
        print(f"Symbolic Link deleted: {linkPath}")
    else:
        print("Symbolic link does not exist!")

#listSymLinks will list all symbolic links to the user
def listSymlinks():
    homePath = get_home_path()
    print("All symbolic links:")

    for item in os.listdir(homePath):
        itemPath = os.path.join(homePath, item)
        if os.path.islink(itemPath):
            targetPath = os.readlink(itemPath)
            print(f"{item} --> {targetPath}")


#Menu function will continuously display the menu to the user
def menu():
    print("1: Create a Symbolic Link")
    print("2: Delete a Symbolic Link")
    print("3: Display all Symbolic Links")
    print("4: Quit")

#main function
def main():
    #Clear the terminal
    subprocess.run("clear", shell=True)
    print("Symbolic Link Manager\n")
    #Continue to loop through the options
    while True:
        #display the menu every time the loop begins
        menu()
        
        #Enter an option
        choice = input("Enter an option: ")
        
        #The user will enter a choice based on the option that they want to use
        if choice == "1":
            targetFile = input("Enter the path of the file to create a Symbolic Link")
            create_symlink(targetFile)
        elif choice == "2":
            delete_symlink()
        elif choice == "3":
            listSymlinks()
        elif choice =="4":
            #Notify the user the script is closing
            print("Exiting")
            break
        #Catch bad input
        else:
            print("Invalid Input")


#call main function
main()

