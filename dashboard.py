import json
def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from NEW1 Lambda !')
    }

import boto3
from datetime import datetime, timedelta
import time
import os
import requests
cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')
s3client=boto3.client('s3', region_name='us-east-2')
lambdaclient = boto3.client('lambda', region_name='us-east-2')
logclient = boto3.client('logs', region_name='us-east-2')
esclient = boto3.client('es')

if os.environ['COMPLEXITY']:
 complexity = int(os.environ['COMPLEXITY'])
else:
 complexity = 6
colors_list=["#d62728","#1f77b4","#2ca02c","#fce205","#9467bd","#bcbd22","#8c564b","#17becf","#7f7f7f","#cc7722","#ff7f0e","#1034a6","#aec7e8","#f7b6d2","#98df8a"]
#=====================================#
#             S3 BUCKETS              #
#=====================================#
sort_size_list=[]
sort_object_list=[]
bucket_color_dict={}
i=0
while  i< len(s3client.list_buckets()["Buckets"]):
 if i < len(colors_list):
  bucket_color_dict[s3client.list_buckets()["Buckets"][i]['Name']]= ', "color": "'+ colors_list[i]+'"'
 else:
  bucket_color_dict[s3client.list_buckets()["Buckets"][i]['Name']]=''
 i+=1

#get BucketSizeBytes, NumberOfObjects, PutRequests of every bucket, store to size_dict, object_dict, active_dict
seconds_in_one_day = 86400  # used for granularity
size_dict = {}
object_dict={}
active_dict={}
for bucket in s3client.list_buckets()["Buckets"]:
  bucket_name = bucket['Name']
  bucket_size = cloudwatch.get_metric_statistics(
    Namespace='AWS/S3',
    Dimensions=[
        {
            'Name': 'BucketName',
            'Value': bucket_name
        },
        {
            'Name': 'StorageType',
            'Value': 'StandardStorage'
        }
    ],
    MetricName='BucketSizeBytes',
    StartTime=datetime.now() - timedelta(days=2),
    EndTime=datetime.now(),
    Period=seconds_in_one_day,
    Statistics=[
        'Average'
    ],
    Unit='Bytes'
  )
  bucket_object = cloudwatch.get_metric_statistics(
    Namespace='AWS/S3',
    Dimensions=[
        {
            'Name': 'BucketName',
            'Value': bucket_name
        },
        {
            'Name': 'StorageType',
            'Value': 'AllStorageTypes'
        }
    ],
    MetricName='NumberOfObjects',
    StartTime=datetime.now() - timedelta(days=2),
    EndTime=datetime.now(),
    Period=seconds_in_one_day,
    Statistics=[
        'Average'
    ],
    Unit='Count'
  )
  bucket_active = cloudwatch.get_metric_statistics(
    Namespace='AWS/S3',
    Dimensions=[
        {
            'Name': 'BucketName',
            'Value': bucket_name
        },
        {
            'Name': 'FilterId',
            'Value': 'EntireBucket'
        }
    ],
    MetricName='PutRequests',
    StartTime=datetime.now() - timedelta(days=2),
    EndTime=datetime.now(),
    Period=seconds_in_one_day,
    Statistics=[
        'Sum'
    ],
    Unit='Count'
  )
  if bucket_size['Datapoints']:
   size_dict[bucket_name]= bucket_size['Datapoints'][0]['Average']
  if bucket_object['Datapoints']:
   object_dict[bucket_name]=bucket_object['Datapoints'][0]['Average']
  if bucket_active['Datapoints']:
   active_dict[bucket_name]=bucket_active['Datapoints'][0]['Sum']

#save names of buckets sorted by size to sort_size_list
listik =[]
for n in size_dict:
  listik.append(float(size_dict[n]))
listik.sort(reverse=True)
for i in range(len(size_dict)):
 for n in size_dict:
  if float(size_dict[n])==listik[i]:
   if n not in sort_size_list:
    sort_size_list.append(n)

