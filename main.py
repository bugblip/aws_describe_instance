import boto3
import sys
import datetime
import csv_reader_writer as crw
import multiple_instance_describe as mid


def runtime(startTime):
    endTime = datetime.datetime.now()
    executionTime = endTime - startTime
    print (f"Script RunTime (HH:MM:SS)= {executionTime}".center(120,"-"))
    print("\n")

if __name__ == '__main__':
    
    startTime = datetime.datetime.now()
    print("\n")
    print (f"Execution started at = {startTime}".center(120,"-"))
    
    #Getting AWS Region
    regions = []
    client = boto3.client('ec2')
    response = client.describe_regions()
    regData = response['Regions']
    print("Select the region in which the AWS resource exist")
    for i in range (0, len(regData)):
        rid = regData[i].get("RegionName")
        regions.append(rid)
        print(f"{i+1}.\t{rid}")
    
    choice1 = int(input())
    if(choice1 >=1 and choice1 <= len(regions)):
        regName = regions[choice1-1]
    else:
        print("Wrong Input, please try again.")
        runtime(startTime)
        sys.exit()
    
    #Counting total Number of EC2 Instances in the region
    var = 0
    client = boto3.client('ec2',region_name=regName)
    response = client.describe_instances()
    totalRes = len(response['Reservations'])

    if (totalRes == 0):
        print(f"The Selected region, {regName} does not have any EC2 instance.")
        runtime(startTime)
        sys.exit()
    for tr in range (0, totalRes):
        MultipleInstanceCount = len(response['Reservations'][tr]['Instances'])
        if ( MultipleInstanceCount > 0):
           var += ( MultipleInstanceCount - 1 )
    TotalCount =  ( var + totalRes )
    print(f"There is/are {TotalCount} EC2 instance(s) in {regName} region.")
    
    #Choices    
    print ("Enter Your choice")
    print(f"1. Details of all EC2 Instance in {regName}")
    print(f"2. Details of specific EC2 instnace in {regName} from an input CSV file containing instnace id(s)")
    choice2 = int(input())
    if (choice2 == 1 ) :
        mid.multiple_instance_describe(regName)
    elif (choice2 == 2 ) :
        print("Please Enter the Complete or absolute path of the input CSV file.")
        inputfilepath = str(input())
        crw.csv_reader(regName, inputfilepath)
    else:
        print("Wrong Input, please try again.")
        runtime(startTime)
        sys.exit()
    
    #calculating script runtime
    runtime(startTime)