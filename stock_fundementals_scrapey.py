import requests
import bs4
from datetime import date, timedelta
from datetime import datetime
import yfinance as yf
import time


def return_yahoo_stats_soup(symbol):
    '''
    Returns Beautiful Soup object for Yahoo Statistics page for given symbol
    Structure for URL is https://finance.yahoo.com/quote/AMZN/key-statistics 
    where AMZN is symbol passed
    '''
    
    url = 'https://finance.yahoo.com/quote/' + symbol + '/key-statistics'
    r= requests.get(url)
    print('Symbol: ' + symbol + ' | Request status: ' + str(r.status_code))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup 


def return_yahoo_income_soup(symbol):
    '''
    Returns Beautiful Soup object for Yahoo Income Statement for given symbol
    Structure for URL (for Amazon in this example):
    https://finance.yahoo.com/quote/AMZN/financials
    '''
    
    url = 'https://finance.yahoo.com/quote/' + symbol + '/financials'
    r= requests.get(url)
    print('Symbol: ' + symbol + ' | Request status: ' + str(r.status_code))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup 


def return_zacks_soup(symbol):
    '''
    Returns Beautiful Soup object for Zacks income statements (ANNUAL reports)
    Structure for URL (for TSLA for example) is
    https://www.zacks.com/stock/quote/AAPL/income-statement
    '''
    
    headers = {
    'User-Agent': 'Mozilla/5.0'
    }
    
    url = 'https://www.zacks.com/stock/quote/' + symbol + '/income-statement'
    r= requests.get(url, headers=headers)
    print('Symbol: ' + symbol + ' | Request status: ' + str(r.status_code))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup 


def return_zacks_bs_soup(symbol):
    '''
    Returns Beautiful Soup object for Zacks Balance Sheet page (ANNUAL reports)
    Structure for URL (for TSLA for example) is
    https://www.zacks.com/stock/quote/AAPL/balance-sheet
    '''
    
    headers = {
    'User-Agent': 'Mozilla/5.0'
    }
    
    url = 'https://www.zacks.com/stock/quote/' + symbol + '/balance-sheet'
    r= requests.get(url, headers=headers)
    print('Symbol: ' + symbol + ' | Request status: ' + str(r.status_code))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup 


def return_macrotrends_soup(symbol):
    '''
    Returns Beautiful Soup object for Macrotrends.net page (to pull P/E symbols)
    for given symbol.
    
    Structure for URL for stock ticker GOOG is:
    https://www.macrotrends.net/stocks/charts/GOOG/xxx/pe-ratio (the 'xxx doesnt matter')
    '''
    
    url = 'https://www.macrotrends.net/stocks/charts/' + symbol + '/xxx/pe-ratio'
    r= requests.get(url)
    print('Symbol: ' + symbol + ' | HTTP Request status: ' + str(r.status_code))
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup 


def clean_pe(soup_str):
    '''
    Strips Yahoo Stats Soup string of everything but the P/E
    '''
    try:
        clean_split = soup_str.split()
        clean = clean_split[-1].split('>')[-2].split('<')[-2]
        if clean == '':
            clean = 1999 #assign very high P/E if stock is unprofitable 
    except:
        clean = None
        
    return clean    

def clean_pe_date(date_elem):
    '''
    Parameters
    ----------
    soup_elem : string version of a Yahoo Stats soup element

    Returns
    -------
    just the date string in format MM/DD/YYYY

    '''
    try:
        first_split = date_elem.split()[-1]
        second_split = first_split.split('>')
        third_split = second_split[-2].split('<')
        date_str = third_split[-2]
        return date_str
    except:
        return None
    

