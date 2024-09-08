# -*- coding: utf-8 -*-

'''
pip install tvdatafeed
pip install ta
pip install pandas


'''
from fyers_api import accessToken
from fyers_api import fyersModel
import pandas_ta as ta
#help(ta.psar)
import math
import time
import threading
import pandas as pd
#import ta
from datetime import datetime, timedelta
import config
import json
'''
with open('accessJSON.json') as files:
    acc = json.load(files)
    access_token=acc['access_token']
'''
access_token = config.access_token

client_id = config.client_id                                        
secret_key = config.secret_key   
date_today = datetime.now().strftime('%Y-%m-%d')
#print(date_today)                                
#open(f'{date_today}.txt','w')
     
fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=client_id,log_path="")



#symbols = ['AARTIIND', 'ABBOTINDIA', 'ABCAPITAL', 'ABFRL', 'ALKEM', 'AMARAJABAT', 'APOLLOHOSP', 'APOLLOTYRE', 'ASHOKLEY', 'ASTRAL', 'ATUL', 'AUROPHARMA', 'AXISBANK', 'BAJAJFINSV', 'BAJFINANCE', 'ACC', 'ADANIENT', 'BALRAMCHIN', 'BANDHANBNK', 'BATAINDIA', 'AMBUJACEM', 'BEL', 'BERGEPAINT', 'BHARTIARTL', 'BHEL', 'BIOCON', 'BOSCHLTD', 'BPCL', 'BSOFT', 'CANBK', 'CANFINHOME', 'CHOLAFIN', 'AUBANK', 'CIPLA', 'COFORGE', 'BAJAJ_AUTO', 'COLPAL', 'CONCOR', 'COROMANDEL', 'DEEPAKNTR', 'DIVISLAB', 'DLF', 'DRREDDY', 'BHARATFORG', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK', 'FSL', 'BRITANNIA', 'GAIL', 'GLENMARK', 'GMRINFRA', 'GNFC', 'GODREJPROP', 'GRANULES', 'GUJGASLTD', 'HAL', 'HCLTECH', 'HDFC', 'HDFCAMC', 'COALINDIA', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDPETRO', 'HINDUNILVR', 'HONAUT', 'ICICIBANK', 'IDFCFIRSTB', 'IEX', 'INDHOTEL', 'INDIACEM', 'INDIAMART', 'INDUSINDBK', 'INDUSTOWER', 'INFY', 'INTELLECT', 'IPCALAB', 'IRCTC', 'ITC', 'JINDALSTEL', 'JUBLFOOD', 'KOTAKBANK', 'L_TFH', 'LALPATHLAB', 'LAURUSLABS', 'LICHSGFIN', 'LT', 'LTI', 'LTTS', 'LUPIN', 'M_M', 'MANAPPURAM', 'MARICO', 'MARUTI', 'MCDOWELL_N', 'MFSL', 'MGL', 'MINDTREE', 'MPHASIS', 'MRF', 'MUTHOOTFIN','NAUKRI', 'NAVINFLUOR', 'NTPC', 'OFSS', 'IOC', 'ONGC', 'PAGEIND', 'PEL', 'PERSISTENT', 'PETRONET', 'PFC', 'PIDILITIND', 'PIIND', 'POWERGRID', 'PVR', 'RAIN', 'RECLTD', 'SBICARD', 'SBILIFE', 'SHREECEM', 'SIEMENS', 'SRF', 'SUNTV', 'TATACOMM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TVSMOTOR', 'UPL', 'M_MFIN', 'WHIRLPOOL', 'ABB', 'WIPRO', 'ZEEL', 'METROPOLIS', 'NESTLEIND', 'ADANIPORTS', 'BANKBARODA', 'RELIANCE', 'CHAMBLFERT', 'CROMPTON', 'CUB', 'CUMMINSIND', 'DABUR', 'DALBHARAT', 'DELTACORP', 'DIXON', 'TATACHEM', 'TCS', 'GODREJCP', 'GRASIM', 'HAVELLS', 'ASIANPAINT', 'HINDALCO', 'HINDCOPPER', 'IBULHSGFIN', 'ICICIGI', 'IDFC', 'IGL', 'INDIGO', 'JKCEMENT', 'JSWSTEEL', 'MCX', 'MOTHERSON', 'NATIONALUM', 'OBEROIRLTY', 'PNB', 'POLYCAB', 'RAMCOCEM', 'RBLBANK', 'SAIL', 'SRTRANSFIN', 'SUNPHARMA', 'SYNGENE', 'TITAN', 'UBL', 'ICICIPRULI', 'ULTRACEMCO', 'VOLTAS', 'ZYDUSLIFE', 'SBIN', 'EICHERMOT', 'BALKRISIND', 'GSPL', 'IDEA', 'NMDC', 'VEDL']




#candle1 = '30min'
#candle2 = '45min'
#candle3 = '60min'


signalha = {}