#save names of buckets sorted by object count to sort_object_list
listik =[]
for n in object_dict:
  listik.append(float(object_dict[n]))
listik.sort(reverse=True)
for i in range(len(object_dict)):
 for n in object_dict:
  if float(object_dict[n])==listik[i]:
   if n not in sort_object_list:
    sort_object_list.append(n)

#decrease sorted lists in accordance to specified complexity
complex_sort_object_list=[]
complex_sort_size_list=[]
i=0
while i < complexity and i< len(sort_object_list):
 complex_sort_object_list.append(sort_object_list[i])
 i+=1
i=0
while i < complexity and i< len(sort_size_list):
 complex_sort_size_list.append(sort_size_list[i])
 i+=1

#save names of buckets sorted by PutRequests to object_sort_active_list and size_sort_active_list
listik =[]
size_sort_active_list=[]
object_sort_active_list=[]
for n in active_dict:
  listik.append(float(active_dict[n]))
listik.sort(reverse=True)
for i in range(len(active_dict)):
 for n in active_dict:
  if float(active_dict[n])==listik[i]:
   if n not in size_sort_active_list:
    if n not in complex_sort_size_list:
     size_sort_active_list.append(n)
  if n not in object_sort_active_list:
    if n not in complex_sort_object_list:
     object_sort_active_list.append(n)
#======================================#
#            LAMBDA FUNCTIONS          #
#======================================#
sort_invocations_list=[]

#get list of functions
invocations_dict={}
for function in lambdaclient.list_functions()['Functions']:
 function_name = function['FunctionName']
 invocations = cloudwatch.get_metric_statistics(
    Namespace='AWS/Lambda',
    Dimensions=[
        {
            'Name': 'FunctionName',
            'Value': function_name
        }
    ],
    MetricName='Invocations',
    StartTime=datetime.now() - timedelta(days=3),
    EndTime=datetime.now(),
    Period=seconds_in_one_day,
    Statistics=[
        'Sum'
    ],
    Unit='Count'
 )
 if invocations['Datapoints']:
   invocations_dict[function_name]= invocations['Datapoints'][0]['Sum']

#save names of functions sorted by invocations count to sort_invocations_list
listik =[]
for n in invocations_dict:
  listik.append(float(invocations_dict[n]))
listik.sort(reverse=True)
for i in range(len(invocations_dict)):
 for n in invocations_dict:
  if float(invocations_dict[n])==listik[i]:
   if n not in sort_invocations_list:
    sort_invocations_list.append(n)

function_color_dict={}
i=0
while  i< len(sort_invocations_list):
 if i < len(colors_list):
  function_color_dict[sort_invocations_list[i]]= ', "color": "'+ colors_list[i]+'"'
 else:
  function_color_dict[sort_invocations_list[i]]=''
 i+=1

#decrease sorted lists in accordance to specified complexity
complex_sort_invocations_list=[]
i=0
while i < complexity and i< len(sort_invocations_list):
 complex_sort_invocations_list.append(sort_invocations_list[i])
 i+=1
