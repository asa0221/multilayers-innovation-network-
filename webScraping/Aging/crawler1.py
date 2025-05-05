import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Set your login credentials
username = "your_username"
password = "your_password"

# Initialize the Chrome driver
driver = webdriver.Chrome()
driver.get("https://konexons.com/login")  # Replace with the login URL

# Automate Login
input("click after page loaded")

# Find the username and password fields and login button by their IDs
username_field = driver.find_element(By.ID, "UserId")  # Replace with the actual element identifier
password_field = driver.find_element(By.ID, "Password")  # Replace with the actual element identifier
login_button = driver.find_element(By.ID, "loginbtn")  # Replace with the actual element identifier

username_field.send_keys('asa_8_1@qq.com')
password_field.send_keys('20020220@Q@k')
login_button.click()

# Set the URL you want to navigate to
base_url = "https://konexons.com/opportunities"

# Navigate to the specified URL
input("click after logged in")
driver.get(base_url)

table = [
    {
        "ID": 2081,
        "Name": "AccelerateKY Connect. Inform. Inspire"
    },
    {
        "ID": 11214,
        "Name": "Aging2.0 | Adelaide, AUS"
    },
    {
        "ID": 11220,
        "Name": "Aging2.0 | Alameda, CA"
    },
    {
        "ID": 11221,
        "Name": "Aging2.0 | Albany, NY"
    },
    {
        "ID": 11696,
        "Name": "Aging2.0 | Alberta, CAN"
    },
    {
        "ID": 11222,
        "Name": "Aging2.0 | Almendralejo, Spain"
    },
    {
        "ID": 11223,
        "Name": "Aging2.0 | Amsterdam, NLD"
    },
    {
        "ID": 11225,
        "Name": "Aging2.0 | Ancona, ITA"
    },
    {
        "ID": 11697,
        "Name": "Aging2.0 | Asia Pacific"
    },
    {
        "ID": 11593,
        "Name": "Aging2.0 | Asuncion, PRY"
    },
    {
        "ID": 8275,
        "Name": "Aging2.0 | Atlanta, GA "
    },
    {
        "ID": 8276,
        "Name": "Aging2.0 | Austin, TX"
    },
    {
        "ID": 11698,
        "Name": "Aging2.0 | Australia"
    },
    {
        "ID": 11594,
        "Name": "Aging2.0 | Baltimore, MD"
    },
    {
        "ID": 11595,
        "Name": "Aging2.0 | Bangkok, THA"
    },
    {
        "ID": 11226,
        "Name": "Aging2.0 | Barcelona, ESP"
    },
    {
        "ID": 11596,
        "Name": "Aging2.0 | Baton Rouge, LA"
    },
    {
        "ID": 11597,
        "Name": "Aging2.0 | Beijing, CHN"
    },
    {
        "ID": 11227,
        "Name": "Aging2.0 | Bengaluru, IND"
    },
    {
        "ID": 11699,
        "Name": "Aging2.0 | Berkeley, CA"
    },
    {
        "ID": 11617,
        "Name": "Aging2.0 | Berlin, DEU"
    },
    {
        "ID": 9114,
        "Name": "Aging2.0 | Bilbao, ESP"
    },
    {
        "ID": 11700,
        "Name": "Aging2.0 | Bogota, COL"
    },
    {
        "ID": 11618,
        "Name": "Aging2.0 | Boise, ID"
    },
    {
        "ID": 11228,
        "Name": "Aging2.0 | Bologna, ITA"
    },
    {
        "ID": 8277,
        "Name": "Aging2.0 | Boston, MA"
    },
    {
        "ID": 11229,
        "Name": "Aging2.0 | Brasília, BRA"
    },
    {
        "ID": 11620,
        "Name": "Aging2.0 | Brescia, ITA"
    },
    {
        "ID": 11623,
        "Name": "Aging2.0 | Brighton, ENG"
    },
    {
        "ID": 11349,
        "Name": "Aging2.0 | Brisbane, AUS"
    },
    {
        "ID": 11350,
        "Name": "Aging2.0 | Brussels, BEL"
    },
    {
        "ID": 11626,
        "Name": "Aging2.0 | Budapest, HUN"
    },
    {
        "ID": 8278,
        "Name": "Aging2.0 | Buenos Aires, ARG"
    },
    {
        "ID": 11701,
        "Name": "Aging2.0 | Calgary, CAN"
    },
    {
        "ID": 11230,
        "Name": "Aging2.0 | Cambridge, MA"
    },
    {
        "ID": 8279,
        "Name": "Aging2.0 | Cambridge, UK"
    },
    {
        "ID": 11628,
        "Name": "Aging2.0 | Cape Cod, MA"
    },
    {
        "ID": 11630,
        "Name": "Aging2.0 | Cape Town, ZAF"
    },
    {
        "ID": 11631,
        "Name": "Aging2.0 | Cedar Rapids, IA"
    },
    {
        "ID": 11702,
        "Name": "Aging2.0 | Central City, CO"
    },
    {
        "ID": 11231,
        "Name": "Aging2.0 | Central Coast, AUS"
    },
    {
        "ID": 11632,
        "Name": "Aging2.0 | Chardon, OH"
    },
    {
        "ID": 11633,
        "Name": "Aging2.0 | Charleston, SC"
    },
    {
        "ID": 11232,
        "Name": "Aging2.0 | Charlotte, NC"
    },
    {
        "ID": 11233,
        "Name": "Aging2.0 | Chennai, IND"
    },
    {
        "ID": 11234,
        "Name": "Aging2.0 | Chicago, IL"
    },
    {
        "ID": 11634,
        "Name": "Aging2.0 | Cincinnati, OH"
    },
    {
        "ID": 11235,
        "Name": "Aging2.0 | Coimbatore, IND"
    },
    {
        "ID": 8281,
        "Name": "Aging2.0 | Colorado Springs, CO"
    },
    {
        "ID": 11236,
        "Name": "Aging2.0 | Copenhagen, DNK"
    },
    {
        "ID": 11237,
        "Name": "Aging2.0 | Curitiba, BRA"
    },
    {
        "ID": 11238,
        "Name": "Aging2.0 | Dallas, TX"
    },
    {
        "ID": 11239,
        "Name": "Aging2.0 | Delhi, IND"
    },
    {
        "ID": 8282,
        "Name": "Aging2.0 | Denver, CO"
    },
    {
        "ID": 11635,
        "Name": "Aging2.0 | Detroit, MI"
    },
    {
        "ID": 11240,
        "Name": "Aging2.0 | Dublin, IRL"
    },
    {
        "ID": 8283,
        "Name": "Aging2.0 | Durham, NC"
    },
    {
        "ID": 11241,
        "Name": "Aging2.0 | Edmond, OK"
    },
    {
        "ID": 11703,
        "Name": "Aging2.0 | Eindhoven, NLD"
    },
    {
        "ID": 11242,
        "Name": "Aging2.0 | Fort Lauderdale, FL"
    },
    {
        "ID": 11705,
        "Name": "Aging2.0 | Grand Rapids, MI"
    },
    {
        "ID": 11243,
        "Name": "Aging2.0 | Greater Philadelphia, PA"
    },
    {
        "ID": 8284,
        "Name": "Aging2.0 | Greater Salt Lake City, UT"
    },
    {
        "ID": 8285,
        "Name": "Aging2.0 | Greater St.George, UT"
    },
    {
        "ID": 11351,
        "Name": "Aging2.0 | Greenwich, CT"
    },
    {
        "ID": 11352,
        "Name": "Aging2.0 | Gulf Coast"
    },
    {
        "ID": 11353,
        "Name": "Aging2.0 | Halifax,CAN"
    },
    {
        "ID": 11636,
        "Name": "Aging2.0 | Helsinki, FIN"
    },
    {
        "ID": 11354,
        "Name": "Aging2.0 | Hong Kong"
    },
    {
        "ID": 11355,
        "Name": "Aging2.0 | Houston,TX"
    },
    {
        "ID": 11244,
        "Name": "Aging2.0 | Hyderabad, IND"
    },
    {
        "ID": 11245,
        "Name": "Aging2.0 | India"
    },
    {
        "ID": 11356,
        "Name": "Aging2.0 | Indianapolis"
    },
    {
        "ID": 11357,
        "Name": "Aging2.0 | Istanbul"
    },
    {
        "ID": 11345,
        "Name": "Aging2.0 | Jacksonville, FL"
    },
    {
        "ID": 11246,
        "Name": "Aging2.0 | Kansas City, MO"
    },
    {
        "ID": 11358,
        "Name": "Aging2.0 | La Paz, BOL"
    },
    {
        "ID": 11248,
        "Name": "Aging2.0 | Lausanne, CHE"
    },
    {
        "ID": 11250,
        "Name": "Aging2.0 | Lima, PER"
    },
    {
        "ID": 11251,
        "Name": "Aging2.0 | Lisbon, PRT"
    },
    {
        "ID": 8289,
        "Name": "Aging2.0 | London, UK"
    },
    {
        "ID": 11637,
        "Name": "Aging2.0 | Long Island, NY"
    },
    {
        "ID": 11252,
        "Name": "Aging2.0 | Los Angeles, CA"
    },
    {
        "ID": 11253,
        "Name": "Aging2.0 | Los Gatos, CA"
    },
    {
        "ID": 8410,
        "Name": "Aging2.0 | Louisville, KY"
    },
    {
        "ID": 11706,
        "Name": "Aging2.0 | Maastricht, NDL"
    },
    {
        "ID": 11638,
        "Name": "Aging2.0 | Madison, WI"
    },
    {
        "ID": 11359,
        "Name": "Aging2.0 | Madrid, ESP"
    },
    {
        "ID": 9115,
        "Name": "Aging2.0 | Maine"
    },
    {
        "ID": 9721,
        "Name": "Aging2.0 | Manaus, BR"
    },
    {
        "ID": 11254,
        "Name": "Aging2.0 | Melbourne, AUS"
    },
    {
        "ID": 11360,
        "Name": "Aging2.0 | Memphis, TN"
    },
    {
        "ID": 11263,
        "Name": "Aging2.0 | Merida, ESP"
    },
    {
        "ID": 11264,
        "Name": "Aging2.0 | Mexico City, NAM"
    },
    {
        "ID": 11707,
        "Name": "Aging2.0 | Miami, FL"
    },
    {
        "ID": 11265,
        "Name": "Aging2.0 | Milan, ITA"
    },
    {
        "ID": 8291,
        "Name": "Aging2.0 | Minneapolis, MN"
    },
    {
        "ID": 11266,
        "Name": "Aging2.0 | Mombasa, KEN"
    },
    {
        "ID": 11639,
        "Name": "Aging2.0 | Montreal, CAN"
    },
    {
        "ID": 11187,
        "Name": "Aging2.0 | Nashville, TN"
    },
    {
        "ID": 11267,
        "Name": "Aging2.0 | New Brunswick, CAN"
    },
    {
        "ID": 11268,
        "Name": "Aging2.0 | New Haven, CT"
    },
    {
        "ID": 11361,
        "Name": "Aging2.0 | New York, NY"
    },
    {
        "ID": 11269,
        "Name": "Aging2.0 | New Zealand"
    },
    {
        "ID": 11270,
        "Name": "Aging2.0 | Newcastle, GBR"
    },
    {
        "ID": 11362,
        "Name": "Aging2.0 | Northern British Columbia"
    },
    {
        "ID": 11640,
        "Name": "Aging2.0 | Notre Dame Village"
    },
    {
        "ID": 11708,
        "Name": "Aging2.0 | Nova Scotia, CAN"
    },
    {
        "ID": 11641,
        "Name": "Aging2.0 | Oklahoma City, OK"
    },
    {
        "ID": 11271,
        "Name": "Aging2.0 | Omaha, NE"
    },
    {
        "ID": 8292,
        "Name": "Aging2.0 | Orange County, CA"
    },
    {
        "ID": 11642,
        "Name": "Aging2.0 | Orlando, FL"
    },
    {
        "ID": 11363,
        "Name": "Aging2.0 | Palm Springs"
    },
    {
        "ID": 8293,
        "Name": "Aging2.0 | Palo Alto, CA"
    },
    {
        "ID": 11296,
        "Name": "Aging2.0 | Panama, NAM"
    },
    {
        "ID": 11272,
        "Name": "Aging2.0 | Paraguay, SAM"
    },
    {
        "ID": 11273,
        "Name": "Aging2.0 | Paris, FRA"
    },
    {
        "ID": 8294,
        "Name": "Aging2.0 | Philadelphia, PA"
    },
    {
        "ID": 8295,
        "Name": "Aging2.0 | Phoenix, AZ"
    },
    {
        "ID": 11643,
        "Name": "Aging2.0 | Pittsburgh, PA"
    },
    {
        "ID": 11274,
        "Name": "Aging2.0 | Portland, OR"
    },
    {
        "ID": 11276,
        "Name": "Aging2.0 | Prague, CZE"
    },
    {
        "ID": 11277,
        "Name": "Aging2.0 | Providence, RI"
    },
    {
        "ID": 11278,
        "Name": "Aging2.0 | Ribeirao Preto, BRA"
    },
    {
        "ID": 11279,
        "Name": "Aging2.0 | Richmond, VA"
    },
    {
        "ID": 11281,
        "Name": "Aging2.0 | Rio de Janeiro, BRA"
    },
    {
        "ID": 11282,
        "Name": "Aging2.0 | Rome, ITA"
    },
    {
        "ID": 11283,
        "Name": "Aging2.0 | Sacramento, CA"
    },
    {
        "ID": 11644,
        "Name": "Aging2.0 | Salvador, BRA"
    },
    {
        "ID": 11645,
        "Name": "Aging2.0 | San Antonio, TX"
    },
    {
        "ID": 8296,
        "Name": "Aging2.0 | San Diego, CA"
    },
    {
        "ID": 8297,
        "Name": "Aging2.0 | San Francisco, CA"
    },
    {
        "ID": 11364,
        "Name": "Aging2.0 | Santa Barbara"
    },
    {
        "ID": 69159,
        "Name": "Aging2.0 | Santiago"
    },
    {
        "ID": 8298,
        "Name": "Aging2.0 | Sao Paulo, BR"
    },
    {
        "ID": 11646,
        "Name": "Aging2.0 | Seattle, WA"
    },
    {
        "ID": 11365,
        "Name": "Aging2.0 | Seville, ESP"
    },
    {
        "ID": 11709,
        "Name": "Aging2.0 | Shanghai, CHN"
    },
    {
        "ID": 11647,
        "Name": "Aging2.0 | Silicon Valley, CA"
    },
    {
        "ID": 11648,
        "Name": "Aging2.0 | Singapore, SGP"
    },
    {
        "ID": 11710,
        "Name": "Aging2.0 | South Africa"
    },
    {
        "ID": 11711,
        "Name": "Aging2.0 | South American Region"
    },
    {
        "ID": 11366,
        "Name": "Aging2.0 | South Central PA"
    },
    {
        "ID": 11289,
        "Name": "Aging2.0 | St. Louis, MO"
    },
    {
        "ID": 63253,
        "Name": "Aging2.0 | Stanford, CA"
    },
    {
        "ID": 9130,
        "Name": "Aging2.0 | Stockholm, SWE"
    },
    {
        "ID": 8299,
        "Name": "Aging2.0 | Sunnyvale, CA"
    },
    {
        "ID": 11291,
        "Name": "Aging2.0 | Sydney, AUS"
    },
    {
        "ID": 11649,
        "Name": "Aging2.0 | Taipei, TWN"
    },
    {
        "ID": 11292,
        "Name": "Aging2.0 | Tel Aviv, ISR"
    },
    {
        "ID": 11713,
        "Name": "Aging2.0 | The Collective - GIS"
    },
    {
        "ID": 11293,
        "Name": "Aging2.0 | Tokyo, JPN"
    },
    {
        "ID": 9722,
        "Name": "Aging2.0 | Toronto, CAN"
    },
    {
        "ID": 11294,
        "Name": "Aging2.0 | Treviso, ITA"
    },
    {
        "ID": 11650,
        "Name": "Aging2.0 | Tri-Valley, CA"
    },
    {
        "ID": 11367,
        "Name": "Aging2.0 | Tucson, AZ"
    },
    {
        "ID": 11295,
        "Name": "Aging2.0 | Valencia, ESP"
    },
    {
        "ID": 8300,
        "Name": "Aging2.0 | Vancouver, CAN"
    },
    {
        "ID": 11368,
        "Name": "Aging2.0 | Victoria, CAN"
    },
    {
        "ID": 11369,
        "Name": "Aging2.0 | Vienna, AUT"
    },
    {
        "ID": 11370,
        "Name": "Aging2.0 | Washington DC"
    },
    {
        "ID": 11372,
        "Name": "Aging2.0 | Westchester"
    },
    {
        "ID": 8301,
        "Name": "Aging2.0 | Winnipeg, CAN"
    },
    {
        "ID": 8302,
        "Name": "Aging2.0 | Zurich, CH"
    },
    {
        "ID": 4256,
        "Name": "Aging2.0 Global Innovation Search 2022"
    },
    {
        "ID": 64609,
        "Name": "Aging2.0 Global Innovation Search 2023"
    },
    {
        "ID": 5751,
        "Name": "AGING2.0 Main"
    },
    {
        "ID": 2926,
        "Name": "Ashland, KY"
    },
    {
        "ID": 2930,
        "Name": "Berea, KY"
    },
    {
        "ID": 2911,
        "Name": "Bowling Green, KY"
    },
    {
        "ID": 7188,
        "Name": "Capital Connections"
    },
    {
        "ID": 70514,
        "Name": "Capital Connections 2023"
    },
    {
        "ID": 7193,
        "Name": "CareTech 2022"
    },
    {
        "ID": 64610,
        "Name": "CareTech Pitch 2023"
    },
    {
        "ID": 998,
        "Name": "CEOc"
    },
    {
        "ID": 2924,
        "Name": "Corbin, KY"
    },
    {
        "ID": 1110,
        "Name": "Derby City Angels"
    },
    {
        "ID": 2922,
        "Name": "Elizabethtown, KY"
    },
    {
        "ID": 1145,
        "Name": "Healthcare Venture Challenge"
    },
    {
        "ID": 2812,
        "Name": "Hopewell Labs"
    },
    {
        "ID": 826,
        "Name": "Kentucky"
    },
    {
        "ID": 3350,
        "Name": "Knoxville"
    },
    {
        "ID": 1080,
        "Name": "LEAP"
    },
    {
        "ID": 2923,
        "Name": "Lexington, KY"
    },
    {
        "ID": 827,
        "Name": "Louisville, KY"
    },
    {
        "ID": 9052,
        "Name": "Med10VC"
    },
    {
        "ID": 7942,
        "Name": "Metals Innovation Initiative (MI2)"
    },
    {
        "ID": 2899,
        "Name": "Morehead Space Science Center"
    },
    {
        "ID": 2929,
        "Name": "Murray, KY"
    },
    {
        "ID": 2928,
        "Name": "Northern Kentucky"
    },
    {
        "ID": 8750,
        "Name": "Optimize 2022"
    },
    {
        "ID": 2927,
        "Name": "Owensboro, KY"
    },
    {
        "ID": 2925,
        "Name": "Paducah, KY"
    },
    {
        "ID": 2921,
        "Name": "Pikeville, KY"
    },
    {
        "ID": 7916,
        "Name": "Prayer Warriors Monday Morning"
    },
    {
        "ID": 11551,
        "Name": "Russell Technology Business Incubator (RTBI)"
    },
    {
        "ID": 1305,
        "Name": "Sheltowee Angel Network"
    },
    {
        "ID": 1071,
        "Name": "Sheltowee Business Network"
    },
    {
        "ID": 2843,
        "Name": "Sheltowee Christian Entrepreneurs"
    },
    {
        "ID": 1306,
        "Name": "Sheltowee Network"
    },
    {
        "ID": 1304,
        "Name": "Sheltowee Venture Fund"
    },
    {
        "ID": 3594,
        "Name": "University of Kentucky"
    },
    {
        "ID": 2908,
        "Name": "University of Louisville"
    },
    {
        "ID": 2907,
        "Name": "Western Kentucky University "
    }
]
for community in table:
    csv_filename = community["Name"]
    # Use a context manager to open the CSV file
    with open(csv_filename + '.csv', mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["CoName", "Tag", "Introduction", "Network", "Stage", "Location",
                             "Industry_Type", "Founding", "Incorporation_Type", "Website", "Description", "Address"])

        base = "https://konexons.com/opportunities/mid/393?qf="
        pages = 0
        while True:
            pages +=1
            url = base + str(community["ID"]) + "&pageno=" + str(pages)
            print(url)
            time.sleep(3)
            driver.get(url)
            # Initialize BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            opportunities = soup.find_all("li", class_="member")
            if len(opportunities) == 0:
                print("No more opportunities found. Exiting the loop.")
                break  # Exit the loop when no opportunities are found
            for opportunity in opportunities:
                try:
                    detail_link  = opportunity.find("a").get("href")
                    print(detail_link)
                    time.sleep(2)
                    driver.get("https://konexons.com/"+detail_link)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    Resource_Info = soup.find("div", class_="resource-info")
                    print('==============')
                    coname = Resource_Info.find("h4").text.strip()
                    print(coname)
                    print('-------------')
                    introduction = Resource_Info.find("p").text.strip()
                    print(introduction)
                    tag = soup.find("span", class_="member-tags").text.strip()
                    print(tag)
                    network = community["Name"]
                    Table = soup.find("div", class_="resource-table")
                    table = Table.find("table")
                    values = []
                    for row in table.find("tbody").find_all("tr"):
                        # Find the second <td> element (index 1) within the <tr>
                        value = row.find_all("td")[1].text.strip()
                        values.append(value)
                    stage = values[0]
                    print(stage)
                    location = values[1]
                    print(location)
                    industry_type = values[2]
                    print(industry_type)
                    founding = values[3]
                    print(founding)
                    incorporation_type = values[4]
                    print(incorporation_type)
                    website = values[5]
                    print(website)
                    description_div = soup.find("div", class_="resoruces-description")
                    if description_div:  # Check if the element is not None
                        p_elements = description_div.find_all('p')
                        description = "\n".join(p.text.strip() for p in p_elements)
                    else:
                        description = None
                    print(description)
                    address = "https://konexons.com/"+detail_link
                    print(address)
                    csv_writer.writerow([coname, tag, introduction, network, stage, location,
                                         industry_type, founding, incorporation_type, website, description, address])
                except Exception as e:
                    print(f"Error processing opportunity: {str(e)}")

                print("Data has been exported to", csv_filename)

# Close the Chrome driver
driver.quit()