def pull_pe(symbol):
    '''
    Pulls Trailing P/E for symbols for most up to 5 past quarterly results
    using Yahoo Stats page
    If company does not have a report for any of those periods returns None 
    for that period
    '''
    
    soup = return_yahoo_stats_soup(symbol)
 
    #most recent quarter
    most_recent_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(3)'))
    most_recent_pe = clean_pe(most_recent_pe_elem)
    most_recent_date_elem = str(soup.select('th.Fw\(b\):nth-child(3) > span:nth-child(1)'))
    most_recent_date = clean_pe_date(most_recent_date_elem)
    
    #previous quarter
    prev_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(4)'))
    prev_pe = clean_pe(prev_pe_elem)
    prev_date_elem = str(soup.select('th.Fw\(b\):nth-child(4) > span:nth-child(1)'))
    prev_date = clean_pe_date(prev_date_elem)
    
    #6 months ago
    six_mos_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(5)'))
    six_mos_pe = clean_pe(six_mos_pe_elem)
    six_mos_date_elem = str(soup.select('th.Fw\(b\):nth-child(5) > span:nth-child(1)'))
    six_mos_date = clean_pe_date(six_mos_date_elem)
    
    #9 months ago
    nine_mos_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(6)'))
    nine_mos_pe = clean_pe(nine_mos_pe_elem)
    nine_mos_date_elem = str(soup.select('th.Fw\(b\):nth-child(6) > span:nth-child(1)'))
    nine_mos_date = clean_pe_date(nine_mos_date_elem)
    
    #year agp
    yr_ago_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(7)'))
    yr_ago_pe = clean_pe(yr_ago_pe_elem)
    yr_ago_date_elem = str(soup.select('th.Fw\(b\):nth-child(7) > span:nth-child(1)'))    
    yr_ago_date = clean_pe_date(yr_ago_date_elem)
          
    return most_recent_date, most_recent_pe, prev_date, prev_pe, six_mos_date, six_mos_pe, \
            nine_mos_date, nine_mos_pe, yr_ago_date, yr_ago_pe


def pull_yahoo_rev(symbol):
    '''
    Pulls Revenue from last 3 available Annual Income Statements from 
    Yahoo Finance
    If company does not have a report a year ago returns 0
    '''
 
    soup = return_yahoo_income_soup(symbol)
    
    most_recent_rev_elem = str(soup.select('.D\(tbrg\) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1)'))
    prev_yr_rev_elem = str(soup.select('.D\(tbrg\) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > span:nth-child(1)'))
    two_yrs_ago_rev_elem = str(soup.select('.D\(tbrg\) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > span:nth-child(1)'))
  
    try:
        last_annual_rev = most_recent_rev_elem.split()[-1].split('>')[-2].split('<')[-2]
    except IndexError:
        last_annual_rev = 0
        
    try:
        prev_year_rev = prev_yr_rev_elem.split()[-1].split('>')[-2].split('<')[-2]
    except IndexError:
        prev_year_rev = 0       
        
    try:
        two_yrs_ago_rev = two_yrs_ago_rev_elem.split()[-1].split('>')[-2].split('<')[-2]
    except IndexError:
        two_yrs_ago_rev = 0   
     
    return last_annual_rev, prev_year_rev, two_yrs_ago_rev


def transform_ratio_soup(string):
    '''
    Little module that helps de-clutter code in the Current Ratio function.  
    Just strips unnecessary CSS text and returns the clean desired string 
    from Zacks.com 
    '''

    try:
        clean_date = string.split('>')[-2].split('<')[-2]
    except:
        clean_date = None
        
    return clean_date


def pull_current_ratios(symbol):
    '''
    Returns Current Ratios for most recent two annual filings using Zacks.com
    '''

    soup = return_zacks_bs_soup(symbol)
    
    most_recent_date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(2)'))
    most_recent_curr_assets_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(7) > td:nth-child(2) > span:nth-child(1)'))
    most_recent_curr_liab_elem = str(soup.select('#annual_income_statement > table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(8) > td:nth-child(2) > span:nth-child(1)'))
    
    most_recent_date = transform_ratio_soup(most_recent_date_elem)
    most_recent_curr_assets = transform_ratio_soup(most_recent_curr_assets_elem)
    most_recent_curr_liab = transform_ratio_soup(most_recent_curr_liab_elem)
    
    try:
        most_recent_curr_ratio = float(most_recent_curr_assets.replace(',','')) / int(most_recent_curr_liab.replace(',',''))
    except:
        most_recent_curr_ratio = None
    
    prev_date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(3)'))    
    prev_curr_assets_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(7) > td:nth-child(3) > span:nth-child(1)'))
    prev_curr_liab_elem = str(soup.select('#annual_income_statement > table:nth-child(4) > tbody:nth-child(2) > tr:nth-child(8) > td:nth-child(3) > span:nth-child(1)'))
    
    prev_date = transform_ratio_soup(prev_date_elem)
    prev_curr_assets = transform_ratio_soup(prev_curr_assets_elem)
    prev_curr_liab = transform_ratio_soup(prev_curr_liab_elem)
    
    try:
        prev_curr_ratio = float(prev_curr_assets.replace(',','')) / float(prev_curr_liab.replace(',',''))
    except:
        prev_curr_ratio = None
    
    return most_recent_date, round(most_recent_curr_ratio, 2), prev_date, round(prev_curr_ratio,2)


def strip_commas_and_convert_to_int(str):
    new = str.replace(',','')
    return int(new)


