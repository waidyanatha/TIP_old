#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from numpy import isin


try:
    # from distutils import filelist
    # from tkinter import NS
    # from turtle import pd

    import numpy as np
    from datetime import datetime, timedelta, date
    import pandas as pd
    import traceback

    print("All packages loaded successfully!")

except Exception as e:
    print("Some packages didn't load\n{}".format(e))

'''
    CLASS with essential data extract, load, and transform processes:
        1) read and save batches of data from coindex API
        2) load data from files into a dataframe and transform into a cross tab table
        3) 
'''

class ExtractLoadTransform():

    # import datetime as dt

    ''' Function
            name: __init__
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
    def __init__(self,
                # dataPath, # : str = np.nan, # default path ="../data/market_cap/"
                # start_date, #: date = np.nan,
                # end_date,   # : date = np.nan,
                ):
        
        # import datetime
        # import pandas as pd

        self.data = pd.DataFrame()
        # self.start_date = start_date.date()
        # self.end_date = end_date.date()
        self.start_date = np.nan
        self.end_date = np.nan
        self.path = np.nan
        self.filelist = np.nan

        # if dataPath:
        #     self.path = dataPath     # path = "../data/market_cap_2021-01-01_2022-06-01/"
        #     self.filelist = self.get_file_list(self.path)
        #     self.data = self.load_data()
        #     self.data['Date'] = pd.to_datetime(self.data['Date']).dt.date
        # else:
        #     self.path = np.nan
        #     self.filelist = np.nan

        # if self.data.shape[0] > 0:
        #     if isinstance(start_date,date) and isinstance(end_date,date):
        #         self.start_date = start_date
        #         self.end_date = end_date
        #         self.data = self.fillter_by_date(self.data,self.start_date,self.end_date)
        self.win_start_dt = ''
        self.win_end_dt = ''
        self.roll_win_len = 7   # rolling window length; e.g., for calculating simple moving average
        self.min_roll_win_len = 7
        self.roll_calc_ops_dict = {} # key:val pair of rolling operations: mean, std, sum, adx and column name
        self.roll_calc_op_types=['simp_move_avg',   # simple moving average
                                'simp_move_std',    # simple moving standard deviation
                                'simp_move_sum',    # simple moving sum
                                'simp_cum_prod',    # simple cummalative product
                                ]

        if self.data.shape[0] > 0:
            # self.win_start_dt = (self.data.Date.min()).date()
            # self.win_end_dt = (self.data.Date.max()).date()
            self.win_start_dt = self.data.Date.min()
            self.win_end_dt = self.data.Date.max()
 
        return None

    ''' Function
            name: get_file_list
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @classmethod
    def get_file_list(self, path):

        # import OS module
        import os

        # Get the list of all files and directories        
        if path:
            self.path = path
#        dir_list = os.listdir(self.path)
        return os.listdir(self.path)

    ''' Function
            name: load_data
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @classmethod
    def fillter_by_date(self,
                        data_df,   # data extracted from the files
                        start_dt,  # fliter start date
                        end_dt,    # filter end date
                       ):

        # import pandas as pd
        # import datetime

        ''' intiatlize returning dataframes '''
        return_df = pd.DataFrame()

        try:
            ''' validate input dataframe '''
            if not (data_df.shape[0] > 0):
                raise ValueError("Invalid dataframe no records found!")
            return_df = data_df.copy()

            ''' >= start-date '''
            if isinstance(start_dt,date):
                mask = (return_df["Date"] >= start_dt)
                return_df = return_df[mask]

            ''' <= end-date '''
            if isinstance(end_dt,date):
                if end_dt > start_dt:
                    mask = (return_df["Date"] <= end_dt)
                    return_df = return_df[mask]

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <fillter_by_date>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return return_df

    ''' Function
            name: load_data
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def load_data(self,
                dataPath, # : str = np.nan, # default path ="../data/market_cap/"
                start_date, #: date = np.nan,
                end_date,   # : date = np.nan,
                ):

        # import traceback
        # import pandas as pd

        try:
