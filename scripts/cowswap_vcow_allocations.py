# -*- coding: utf-8 -*-
"""cowswap-vcow-allocations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JRTOpBw6h7g7VK-tggM4JvOQpGHOWKm9
"""

import io
import requests
import pandas as pd
import numpy as np
import math
import time
import random

url = "https://raw.githubusercontent.com/starwalker00/cowswap-airdrop-data/main/data/vCoW_Allocations(Updated28_01_22).csv"
fullRes=requests.get(url).content
print(fullRes[:10])

#Account,Airdrop,GnoOption,UserOption,Claiming on:
#df=pd.read_csv(io.StringIO(fullRes.decode('utf-8')),dtype={'Account': np.str,'Airdrop': np.float, 'GnoOption': np.float, 'UserOption': np.float, 'Claiming on': np.str})
df=pd.read_csv(io.StringIO(fullRes.decode('utf-8')))
pd.set_option('display.max_columns', None)
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.info())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.head())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.describe())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
# drop airdrop of no value
indexAddresses = df[ (df['Airdrop'] <= 0.1) ].index
df.drop(indexAddresses , inplace=True)
# drop GnoOption and UserOption columns
df = df.drop(df.columns[[2,3]], axis=1)
# round airdrop value
df['Airdrop'] = df['Airdrop'].apply(np.floor)
df['Airdrop'] = df['Airdrop'].astype(np.int64)
# prepare new column
df.insert(3, 'user_total_usd_value', 0)
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.info())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.head())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.describe())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")

#https://openapi.debank.com/docs
#
filepath='drive/MyDrive/TMP/cowswap-airdrop-metrics-updated20220128_tmp.csv'
df=pd.read_csv(filepath)
print(df.info())

verbose = False
print_ind = True
nb_row = len(df.index)
print(nb_row)
nb_rows_between_sleep = 750
max_row = 10000000000
#for ind in df.index:
for ind in range(46498, nb_row):
  print("-------------------------------")
  print(ind,"/",nb_row) if print_ind == True else 0
  time.sleep(0.2)
  if ind == max_row:
    break
  elif (ind != 0 ) & (ind % nb_rows_between_sleep == 0):
    sleep_time_between_batch_of_calls = random.randrange(2, 10, 2)
    print("sleep ",sleep_time_between_batch_of_calls)
    filepath='drive/MyDrive/TMP/cowswap-airdrop-metrics-updated20220128_tmp.csv'
    df.to_csv(filepath)
    print("saved")
    time.sleep(sleep_time_between_batch_of_calls)
  print(ind, df['Account'][ind], df['Airdrop'][ind]) if verbose == True else 0
  request_url = "https://openapi.debank.com/v1/user/total_balance?id=" + str(df['Account'][ind])
  print(request_url) if verbose == True else 0
  result = requests.get(request_url, headers={"accept":"application/json"})
  print(result.status_code) #if verbose == True else 0
  try:
    result_json = result.json()
    print(result_json) if verbose == True else 0
    user_total_usd_value=result_json['total_usd_value']
    print(user_total_usd_value) if verbose == True else 0
    user_total_usd_value = math.floor(user_total_usd_value)
    print(user_total_usd_value) #if verbose == True else 0
    #df['user_total_usd_value'][ind] = user_total_usd_value
    df.at[ind, 'user_total_usd_value'] = user_total_usd_value
  except:
    print("An exception occurred")

filepath='drive/MyDrive/TMP/cowswap-airdrop-metrics-updated20220128_finished.csv'
df.to_csv(filepath)
print("saved finished")

print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.info())
print("-----------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------")
print(df.head())

print(df.head())
df.drop(df.columns[0], axis=1, inplace=True)
print(df.head())

pd.set_option('display.max_columns', None)
print(df.head())

### REINDEX
df = df.reindex(columns=["Account", "ClaimingOn", "user_total_usd_value", "Airdrop"])
print(df.head())