def str_to_date_yy(date_string):
    '''
    changes date string in format DD/MM/YY to proper datetime object
    NOTE: This is different than "str_to_date" function which looks for date 
    format DD/MM/YYYY
    '''
    
    return datetime.strptime(date_string, '%m/%d/%y')
    

def pull_annual_rev_and_ni(symbol):
    '''
    Pulls Revenue and Net Income for last three available annual reports from 
    zacks.com
    '''

    soup = return_zacks_soup(symbol)
    
    ni_list = [] #pulls Net Income 
    for i in range(2,5):
        ni_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) > '\
                                  'tr:nth-child(15) > td:nth-child(' + str(i) + ') > span:nth-child(1) >'\
                                  ' a:nth-child(1)'))
        try:
            ni = ni_elem.split(">")[-2].split("<")[-2]
            if ni != '' and ni != 'NA':
                ni += ',000' #add zeros since this site reports in millions 
            elif ni == 'NA':
                ni = None
        except IndexError:
            ni = None
        ni_list.append(strip_commas_and_convert_to_int(ni))
        
    date_list = [] #pulls Dates
    for i in range(2,5):
        date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1)'\
                                    ' > tr:nth-child(1) > th:nth-child(' + str(i) + ')'))
        try:
            date = date_elem.split('>')[-2].split('<')[-2]
        except:
            date = None
        date_list.append(str_to_date_yy(date))
        
    rev_list = [] #pulls revenue
    for i in range(2,5):
        rev_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) >'\
                                   ' tr:nth-child(1) > td:nth-child(' + str(i) + ')'))
        try:
            rev = rev_elem.split('>')[-2].split('<')[-2]
            if rev != '' and rev != 'NA':
                rev += ',000'
            elif rev == 'NA':
                rev = None
        except:
            rev = 0 #if no revenue is available returns a zero
        rev_list.append(strip_commas_and_convert_to_int(rev))
        
        z = zip(date_list, rev_list, ni_list)
        lst = list(z)
              
    return lst

def clean_elem(elem):
    '''
    If element is not empty, strips everything from string elem except the desired data.
    
    Function is used by pull_pe_and_ep function to pull data from macrotrends.net
    '''
    try:
        clean = elem.split()[-1].split('>')[-2].split('<')[-2] 
    except:
        clean = None
    return clean 


def remove_dollar_sign(str):
    return str.replace('$','')


def change_date_format(date_str):
    '''
    Changes date format of macrotrends.net to match that of other data pulls
    Example: Takes a string '2020-06-30' and returns '6/30/2020'
    '''
    year, month, day = date_str.split('-')
    return month + '/' + day + '/' + year


def pull_pe_and_ep(symbol):
    '''
    Given a ticker symbol, returns 7 most recent quarters of info as a 
    list of lists formatted as folows:
    [date, price, EPS, P/E, E/P]
    
    Uses macrotrends.net for source data
    
    '''
    soup = return_macrotrends_soup(symbol)
    all_dates = []
    for i in range(2, 9):
        data = []
        for j in range(1, 4):
            elem = str(soup.select('#style-1 > table:nth-child(1) > tbody:nth-child(3)'\
                                   ' > tr:nth-child(' + str(i) + ') > td:nth-child('\
                                   + str(j) + ')'))
            clean = clean_elem(elem)
            data.append(clean)
        if clean != None:
            data.append(float(data[1]) / float(remove_dollar_sign(data[2]))) # Calculates P/E
            data.append(float(remove_dollar_sign(data[2])) / float(data[1])) # Calculates E/P
            all_dates.append(data)
        
    for x in all_dates: #converts date format of macrotrends to match other data sources
        x[0] = change_date_format(x[0])
            
    return all_dates

def pull_yahoo_pe_list(symbol_list):
    
    '''
    Preference is to use new pull_pe_list function before using this one.
    
    Returns dictionary of up to a year's worth of trailing P/E ratios from 
    quarterly reports.
    
    Uses Yahoo! Stats page
    
    Dictionary has following structure: 
    {symbol: [(most_recent_date, most_recent_pe), 
           (prev_date, prev_pe), 
           (six_mos_date, six_mos_pe), 
           (nine_mos_date, nine_mos_pe),
            (yr_ago_date, yr_ago_pe)]]
      }

    '''

    dict = {}
    
    for symbol in symbol_list:
        most_recent_date, most_recent_pe, prev_date, prev_pe, six_mos_date, six_mos_pe, \
        nine_mos_date, nine_mos_pe, yr_ago_date, yr_ago_pe = pull_pe(symbol)
        dict[symbol] = [(most_recent_date, most_recent_pe), (prev_date, prev_pe), \
                        (six_mos_date, six_mos_pe), (nine_mos_date, nine_mos_pe), \
                        (yr_ago_date, yr_ago_pe)]
    
    return dict     