#get memory usage from cloudWatch logs (for lambdas in complex_sort_invocations_list)
start_time = int(time.time()*1000 - 86400000) 
end_time=int(time.time())*1000
for function_name in complex_sort_invocations_list:
 print ("function name: "+function_name)
 """
 #SLOW code that uses filter_log_events, it return very accurate values
 mem_sum=0
 mem_num=0
 mem_max=0
 mem_average=0
 paginator = logclient.get_paginator('filter_log_events')
 response_iterator = paginator.paginate(
    logGroupName='/aws/lambda/'+function_name,
    filterPattern='REPORT',
    startTime=start_time,
    endTime=end_time
 )
 for log_event in response_iterator:
  for event in log_event['events']:
    mem_sum+=float(event['message'][-8:-4])
    mem_num+=1
    if mem_max < float(event['message'][-8:-4]):
     mem_max=float(event['message'][-8:-4])
 if mem_num:
  mem_average=mem_sum/mem_num
 """
 #FAST code that uses log insight but returns not accurate values
 mem_sum=0
 mem_num=0
 mem_max=0
 mem_average=0
 start_query = logclient.start_query(
    logGroupName='/aws/lambda/'+function_name,
    startTime=start_time,
    endTime=end_time,
    queryString='stats max(@maxMemoryUsed) as memoryused by bin(10s)| filter @message like /REPORT/'
 )
 i=0
 while i <=30:
  get_query = logclient.get_query_results(
   queryId= start_query['queryId']
  )
  if get_query['status']=='Complete':
   for datapoint in get_query['results']:
    if len(datapoint)>1:
     mem_sum+=float(datapoint[1]['value'])
     mem_num+=1
     if mem_max < float(datapoint[1]['value']):
      mem_max=float(datapoint[1]['value'])
   if mem_num:
    mem_average=mem_sum/mem_num/1024/1024
    mem_max=mem_max/1024/1024
   break
  else:
   time.sleep(1)
  i+=1
 print ("number of datapoints: ", mem_num)
 print ("memory average: ", mem_average)
 print ("memory max: ", mem_max)
 response = cloudwatch.put_metric_data(
    Namespace='Custom metrics',
    MetricData=[
        {
            'MetricName': 'memory_average',
            'Dimensions': [
                {
                    'Name': 'Lambda Function',
                    'Value': function_name
                },
            ],
            'Value': mem_average,
            'Unit': 'Megabytes',
            'StorageResolution': 60
        },
    ]
 )
 response = cloudwatch.put_metric_data(
    Namespace='Custom metrics',
    MetricData=[
        {
            'MetricName': 'memory_max',
            'Dimensions': [
                {
                    'Name': 'Lambda Function',
                    'Value': function_name
                },
            ],
            'Value': mem_max,
            'Unit': 'Megabytes',
            'StorageResolution': 60
        },
    ]
 )
 
#======================================#
#            Elasticsearch             #
#======================================#
InstanceCount=''
#get number of Instances in cluster
try:
 es_domain = esclient.describe_elasticsearch_domain(DomainName='dev')
 InstanceCount= es_domain['DomainStatus']['ElasticsearchClusterConfig']['InstanceCount']
except:
 InstanceCount=''
 pass

#get size and documents count of indices
sort_indices_list=[]
indices_count_dict={}
indices_size_dict={}
es_endpoint_URL = "https://vpc-dev-rpn27btciwtl44zy45xs3xgohy.us-east-2.es.amazonaws.com/"
r = requests.get(url = es_endpoint_URL+'_all/_stats')
data = r.json()
for index in  data['indices']:
   indices_count_dict[index]= data['indices'][index]['primaries']['docs']['count']
   indices_size_dict[index]= data['indices'][index]['primaries']['store']['size_in_bytes']
#print ("count: ",indices_count_dict)
#print ("size: ",indices_size_dict)

#save names of indices sorted by doc count to sort_indices_list
listik =[]
for n in indices_count_dict:
  listik.append(float(indices_count_dict[n]))
listik.sort(reverse=True)
for i in range(len(indices_count_dict)):
 for n in indices_count_dict:
  if float(indices_count_dict[n])==listik[i]:
   if n not in sort_indices_list:
    sort_indices_list.append(n)

#print ("sorted indices", sort_indices_list)
indices_color_dict={}
i=0
while  i< len(sort_indices_list):
 if i < len(colors_list):
  indices_color_dict[sort_indices_list[i]]= ', "color": "'+ colors_list[i]+'"'
 else:
  indices_color_dict[sort_indices_list[i]]=''
 i+=1
#print ("indices colors: ", indices_color_dict)

#decrease sorted lists in accordance to specified complexity
complex_sort_indices_list=[]
i=0
while i < complexity and i< len(sort_indices_list):
 complex_sort_indices_list.append(sort_indices_list[i])
 i+=1