#d            dir_list = self.get_file_list(path)

            # if len(list(filelist)) > 0:
            #     self.filelist = filelist
            # else:
            #     ''' get file list from dir path '''
            #     self.filelist = self.get_file_list(self.path)

            if dataPath:
                self.path = dataPath     # path = "../data/market_cap_2021-01-01_2022-06-01/"
                self.filelist = self.get_file_list(self.path)
                ''' confirm data files exist'''
                if not (len(self.filelist) > 0):
                    raise ValueError("No data files found in dir: %s" % (self.path))
                # self.data = self.load_data()
                # self.data['Date'] = pd.to_datetime(self.data['Date']).dt.date
            else:
                raise ValueError("Invalid path %s given for retrieving data" % (dataPath))

            '''' loop through files to get the data  '''
            columns = ["Date","ID","Symbol","market_cap"]
            self.data = pd.DataFrame([],columns=columns)
            for _s_file in self.filelist:
                if _s_file.endswith(".csv"):
                    _s_rel_path = self.path+_s_file
                    _tmp_df = pd.read_csv(_s_rel_path, index_col=False)
                    self.data = pd.concat([self.data,_tmp_df[columns]])
            self.data.reset_index(drop=True)
            self.data = self.data[self.data['market_cap'].notna()]
            # self.data['Date'] = self.data['Date'].astype('datetime64[D]')
            self.data['Date'] = pd.to_datetime(self.data['Date']).dt.date
            self.data['market_cap'] = self.data['market_cap'].astype('float64')

            if self.data.shape[0] > 0:
                if isinstance(start_date,date) and isinstance(end_date,date):
                    self.start_date = start_date
                    self.end_date = end_date
                    self.data = self.fillter_by_date(self.data,self.start_date,self.end_date)

            # ''' confirm data files exist'''
            # if not (len(self.filelist) > 0):
            #     raise ValueError("No data files found in dir: %s" % (self.path))

            # columns = ["Date","ID","Symbol","market_cap"]
            # data_df = pd.DataFrame([],columns=columns)
            # for _s_file in self.filelist:
            #     if _s_file.endswith(".csv"):
            #         _s_rel_path = self.path+_s_file
            #         _tmp_df = pd.read_csv(_s_rel_path, index_col=False)
            #         data_df = pd.concat([data_df,_tmp_df[columns]])
            # data_df.reset_index(drop=True)
            # data_df = data_df[data_df['market_cap'].notna()]
            # # data_df['Date'] = data_df['Date'].astype('datetime64[ns]')
            # data_df['Date'] = data_df['Date'].astype('datetime64[D]')
            # data_df['market_cap'] = data_df['market_cap'].astype('float64')

#            data_df = self.fillter_by_date(data_df,self.start_date,self.end_date)

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <load_data>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return self.data

    ''' Function
            name: get_significant_topN_assets
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: apply a probailistic method by taking all assets one deviations from the mean
            return DataFrame
    '''