def pull_rev_list(symbol_list):
   
    '''
    returns dictionary with following structure:
    {symbol: [last_annual_rev, prev_yr_annual_rev, two_yrs_ago_rev]}
    
    Uses Yahoo! Finance Revenue; use only if pull_rev_and_ni_list function
    (which uses Zacks.com) doesn't return a value
    
    '''
    dict = {}
    
    for symbol in symbol_list:
        last_annual_rev, prev_yr_annual_rev, two_yrs_ago_rev = pull_yahoo_rev(symbol)
        dict[symbol] = [last_annual_rev, prev_yr_annual_rev, two_yrs_ago_rev]
        
    return dict


def pull_curr_ratio_list(symbol_list):
    
    '''
    returns two most recent annual current ratios as a dictionary with 
    following structure: 
    {symbol: [(most_recent_date, most_recent_curr_ratio), (prev_date, prev_curr_ratio)]}
    
    '''
    
    dict = {}
    
    for symbol in symbol_list:
        most_recent_date, most_recent_curr_ratio, prev_date, prev_curr_ratio = pull_current_ratios(symbol)
        dict[symbol] = [(most_recent_date, most_recent_curr_ratio),(prev_date, prev_curr_ratio)]
        
    return dict


def pull_rev_and_ni_list(symbol_list):
    
    '''
    returns Annual Revenu and Net Income for last 3 annual reports.
    Structure is as follows: 
    {symbol: [(most_recent_date, most_recent_rev, most_recent_ni), 
              (yr_ago_date, yr_ago_rev, yr_ago_ni), 
              (2yrs_ago_date, 2yrs_ago_rev, 2yrs_ago_ni)]}
    
    '''   
    dict = {}
    for symbol in symbol_list:
        lst = pull_annual_rev_and_ni(symbol)
        dict[symbol] = lst
    return dict



def pull_pe_list(stocks):
    '''
    
    Parameters
    ----------
    stocks : a list of stock tickers 

    Returns
    -------
    dict : {stock name: [[date, stock price, EPS, P/E, E/P]]}.
    
    NOTE: list of lists for each stock ticker includes 7 most recent quarterly
    results for price, EPS, P/E and E/P

    '''
         
    dict = {}
    count = 0 
    for stock in stocks:
        count += 1
        dict[stock] = pull_pe_and_ep(stock)
        if count == 10: # after 10 pulls, waits 4 seconds before resuming
            print("...10 pulls complete, pausing for 5 seconds...")
            time.sleep(5)
            count = 0 
    return dict 


def fix_date_if_weekend(date_given):
    
    '''
    Checks if date is a Saturday or Sunday.  If it is, it subtracts
    date to be the previous Friday (one or two days earlier)
    '''
    
    d = date_given.weekday()
    if d < 5: #date is a weekday
        return date_given
    elif d == 5: #Saturday
        return date_given - timedelta(days = 1)
    elif d == 6: #Sunday
        return date_given - timedelta(days = 2)
    
def str_to_date(date_string):
    '''
    changes date string in format DD/MM/YYYY to proper datetime object
    NOTE: this is different than previous function called str_to_date_yy which
    looks for strings in the format DD/MM/YY
    '''
    
    return datetime.strptime(date_string, '%m/%d/%Y')


def get_price_change(symbol, beg_date, days_to_add):
    
    '''
    Returns stock price difference for given symbol between the
    start_date and date after days_to_add is added to start_date.
    Uses Yahoo Finance library. 
    Assumes dates are given as strings in format MM/DD/YYYY.
    Returns begining stock price, ending stock price and difference.
    '''
    
    stock = yf.Ticker(symbol)
    
    start_date = fix_date_if_weekend(str_to_date(beg_date))
    end_date = fix_date_if_weekend(start_date + timedelta(days = days_to_add))
    
    try:
        beg_price_df = stock.history(start = start_date, end = start_date + timedelta(days = 1))
        beg_price = float(beg_price_df['Close'])
    except:
        beg_price = None
    
    try:
        end_price_df = stock.history(start = end_date, end = end_date + timedelta(days = 1))
        end_price = float(end_price_df['Close'])
    except:
        end_price = None
    
    try:
        change = end_price / beg_price
    except TypeError:
        change = None
        
    return beg_price, end_price, change
