import yfinance as yf
import pandas as pd
import numpy as np
import requests
import sys

'''
Income statements:
    Revenue
        -sales
    Costs
        -COGS
        ------------------ Revenue - COGS = Gross profit
        -Fixed costs
        -Depreciation and amortization
    ------------------------ EBIT
        - Interest and taxes
    Earnings  or net income


Operation income = Gross Profit - Operating Expenses
Operating Margin for the bussiness = Operation income/Revenue >= 15% good



Balance sheet:
    Shareholders' equity = Assets (enterprise owns) - Liabilities (enterprise owes)
    Assets/Liabilities > 1 for a good investment (>2 is very good)

Cashflow
    Free cash flow (FCF) is the cash a company generates after taking into consideration cash outflows that support its operations and maintain its capital assets. 


Fundamental Analysis:
    Enterprise Value = net debt + market cap = gross debt - cash + market cap
    EV/EBITDA <10 is good
    EV/Revenue lower is better
    
    P/S = Market Cap/ Sales  << 1 under, >> 1 over lower is better
    P/E = MC/Earnings = Share Price/EPS   the lower the better
    P/B = MC/Book = MC/ (Tangible Assets - Liabilities)  << 1 under, >> 1 over, lower is better
    PEG = P/(E*Growth) < 1 is better
    
    Profit Margin = Net income/Sales The greater the better
    ROA = Net Income/Assets the greater the better > 20% is great
    ROE = Net Income/Equity the greater the better >20%
    Debt to Equity = Total debt/Equity  The lower the better < 1
    Current Ratio = Assets/Liabilities the greater the better >1

    
'''

# The weighted average cost of capital (WACC) represents a firm's average cost of capital from all sources, including common stock, preferred stock, bonds, and other forms of debt.
# Used to estimate a rate of return of an investment

def WACC(w):
    
    if w == '0':
        try:
            balance = stock.balance_sheet.T
            financials = stock.financials.T
            
            short_long_debt = balance[['Short Long Term Debt']].to_numpy()
            short_long_debt = short_long_debt[0,0]
            
            long_debt = balance[['Long Term Debt']].to_numpy()
            long_debt = long_debt[0,0]
            
            interest_expense = financials[['Interest Expense']].to_numpy()
            interest_expense = interest_expense[0,0]*np.sign(interest_expense[0,0])
            
            income_before_tax = financials[['Income Before Tax']].to_numpy()
            income_before_tax = income_before_tax[0,0]
            
            income_tax_expense = financials[['Income Tax Expense']].to_numpy()
            income_tax_expense = income_tax_expense[0,0]
            
            rd = interest_expense/(short_long_debt+long_debt) 
            t = income_tax_expense/income_before_tax 
           
            Rf = 1.275/100             # Treasury Yield 10 Years
            beta = stock.info['beta']
            Rm = 0.1                   # 10yr return of s&p500
            
            re = Rf+beta*(Rm-Rf)
            
            wd = stock.info['totalDebt']/stock.info['marketCap']
            we = 1-wd 
           
            wacc = wd*rd*(1-t)+we*re
            
        except:

            print('Wacc defined as 8%')
            wacc = 8/100

    else:
           wacc = float(w)/100
           
    return wacc
    
    