#    @staticmethod
    def get_significant_topN_assets(self,
                                    data_df:pd.DataFrame,
                                    val_col_name='Value',
                                    **kwargs):

        # import traceback
        # import pandas as pd

        try:
            if not data_df.shape[0] > 0:
                raise ValueError('Invalid dataframe with %d rows' % (data_df.shape[0]))

            _l_dates = data_df['Date'].unique()
            _l_topNassets = []
            topNAssets = pd.DataFrame([],columns=['Date','ID',val_col_name])
            for date in _l_dates:
                ''' get assets and sort by value column '''
                assets = data_df.loc[data_df['Date'] == date]
                assets = assets.dropna(axis=0, how='any', inplace=False)
                ''' keep only postive values '''
                if 'greater than' in kwargs.keys():
                    assets = assets.loc[assets[val_col_name] > kwargs['greater than']]
                ''' calulate the mean and standard diviation of the value column '''
                _asset_mean = assets[val_col_name].mean()
                _asset_stdv = assets[val_col_name].std()
                assets = assets.loc[assets[val_col_name] >= (_asset_mean - _asset_stdv)]
                _l_assetsID = []
                _l_marketCap = []
                for idx, row in assets.iterrows():
                    asset_dict = {'Date' : row['Date'], 'ID' : row['ID'], val_col_name : row[val_col_name]}
                    topNAssets = pd.concat([topNAssets,pd.DataFrame([asset_dict])])
            # topNAssets['Date'] = topNAssets['Date'].astype('datetime64[ns]')
            topNAssets['Date'] = pd.to_datetime(topNAssets['Date']).dt.date

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <get_significant_topN_assets>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return topNAssets

    ''' Function MAYBE DEPRECATE
            name: get_weighted_index
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def get_fixed_topN_assets(self,data_df, N = 3, val_col_name='Value'):

        # import traceback
        # import pandas as pd

        try:
            _l_dates = data_df['Date'].unique()
            _l_topNassets = []
            topNAssets = pd.DataFrame([],columns=['Date','ID',val_col_name])
            for date in _l_dates:
                ''' get assets and sort by value column '''
                assets = data_df.loc[data_df['Date'] == date]
#                assets.dropna(axis=0, how='any', inplace=True)
                assets = assets.sort_values(by=val_col_name,axis=0, ascending=False)
                _l_assetsID = []
                _l_marketCap = []
                for idx, row in assets.head(N).iterrows():
                    asset_dict = {'Date' : date, 'ID' : row['ID'], val_col_name : row[val_col_name]}
                    topNAssets = pd.concat([topNAssets,pd.DataFrame([asset_dict])])
            topNAssets['Date'] = topNAssets['Date'].astype('datetime64[ns]')

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <get_topN_assets>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return topNAssets

    ''' Function MAYBE DEPRECATE
            name: weights_matrix
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def weights_matrix(self, N=3,S=10):

        # import numpy as np   #numpy.random
        # import traceback

        try:
            rand_arr = []
            rand_arr.append(np.random.dirichlet(np.ones(N),size=S))

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <weights_matrix>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return np.around(rand_arr,4)

    ''' Function
            name: set_valid_rolling_vars
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def set_valid_rolling_vars(self,
                       ticker_data,     # data frame with date, ticker id and value
                       rolling_window_length,   # retrospective start date of moving average
                       window_start_date,       # rolling windonw start date
                       window_end_date,         # rolling window end date
                       roll_calc_ops_dict,        # dict of rolling operations: mean, std, sum, adx 
                    #    value_col_name='Value',  # column name contaning the values
                        ):
        try:
            if not (isinstance(ticker_data,pd.DataFrame) and ticker_data.shape[0] > 0):
                raise ValueError("Invalid dataframe with %d records!" % (ticker_data.shape[0]))

            if isinstance(rolling_window_length,int) and rolling_window_length >= self.min_roll_win_len:
                self.roll_win_len = rolling_window_length
            else:
                print("%d days is an invalid rolling window. using default %d days"
                        %(rolling_window_length,self.roll_win_len))

            if isinstance(window_end_date, date):
                if window_end_date in ticker_data.Date.unique():
                    self.win_end_dt = window_end_date
                    # print("setting rolling windown end date",self.win_end_dt)
                else:
                    self.win_end_dt = ticker_data.Date.max()
                    # print("setting rolling windown end date to maximum date in dataframe",self.win_end_dt)
            else:
                raise ValueError("Invalid datetime.date type window end date %s" % (type(window_end_date)))
            
            if isinstance(window_start_date, date):
                if ((self.win_end_dt - window_start_date).days > 2*self.roll_win_len):   # start date must be twice window length
                    # print("Rolling windown start date: %s > %d days from the end date: %s"
                        # %(str(window_start_date),2*self.roll_win_len, str(self.end_date)))
                    if (window_start_date - timedelta(days=rolling_window_length)) in ticker_data['Date'].unique():
                        self.win_start_dt = window_start_date
                    elif (self.win_end_dt - timedelta(days=(2*self.roll_win_len))) in ticker_data['Date'].unique():
                        # print("In valid rolling windown start date %s. Must be at least twice the window length %d from end date %d"
                                # % (str(window_start_date),self.roll_win_len,str(window_end_date)))
                        self.win_start_dt = self.win_end_dt - timedelta(days=(2*rolling_window_length))
                        # print("Start date set to %s" % (self.win_start_dt))
                else:
                    raise ValueError("Invalid start date: %s. It must be %d days less than end date: %s"
                                        % (str(window_start_date),2*self.roll_win_len,str(self.win_end_dt)))
            else:
                raise ValueError("Invalid datetime.date type window start date %s" % (type(window_start_date)))
            _keys = list(set(roll_calc_ops_dict.keys()).intersection(set(self.roll_calc_op_types)))
            # if roll_calc_ops_dict.keys() in self.roll_calc_op_types:
            if len(_keys) > 0:
                self.roll_calc_ops_dict = roll_calc_ops_dict
            else:
                raise ValueError("No valid rolling calculations defined to continue", roll_calc_ops_dict)

            return True

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <weights_matrix>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

            return False

    ''' Function
            name: get_momentum
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
    def linreg_momentum(self,data,):
        from scipy.stats import linregress

        try:
                # returns = np.log(closes)
                x = np.arange(len(data))
                slope, _, rvalue, _, _ = linregress(x, data)
                
        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <linreg_momentum>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return ((1 + slope) ** 1) * (rvalue ** 2)  # annualize slope and multiply by R^2


    ''' Function
            name: get_rolling_measures
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def get_rolling_measures(
            self,
            ticker_data,     # data frame with date, ticker id and value
            rolling_window_length,  # retrospective start date of moving average
            window_start_date,      # rolling windonw start date
            window_end_date,        # rolling window end date
            rolling_measure_dict,   # dictionary of rolling calculations  ; e.g. sum, mean, adx
            # value_col_name='Value',  # column name contaning the values
        ):

        # import traceback
        # import pandas as pd
        # from datetime import datetime, timedelta, date
#        import numpy as np

        _rolling_df = pd.DataFrame()

        try:
            if not self.set_valid_rolling_vars(
                            ticker_data,     # data frame with date, ticker id and value
                            rolling_window_length,   # retrospective start date of moving average
                            window_start_date,       # rolling windonw start date
                            window_end_date,         # rolling window end date
                            rolling_measure_dict,   # dictionary of rolling calculations  ; e.g. sum, sma, std
                            # value_col_name='Value',  # column name contaning the values
                            ):
                raise ValueError("One or more invalid inputs")

            mask = (ticker_data.Date <= self.win_end_dt) & (ticker_data.Date >= self.win_start_dt)
            ticker_data = ticker_data[mask]
            _l_coin_ids = ticker_data.ID.unique()
            ''' loop through each operation to generate a colum of the measure '''
            for op_key in self.roll_calc_ops_dict.keys():
                ''' loop through each ticker to perform the operation '''
                for c_id in _l_coin_ids:
                    coin_df = pd.DataFrame(ticker_data[ticker_data['ID']==c_id],columns = ticker_data.columns)
                    ''' compute the rolling values for the period '''
                    if op_key == 'simp_move_avg':
                        coin_df['simp_move_avg'+'_'+self.roll_calc_ops_dict[op_key]]=\
                            coin_df[self.roll_calc_ops_dict[op_key]].rolling(self.roll_win_len,min_periods=1).mean()
                    elif op_key == 'simp_move_std':
                        coin_df['simp_move_std'+'_'+self.roll_calc_ops_dict[op_key]]=\
                            coin_df[self.roll_calc_ops_dict[op_key]].rolling(self.roll_win_len,min_periods=1).std()
                    elif op_key == 'simp_move_sum':
                        coin_df['simp_move_sum'+'_'+self.roll_calc_ops_dict[op_key]]=\
                            coin_df[self.roll_calc_ops_dict[op_key]].rolling(self.roll_win_len,min_periods=1).sum()
                    elif op_key == 'simp_cum_prod':
                        coin_df['simp_cum_prod'+'_'+self.roll_calc_ops_dict[op_key]]=\
                            coin_df[self.roll_calc_ops_dict[op_key]].rolling(self.roll_win_len,min_periods=1).sum()
                    elif op_key == 'momentum':
                        coin_df['momentum'+'_'+self.roll_calc_ops_dict[op_key]]=\
                            coin_df[self.roll_calc_ops_dict[op_key]].rolling(self.roll_win_len,min_periods=1).\
                                apply(self.linreg_momentum,raw=False)
                    else:
                        pass
                    _rolling_df = pd.concat([_rolling_df,coin_df])
                # break
            # _rolling_mean['Date'] = _rolling_mean['Date'].astype('datetime64[ns]')

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <get_rolling_measures>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return _rolling_df

#     ''' Function
#             name: rolling_mean
#             parameters:
#                     @name (str)
#                     @clean (dict)
#             procedure: 
#             return DataFrame
#     '''
# #    @staticmethod
#     def get_rolling_mean(self,
#                        ticker_data,     # data frame with date, ticker id and value
#                        rolling_window_length,   # retrospective start date of moving average
#                        window_start_date,       # rolling windonw start date
#                        window_end_date,         # rolling window end date
#                        value_col_name='Value',  # column name contaning the values
#                         ):

