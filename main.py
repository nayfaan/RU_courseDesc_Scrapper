import services.startDriver
from services.startDriver import *
import csv
import time

def initiate_driver(driver, url):
    driver.get(url)
    
def output_csv(desc):
    with open('output/course_desc.csv', 'w', newline='') as csvfile:
        output = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in desc:
            output.writerow([row])
            print(row)

def scrap(driver,url):
    
    course_desc = []
    find_tag = "div#courseProfileOfficialCourseDescription"
    
    try:
        for row in url:
            if row[0]:
                driver.get(row[0])
                #WebDriverWait(driver, timeout=120).until(ec.visibility_of_element_located((By.CSS_SELECTOR, find_tag)))
                course_desc_inner = driver.find_elements_by_css_selector(find_tag+" p")
                if course_desc_inner:
                    course_desc_inner = course_desc_inner[0].get_attribute("innerHTML")
                else:
                    course_desc_inner = driver.find_elements_by_css_selector(find_tag)[0].get_attribute("innerHTML").replace("<h2>Course Description</h2>","").replace("<p>","").replace("</p>","")
                course_desc.append(course_desc_inner.strip())
            else:
                course_desc.append("")
    finally:
        output_csv(course_desc)
    
def run():
    course_url=[]
    
    with open('./input/course_url.csv', newline='') as csvfile:
        url_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for row in url_csv:
            if row:
                course_url.append(row)
            else:
                course_url.append([''])
    
    driver = services.startDriver.start()
    initiate_driver(driver, "https://www.google.com/")
    
    try:
        scrap(driver,course_url)
    except:
        pass
    finally:
        driver.close()

if __name__ == "__main__":
    run()
