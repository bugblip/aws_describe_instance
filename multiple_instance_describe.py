import boto3
import csv
import os
import single_instance_describe as sid
import csv_reader_writer as crw

def multiple_instance_describe(regName):
    client = boto3.client('ec2',region_name=regName)
    response = client.describe_instances()
    try:
        count = len(response['Reservations'])
        for i in range (0, count):
            InstanceId = response['Reservations'][i]['Instances'][0].get("InstanceId")
            dataDict, volumeDict, tagDict = sid.single_instance_describe(regName,InstanceId)
            crw.csv_writer(dataDict, volumeDict, tagDict, i)
    except Exception as error:
            print(error)