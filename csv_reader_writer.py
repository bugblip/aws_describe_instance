import boto3
import csv
import os
import datetime
import single_instance_describe as sid

#Output File Variables
basename = "output"
suffix = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
filename = "_".join([basename, suffix])
filename = filename+".csv"
cw_path = os.getcwd()
outputFilePath = cw_path +"/"+ filename


def csv_reader(regName,inputfilepath):
    try:
        with open(inputfilepath, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for rowNum, line in enumerate(csv_reader):
                instID=str("".join(line))
                dataDict, volumeDict, tagDict = sid.single_instance_describe(regName,instID)
                csv_writer(dataDict, volumeDict, tagDict, rowNum)
    except Exception as error:
        print(error)
        

def csv_writer(dataDict, volumeDict, tagDict, rowNum):

    #Writing to CSV file and formatting       
    with open(filename, 'a') as f:
        if ( rowNum == 0 ):
            print(f"Generating output file at - {outputFilePath}") 
            for key,value in dataDict.items():
                f.write(f"{key},")
        f.write(f"\n")
        for key,value in dataDict.items():
            if ( key == "Volume"):
                for k,v in volumeDict.items():
                    f.write(f"{k} = {v} \t\t")
                #Once All the details of the dict are written we need to move to another column
                f.write(",")
            elif ( key == "Tags"):
                for tdk,tdv in tagDict.items():
                    f.write(f"{tdk} = {tdv};")
                #Once All the details of the dict are written we need to move to another column
                f.write(",")
            else:
                f.write(f"{value},")