import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import boto3

print("just before any connection")
dynamodb = boto3.resource('dynamodb')
player_table = dynamodb.Table('Players')
resp_user = player_table.get_item(Key={'user_id':"RicardoShimoda"})
print(resp_user["Item"])


#def main():


#if __name__ == '__main__':
   #print('Starting operations')
   #main()
   