#put indices doccount and size as custom metrics to cloudwatch
for index in complex_sort_indices_list:
 response = cloudwatch.put_metric_data(
    Namespace='Custom metrics',
    MetricData=[
        {
            'MetricName': 'documents_count',
            'Dimensions': [
                {
                    'Name': 'Index name',
                    'Value': index
                },
            ],
            'Value': indices_count_dict[index],
            'Unit': 'Count',
            'StorageResolution': 60
        },
    ]
 )
 response = cloudwatch.put_metric_data(
    Namespace='Custom metrics',
    MetricData=[
        {
            'MetricName': 'index_size',
            'Dimensions': [
                {
                    'Name': 'Index name',
                    'Value': index
                },
            ],
            'Value': indices_size_dict[index]/1024/1024,
            'Unit': 'Megabytes',
            'StorageResolution': 60
        },
    ]
 )

#======================================#
#         CLOUDWATCH DASHBOARD         #
#======================================#

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    widget_text    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_text= '{"type":"text","x":0,"y":0,"width":24,"height":1,"properties":{"markdown":"\\n# S3 Buckets (total: '+ str(len(s3client.list_buckets()['Buckets'])) +')\\n"}},{"type":"text","x":0,"y":7,"width":24,"height":1,"properties":{"markdown":"\\n# Lambda Functions (total: '+ str(len(lambdaclient.list_functions()['Functions']))+')\\n"}},{"type":"text","x":0,"y":32,"width":24,"height":1,"properties":{"markdown":"\\n# Elasticsearch (total instances: '+ str(InstanceCount) +')\\n"}},{"type":"text","x":0,"y":33,"width":24,"height":1,"properties":{"markdown":"\\n## ES Cluster health\\n"}},{"type":"text","x":0,"y":40,"width":24,"height":1,"properties":{"markdown":"\\n## ES Cluster performance\\n"}},{"type":"text","x":0,"y":47,"width":24,"height":1,"properties":{"markdown":"\\n## ES Cluster latency\\n"}},{"type":"text","x":0,"y":54,"width":24,"height":1,"properties":{"markdown":"\\n## ES Indices\\n"}},'

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    widget_top_buckets_size    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_top_buckets_size=''
buckets_size_metrics = ''
size_most_active = ''
if sort_size_list:
 i=0
 while i < len(sort_size_list) and i< complexity:
  buckets_size_metrics += '["AWS/S3","BucketSizeBytes","StorageType","StandardStorage","BucketName","' + sort_size_list[i] + '",{"period":86400' +bucket_color_dict[sort_size_list[i]]+ '}],'
  i+=1
 buckets_size_metrics=buckets_size_metrics[:-1]
 i=0
 if size_sort_active_list:
  while i < len(size_sort_active_list) and i< complexity:
   size_most_active+= ',["...","' + size_sort_active_list[i] + '",{"period":86400' + bucket_color_dict[size_sort_active_list[i]]+'}]'
   i+=1
 widget_top_buckets_size = '{"type":"metric","x":0,"y":1,"width":12,"height":6,"properties":{"view":"timeSeries","stacked":false,"region":"us-east-2","metrics":['+buckets_size_metrics + size_most_active + '],"start":"-P3D","end":"P0D","legend":{"position":"right"},"title":"Top Buckets (size)"}},'

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    widget_top_buckets_count    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_top_buckets_count=''
buckets_object_metrics = ''
object_most_active = ''
if sort_object_list:
 i=0
 while i < len(sort_object_list) and i< complexity:
  buckets_object_metrics += '["AWS/S3","NumberOfObjects","StorageType","AllStorageTypes","BucketName","' + sort_object_list[i] + '",{"period":86400'+bucket_color_dict[sort_object_list[i]]+'}],'
  i+=1
 buckets_object_metrics=buckets_object_metrics[:-1]
 i=0
 if object_sort_active_list:
  while i < len(object_sort_active_list) and i< complexity:
   object_most_active+= ',["...","' + object_sort_active_list[i] + '",{"period":86400'+bucket_color_dict[object_sort_active_list[i]]+'}]'
   i+=1
 widget_top_buckets_count = '{"type":"metric","x":12,"y":1,"width":12,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":['+buckets_object_metrics+ object_most_active + '],"region":"us-east-2","legend":{"position":"right"},"title":"Top Buckets (object count)"}},'

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_invocations    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_invocations=''
lambda_invocations_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_invocations_metrics += '["AWS/Lambda","Invocations","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Sum"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_invocations_metrics=lambda_invocations_metrics[:-1]
 widget_lambda_invocations= '{"type":"metric","x":0,"y":8,"width":12,"height":6,"properties":{"metrics":['+lambda_invocations_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"}}},'

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_errors    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_errors=''
lambda_errors_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_errors_metrics += '["AWS/Lambda","Errors","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Sum"' +function_color_dict[sort_invocations_list[i]]+ '}],'
  i+=1
 lambda_errors_metrics=lambda_errors_metrics[:-1]
 widget_lambda_errors= '{"type":"metric","x":12,"y":8,"width":12,"height":6,"properties":{"metrics":['+lambda_errors_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"}}},'

