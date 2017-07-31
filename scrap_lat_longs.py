# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchWindowException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.alert import Alert
# import codecs


from selenium import webdriver
import time
import csv

with open('interviewed_raw.csv', 'r') as f:
    reader = csv.reader(f.read().splitlines(), delimiter = ',')
    data = [row for row in reader]

##############
filename = 'interviewed'
############

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.latlong.net/')

crash = 1
results = []
skipped = []
for i,row in enumerate(data[1:]):
    print i
    search = driver.find_element_by_id('gadres')
    search_term = row[2]
    search.clear()
    try:
        search.send_keys(search_term)
    except:
        print 'Skiped %s' %search_term
        print row
        skipped.append(row)
        continue

    search.submit()
    time.sleep(1)
    try:
        lat = driver.find_element_by_id('latlngspan')
    except:
        alert = driver.switch_to_alert()
        alert.accept()
        driver.switch_to_default_content()
        print 'Couldnt find %s' %search_term
        print row
        skipped.append(row)
        continue

    lat_long = lat.text.strip('() ').split(',')
    lat_long_clean = [float(n) for n in lat_long]

    try:
        driver.refresh()
    except:
        with open(filename + 'recovered' + '%i' %crash + '.csv' , "wb") as f:
            writer = csv.writer(f)
            writer.writerows(results)
        crash +=1

    print lat_long_clean
    r = row
    r.extend(lat_long_clean)
    r.insert(0, i)
    print r
    results.append(r)

    with open(filename + ".csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(r)

with open(filename + "complete.csv" , "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)