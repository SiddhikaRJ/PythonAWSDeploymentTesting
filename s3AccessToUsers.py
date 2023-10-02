    
import boto3
import json
import csv

print("Code Running")

aws_access_key_id=''
aws_secret_access_key=''
region_name=''

#fidlist={'pythonuser1Testing':'dev/1noaccess1','accountadminaccess':'dev/1access1'}
fidlist={'pythonuser1Testing':'dev/1noaccess1','accountadminaccess':'dev/1access1'}
class CheckS3Acess:
    def __init__(self):
        
        self.session = boto3.session.Session()
        self.client = self.session.client(
        service_name='secretsmanager',
        region_name='ap-south-1'     
    )
    def GettingAccessDetails(self,Username):
        try:
            print("1. Inside GettingAccessDetails")
            print(Username)
            Secret_name=fidlist[Username]
            self.getkeydetails(Secret_name)
            #print(Secret_name)
        except Exception as e:
            raise e
    
    def getkeydetails(self,Secret_name):
        try:
            print("2. Inside getkeydetails")
            if Secret_name== '':raise Exception("Secret Name cannot be Null ")
            get_secret_value_response = self.client.get_secret_value(
                 SecretId=Secret_name
             )
            print(get_secret_value_response)
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                secret = json.loads(secret)

            #print(secret)
            for k,v in secret.items():
                aws_access_key_id=secret['aws_access_key_id']
                aws_secret_access_key=secret['aws_secret_access_key']
                region_name=secret['region_name']
            #print(aws_access_key_id,aws_secret_access_key,region_name)
            self.CreateS3Connection(aws_access_key_id,aws_secret_access_key,region_name)
        except Exception as e:
            return e
        
    def CreateS3Connection(self,aws_access_key_id,aws_secret_access_key,region_name):
        try:
            print("3. Inside CreateS3Connection")
            print("Staring with Connection")
            s3_client=boto3.client('s3',aws_access_key_id=aws_access_key_id
                    ,aws_secret_access_key=aws_secret_access_key
                    ,region_name=region_name)
            print("Staring with recevied")
            #self.AccessBucketDisplayList(s3_client)
            self.read_file_from_s3(s3_client,'onemorebucket-siddhika','EMR.txt')
        except Exception as e:
            print(e)


        
    def AccessBucketDisplayList(self,s3_client):
        try:
            print("4. Inside AccessBucketDisplayList")
            print("Listing Bucket")
            response = s3_client.list_buckets()
            print(response)
            #print('Bucket Name - {}'.format(response['Buckets'][0]['Name']))
            for obj in response['Buckets']:
                print(obj['Name'])
        except Exception as e:
            print(e)

    def read_file_from_s3(self,s3_client,bucket_name, file_name):
        print("4. Inside Reading")
        #---code for csv file start
        # obj = s3_client.get_object(bucket_name, file_name) 
        # data = obj['Body'].read().decode('utf-8').splitlines() 
        # records = csv.reader(data) 
        # headers = next(records) 
        # print('headers: %s' % (headers)) 
        # for eachRecord in records: 
        #     print(eachRecord)
        #---code for csv file end
        #---code for txt file Start 
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        #print(obj)
        data = obj['Body'].read()
        print(data)
        #---code for txt file end 

    
secret_manager = CheckS3Acess()
secret_manager.GettingAccessDetails('accountadminaccess')
#secret_manager.GettingAccessDetails('pythonuser1Testing')