#    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_throttles    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_throttles=''
lambda_throttles_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_throttles_metrics += '["AWS/Lambda","Throttles","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Sum"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_throttles_metrics=lambda_throttles_metrics[:-1]
 widget_lambda_throttles= '{"type":"metric","x":0,"y":14,"width":12,"height":6,"properties":{"metrics":['+lambda_throttles_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"}}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_ConcurrentExecutions    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_ConcurrentExecutions=''
lambda_ConcurrentExecutions_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_ConcurrentExecutions_metrics += '["AWS/Lambda","ConcurrentExecutions","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Sum"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_ConcurrentExecutions_metrics=lambda_ConcurrentExecutions_metrics[:-1]
 widget_lambda_ConcurrentExecutions= '{"type":"metric","x":12,"y":14,"width":12,"height":6,"properties":{"metrics":['+lambda_ConcurrentExecutions_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"}}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_duration_average    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_duration_average=''
lambda_duration_average_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_duration_average_metrics += '["AWS/Lambda","Duration","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Average"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_duration_average_metrics=lambda_duration_average_metrics[:-1]
 widget_lambda_duration_average= '{"type":"metric","x":0,"y":20,"width":12,"height":6,"properties":{"metrics":['+lambda_duration_average_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Duration (average)"}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_duration_max    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_duration_max=''
lambda_duration_max_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_duration_max_metrics += '["AWS/Lambda","Duration","FunctionName","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Maximum"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_duration_max_metrics=lambda_duration_max_metrics[:-1]
 widget_lambda_duration_max= '{"type":"metric","x":12,"y":20,"width":12,"height":6,"properties":{"metrics":['+lambda_duration_max_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Duration (max)"}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_mem_average   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_mem_average=''
lambda_mem_average_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_mem_average_metrics += '["Custom metrics", "memory_average", "Lambda Function","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Average"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_mem_average_metrics=lambda_mem_average_metrics[:-1]
 widget_lambda_mem_average= '{"type":"metric","x":0,"y":26,"width":12,"height":6,"properties":{"metrics":['+lambda_mem_average_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Memory (average)"}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_lambda_mem_max   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_lambda_mem_max=''
lambda_mem_max_metrics=''
if sort_invocations_list:
 i=0
 while i < len(sort_invocations_list) and i< complexity:
  lambda_mem_max_metrics += '["Custom metrics", "memory_max", "Lambda Function","'+ sort_invocations_list[i] +'",{"period":86400,"stat":"Average"'+function_color_dict[sort_invocations_list[i]]+'}],'
  i+=1
 lambda_mem_max_metrics=lambda_mem_max_metrics[:-1]
 widget_lambda_mem_max= '{"type":"metric","x":12,"y":26,"width":12,"height":6,"properties":{"metrics":['+lambda_mem_max_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Memory (max)"}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   ES Cluster health widgets    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_es_all_cluster_health=''
