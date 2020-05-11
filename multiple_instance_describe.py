import boto3
import csv
import os
import sys
import single_instance_describe as sid
import csv_reader_writer as crw

def multiple_instance_describe(regName):
    client = boto3.client('ec2',region_name=regName)
    response = client.describe_instances()
    try:
        count = len(response['Reservations'])
        
        for i in range (0, count):
            
            # If the user has selected to launch more than one (n) instances from console, the describe api call put the details of n instance inside same reservations, inside the list 'Instances'
            MultipleInstanceCount = len(response['Reservations'][i]['Instances'])
            for mic in range (0, MultipleInstanceCount):
                InstanceId = response['Reservations'][i]['Instances'][mic].get("InstanceId")
                dataDict, volumeDict, tagDict = sid.single_instance_describe(regName,InstanceId)
                #Instead of passing another argument to writer function, the mic value has been added to the data dictionary.
                #Otherwise, it would have broken the reader functionality.
                dataDict["mic"] = mic
                crw.csv_writer(dataDict, volumeDict, tagDict, i)
    
    except Exception as error:
            print(error)