import numpy as np
import pandas as pd
import itertools
nbinitialscenario=10
nbfinalscenario=7
demand=pd.read_csv('/content/Simulation_D32.csv')

#####distance between each scenario
demand_transposed = demand.T
demand_transposed.insert(loc=0, column="row", value=demand_transposed.reset_index().index+1)
#####probability of each scenario
for i in range(nbinitialscenario):
  demand_transposed['count']=demand_transposed.iloc[:,0:11].count(axis=1)

demand_transposed['probability']=(1/demand_transposed['count'])

#####loooop
for k in range(nbfinalscenario):
  dis= pd.DataFrame(columns = ['i', 'j', 'd_ij'])
  for i, j in itertools.combinations(demand_transposed.index, 2):
      d_ij = np.linalg.norm(demand_transposed.loc[i] - demand_transposed.loc[j])
    
      dis=dis.append({'i':i,'j':j,'d_ij':d_ij},ignore_index=True)
      dis=dis.append({'i':j,'j':i,'d_ij':d_ij},ignore_index=True)

  ####min distance and remove dup
  dfc = dis.groupby('i')['d_ij']
  dis['min' ] = dfc.transform('min')
  j=dis[['d_ij','j']]
  j.rename(columns = {'d_ij':'min'}, inplace = True)
  dis=dis.merge(j,  on='min' ,  how ='inner')
  dis=dis.drop_duplicates(subset=['i', 'min','j_y'])
  #print(dis)
  index_names = dis[ (dis['i'] == dis['j_y'])].index
  dis.drop(index_names, inplace = True)

  ###i,j_y,min(tarkib min dis)

  




  dis.insert(loc=0, column="row", value=dis.reset_index().index+1)
  

  dis=dis.merge(demand_transposed,  on='row' ,  how ='inner')
  new_order = [0,1,4,5,19]
  dis=dis[dis.columns[new_order]]

  dis['total'] = dis['min'] * dis['probability']

  dis=dis.sort_values(['total'], ascending=True)
  f=dis.sort_values(['total'], ascending=True).head(1)

  print(f)
  print(dis)

  dis['probability'][dis['i'] == f['j_y'].iloc[0]]=f['probability'].iloc[0]+dis['probability'][dis['i'] == f['j_y'].iloc[0]]
  demand_transposed['probability'][demand_transposed.index == f['j_y'].iloc[0]]=f['probability'].iloc[0]+demand_transposed['probability'][demand_transposed.index]
  #hazf scenario az dis*p
  cond = dis['i'].isin(f['i'])
  dis.drop(dis[cond].index, inplace = True)
  print('diss',dis)

  #hazf scenario az demand avali
  conddemand = demand_transposed.index.isin(f['i'])
  demand_transposed.drop(demand_transposed[conddemand].index, inplace = True)
  dis=dis.drop(['row', 'i','min','j_y','probability','total'], axis=1, inplace=True)
  print('dell',dis)
  nbfinalscenario=nbfinalscenario-1

#print('demt',demand_transposed)