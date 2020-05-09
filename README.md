### Features

This code will generate an csv output file with details of EC2 instnaces in a prticular region.

The ouput file will include following details.

    InstanceName
    InstanceId
    InstanceState
    AvailabilityZone
    ImageId
    SubnetId
    VpcId
    SecurityGroups
    Volume
    RootDeviceName
    PrivateIpAddress
    PublicIpAddress
    KeyName
    IamInstanceProfileName
    LaunchTime
    Platform
    NetworkInterfaceId
    MacAddress
    Tags

### Usage

Run the main file using `python main.py` . The first input will ask for the AWS region where the EC2 Describe Instance API  will be called.

Afterthat, the code will give the user 2 options,
> 1. Details of all EC2 Instance in us-east-1
> 2. Details of specific EC2 instnace in us-east-1 from an input CSV file containing instnace id(s)

- For 1st option, no extra input is required.
- For 2nd option , path of an input csv file containing instance ids is required. (for ex, /home/ec2-user/environment/temp/samplefile.csv)

The input file will be in following format
```
i-091c628ed0fhd1952
i-05076491b03467cb8
```

The ouput file will be generated with following name format `output_ddmmYYYY_HHMMSS` in present working directory.