#         # import traceback
#         # import pandas as pd
#         # from datetime import datetime, timedelta, date
# #        import numpy as np

#         _rolling_mean = pd.DataFrame()

#         try:
#             if not self.set_valid_rolling_vars(
#                             ticker_data,     # data frame with date, ticker id and value
#                             rolling_window_length,   # retrospective start date of moving average
#                             window_start_date,       # rolling windonw start date
#                             window_end_date,         # rolling window end date
#                             value_col_name='Value',  # column name contaning the values
#                             ):
#                 raise ValueError("One or more invalid inputs")

#             mask = (ticker_data.Date <= self.win_end_dt) & (ticker_data.Date >= self.win_start_dt)
#             ticker_data = ticker_data[mask]
#             _l_coin_ids = ticker_data.ID.unique()
#             for c_id in _l_coin_ids:
#                 coin_df = pd.DataFrame(ticker_data[ticker_data['ID']==c_id],columns = ticker_data.columns)
#                 ''' compute the simple moving average for the period '''
#                 coin_df['sma_'+value_col_name] = coin_df[value_col_name].rolling(self.roll_win_len,min_periods=1).mean()
#                 _rolling_mean = pd.concat([_rolling_mean,coin_df])

#             # _rolling_mean['Date'] = _rolling_mean['Date'].astype('datetime64[ns]')

