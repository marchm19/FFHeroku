import dash
import dash_table
import pandas as pd
import requests
import dash_core_components as dcc
import dash_html_components as html

rosters = {
  "Yovel":[1,'#EC7063'],
  "Marek":[2,'#EB984E'],
  "Derek":[3,'#5DADE2'],
  "Ethan":[4,'#A9CCE3'],
  "Max":[5,'#D2B4DE'],
  "Matt":[7,'#F7DC6F'],
  "Lukasz":[8,'#D5F5E3'],
  "Brian":[9,'#EBDEF0']
}
columns = ['Running Back', 'Wide Receiver', 'Tight End', 'Quarterback', 'Defense']

for key in rosters:
  teamData = requests.get("https://fantasy.nfl.com/league/6594386/team/"+str(rosters[key][0])).text
  teamList = teamData.split('playerCard">')[1::]
  playerList=[]
  for player in teamList:
      player=player[0:player.find("<")]
      playerList.append(player)
  rosters[key].append(playerList)

def checkInRoster(playerName,owner):
 for player in rosters[owner][2]:
     if playerName == player:
         return playerName
     else:
          return "Not in Roster"

df = pd.read_csv('FFPreseason.csv',header=2,usecols=[1,2,3,6,9,12,15])
df.dropna(axis=0,how='all',inplace=True)
dfdict = df.to_dict('records')
row=0
for d in dfdict:
    d['row_id']=row
    row+=1
rowWidths=[
    {'if':{'column_id':'Tier'},'width':'20px'},
    {'if':{'column_id':'Trade Value'},'width':'40px'},
    {'if':{'column_id':'Running Back'},'width':'80px'},
    {'if':{'column_id':'Wide Receiver'},'width':'80px'},
    {'if':{'column_id':'Tight End'},'width':'80px'},
    {'if':{'column_id':'Quarterback'},'width':'80px'},
    {'if':{'column_id':'Defense'},'width':'60px'},
]
conditions=[]
for key in rosters:
    for player in rosters[key][2]:
        for row  in dfdict:
            for column in columns:
                if row[column]==player:
                 conditions.append(
                 {
                     'if':{
                        'column_id':column,
                        'row_index':row['row_id']
                     },
                     'backgroundColor':rosters[key][1]
                 }
                 )

def convertToDict(playerList,owner):
    playerDictList=[]
    for player in playerList:
        playerDictList.append({owner:player})
    return playerDictList

def convertRostersTable():
    table = []
    for i in range(0,19):
        row={}
        for key in rosters:
            try:
                row[key]=rosters[key][2][i]
            except:
                row[key]=''
        table.append(row)
    return table

app = dash.Dash(__name__)
server=app.server

tradeTable = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    # data=df.to_dict('records'),
    data=dfdict,
    style_data_conditional=conditions,
    style_cell_conditional=rowWidths
    # fixed_rows={'headers':True,'data':0}
)
rostersColors=[]
for key in rosters:
    rostersColors.append(
                     {
                         'if':{
                            'column_id':key,
                         },
                         'backgroundColor':rosters[key][1]
                     }
                     )
tables=[tradeTable]
rosterTable = dash_table.DataTable(
    id='rosterTable'+key,
    columns=[{"name":key,"id":key} for key in rosters],
    data=convertRostersTable(),
    style_header_conditional=rostersColors
    # fixed_rows={'headers':True,'data':0}
)
tables.append(rosterTable)
app.layout = html.Div([tradeTable,html.H1(),rosterTable])



if __name__ == '__main__':
    app.run_server(debug=True)
