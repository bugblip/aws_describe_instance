import boto3
import csv_reader_writer as crw
import multiple_instance_describe as mid
import sys

if __name__ == '__main__':
    
    regions = ["us-east-2","us-east-1","us-west-1","us-west-2","af-south-1","ap-east-1","ap-south-1","ap-northeast-3","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1","ca-central-1","eu-central-1","eu-west-1","eu-west-2","eu-south-1","eu-west-3","eu-north-1","me-south-1","sa-east-1"]
    
    print("Select the region in which the AWS resource exist")
    for reg in range(0, len(regions)):
        print(f"{reg+1}.\t{regions[reg]}")
    
    choice1 = int(input())
    if(choice1 >=1 and choice1 <= len(regions)):
        regName = regions[choice1-1]
    else:
        print("Wrong Input, please try again.")
        sys.exit()
    
    #Counting total Number of EC2 Instances in the region
    var = 0
    client = boto3.client('ec2',region_name=regName)
    response = client.describe_instances()
    totalRes = len(response['Reservations'])
    print("tr",totalRes)
    if (totalRes == 0):
        print(f"The Selected region, {regName} does not have any EC2 instance.")
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