#         except Exception as err:
#             _s_fn_id = "Class <ExtractLoadTransform> Function <rolling_mean>"
#             print("[Error]"+_s_fn_id, err)
#             print(traceback.format_exc())

#         return _rolling_mean

    # ''' Function
    #         name: rolling_stdv
    #         parameters:
    #                 @name (str)
    #                 @clean (dict)
    #         procedure: 
    #         return DataFrame
    # '''
#    @staticmethod
#    def rolling_stdv(self, data_df, period=7, value_col_name='Value'):
    # def get_rolling_stdv(self,
    #                 ticker_data,     # data frame with date, ticker id and value
    #                 rolling_window_length,   # retrospective start date of moving average
    #                 window_start_date,       # rolling windonw start date
    #                 window_end_date,         # rolling window end date
    #                 value_col_name='Value',  # column name contaning the values
    #                 ):

    #     # import traceback
    #     # import pandas as pd
    #     # from datetime import datetime, timedelta

    #     _rolling_stdv = pd.DataFrame()

    #     try:
    #         if not self.set_valid_rolling_vars(
    #                         ticker_data,     # data frame with date, ticker id and value
    #                         rolling_window_length,   # retrospective start date of moving average
    #                         window_start_date,       # rolling windonw start date
    #                         window_end_date,         # rolling window end date
    #                         value_col_name='Value',  # column name contaning the values
    #                         ):
    #             raise ValueError("One or more invalid inputs")

    #         mask = (ticker_data.Date <= self.win_end_dt) & (ticker_data.Date >= self.win_start_dt)
    #         ticker_data = ticker_data[mask]
    #         _l_coin_ids = ticker_data.ID.unique()
    #         for c_id in _l_coin_ids:
    #             coin_df = pd.DataFrame(ticker_data[ticker_data['ID']==c_id],columns = ticker_data.columns)
    #             ''' compute the simple moving average for the period '''

    #             coin_df['smd'] = coin_df[value_col_name].rolling(rolling_window_length,min_periods=1).std()
    #             _rolling_stdv = pd.concat([_rolling_stdv,coin_df])
    #         # _rolling_stdv['Date'] = _rolling_stdv['Date'].astype('datetime64[ns]')

    #     except Exception as err:
    #         _s_fn_id = "Class <ExtractLoadTransform> Function <get_rolling_stdv>"
    #         print("[Error]"+_s_fn_id, err)
    #         print(traceback.format_exc())

    #     return _rolling_stdv

    # ''' Function
    #         name: get_momentum
    #         parameters:
    #                 @name (str)
    #                 @clean (dict)
    #         procedure: 
    #         return DataFrame
    # '''
    # def get_rolling_momentum(self,
    #                 ticker_data,     # data frame with date, ticker id and value
    #                 rolling_window_length,   # retrospective start date of moving average
    #                 window_start_date,       # rolling windonw start date
    #                 window_end_date,         # rolling window end date
    #                 value_col_name='Value',  # column name contaning the values
    #                 ):

    #     _rolling_momentum = pd.DataFrame()

    #     try:
    #         if not self.set_valid_rolling_vars(
    #                         ticker_data,     # data frame with date, ticker id and value
    #                         rolling_window_length,   # retrospective start date of moving average
    #                         window_start_date,       # rolling windonw start date
    #                         window_end_date,         # rolling window end date
    #                         value_col_name='Value',  # column name contaning the values
    #                         ):
    #             raise ValueError("One or more invalid inputs")

    #         mask = (ticker_data.Date <= self.win_end_dt) & (ticker_data.Date >= self.win_start_dt)
    #         ticker_data = ticker_data[mask]
    #         _l_coin_ids = ticker_data.ID.unique()
    #         for c_id in _l_coin_ids:
    #             coin_df = pd.DataFrame(ticker_data[ticker_data['ID']==c_id],columns = ticker_data.columns)
    #             ''' compute the simple moving average for the period '''

    #             coin_df['momentum'] = coin_df[value_col_name].\
    #                         rolling(self.roll_win_len,min_periods=1).\
    #                             apply(self.linreg_momentum,raw=False)
    #             _rolling_momentum = pd.concat([_rolling_momentum,coin_df])
    #         # _rolling_momentum['Date'] = _rolling_momentum['Date'].astype('datetime64[ns]')

    #     except Exception as err:
    #         _s_fn_id = "Class <ExtractLoadTransform> Function <get_rolling_momentum>"
    #         print("[Error]"+_s_fn_id, err)
    #         print(traceback.format_exc())

    #     return _rolling_momentum

    ''' Function REPLACE with dataframe.melt function
            name: transfrom_data
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
#    @staticmethod
    def transfrom_data(self,data_df, value_col_name = "Value"):

        # import pandas as pd

        ''' Initialize variables '''
        _l_coin_ids = sorted(data_df['ID'].unique())
        _l_dates = sorted(data_df['Date'].unique())
        _l_columns = list(sorted(data_df['ID'].unique()))
        _l_columns.insert(0,"Date")

        market_df = pd.DataFrame([], columns=_l_columns)
        market_df["Date"] = _l_dates

        for _s_coin_id in _l_coin_ids:
            tmp_df = pd.DataFrame([])
            tmp_df = data_df.loc[data_df["ID"] == _s_coin_id]
            tmp_df = tmp_df.sort_values(by=['Date'])
            tmp_df = tmp_df.dropna(inplace=False)

            for _date in tmp_df["Date"]:
                _value = tmp_df.loc[tmp_df['Date'] == _date, value_col_name].item()
                market_df.loc[market_df['Date']==_date, _s_coin_id] = _value

        ''' DEPRECATED Cleanup rows and columns elsewhere '''
#        market_df=market_df.drop_duplicates()
#        market_df = market_df.dropna(axis=1)

        ''' Set the dtypes '''
        market_df['Date'] = market_df['Date'].astype('datetime64[ns]')
        market_df.loc[:,market_df.columns !='Date'] = market_df.loc[:,market_df.columns !='Date'].astype('float64')

        return market_df

    ''' Function
            name: weights_matrix
            parameters:
                    @name (str)
                    @clean (dict)
            procedure:
            return DataFrame
    '''
#    @staticmethod
    def transpose_pivot(self, data_df):

        # import traceback
        # import pandas as pd
        
        transp_df = pd.DataFrame([], columns=['Date','ID','market_cap'])
        _l_dates = data_df['Date'].unique()
        _l_coin_ids = [col for col in data_df.columns if col !='Date']
        try:
            for date in _l_dates:
                for coin_id in _l_coin_ids:
                    value = data_df[data_df['Date'] == date][coin_id]
                    transp_df = pd.concat([transp_df,
                                           pd.DataFrame({'Date':date, 'ID':coin_id, 'market_cap':value})])
            transp_df['Date'] = transp_df['Date'].astype('datetime64[ns]')
            transp_df['market_cap'] = transp_df['market_cap'].astype('float64')

        except Exception as err:
            _s_fn_id = "Class <ExtractLoadTransform> Function <weights_matrix>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return transp_df

    ''' Function DEPRECATED replaced with dataframe.merge function
            name: match_dataframes
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
    def match_df(self, source_data_df, to_base_data_df):

        # import traceback
        # import pandas as pd
        # import datetime