if InstanceCount:
 cluster_status ='{"type": "metric","x": 0,"y": 34, "width": 6,"height": 6,"properties": {"metrics": [[ { "expression": "m1/3", "label": "ClusterStatus.green", "id": "e1", "color": "#093" } ],[ "AWS/ES", "ClusterStatus.green", "DomainName", "dev", "ClientId", "731184136185", { "color": "#dbdb8d", "yAxis": "left", "id": "m1", "visible": false } ],[ ".", "ClusterStatus.yellow", ".", ".", ".", ".", { "color": "#c7c7c7", "id": "m2", "visible": false } ],[ { "expression": "m2*2/3", "label": "ClusterStatus.yellow", "id": "e2", "color": "#e07700" } ],[ "AWS/ES", "ClusterStatus.red", "DomainName", "dev", "ClientId", "731184136185", { "id": "m3", "color": "#C00" } ]],"view": "timeSeries","stacked": false,"region": "us-east-2","title": "Cluster status","fill": "Below","period": 60,"stat": "Maximum","yAxis": {"left": {"min": 0,"max": 1,"showUnits": false}},"legend": {"position": "hidden"}}},'
 cluster_writes_status='{"type":"metric","x":6,"y":34,"width":6,"height":6,"properties":{"metrics":[[{"expression":"(m3*(-1))+1","label":"ClusterIndexWritesBlocked-green","id":"e1","color":"#093"}],[{"expression":"m3*2","label":"ClusterIndexWritesBlocked-red","id":"e2","color":"#C00"}],["AWS/ES","ClusterIndexWritesBlocked","DomainName","dev","ClientId","731184136185",{"id":"m3","color":"#C00","visible":false}]],"view":"timeSeries","stacked":false,"region":"us-east-2","title":"Clusterwritesstatus","fill":"Below","period":60,"stat":"Maximum","yAxis":{"left":{"min":0,"max":2,"showUnits":false}},"legend":{"position":"hidden"}}},'
 deleted_documents='{"type": "metric","x": 12,"y": 34,"width": 6,"height": 6,"properties": {"view": "timeSeries","stacked": false,"metrics": [[ "AWS/ES", "DeletedDocuments", "DomainName", "dev", "ClientId", "731184136185" ]],"region": "us-east-2","title": "Deleted documents (Count)","period": 60,"stat": "Average","yAxis": {"left": {"showUnits": false}}}},'
 totalFreeStorageSpace='{"type":"metric","x":18,"y":34,"width":6,"height":6,"properties":{"metrics":[[{"expression":"FLOOR((m2+m3+m4+m5+m6+m7)*0.71/1024/1024)","label":"FreeStorageSpace","id":"e1"}],["AWS/ES","FreeStorageSpace","DomainName","dev","NodeId","8QVRkqbvQLakFxO4htJPHA","ClientId","731184136185",{"period":86400,"id":"m2","stat":"Sum","visible":false}],["...","LrodLvVYQBOXTgVlytQeKQ",".",".",{"period":86400,"id":"m3","stat":"Sum","visible":false}],["...","3lFUslTeTBqgE_-H8V_5jA",".",".",{"period":86400,"id":"m4","visible":false,"stat":"Sum"}],["...","Q9nZytBoSYGe7U-Gk2uuPA",".",".",{"period":86400,"id":"m5","visible":false,"stat":"Sum"}],["...","SukWxdKHQd2T8BYPAB_0DQ",".",".",{"period":86400,"id":"m6","visible":false,"stat":"Sum"}],["...","Kf3o4t7SRTet8wtawIVX7w",".",".",{"period":86400,"id":"m7","visible":false,"stat":"Sum"}]],"view":"timeSeries","stacked":false,"region":"us-east-2","title":"Totalfreestoragespace(GiB)","period":60,"stat":"Sum","yAxis":{"left":{"showUnits":false,"min":0,"label":"Gigabytes"},"right":{"showUnits":false,"label":""}},"liveData":false}},'
 max_jvm_mem='{"type":"metric","x":0,"y":41,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","JVMMemoryPressure","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2","title":"MaximumJVMmemorypressure(Percent)","period":60,"stat":"Maximum","yAxis":{"left":{"showUnits":false,"min":0,"max":100}}}},'
 max_cpu='{"type":"metric","x":6,"y":41,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","CPUUtilization","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2","title":"MaximumCPUutilization(Percent)","period":60,"stat":"Maximum","yAxis":{"left":{"showUnits":false,"min":0,"max":100}}}},'
 search_rate= '{"type":"metric","x":12,"y":41,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","SearchRate","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2","legend":{"position":"bottom"}}},'
 indexing_rate='{"type":"metric","x":18,"y":41,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","IndexingRate","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2"}},'
 search_latency='{"type":"metric","x":0,"y":48,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","SearchLatency","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2"}},'
 index_latency='{"type":"metric","x":6,"y":48,"width":6,"height":6,"properties":{"view":"timeSeries","stacked":false,"metrics":[["AWS/ES","IndexingLatency","DomainName","dev","ClientId","731184136185"]],"region":"us-east-2"}},'
 widget_es_all_cluster_health= cluster_status+deleted_documents+cluster_writes_status+totalFreeStorageSpace+max_jvm_mem+max_cpu+search_rate+indexing_rate+search_latency+index_latency

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_indices_doccount   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_indices_doccount=''
indices_doccount_metrics=''
if sort_indices_list:
 i=0
 while i < len(sort_indices_list) and i< complexity:
  indices_doccount_metrics += '["Custom metrics", "documents_count", "Index name","'+ sort_indices_list[i] +'",{"period":86400,"stat":"Average"'+indices_color_dict[sort_indices_list[i]]+'}],'
  i+=1
 indices_doccount_metrics=indices_doccount_metrics[:-1]
 widget_indices_doccount= '{"type":"metric","x":0,"y":55,"width":12,"height":6,"properties":{"metrics":['+indices_doccount_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Indices documents count"}},'

