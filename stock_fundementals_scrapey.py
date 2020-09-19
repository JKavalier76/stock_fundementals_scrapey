import requests
import bs4
from datetime import date, timedelta
from datetime import datetime
import yfinance as yf


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

def clean_pe(soup_str):
    '''
    Strips Soup string of everything but the P/E
    '''
    try:
        clean_split = soup_str.split()
        clean = clean_split[-1].split('>')[-2].split('<')[-2]
        if clean == '':
            clean = 1999 #assign very high P/E if stock is unprofitable 
    except:
        clean = None
        
    return clean    

def pull_pe(symbol):
    '''
    Pulls Trailing P/E for symbols for most up to 5 past quarterly results
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
    Pulls Revenue from last 3 available Annual Income Statements
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
        ni_list.append(ni)
        
    date_list = [] #pulls Dates
    for i in range(2,5):
        date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1)'\
                                    ' > tr:nth-child(1) > th:nth-child(' + str(i) + ')'))
        try:
            date = date_elem.split('>')[-2].split('<')[-2]
        except:
            date = None
        date_list.append(date)
        
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
        rev_list.append(rev)
        
        z = zip(date_list, rev_list, ni_list)
        lst = list(z)
              
    return lst


def pull_pe_list(symbol_list):
    
    '''
    Returns dictionary of up to a year's worth of trailing P/E ratios from 
    quarterly reports.
    
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
    returns two most recent annual current ratios as a dictionary with following structure: 
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
    '''
    
    return datetime.strptime(date_string, '%m/%d/%Y')


def get_price_change(symbol, beg_date, days_to_add):
    
    '''
    Returns stock price difference for given symbol between the
    start_date and date after days_to_add is added to start_date.
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
