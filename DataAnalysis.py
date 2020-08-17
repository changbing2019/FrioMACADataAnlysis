# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 20:56:22 2020

@author: cyang
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, glob
import seaborn as sns
#sns.set(style="darkgrid")


class Macadata:
    
    def __init__(self,basin,filepath,zone,rcp,iplot): #,monthlyP,monthlyT,dailyP,dailyT):
        self.basin=basin
        self.filepath=filepath
        self.zone=zone
        self.rcp=rcp
        self.iplot=iplot
        self.monthlyP=pd.DataFrame()
        self.monthlyT=pd.DataFrame()
        self.dailyP=pd.DataFrame()
        self.dailyT=pd.DataFrame()



    def obtain_dailydata(self):  #,basin,rcp,filepath,zone,iplot):

         pathnew=os.path.join(self.filepath,'dataT')
         self.dailyT=self.Concate_dailydata(pathnew) #,self.basin,rcp=self.rcp,zone=self.zone) #pathnew,basin=self.basin,rcp=self.rcp,zone=self.zone)  ## daily data

         pathnew=os.path.join(self.filepath,'dataPre')
         self.dailyP=self.Concate_dailydata(pathnew) #,basin=self.basin,rcp=self.rcp,zone=self.zone)  ## daily data
         
        # return dailyP, dailyT 

         

    def read_dailydata(self,fileb,zone='Recharge'):
   # print('In reading_data_rch ',zone)
   # print(fileb)
        data=pd.read_csv(fileb)
        data['Datetime']=pd.to_datetime(data['Datetime'])
        data=data.set_index('Datetime')
        rechColname=[col for col in data.columns if zone in col]
        newrechColname=[col.split('_')[2] for col in rechColname]
        df=data[rechColname]
        df.columns=newrechColname
        
        return df
    

    def Concate_dailydata(self,filepath):  #,filepath,basin,rcp,zone='Recharge'):
        
        os.chdir(filepath)
        csvftemp=glob.glob('*.csv')   
    #    print('in reading_concating_data ',zone)
        for file in csvftemp:
            if (self.basin in file) and ('hist' in file):
                histfile=os.path.join(filepath,file)
            if (self.basin in file) and (self.rcp in file):
                rcpfile=os.path.join(filepath,file)
        
        histdf=self.read_dailydata(histfile,self.zone)
        projdf=self.read_dailydata(rcpfile,self.zone)
        
        dailydf=pd.concat([histdf,projdf],axis=0)
        
        
        return dailydf
   

    
    def obtain_monthlyData(self): #,basin,rcp,filepath,iplot,zone):
        

         self.obtain_dailydata()

         self.monthlyT=self.dailyT.resample('M').mean()-273.15   ## monthly mean and convert to oC

         self.monthlyP=self.dailyP.resample('M').sum()             ## monthly precipitation 

         if self.iplot is True:   
            self.drawplot_raw()    
            
        
    
    def drawplot_raw(self): # ,monthlyP, monthlyT):
        
           self.monthlyP.plot(figsize=(15,15))
           self.monthlyT.plot(figsize=(15,15))
           plt.subplots(figsize=(15,12))
           sns.heatmap(self.monthlyT.corr())
           plt.subplots(figsize=(15,12))
           sns.heatmap(self.monthlyP.corr())
        
    def processseason(self,predf,period):
            df=predf.groupby(['year','season']).sum().groupby('season').mean()
            
            df=df.drop('month',axis=1)
            df=df.T
            df.columns=['Winter','Spring','Summer','Fall']
            df['period']=period
            return df


    def processmacapre(self):
    
        pre_rch_month=self.monthlyP.copy()
        pre_rch_month['year']=pre_rch_month.index.year
        pre_rch_month['month']=pre_rch_month.index.month
        pre_rch_month['season']=(pre_rch_month.index.month%12 + 3)//3
        pre19501970=pre_rch_month.loc['1950-01-01':'1970-12-31']
        pre19502005=pre_rch_month.loc['1950-01-01':'2005-12-31']
        pre19712000=pre_rch_month.loc['1971-01-01':'2000-12-31']
        pre20012009=pre_rch_month.loc['2001-01-01':'2009-12-31']
        pre20102039=pre_rch_month.loc['2010-01-01':'2039-12-31']
        pre20402069=pre_rch_month.loc['2040-01-01':'2069-12-31']
        pre20702099=pre_rch_month.loc['2070-01-01':'2099-12-31']
        
        macamodels=['bcc-csm1-1-m', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CNRM-CM5',
               'CSIRO-Mk3-6-0', 'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-CC365',
               'HadGEM2-ES365', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR',
               'IPSL-CM5B-LR', 'MIROC-ESM-CHEM', 'MIROC-ESM', 'MIROC5', 'MRI-CGCM3',
               'NorESM1-M','year']
        
        annulmean19712000=pre19712000[macamodels].groupby('year').sum().mean()
        annulmean19502005=pre19502005[macamodels].groupby('year').sum().mean()
        annulmean20102039=pre20102039[macamodels].groupby('year').sum().mean()
        annulmean20402069=pre20402069[macamodels].groupby('year').sum().mean()
        annulmean20702099=pre20702099[macamodels].groupby('year').sum().mean()
        
        anualmean=pd.concat([annulmean19712000,annulmean19502005,annulmean20102039,annulmean20402069,annulmean20702099],axis=1)
        anualmean.columns=['1971-2000','1950-2005','2010-2039','2040-2069','2070-2099']
        
        seasonmean19712000=self.processseason(pre19712000,'1971-2000')
        seasonmean19502005=self.processseason(pre19502005,'1950-2005')
        seasonmean20102039=self.processseason(pre20102039,'2010-2039')
        seasonmean20402069=self.processseason(pre20402069,'2040-2069')
        seasonmean20702099=self.processseason(pre20702099,'2070-2099')
        
        seasonmean=pd.concat([seasonmean19712000,seasonmean19502005,seasonmean20102039,seasonmean20402069,seasonmean20702099],axis=0)

        return anualmean,seasonmean   # convert to inches

    def processseasonTempr(self,tdf,period):
            df=tdf.groupby(['year','season']).mean().groupby('season').mean()
            
            df=df.drop('month',axis=1)
            df=df.T
            df.columns=['Winter','Spring','Summer','Fall']
            df['period']=period
            return df
    
    
    def processmacaTempr(self):
    
        t_rch_month=self.monthlyT.copy()
        t_rch_month['year']=t_rch_month.index.year
        t_rch_month['month']=t_rch_month.index.month
        t_rch_month['season']=(t_rch_month.index.month%12 + 3)//3
        t19501970=t_rch_month.loc['1950-01-01':'1970-12-31']
        t19502005=t_rch_month.loc['1950-01-01':'2005-12-31']
        t19712000=t_rch_month.loc['1971-01-01':'2000-12-31']
        t20012009=t_rch_month.loc['2001-01-01':'2009-12-31']
        t20102039=t_rch_month.loc['2010-01-01':'2039-12-31']
        t20402069=t_rch_month.loc['2040-01-01':'2069-12-31']
        t20702099=t_rch_month.loc['2070-01-01':'2099-12-31']
        
        macamodels=['bcc-csm1-1-m', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CNRM-CM5',
               'CSIRO-Mk3-6-0', 'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-CC365',
               'HadGEM2-ES365', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR',
               'IPSL-CM5B-LR', 'MIROC-ESM-CHEM', 'MIROC-ESM', 'MIROC5', 'MRI-CGCM3',
               'NorESM1-M','year']
        
        annulmean19712000=t19712000[macamodels].groupby('year').mean().mean()
        annulmean19502005=t19502005[macamodels].groupby('year').mean().mean()
        annulmean20102039=t20102039[macamodels].groupby('year').mean().mean()
        annulmean20402069=t20402069[macamodels].groupby('year').mean().mean()
        annulmean20702099=t20702099[macamodels].groupby('year').mean().mean()
        
        anualmean=pd.concat([annulmean19712000,annulmean19502005,annulmean20102039,annulmean20402069,annulmean20702099],axis=1)
        anualmean.columns=['1971-2000','1950-2005','2010-2039','2040-2069','2070-2099']
        
        
        seasonmean19712000=self.processseasonTempr(t19712000,'1971-2000')
        seasonmean19502005=self.processseasonTempr(t19502005,'1950-2005')
        seasonmean20102039=self.processseasonTempr(t20102039,'2010-2039')
        seasonmean20402069=self.processseasonTempr(t20402069,'2040-2069')
        seasonmean20702099=self.processseasonTempr(t20702099,'2070-2099')
        
        seasonmean=pd.concat([seasonmean19712000,seasonmean19502005,seasonmean20102039,seasonmean20402069,seasonmean20702099],axis=0)
        #seasonmean.columns=['1971-2000','2010-2039','2040-2069','2070-2099']
       # seasonmean
        return anualmean,seasonmean   # convert to inches

    def plotPT(self,ntot=3,istart=0,p=True,ylabel='Monthly Precipitation (inch)'):
        
         
        
         if p:
             df=self.monthlyP.copy()
         else:
             df=self.monthlyT.copy()
             
         fig,ax=plt.subplots(ntot,2,figsize=(15,15))
         
         for  i in range(ntot):
                col1=df.columns[(i+istart)*2]
                col2=df.columns[(i+istart)*2+1]
                print(col1,col2)
                df1=df[col1]   # convert to inches
                df2=df[col2]
    
                if p:
                    df1=df1*0.0393701   # convert to inches
                    df2=df2*0.0393701
                
                df1.loc['1950-01-01':'1970-12-31'].plot(ax=ax[i,0],linestyle='-',color='b',label='1950-1970')
                df1.loc['1971-01-01':'2000-12-31'].plot(ax=ax[i,0],linestyle='-',color='k',label='1971-2000')
                df1.loc['2001-01-01':'2009-12-31'].plot(ax=ax[i,0],linestyle='-',color='grey',label='2001-2009')
                df1.loc['2010-01-01':'2039-12-31'].plot(ax=ax[i,0],linestyle='-',color='r',label='2010-2039')
                df1.loc['2040-01-01':'2069-12-31'].plot(ax=ax[i,0],linestyle='-',color='y',label='2040-2069')
                df1.loc['2070-01-01':'2099-12-31'].plot(ax=ax[i,0],linestyle='-',color='g',label='2070-2099')    
                ax[i,0].set_title(col1)
               # ax[i,0].plot(df1.index,df1.loc[:,'gradientboost'],label='Gradient boost')
              #  ax[i,0].set_yscale('log')
                ax[i,0].set_ylabel(ylabel)
                ax[i,0].legend(loc="best")
            
                df2.loc['1950-01-01':'1970-12-31'].plot(ax=ax[i,1],linestyle='-',color='b',label='1950-1970')
                df2.loc['1971-01-01':'2000-12-31'].plot(ax=ax[i,1],linestyle='-',color='k',label='1971-2000')
                df2.loc['2001-01-01':'2009-12-31'].plot(ax=ax[i,1],linestyle='-',color='grey',label='2001-2009')
                df2.loc['2010-01-01':'2039-12-31'].plot(ax=ax[i,1],linestyle='-',color='r',label='2010-2039')
                df2.loc['2040-01-01':'2069-12-31'].plot(ax=ax[i,1],linestyle='-',color='y',label='2040-2069')
                df2.loc['2070-01-01':'2099-12-31'].plot(ax=ax[i,1],linestyle='-',color='g',label='2070-2099')    
         #       ax[i,1].plot(df2.index,df2.loc[:,'gradientboost'],label='Gradient boost')
                ax[i,1].legend(loc="best")
                ax[i,1].set_title(col2)
                ax[i,1].set_ylabel(ylabel)
    
