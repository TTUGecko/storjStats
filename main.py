'''
    This is the main file that runs the storjStats program
    Copyright (C) 2018  Jeff Tweed / jtweeder@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see http://www.gnu.org/licenses/.
'''



import pandas as pd
import os


logPath = "***Replace with the fully qualified path to Storj Logs***"
timezone = "***Replace with local timezone***"
installDir = "**Fully qualified path to the directory where you insall storjStats**" #Ex: "/home/<user>/storjStats"

'''
Sample Acceptable Timezones example:
'America/Chicago'
See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for a full listing of acceptable timezones.
Accepts timezones from the Olson timezone database
'''

#Build a list of the Nodes found in Log Folder
nodes = set([x[:x.find('_')] for x in os.listdir(logPath) if '.log' in x])

from logger import nodeLogData

try:
    nodeDF = pd.read_csv(installDir + '/outputs/nodeDF.csv',sep='|',index_col=0,parse_dates=True,infer_datetime_format=True)
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
        nodeDF.reset_index().drop_duplicates().to_csv(installDir + '/outputs/nodeDF.csv',index=False,sep='|')

for node in nodes:
    nodeData = nodeLogData(node,logPath,pd.to_datetime(nodeDF.index.max().tz_convert(timezone).date()))
    nodeData.decodeLines()
    nodeDF = nodeDF.append(nodeData.lines)
    nodeDF = nodeDF.sort_index()
    nodeDF.reset_index().drop_duplicates().to_csv(installDir + '/outputs/nodeDF.csv',index=False,sep='|')