#        matching_df = pd.DataFrame([],columns=['Date','ID','Value'])
        matching_df = pd.DataFrame()

        try:
            pass
        except Exception as err:
            _s_fn_id = "Class <ExchangeTradeProtocol> Function <match_df>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return matching_df

        
    ''' Function DEPRECATED replaced with dataframe.merge function
            name: match_dataframes
            parameters:
                    @name (str)
                    @clean (dict)
            procedure: 
            return DataFrame
    '''
    def match_dataframes(self, source_data_df, to_base_data_df):

        # import traceback
        # import pandas as pd
        # import datetime

        matching_df = pd.DataFrame([],columns=['Date','ID','Value'])

        try:
            ''' get unique dates from base frame '''
            _l_base_dates = to_base_data_df['Date'].unique()
            for date in _l_base_dates:
                date = pd.to_datetime(date)
                ''' get unique coin ids for the date '''
                coin_ids = to_base_data_df[to_base_data_df['Date']==date]['ID']
                for c_id in coin_ids:
                    mask = (source_data_df['Date']==date) & (source_data_df['ID']==c_id)
                    value = source_data_df[mask]['market_cap']
                    matching_df = pd.concat([matching_df,
                                             pd.DataFrame({'Date':date,'ID':c_id,'Value':value})])

        except Exception as err:
            _s_fn_id = "Class <ExchangeTradeProtocol> Function <match_dataframes>"
            print("[Error]"+_s_fn_id, err)
            print(traceback.format_exc())

        return matching_df
