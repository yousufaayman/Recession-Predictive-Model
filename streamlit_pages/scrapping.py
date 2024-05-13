from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException, StaleElementReferenceException
import threading
from datetime import datetime, date
import time
import streamlit as st


def twitterScrapper(link, credentials, searchFilter, dataSet): 
    lock = threading.Lock()
    st.error('Scraping already initiated.')   
    driverOpts = Options()

    driverOpts.headless = True
    
    driver = webdriver.Chrome(options=driverOpts)

    driver.get(link)
    try:
        # Login to twitter
        waitToLoad = WebDriverWait(driver, 20)
        waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="username"]'))).send_keys(credentials[0])
        driver.find_element(By.XPATH, ("//*[contains(text(), 'Next')]")).click();
        waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="current-password"]'))).send_keys(credentials[1])
        waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button'][role='button']"))).click()
        
        #Add Search Filter
        searchBar = waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='SearchBox_Search_Input'][role='combobox']")))
        searchBar.send_keys(searchFilter)
        searchBar.send_keys(Keys.ENTER)
        
        # Sort by Latest
        latestTab = waitToLoad.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]//*[contains(text(), 'Latest')]")))
        latestTab.click()
        
        #Scrapping Tweets
        scrappedUserNames = []
        scrappedTweets = []
        scrappedTweetDate = []

        prevHeight = driver.execute_script('return document.body.scrollHeight')

        while True:
            time.sleep(10)

            users = driver.find_elements(By.XPATH, ("//div[@data-testid='User-Name']/div[1]/div[1]/a"))
            tweets = driver.find_elements(By.XPATH, ("//div[@data-testid='tweetText']"))
            tweetDates = driver.find_elements(By.XPATH, ("//div[@data-testid='User-Name']/div[2]/div[1]/div[3]/a/time"))
            
            for user in users:
                scrappedUserNames.append(user.text)
                
            for tweet in tweets:
                scrappedTweets.append(tweet.text)
                
            for date in tweetDates:
                scrappedTweetDate.append(date.text)

            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            currentHeight = driver.execute_script('return document.body.scrollHeight')

            if (currentHeight == prevHeight):
                break
            
            prevHeight = currentHeight
            
    except NoSuchWindowException:
          print("Selenium window closed unexpectedly.")
    
    except StaleElementReferenceException:
            pass
        
    finally:
        driver.close()
        with lock:
            for username, tweet, date in zip(scrappedUserNames, scrappedTweets, scrappedTweetDate):
                dataSet[username] = [tweet, date]
        print("Scrapping is Completed")


def app():

    st.header("⛏️ Scrapping Data")
    st.image("imgs/how-to-scrape-twitter_banner_light.svg")
    st.write("""    
                Data scraping was done through the use of selenium. Selenium was chosen over other scraping 
                tools as it offered dynamic scrapping and active interaction with websites which is integral 
                to scraping social media websites as they are primarily structured around elements being 
                dynamically loaded into and out of the DOM.
            """) 

    ###########################Twitter Scrapper init
    if 'threads_running' not in st.session_state:
        st.session_state.threads_running = False
    if st.checkbox('Show Scrapping Code:'):
            twitterScrapperCode = """
            lock = threading.Lock()
            def twitterScrapper(link, credentials, searchFilter, dataSet):    
                driverOpts = Options()

                driverOpts.headless = True
                
                driver = webdriver.Chrome(options=driverOpts)

                driver.get(link)
                try:
                    # Login to twitter
                    waitToLoad = WebDriverWait(driver, 20)
                    waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="username"]'))).send_keys(credentials[0])
                    driver.find_element(By.XPATH, ("//*[contains(text(), 'Next')]")).click();
                    waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="current-password"]'))).send_keys(credentials[1])
                    waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button'][role='button']"))).click()
                    
                    #Add Search Filter
                    searchBar = waitToLoad.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='SearchBox_Search_Input'][role='combobox']")))
                    searchBar.send_keys(searchFilter)
                    searchBar.send_keys(Keys.ENTER)
                    
                    # Sort by Latest
                    latestTab = waitToLoad.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]//*[contains(text(), 'Latest')]")))
                    latestTab.click()
                    
                    #Scrapping Tweets
                    scrappedUserNames = []
                    scrappedTweets = []
                    scrappedTweetDate = []

                    prevHeight = driver.execute_script('return document.body.scrollHeight')

                    while True:
                        time.sleep(10)

                        users = driver.find_elements(By.XPATH, ("//div[@data-testid='User-Name']/div[1]/div[1]/a"))
                        tweets = driver.find_elements(By.XPATH, ("//div[@data-testid='tweetText']"))
                        tweetDates = driver.find_elements(By.XPATH, ("//div[@data-testid='User-Name']/div[2]/div[1]/div[3]/a/time"))
                        
                        for user in users:
                            scrappedUserNames.append(user.text)
                            
                        for tweet in tweets:
                            scrappedTweets.append(tweet.text)
                            
                        for date in tweetDates:
                            scrappedTweetDate.append(date.text)

                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        currentHeight = driver.execute_script('return document.body.scrollHeight')

                        if (currentHeight == prevHeight):
                            break
                        
                        prevHeight = currentHeight
                        
                except NoSuchWindowException:
                    print("Selenium window closed unexpectedly.")
                
                except StaleElementReferenceException:
                        pass
                    
                finally:
                    driver.close()
                    with lock:
                        for username, tweet, date in zip(scrappedUserNames, scrappedTweets, scrappedTweetDate):
                            dataSet[username] = [tweet, date]
                    print("Scrapping is Completed")

            """
            st.code(twitterScrapperCode, language='python')

    st.subheader("🧵 Parallel Scraping and Multi Threading")
    st.write("""    
            Utilizing the concept of multithreading and python's "threading" library, I was able to scrape data 
            concurrently from different pages which not only significantly improved the program's performance, 
            but also allowed for the use of different accounts for scrapping to avoid detection. Concepts such as 
            locks were utilized in order to prevent any data corruption, loss, or race conditions from occuring. 
            """)

    min_date = date(2006, 1, 1)
    max_date = date.today()
    start_date, end_date = st.slider(
        "Select a date range to scrap data from",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )   

    if st.button('Run Scrapper Demo', disabled=st.session_state.threads_running):
        if not st.session_state.threads_running:
            st.session_state.threads_running = True
            st.empty()
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')    
            startDate = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            endDate = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            st.write(f"Start Date: {startDate}")
            st.write(f"End Date: {endDate}")

            twitterCredentials =[["ScrpperR16322", "Test8dcln"]]
            linkTwitter = "https://twitter.com/i/flow/login"
            scrappedTwitterData = {}
            searchFilter = [
                f'("business confidence" OR "economic growth" OR "fiscal policy" OR "monetary policy" OR "interest rates" OR "income inequality" OR "financial stability" OR "labor market" OR "economic indicators" OR "economic recovery" OR "cost of living") until:{endDate} since:{startDate} -filter:links -filter:replies -from:MARKET_JP',
                f'("economy" OR "economic" OR "job market" OR "unemployment" OR "inflation" OR "recession" OR "stock market" OR "GDP" OR "consumer spending") until:{endDate} since:{startDate} -filter:links -filter:replies -from:MARKET_JP'
            ]   
            threads=[]
            
            for i in range(2):
                    th = threading.Thread(target=twitterScrapper, args=(linkTwitter, twitterCredentials[0], searchFilter[i], scrappedTwitterData))
                    threads.append(th)
                    th.start()
            for thread in threads:
                thread.join()
                
            st.session_state.threads_running = False
            