### SAVE
filepath='drive/MyDrive/TMP/cowswap-airdrop-metrics-updated20220128_final.csv'
df.to_csv(filepath)

### READ
filepath='drive/MyDrive/TMP/cowswap-airdrop-metrics-updated20220128_final.csv'
df_read = pd.read_csv(filepath,index_col=[0])

#df_read['user_total_usd_value']=df_read['user_total_usd_value']/1000 #convert to k$
print(df_read.info())
print(df_read.head())
print(df_read.describe())

## PLOT

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from matplotlib.ticker import *
from matplotlib.scale import *
from matplotlib.font_manager import FontProperties

print(df_read.describe())

font = FontProperties()
#font.set_family('serif')
font.set_size(14)
#font.set_name('Times New Roman')
#font.set_style('italic')
font.set_weight('bold')

#plot
fig, axs = plt.subplots(figsize=(20, 10))
axs.set_title('vCow airdropped amount by user total balance', fontproperties=font)
#df_read.plot.scatter(ax=axs, x='user_total_usd_value',y='Airdrop', alpha=0.5, c=df_read['ClaimingOn'])
df_read.plot.scatter(ax=axs, x='user_total_usd_value',y='Airdrop',c=df_read['ClaimingOn'].apply(lambda val: "Red" if val == "Ethereum Mainnet" else "Darkblue"))
#add legend mainnet/gnosis
red_patch = mpatches.Patch(color='Red', label='Ethereum Mainnet')
darkblue_patch = mpatches.Patch(color='Darkblue', label='Gnosis Chain')
axs.legend(handles=[red_patch, darkblue_patch])
#plt.figtext(0.5, 0.01, "data gathered from github.com/gnosis/cow-token-allocation and openapi.debank.com", ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
plt.figtext(0.5, 0.04, "data gathered from github.com/gnosis/cow-token-allocation and openapi.debank.com on January 30, 2022  ", ha="center", fontsize=10)
#fig.patch.set_facecolor('black')
#fig.patch.set_alpha(0.1)
#axs.patch.set_facecolor('white')
#axs.patch.set_alpha(1)
#axes labels
axs.set_xlabel("User balance \n", fontproperties=font)
axs.set_ylabel("vCow airdropped amount", fontproperties=font)
#axes x scale
axs.set_xlim(left=0)
axs.set_xscale('symlog')
positions = [10, 100, 1000, 1e4, 1e5, 1e6, 1e7, 1e8]
labels = ['10 $', '100 $', '1 000 $', '10 000 $', '100 000 $', '1 000 000 $', '10 000 000 $', '100 000 000 $']
axs.xaxis.set_major_locator(FixedLocator(positions))
axs.xaxis.set_major_formatter(FixedFormatter(labels))
#axes y scale
axs.set_ylim(bottom=2)
axs.set_yscale('symlog')
positions = [10, 100, 1000, 1e4, 1e5, 1e6, 1e7, 1e8]
labels = ['10', '100', '1 000', '10 000', '100 000', '1 000 000', '10 000 000', '100 000 000']
axs.yaxis.set_major_locator(FixedLocator(positions))
axs.yaxis.set_major_formatter(FixedFormatter(labels))

#fig.savefig("drive/MyDrive/TMP/cowswap-airdrop-metrics.jpg",facecolor='white', transparent=False)
fig.savefig("drive/MyDrive/TMP/cowswap-airdrop-metrics.jpg",transparent=False)

## HIST
#plt.plot.hist(df_read['user_total_usd_value'])
fig, axs = plt.subplots(figsize=(20, 10))
n_bins = 20
axs.hist(df_read['user_total_usd_value'], bins=n_bins)

## CHECKS
pd.set_option('display.max_columns', None)
#subset_df = df_read[df_read["user_total_usd_value"] > 100e7]
subset_df = df_read[df_read["user_total_usd_value"] < 100]
column_count = subset_df.count()
print(column_count)
print(subset_df)
print(subset_df.describe())