def data_download(symbol,gui,candle1,candle2,candle3,dayys=5):
    i=0
    try:
        if symbol not in signalha:
            signalha[symbol]= 'None'
                                
        candle1_signal = 4
        candle2_signal = 5
        candle3_signal = 5
        today  = datetime.now().strftime("%Y-%m-%d") 
        tod = datetime.now()
        yest = tod-timedelta(days=int(dayys))
        start = yest.strftime("%Y-%m-%d")
        symbol2 = f'NSE:{symbol}-EQ'
        data = {"symbol":symbol2,"resolution":"1","date_format":"1","range_from":start,"range_to":today,"cont_flag":"1"}
        candl_data=fyers.history(data)['candles']
        df = pd.DataFrame(candl_data,columns=['datetime','open','high','low','close','volume'])
        df['datetime'] = pd.to_datetime(df['datetime'],unit='s')
        df['datetime']=df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
        df['datetime']=df['datetime'].dt.tz_localize(None)
        df = df.set_index('datetime')
        first_df = df.copy()
        second_df = df.copy()
        third_df = df.copy()

        ohlc_dict = {
        'open':'first',
        'high':'max',
        'low':'min',
        'close':'last',
        'volume':'sum'
        }

        first_df = first_df.resample(candle1).agg(ohlc_dict)
        first_df = first_df.dropna()
        firstpsar =ta.trend.psar(high=first_df['high'], low=first_df['low'], close=first_df['close'], tv=True)
        
        first_df['long']=firstpsar['PSARl_0.02_0.2']
        first_df['short']= firstpsar['PSARs_0.02_0.2']
        first_df['reversal'] = firstpsar['PSARr_0.02_0.2']
       
        if candle2 !='None':
            second_df = second_df.resample(candle2).agg(ohlc_dict)
            second_df = second_df.dropna()
            secondpsar =ta.trend.psar(high=second_df['high'], low=second_df['low'], close=second_df['close'], tv=True)
            second_df['long']= secondpsar['PSARl_0.02_0.2']
            second_df['short']= secondpsar['PSARs_0.02_0.2']
            second_df['reversal'] = secondpsar['PSARr_0.02_0.2']
            
        
        if candle3 !='None':
            third_df = third_df.resample(candle3).agg(ohlc_dict)
            third_df = third_df.dropna()
            thirdpsar =ta.trend.psar(high=third_df['high'], low=third_df['low'], close=third_df['close'], tv=True)
            third_df['long']= thirdpsar['PSARl_0.02_0.2']
            third_df['short']= thirdpsar['PSARs_0.02_0.2']
            third_df['reversal'] = thirdpsar['PSARr_0.02_0.2']

        if candle3 !='None':
            if math.isnan(third_df['long'][-1]) ==True and third_df['reversal'][-1] == 1:
              
                first_df_filt = first_df[first_df.index >= third_df.index[-1]]
                first_df_signal = first_df_filt[first_df_filt['reversal']==1]
                second_df_filt = second_df[second_df.index >= third_df.index[-1]]
                second_df_signal = second_df_filt[second_df_filt['reversal']==1]
                
                if len(first_df_signal) >=1 and len(second_df_signal) >=1:
                    if (math.isnan(first_df_signal['long'][-1]) ==True and first_df_signal['reversal'][-1] == 1) and (math.isnan(second_df_signal['long'][-1]) ==True and second_df_signal['reversal'][-1] == 1):
                        if signalha[symbol] !='bearish3':
                            signalha[symbol] = 'bearish3'
                            gui.signals.insertItem(-1,f'Bearish Signal On: {symbol}')
                            print('its a bearish reversal on symbol:',symbol)

            elif math.isnan(third_df['long'][-1]) != True and third_df['reversal'][-1] == 1:
                
                first_df_filt = first_df[first_df.index >= third_df.index[-1]]
                first_df_signal = first_df_filt[first_df_filt['reversal']==1]
                second_df_filt = second_df[second_df.index >= third_df.index[-1]]
                second_df_signal = second_df_filt[second_df_filt['reversal']==1]
                if len(first_df_signal) >=1 and len(second_df_signal) >=1:
                    if (math.isnan(first_df_signal['long'][-1]) !=True and first_df_signal['reversal'][-1] == 1) and (math.isnan(second_df_signal['long'][-1]) !=True and second_df_signal['reversal'][-1] == 1):
                        if signalha[symbol] != 'bullish3':
                            signalha[symbol] = 'bullish3'
                            gui.signals.insertItem(-1,f'Bullish Signal On: {symbol}')
                            print('its a bullish reversal on:',symbol)
    except:
        pass
        
def run_once(symbols,gui,candle1,candle2,candle3,days):
    threads = []
    for symbol in symbols:
        print(symbol)
        p=threading.Thread(target=data_download, args=[symbol,gui,candle1,candle2,candle3,days])
        p.start()
        threads.append(p)
        time.sleep(0.1)

    for thread in threads:
        thread.join()
   

#run_script(symbols,candle1,candle2,candle3)

   
def run_multiple(symbols,gui,candle1,candle2,candle3,days):
    threads = []
    while True:
        for symbol in symbols:
            p=threading.Thread(target=data_download, args=[symbol,gui,candle1,candle2,candle3,days])
            p.start()
            threads.append(p)
            time.sleep(0.1)

        for thread in threads:
            thread.join()
        time.sleep(100)
