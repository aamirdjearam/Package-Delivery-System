#C950 Submission | Aamir Djearam | 009101364

#Import relevant files and packages
import csv
import Package
import HashTable
import datetime

#Create Empty Lists
distanceList = []
addressList = []
addressDict = {}


#Read the Distance CSV and insert into a list
#Time Complexity O(1)
with open("csv/distanceCSV.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)

packageHash = HashTable.ChainingHashTable()


#Read the Address CSV and insert information into the dictionary
#Time Complexity O(N)
with open("csv/addressCSV.csv") as dataFile:
    addressinfo = csv.reader(dataFile, delimiter=",")
    for addressValue in addressinfo:
        addressList.append(addressValue[2])
        addressDict[addressValue[2]] = addressValue[0]

#Load the Package Data into the Hash Table
#Time Complexity O(N)
    with open("csv/packageCSV.csv", encoding='utf-8-sig') as dataFile:
        packageinfo = csv.reader(dataFile, delimiter=",")

        for section in packageinfo:
            PackageID = int(section[0])
            address = section[1]
            city = section[2]
            state = section[3]
            zip = section[4]
            deliveryTime = section[5]
            size = section[6]
            notes = section[7]
            start_time = ""
            end_time = ""
            status = "On Truck"
            newPackage = Package.Package(PackageID, address, city, state, zip, deliveryTime, size, notes, start_time, end_time)
            packageHash.insert(PackageID, newPackage)



class Truck:
    #Time Complexity O(N)
    def __init__(self, id, time, packages):
        self.currentLocation = "4001 South 700 East"
        self.id = id
        self.mileage = 0
        self.time = time
        self.departure_time = time
        self.packages = packages

        for i in packages:
            package = packageHash.lookup(i)
            package.status = "En route"

    #Time Complexity O(1)
    #This function removes a package from a truck
    def unload(self, packageID):
        if packageID in self.packages:
            self.packages.remove(packageID)
        else:
            print("Cannot unload Package")


#Time Complexity O(1)
#This function finds the distance between two given addresses
def distance_in_between(current, address):
    distance_between = CSV_Distance[current][address]
    if distance_between == '':
        distance_between = CSV_Distance[address][current]
    return float(distance_between)

#Time Complexity O(N)
#This function uses a nearest neighbor algorithm to find the next closest delivery and returns the relevant information
def minDistanceFrom(currentLocation, remainingPackagesList):
    closestDelivery = 100
    newLocation = ""
    packageToDeliver = 0
    for PackageID in remainingPackagesList:
        currentPackage = packageHash.lookup(PackageID)
        addressNumber = int(addressDict[currentPackage.address])
        distance = distance_in_between(currentLocation, addressNumber)
        if (distance < closestDelivery):
            closestDelivery = distance
            newLocation = currentPackage.address
            packageToDeliver = PackageID
    return closestDelivery, newLocation, packageToDeliver

#Time Complexity O(N^2)
#This function delivers packages on a given truck until there are no packages left.
#It tracks the mileage of the truck and the time it takes to deliver pacakges, updating packages when they have been delivered
def truckDeliverPackages(truck):
    while len(truck.packages) > 0:

        #Finding the next addres to Deliver
        currentAddress = int(addressDict[truck.currentLocation])
        nearestDelivery = minDistanceFrom(currentAddress, truck.packages)
        packageToDeliver = packageHash.lookup(nearestDelivery[2])

        #Delivering the Package
        truck.mileage += (nearestDelivery[0])
        travelTime = datetime.timedelta(seconds=(nearestDelivery[0] / 0.005))
        truck.time = truck.time + travelTime

        truck.currentLocation = nearestDelivery[1]

        packageToDeliver.end_time = truck.time
        packageToDeliver.status = "Delivered"
        packageToDeliver.truck = ("Assigned to Truck " + str(truck.id))

        truck.unload(nearestDelivery[2])

    else:
        currentAddress = int(addressDict[truck.currentLocation])
        truck.mileage += (distance_in_between(0, currentAddress))
        truck.currentLocation = "4001 South 700 East"



#Time Complexity O(N)
#This function sets the status of all packages on the given truck to "En Route" and it sets the departure time of the packages
def loadPackages(truck):
    for i in truck.packages:
        package = packageHash.lookup(int(i))
        package.status = "En Route"
        package.start_time = truck.departure_time

#Time Complexity O(1)
#This function checks if the package has been delivered or if it is on route. It also changes the address for Package 9 which has an address change request
def validateTime(package, timeStamp):
    timeofUpdate = datetime.datetime.strptime("10:20:00", "%H:%M:%S") - datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    if timeStamp > package.start_time:
        if timeStamp > package.end_time:
            package.status = "Delivered"
        else:
            package.status = "En Route"
    else:
        package.status = "At Hub"
    if package.id == 9 and timeStamp <= timeofUpdate:
       packageToUpdate = packageHash.lookup(9)
       packageToUpdate.address = "300 State St"
       packageToUpdate.zip = "84103"



#Time Complexity O(N^2)
#This function manually loads the trucks with their curated packages lists
def loadTrucks():
    truck1 = Truck(1, datetime.timedelta(hours=8, minutes=0, seconds=0), [13, 14, 15, 16, 19, 20, 1, 30, 31, 34, 37, 39, 29, 40])
    loadPackages(truck1)
    truckDeliverPackages(truck1)

    truck2 = Truck(2, datetime.timedelta(hours=9, minutes=5, seconds=0), [3, 18, 36, 38, 25, 6])
    loadPackages(truck2)
    truckDeliverPackages(truck2)

    truck3 = Truck(3, datetime.timedelta(hours=10, minutes=20, seconds=0), [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 28, 32, 33, 35, 39])
    loadPackages(truck3)
    truckDeliverPackages(truck3)

    totalMileage = round(truck1.mileage + truck2.mileage + truck3.mileage, 2)

    return totalMileage


#Time Complexity O(N^2)
#The main class initiatizes the programs and calls all of the functions when appropriate
class Main:

    totalMileage = loadTrucks()

    #Intro Text
    print("Created by Aamir Djearam")
    print("Submission for C950 Data Structures and Algorithms II")
    print("\nWGUPS Routing Program")


    #Menu Items

    program = True
    while program == True:
        print("\nPlease Select from one of the following Menu Items")
        print("1: Status for all Packages and Total Mileage for all deliveries")
        print("2: Status for all Packages at a specific time")
        print("3: Status of a specific package at a specific time")
        print("4: Exit the program")
        option = input("Select an Option: ")

        #Option 1 prints the status for all packages after they have all been delivered along with the total mileage of all trucks
        if option == "1":
            print("\nALL PACKAGES \n")
            for packID in range(1, 41):
                package = packageHash.lookup(packID)
                print("Package ID: " + str(package.id) + " | Address: " + str(package.address) + " | City: " + str(package.city) + " | Zip: " + str(package.zip) + " | Delivery Time " + str(package.end_time) + " | Status: " + str(package.status) + " | Truck: " + str(package.truck) + " | Notes: " + str(package.notes))
            print("")
            print("Total Mileage = " + str(totalMileage) + " miles \n")

        #Option 2 prints the status for all packages at a certain time
        elif option == "2":
            print("\nAll Packages at Time: \n")
            timeInput = input("Please Enter a time value in the format HH:MM:SS: ")
            try:
                time = datetime.datetime.strptime(timeInput, "%H:%M:%S") - datetime.datetime.strptime("00:00:00","%H:%M:%S")
            except ValueError:
                print("Invalid Time Entered. Please try again")
                continue
            for packID in range(1, 41):
                package = packageHash.lookup(packID)
                validateTime(package, time)
                print("Package ID: " + str(package.id) + " | Address: " + str(package.address) + " | City: " + str(package.city) + " | Zip: " + str(package.zip) + " | Delivery Time " + str(package.end_time) + " | Status: " + str(package.status) + " | Truck: " + str(package.truck) + " | Notes: " + str(package.notes))
            #Reset the trucks
            loadTrucks()

        #Option 3 prints the status for an individual package at a certain time
        elif option == "3":
            print("Please Enter a Package ID between 1 - 40")
            findPackage = input("Package ID: ")
            try:
                if 1 > int(findPackage) or int(findPackage) > 40:
                    print("An incorrect value has been entered. Returning to Main Menu")
                else:
                    timeInput = input("Please Enter a time value in the format HH:MM:SS: ")
                    try:
                        time = datetime.datetime.strptime(timeInput, "%H:%M:%S") - datetime.datetime.strptime("00:00:00", "%H:%M:%S")
                        package = packageHash.lookup(int(findPackage))
                        validateTime(package, time)
                        print("\nPackage ID: " + str(package.id) + " | Address: " + str(package.address) + " | City: " + str(package.city) + " | Zip: " + str(package.zip) + " | Delivery Time " + str(package.end_time) + " | Status: " + str(package.status) + " | Truck: " + str(package.truck) + " | Notes: " + str(package.notes))
                        loadTrucks()
                    except ValueError:
                        print("An incorrect value has been entered. Returning to Main Menu")
                loadTrucks()
            except ValueError:
                print("Error. Returning to the the main menu")

        #Option 4 closes the program
        elif option == "4":
            print("Closing the program. Thank you!")
            program == False
            quit()

        else:
            print("Invalid Option. Closing Program. Goodbye")
            program == False
            quit()
