import pandas as pd
import os


logPath = "/home/jeff/recdb/python/Storj/StorjLogs"
timezone = 'America/Chicago'

#Build a list of the Nodes found in Log Folder
nodes = set([x[:x.find('_')] for x in os.listdir(logPath) if '.log' in x])

from logger import nodeLogData

try:
    nodeDF = pd.read_csv('outputs/nodeDF.csv',sep='|',index_col=0,parse_dates=True,infer_datetime_format=True)
    nodeDF.index = nodeDF.index.tz_localize('UTC')
    
except FileNotFoundError:
    for node in nodes:
        nodeData = nodeLogData(node,logPath)
        nodeData.decodeLines()
        try:
            nodeDF = nodeDF.append(nodeData.lines)
        except NameError:
            nodeDF = nodeData.lines
        nodeDF = nodeDF.sort_index()
        nodeDF.reset_index().drop_duplicates().to_csv('outputs/nodeDF.csv',index=False,sep='|')

for node in nodes:
    nodeData = nodeLogData(node,logPath,pd.to_datetime(nodeDF.index.max().tz_convert(timezone).date()))
    nodeData.decodeLines()
    nodeDF = nodeDF.append(nodeData.lines)
    nodeDF = nodeDF.sort_index()
    nodeDF.reset_index().drop_duplicates().to_csv('outputs/nodeDF.csv',index=False,sep='|')
