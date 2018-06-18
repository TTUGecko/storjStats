import pandas as pd
import numpy as np
import os
import ast

class nodeLogData():
    def __init__(self,nodeID,logPath,startDate=pd.to_datetime('1900-01-01')):
        self.nodeID = nodeID
        self.logPath = logPath
        self.startDate = startDate
        
    def pullLines(self):
        self.wantedLines = []
        for file in [x for x in os.listdir(self.logPath) if self.nodeID in x]: 
            if pd.to_datetime(file[file.find('_')+1:file.find('.')]) >= self.startDate:
                with open(self.logPath+'/'+file,'r') as logFile:
                    for line in logFile:
                        if line.find('hash') > -1:
                            self.wantedLines.append(line)
                        else:
                            continue
            else:
                continue
        return
    
    def decodeLines(self):
        #Check to see if wantedLines was already built, ifnot build it
        if not hasattr(self,'wantedLines'):
            self.pullLines()
        i = 0
        for dLine in [ast.literal_eval(x.strip("\n")) for x in self.wantedLines]:
            idx = pd.to_datetime(dLine['timestamp'], infer_datetime_format=True, utc=True)
            hashID, lineType, direction, size = self.lineReader(dLine['message'])
            d = {'hostNode':self.nodeID, 'hashID':hashID, 'activity':lineType, 'direction':direction, 'bytes':size}
            if i == 0:
                self.lines = pd.DataFrame(data=d, index=[idx])
            else:
                self.lines = self.lines.append(pd.DataFrame(data=d, index=[idx]))
            i += 1              
        return
    
    def lineReader(self,line):
        hashSize = lambda z: [x.strip() for x in line[z.find('hash')+5:].split('size')]
        if 'alloc request' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Alloc Request'
            direction = 'Message'
        elif 'alloc response' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Alloc Response'
            direction = 'Message'
        elif 'mirror request' in line.lower():
            hashID = hashSize(line)
            size = np.nan
            lineType = 'Mirror Request'
            direction = 'Message'  
        elif 'mirrored' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Mirror Shard'
            direction = 'Download'
        elif 'shard upload' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Host Shard'
            direction = 'Download'
        elif 'storage retrieve' in line.lower():
            hashID = hashSize(line)
            size = np.nan
            lineType = 'Request Shard'
            direction = 'Message'
        elif 'mirror download complete' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Mirror Upload'
            direction = 'Upload'
        elif 'shard download completed' in line.lower():
            hashID, size = hashSize(line)
            size = np.int(size)
            lineType = 'Shard Upload'
            direction = 'Upload'          
        return hashID, lineType, direction, size
            
    
    
