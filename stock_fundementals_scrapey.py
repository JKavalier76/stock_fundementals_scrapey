import requests
import bs4

def return_yahoo_stats_soup(symbol):
    '''
    Returns Beautiful Soup object for Yahoo Statistics page for given symbol
    Structure for URL is https://finance.yahoo.com/quote/AMZN/key-statistics where AMZN is symbol passed
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
    Returns Beautiful Soup object for Zacks income statements page (ANNUAL reports)
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



        

def pull_annual_ni(symbol):
    '''
    Pulls Net Income for last two available annual reports from zacks.com
    '''

    soup = return_zacks_soup(symbol)
           
    most_recent_ni_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(15) > td:nth-child(2) > span:nth-child(1) > a:nth-child(1)'))
    try:
        most_recent_ni = most_recent_ni_elem.split(">")[-2].split("<")[-2]
        if most_recent_ni != '':
            most_recent_ni += ',000' #add zeros since this site reports in millions instead of thousands
    except IndexError:
        most_recent_ni = None
        
       
    prev_yr_ni_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(15) > td:nth-child(3) > span:nth-child(1) > a:nth-child(1)'))
    try:
        prev_yr_ni = prev_yr_ni_elem.split(">")[-2].split("<")[-2]
        if prev_yr_ni != '':
            prev_yr_ni += ',000' #add zeros since this site reports in millions instead of thousands
    except IndexError:
        prev_yr_ni = None 
        
    most_recent_date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(2)'))
    prev_yr_date_elem = str(soup.select('#annual_income_statement > table:nth-child(3) > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(3)'))
    
    try:
        most_recent_date = most_recent_date_elem.split('>')[-2].split('<')[-2]
    except:
        most_recent_date = None
    
    try:
        prev_yr_date = prev_yr_date_elem.split('>')[-2].split('<')[-2]
    except:
        prev_yr_date = None
          
    return most_recent_date, most_recent_ni, prev_yr_date, prev_yr_ni

def pull_pe(symbol):
    '''
    Pulls Trailing P/E for symbols for most recent quarterly and 1-year old quarterly results
    If company does not have a report a year ago returns None
    '''
 
    soup = return_yahoo_stats_soup(symbol)
 
    yr_ago_pe_element = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(7)'))
    yr_ago_date_element = str(soup.select('th.Fw\(b\):nth-child(7) > span:nth-child(1)'))
    
    most_recent_pe_elem = str(soup.select('tr.fi-row:nth-child(3) > td:nth-child(3)'))
    most_recent_date_elem = str(soup.select('th.Fw\(b\):nth-child(3) > span:nth-child(1)'))
 
    date_available = False
    
    
    ## Get year ago quarterly report date
    try:
        yr_ago_date = yr_ago_date_element.split('>')[-2].split('<')[-2]
        date_available = True
    except IndexError:
        yr_ago_date = None
        print("No Yr-Ago data was available for symbol: " + symbol)
        
    ## get most recent quarterly report date
    try:
        most_recent_date = most_recent_date_elem.split('>')[-2].split('<')[-2]
        date_available = True
    except IndexError:
        most_recent_date = None
        print("No recent P/E data was available for symbol: " + symbol)   
    
    ## P/E from quarterly report one  year ago    
    try:
        yr_ago_pe_element_split = yr_ago_pe_element.split() #make element a string and split it by blanks
        yr_ago_pe = yr_ago_pe_element_split[-1].split('>')[-2].split('<')[-2] #finds Price/Earnings in CSS element
        if yr_ago_pe == '':
            yr_ago_pe = 1999 #assigns fake very high P/E because company was unprofitable at date
    except IndexError:
        yr_ago_pe = None
        
    ## P/E from most recent quarterly report 
    try:
        most_recent_element_split = most_recent_pe_elem.split() #make element a string and split it by blanks
        most_recent_pe = most_recent_element_split[-1].split('>')[-2].split('<')[-2] #finds Price/Earnings in CSS element
        if most_recent_pe == '':
            most_recent_pe = 999 #assigns fake very high P/E because company was unprofitable at date
    except IndexError:
        most_recent_pe = None
         
    return most_recent_date, most_recent_pe, yr_ago_date, yr_ago_pe


def pull_yahoo_rev(symbol):
    '''
    Pulls Revenue from last 2 available Annual Income Statements
    If company does not have a report a year ago returns None
    '''
 
    soup = return_yahoo_income_soup(symbol)
    
    most_recent_rev_elem = str(soup.select('.D\(tbrg\) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1)'))
    prev_yr_rev_elem = str(soup.select('.D\(tbrg\) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > span:nth-child(1)'))
    
  
    try:
        last_annual_rev = most_recent_rev_elem.split()[-1].split('>')[-2].split('<')[-2]
    except IndexError:
        last_annual_rev = 0
        
    try:
        prev_year_rev = prev_yr_rev_elem.split()[-1].split('>')[-2].split('<')[-2]
    except IndexError:
        prev_year_rev = 0       
     
    return last_annual_rev, prev_year_rev


def transform_ratio_soup(string):
    '''
    Little module that helps de-clutter code in the Current Ratio function.  Just strips unnecessary CSS
    text and returns the clean desired string from Zacks.com 
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


def pull_pe_list(symbol_list):
    '''
    returns dictionary with following structure: 
    {symbol: [(most_recent_date, most_recent_pe), (yr_ago_date, yr_ago_pe)]}
    
    '''
    
    dict = {}
    
    for symbol in symbol_list:
        most_recent_date, most_recent_pe, prev_yr_date, prev_yr_pe = pull_pe(symbol)
        dict[symbol] = [(most_recent_date, most_recent_pe), (prev_yr_date, prev_yr_pe)]
    
    return dict       


def pull_rev_list(symbol_list):
    '''
    returns dictionary with following structure:
    {symbol: [most_recent_annual_rev, prev_yr_annual_rev]}
    
    '''
    dict = {}
    
    for symbol in symbol_list:
        last_annual_rev, prev_yr_annual_rev = pull_yahoo_rev(symbol)
        dict[symbol] = [last_annual_rev, prev_yr_annual_rev]
        
    return dict


def pull_curr_ratio_list(symbol_list):
    '''
    returns two most recent annualcurrent ratios as a dictionary with following structure: 
    {symbol: [(most_recent_date, most_recent_curr_ratio), (prev_date, prev_curr_ratio)]}
    
    '''
    
    dict = {}
    
    for symbol in symbol_list:
        most_recent_date, most_recent_curr_ratio, prev_date, prev_curr_ratio = pull_current_ratios(symbol)
        dict[symbol] = [(most_recent_date, most_recent_curr_ratio),(prev_date, prev_curr_ratio)]
        
    return dict


def pull_ni_list(symbol_list):
    '''
    returns Annual Net Income dictionary with following structure: 
    {symbol: [(most_recent_date, most_recent_ni), (yr_ago_date, yr_ago_ni)]}
    
    '''
    
    dict = {}
    
    for symbol in symbol_list:
        most_recent_date, most_recent_ni, prev_yr_date, prev_yr_ni = pull_annual_ni(symbol)
        dict[symbol] = [(most_recent_date, most_recent_ni), (prev_yr_date, prev_yr_ni)]
    
    return dict      

