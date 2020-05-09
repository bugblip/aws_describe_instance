import boto3
import csv
import os
import datetime
import csv_reader_writer as crw

def single_instance_describe(regName,instID):
    client = boto3.client('ec2',region_name=regName)
    volumeDict = {}
    dataDict = {}
    sgList = []
    tagDict = {}
    response = client.describe_instances(InstanceIds=[instID])
    InstanceData = response['Reservations'][0]['Instances'][0]
 
    #Storing the Security Group ID in an empty List
    sgroups = InstanceData['SecurityGroups']
    for s in range (0, len(sgroups)):
        GroupId = sgroups[s]['GroupId']
        sgList.append(GroupId)
    #Storing the block device mapping and corresponding volume in a dictionary
    deviceMapping = InstanceData['BlockDeviceMappings']
    totalVol=len(deviceMapping)
    for v in range (0, totalVol):
        DeviceName = deviceMapping[v]['DeviceName']
        VolumeId = deviceMapping[v]['Ebs']['VolumeId']
        volumeDict[DeviceName] = VolumeId
        
    #Getting IAM Instance Profile
    if 'IamInstanceProfile' in InstanceData:
        IamInstanceProfile = (InstanceData['IamInstanceProfile'].get("Arn")).split("/")
        IamInstanceProfileName = IamInstanceProfile[1]
    else:
        IamInstanceProfileName = "-"
        
    #Getting Instance Tags
    if 'Tags' in InstanceData:
        TagList = InstanceData['Tags']
        for n in range (0, len(TagList)):
            tk = TagList[n].get("Key")
            tv = TagList[n].get("Value")
            tagDict[tk]=tv
        #The Tag Dictionary will have the aws server name under key Name
        InstanceName = tagDict.get("Name","-")
    else:
        InstanceName = "-"
    
    #Adding all the info to the data Dictionary
    dataDict["InstanceName"] = InstanceName
    dataDict["InstanceId"] = InstanceData.get("InstanceId","-")
    dataDict["InstanceState"] = InstanceData['State']['Name']
    dataDict["AvailabilityZone"] = InstanceData['Placement']['AvailabilityZone']
    dataDict["ImageId"] = InstanceData.get("ImageId","-")
    dataDict["SubnetId"] = InstanceData.get("SubnetId","-")
    dataDict["VpcId"] = InstanceData.get("VpcId","-")
    dataDict["SecurityGroups"] = " ".join(sgList)
    dataDict["Volume"] = volumeDict
    dataDict["RootDeviceName"] = InstanceData.get("RootDeviceName","-")
    dataDict["PrivateIpAddress"] = InstanceData.get("PrivateIpAddress","-")
    dataDict["PublicIpAddress"] = InstanceData.get("PublicIpAddress","-")
    dataDict["KeyName"] = InstanceData.get("KeyName","-")
    dataDict["IamInstanceProfileName"] = IamInstanceProfileName
    dataDict["LaunchTime"] = str(InstanceData['LaunchTime'])
    dataDict["Platform"] = InstanceData.get("Platform","-")
    dataDict["NetworkInterfaceId"] = InstanceData.get("NetworkInterfaceId","-")
    dataDict["MacAddress"] = InstanceData.get("MacAddress","-")
    dataDict["Tags"] = tagDict
    
    return (dataDict, volumeDict, tagDict)