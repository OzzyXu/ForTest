########################
# Created by ZS on 6/25
########################




def optimizer_test(equity_funds_list, start_date,
                   end_date = dt.date.today().strftime("%Y/%m/%d"), frequency = 60, name = None):

    # according to start_date to work out testing time_frame

    trading_date_s = get_previous_trading_date(start_date)
    trading_date_e = get_previous_trading_date(end_date)

    trading_dates = get_trading_dates(trading_date_s, trading_date_e)
    time_len = len(trading_dates)

    count = floor(time_len/frequency)


    #for i in range(frequency + 1):
    #    start_date = get_previous_trading_date(start_date)

    time_frame = {}
    #time_frame[0] = start_date
    for i in range(0, count+1):
        time_frame[i] = trading_dates[i*frequency]


    #break_tag = 0
    opt_res = {}
    for i in range(0, count+1):
        opt_res[i] = optimizer(equity_funds_list, start_date=time_frame[i],  asset_type='fund', method='all')

    #     if opt_res[i] is None:
    #         break_tag = 1
    #         print(name, i, opt_res[i], equity_funds_list, start_date)
    #
    # if break_tag ==1:
    #     pass
    #








    methods = ['risk_parity', 'min_variance', 'equal_weight']

    ## add equal weights or self-defined weights into weights


    for i in range(0,count+1):
        try:
            opt_res[i][0]['equal_weight']= [1 / len(opt_res[i][0])] * len(opt_res[i][0])
        except:
            print(i, name)


    weights = {}

    daily_methods_a_r = {}

    for j in methods:
        daily_arithmetic_return = []


        for i in range(0, count):

            weights[j+str(i)] = opt_res[i][0]
            period_prices_pct_change = opt_res[i+1][1]
            c_m = opt_res[i][2]


            period_daily_return_pct_change = pd.DataFrame(period_prices_pct_change)[1:]

            corresponding_data_in_weights = period_daily_return_pct_change.iloc[:,
                                        [x in weights[j+str(i)].index for x in period_daily_return_pct_change.columns]]

            weighted_sum = corresponding_data_in_weights.multiply(weights[j+str(i)][j]).sum(axis=1)
            daily_arithmetic_return.extend(weighted_sum)



        daily_methods_a_r[j] = daily_arithmetic_return




    annualized_vol = {}
    annualized_return = {}

    for j in methods:
        temp = np.log(daily_methods_a_r[j][0] + 1)

        annualized_vol[j] = sqrt(244) * temp.std()
        days_count = len(daily_methods_a_r[j][0])
        daily_cum_log_return = temp.cumsum()
        annualized_return[j] = (daily_cum_log_return[-1] + 1) ** (365 / days_count) - 1

    #fig1 = plt.figure()


        str1 = """%s: r = %f, $\sigma$ = %f. """ %(j, annualized_return[j], annualized_vol[j])
    #s   tr2 = """Minimum variance: r = %f, $\sigma$ = %f.""" % %(annualized_return[j], annualized_vol[j])


        plt.figure(1, figsize=(10, 8))

        p1 = daily_cum_log_return.plot(legend=True, label=str1)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3))


    plt.savefig('test_res/%s'%(name))
#    plt.ioff()
    plt.close()

    #plt.figure(2)
    #p2 = daily_cum_log_return.plot(legend=True, label=str1)

    return weights, annualized_return, annualized_vol





equity_funds_list = ['002832',
'002901',
 '002341',
 '003176',
 '003634',
 '002621',
 '000916',
 '001416']



equity_funds_list = ['002832',
'002901',
 '002341',
 '003176',
 '003634',
 '002621',
 '000916',]


start_date = '2014-1-1'
end_date = '2017-06-25'
#end_date = today_date,


a = optimizer_test(equity_funds_list, start_date, end_date , frequency= 60, name = None)





def wrap_and_run(test_suite, start_date, end_date, frequency):


    test_res = pd.DataFrame(columns=['risk_parity_return', 'min_variance_return', 'equal_weight_return',
                                             'risk_parity_sigma', 'min_variance_sigma', 'equal_weight_sigma'])
    for i in test_suite.keys():
        df1 = pd.DataFrame(index=[i], columns=['risk_parity_return', 'min_variance_return', 'equal_weight_return',
                                             'risk_parity_sigma', 'min_variance_sigma', 'equal_weight_sigma'])
        equity_funds_list = test_suite[i]
        # try:
        #     a = optimizer_test(equity_funds_list, start_date, end_date, frequency, name=i)
        # except:
        #     print('outside:', i)
        a = optimizer_test(equity_funds_list, start_date, end_date, frequency, name=i)
        if a is None:
            pass
        else:
            df1['risk_parity_return'] = a[1]['risk_parity']
            df1['risk_parity_sigma'] = a[2]['risk_parity']

            df1['min_variance_return'] = a[1]['min_variance']
            df1['min_variance_sigma'] = a[2]['min_variance']

            df1['equal_weight_return'] = a[1]['equal_weight']
            df1['equal_weight_sigma'] = a[2]['equal_weight']
            test_res = pd.concat([test_res, df1])


    return test_res


test_suite =  {key:fund_test_suite[key] for key in ['Hybrid_Related_Stock_3*2=6', 'Hybrid_QDII_Stock_3*3=9', 'Related_StockIndex_2*3=6'
]}

 start_date = '2014-01-01'
 end_date = '2017-06-25'
 frequency = 132



test_suite = fund_test_suite
len(fund_test_suite)
res_zs = wrap_and_run(test_suite, start_date, end_date, frequency )



###

q_key = 'Bond_Related_Stock_3*4=12'

equity_funds_list = fund_test_suite[q_key]
a11 = ['560005',
 '217011',
 '519112',
 '450006',
 '161211',
 '160706',
 '040180',
 '240016',
 '540007',
 '240005',
 '162208',
 '340006']




equity_funds_list = ['002832', '002901', '002341', '003176', '001237', '004069', '000307', '003524', '003634', '002621', '000916', '001416']
start_date






####



res_zs.to_csv('res_zs.csv', sep =',')








for i in fund_test_suite.keys():
    print(i)










def try11(a = None):
    if a is None:
        pass
        print(4)
    print(3)

b =try11()
try11(1)



def try12(a = None):
    try:
        a !=-None
    except:
        print(3)
    print(4)



try12(5)


if 1==1:
    if b is None:
        pass

    else:
        print(3)
    print(4)


try:
    print(3)
except:



recip = float('Inf')
try:
    recip = 1 / 3
except ZeroDivisionError:
    logging.info('Infinite result')
else:
    logging.info('Finite result')


try:
    df1 == 1
except:
    print(3)