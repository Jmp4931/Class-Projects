#Jake Paczkowski
#Script 1 NSSA-221
#!/bin/python3

#import packages
import os
import socket

#selection menu
def displayMenu():
    print("1. Display the local default gateway")
    print("2. Test Local Connectivity")
    print("3. Test Remote Connectivity")
    print("4. Test DNS Resolution")
    print("5. End the script")
    

#method to dynamically find and display the default gateway
def getDefaultGateway():
    try:
        result = os.popen("ip route show default").read()
        #get rid of excess whitespace
        gw = result.split(" ")[2]
        return gw.strip()
    except Exception as e:
        return str("Error Finding the default gateway")

#method that will ping the host IP address
def testLocalConnection():
    hostName = "192.168.203.87"
    
    #response will be 0 on a successful ping, and 1 on a failed ping
    response = os.system("ping -c 4 " + hostName)

    if response == 0:
        return True
    else:
        return False

#Method to test a ping to a remote connection
def testRemoteConnection():
    #Use the RIT DNS as a ping test
    hostName = "129.21.3.17"

    response = os.system("ping -c 4 " + hostName)

    if response == 0:
        return True
    else:
        return False

#test DNS resolution method
def dnsResolution():
    #use googles public DNS as the test
    domain = "www.google.com"

    try:
        #Retuen true if there are no errors, return false if there is an error 
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


#Main method
def main():

   print("Network Connectivity Tester")
   
   
   keepGoing = True
   #While loop that will only close when the flag is set to false
   while(keepGoing):
       #display the menu every time the loop continues
       displayMenu()
       #Make sure that the user is entering valid, integer input
       try:
           selection = int(input("Enter your selection from the corresponding number: "))
       except ValueError:
           continue
        
       #display the default gateway
       if selection == 1:
           print(f"The host's default gateway is: {getDefaultGateway()}")
       #Do the local ping test and display the results
       if selection == 2:
          
           print("Testing local connectivity...")

           if testLocalConnection() == True:
               print("The local ping test completed successfully")
           else:
               print("The ping failed...")
      #Do the remote ping test and display the results
       if selection == 3:

            print("Testing remote connectivity...")
            if testRemoteConnection() == True:
                print("The remote ping test completed successfully")
            else:
                print("The ping failed...")
       #Do the DNS Resolution test and display the results
       if selection == 4:
           if dnsResolution:
               print("Successful DNS Resolution test")
           else:
               print("The test failed...")
       #end the script
       if selection == 5:
           keepGoing = False
           print("Script Closing...")
       #make sure that the number that is entered is a valid menu option
       elif selection < 1 or selection > 5 or isinstance(selection, float):
           print("Invalid input, please try again")

       
#call the main function
main()