#   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   widget_indices_size   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
widget_indices_size=''
indices_size_metrics=''
if sort_indices_list:
 i=0
 while i < len(sort_indices_list) and i< complexity:
  indices_size_metrics += '["Custom metrics", "index_size", "Index name","'+ sort_indices_list[i] +'",{"period":86400,"stat":"Average"'+indices_color_dict[sort_indices_list[i]]+'}],'
  i+=1
 indices_size_metrics=indices_size_metrics[:-1]
 widget_indices_size= '{"type":"metric","x":12,"y":55,"width":12,"height":6,"properties":{"metrics":['+indices_size_metrics+'],"view":"timeSeries","stacked":false,"region":"us-east-2","legend":{"position":"right"},"title":"Indices size"}},'

#put DevOps-Dashboard to CloudWatch
DashboardBodyString= '{"widgets":['+widget_top_buckets_size+widget_top_buckets_count+widget_lambda_invocations+widget_text+widget_lambda_errors+widget_lambda_throttles+widget_lambda_ConcurrentExecutions+widget_lambda_duration_average+widget_lambda_duration_max+ widget_lambda_mem_average+widget_lambda_mem_max+ widget_es_all_cluster_health+widget_indices_doccount+widget_indices_size+']}'
if DashboardBodyString[-3]==",":
 DashboardBodyString=DashboardBodyString[:-3]+']}'

response = cloudwatch.put_dashboard(
   DashboardName = 'DevOps-Dashboard',
   DashboardBody = DashboardBodyString
)