if __name__ == "__main__":
        
    pd.set_option("display.max_rows", None, "display.max_columns", None)
           
    company = input('Inform the company: ') 

    op = input('1 - Compare stocks \n2 - Intrinsic Value by Discouted Cash Flow Method\n')

    if op == '1': 

        stocks = []
        evaluate = company
        print("Inform the stocks you want to compare:")
        while True:
            temp = input("Enter 0 to exit: ")
            if temp == '0':
                break
            else:
                stocks.append(temp)
        stocks.append(evaluate)
        
        # Parameters to compare
        i = 0
        n = len(stocks)
        market_cap = np.zeros(n) #  It is calculated by multiplying the total number of a company's outstanding shares by the current market price of one share. 
        ev = np.zeros(n) # Enterprise value: net debt + market cap = gross debt - cash + market cap
        Trailing_PE = np.zeros(n) # The trailing P/E, which is the standard form of a price-to-earnings ratio, is calculated using recent past earnings. 
        Forward_PE = np.zeros(n) # The forward P/E uses projected future earnings to calculate the price-to-earnings ratio.
        PEG_5 = np.zeros(n) #  Price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period (5 years).
        P_R_12 = np.zeros(n) # Price/Revenue value 12 months
        P_B_3 = np.zeros(n) # Price/Book value 3 months
        EV_R = np.zeros(n) # EV/ Revenues
        EV_EBITDA = np.zeros(n) # EV/EBITDA
        
        data = np.zeros(n+1)
        
        for company in stocks:
            site = f'https://finance.yahoo.com/quote/{company}/key-statistics?p={company}'
            try:
                statistics = pd.read_html(requests.get(site, headers={'User-agent': 'Mozilla/5.0'}).text)
            except:
                print(f"Company {company} was not found")
                sys.exit()
                
            for j in range(n+1):
                aux = str(statistics[0][1][j])
                if aux != 'nan': 
                    if "B" in aux:
                        aux = aux.replace("B","")
                        aux = float(aux)*1e9
                    elif "T" in aux:
                        aux = aux.replace("T","")
                        aux = float(aux)*1e12    
                    elif "M" in aux:
                        aux = aux.replace("M","")
                        aux = float(aux)*1e6
                    data[j] = aux
                
            market_cap[i] = np.round(data[0]/1e6,2)
            ev[i] = np.round(data[1]/1e6,2)
            Trailing_PE[i] = np.round(data[2],2)
            Forward_PE[i] = np.round(data[3],2)
            PEG_5[i] = np.round(data[4],2)
            P_R_12[i] = np.round(data[5],2)
            P_B_3[i] = np.round(data[6],2)
            EV_R[i] = np.round(data[7],2)
            EV_EBITDA[i] = np.round(data[8],2)
        
            i += 1
       
        
        # averaging each parameter
        average = np.array([np.average(market_cap[0:len(stocks)-1]), np.average(ev[0:len(stocks)-1]), np.average(Trailing_PE[0:len(stocks)-1]),np.average(Forward_PE[0:len(stocks)-1]), 
        np.average(PEG_5[0:len(stocks)-1]), np.average(P_R_12[0:len(stocks)-1]), np.average(P_B_3[0:len(stocks)-1]), np.average(EV_R[0:len(stocks)-1]),np.average(EV_EBITDA[0:len(stocks)-1])])
        average=np.round(average,2)
        
        difference = np.array([market_cap[-1]/average[0], ev[-1]/average[1], Trailing_PE[-1]/average[2],Forward_PE[-1]/average[3],PEG_5[-1]/average[4],P_R_12[-1]/average[5],P_B_3[-1]/average[6],EV_R[-1]/average[7],EV_EBITDA[-1]/average[8]])
        difference = np.round(difference,2)
        
        np.set_printoptions(suppress=False)
        
        stocks.insert(0,'Recomendation')
        stocks.append('Average')
        stocks.append(evaluate + '/Average')
        parameters=(market_cap, ev, Trailing_PE,Forward_PE,PEG_5,P_R_12,P_B_3,EV_R,EV_EBITDA)
        DATA=np.vstack(parameters)
        DATA=DATA.transpose()
        parameters=(DATA,average,difference)
        DATA=np.vstack(parameters)
        recomendation = ['bigger','bigger','lower','lower','lower','lower << 1','lower <1','lower','lower <10']
        parameters=(recomendation,DATA)
        DATA=np.vstack(parameters)

        # pandas dataframe
        dataframe = pd.DataFrame(data=DATA,index=stocks,columns=['Market Cap (M)', 'EV (M)','Trailing P/E','Forward P/E','PEG 5 yr','Price/Sales 12 months)','Price/Book 3 months','EV/R','EV/EBITDA'])
        pd.set_option("display.max_rows", None, "display.max_columns", None)
       
        dataframe.style.applymap('font-weight: bold',
                      subset=pd.IndexSlice[dataframe.index[dataframe.index==evaluate], :])
        print(dataframe)
            
            
            
            
    elif op == '2':
        
        '''
        Method:
            Intrinsic Value = FCF1/(1+r)^1 + FCF2/(1+r)^2 + ... + FCFn/(1+r)^n + FCFn*(1+g)/(r-g)
            
            
            FCF (to Equity) (simple formula without net borrowings) = Total Cash Flow from Operating activities - Capital Expenditures
            
            r = required rate of return ~= WACC Weighted cost of capital
            
            g = perpetual growth of global economy ~= 2.5%
            
        '''
        
        print(f'{company}')
        
        stock = yf.Ticker(company)
        cash = stock.cashflow.transpose()
       
       #gets the cash flow for the past 4 years
        
        free_cash_flow = (cash[['Total Cash From Operating Activities']].to_numpy()+cash[['Capital Expenditures']].to_numpy()) #+cash[3,:] #FCF to Equity = Cash from Operations -Capital Expenditures + Net Borrowings
        free_cash_flow = free_cash_flow.T
        
        free_earnings = free_cash_flow/((cash[['Net Income']].to_numpy()).T) # FCFE/NET INCOME -> needs to be consistent. Choose the lower one
        
        free_earnings_rate = min(free_earnings)
        free_cash_flow = np.flip(free_cash_flow) #to get yr-4 yr-3 yr-2 yr-1
        
        
        #revenues for the next 2 years (actual year and the next) following analysts
        site = f'https://finance.yahoo.com/quote/{company}/analysis?p={company}'
        analyst = pd.read_html(requests.get(site, headers={'User-agent': 'Mozilla/5.0'}).text)
        revenues = analyst[1].to_numpy()
        revenues = revenues[1,3:] #  yr yr+1
        
        for i in range(len(revenues)):
            aux = revenues[i]
            if "B" in aux:
                aux = aux.replace("B","")
                aux = float(aux)*1e9
            elif "T" in aux:
                aux = aux.replace("T","")
                aux = float(aux)*1e12    
            elif "M" in aux:
                aux = aux.replace("M","")
                aux = float(aux)*1e6
            revenues[i] = aux
        
       
        past_revenues = stock.financials.T
        past_revenues = past_revenues[['Total Revenue']].to_numpy().T # yr-1 yr-2 yr-3 yr-4
        
        past_revenues = np.flip(past_revenues) # yr-4 yr-3 yr-2 yr-1        
        
        revenues = np.concatenate([past_revenues[0,:],revenues])  # yr-4 yr-3 yr-2 yr-1 yr yr+1
        
        growth = np.zeros(len(revenues)-1) # calculate the growth rate from the years available
        for i in range(len(revenues)-1):
            growth[i]=revenues[i+1]/revenues[i]-1
        
        #prediction for 2 years more in the future for revenues being conservative -> get the 
        # lowest growth rate from the past in modulus and apply to the next two years
        growth_next = 1+min(np.absolute(growth))
        
        revenues = np.concatenate([revenues,np.array([revenues[-1]*growth_next,revenues[-1]*growth_next*growth_next])])
        revenues = np.round(revenues.astype(np.double),2) # yr-4 yr-3 yr-2 yr-1 yr yr+1 yr+2 yr+3

        #net income from the past 4 years
        net_income_past = np.flip(cash[['Net Income']].to_numpy().T)
        net_income_past = net_income_past[0,:]

        #net income margins = net income/revenue
        net_income_margin = np.average(np.abs(net_income_past/revenues[0:4]))
        
        
        NI_next = revenues[4:]*net_income_margin
        net_income = np.concatenate([net_income_past.astype(np.double),NI_next])
        
        free_cash_flow = np.concatenate([free_cash_flow[0,:],NI_next*free_earnings_rate])
        
        #-----------------------------------------------------------------------------
        #d is debt and e is equity, w is weight and r is rate, t is taxes
        # WACC = wd*rd*(1-t)+we*re = r
        print('Inform wacc in %: 0 if you want the program calculate')
        w = input()
        wacc = WACC(w)
        r = wacc
        print('WACC = ', np.round(wacc*100,2), '%')
       #------------------------------------------------------------------------------------
        #perpetual growth rate
        g = 2.5/100
        shares_out = stock.info['sharesOutstanding']
        
        #final value for cash flow
        V0 = free_cash_flow[-1]*(1+g)/(r-g)
       
        # FCF yr-4 yr-3 yr-2 yr-1 yr yr+1 yr+2 yr+3
        FCF = free_cash_flow[4:]
        
        add = 0
        for i in range(len(FCF)):
                add += FCF[i]/((1+r)**(i+1))
        
        intrinsic_value = (add + V0/((1+r)**(i+1)))/shares_out 
        
        print("Number of shares: ", f'{shares_out:,}')
        print('Final value:', np.round(V0/1e9,2), "B$")
        print('Intrinsic Value: ', np.round(intrinsic_value,2), '$')
        print('Current Price: ', stock.info['currentPrice'] )
        
        value = (np.round(intrinsic_value/stock.info['currentPrice']-1,2))*100
        
        if(value >= 0):
            print('underpriced (buy): ', value, '%')
        else:
            print('overpriced: ', value, '%')
      

       
