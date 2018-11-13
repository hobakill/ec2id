#!/usr/bin/env python

import boto3
import argparse
import sys

region = {
    'ap2': 'ap-northeast-1',
    'ap3': 'ap-southeast-2',
    'bs1': 'us-east-2',
    'ea1': 'us-east-1',
    'eu1': 'eu-west-1',
    'fu2': 'us-west-2',
    'op1': 'us-east-2',
    'we1': 'us-west-1'
    }

parser = argparse.ArgumentParser(description='Get you some instanceID info')
parser.add_argument(
    'name', nargs='?', const=1, help='eg: tagserve01ea1, lb02bs1, ops99fu2'
    )
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


def list_instances_by_tag_value(tagkey, tagvalue):
    ec2 = boto3.client('ec2', region_name=region.get(args.name[-3:]))
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    return instancelist


results = list_instances_by_tag_value("Name", args.name)

print(' '.join(results))
