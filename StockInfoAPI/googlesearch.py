import httpx
import asyncio
from bs4 import BeautifulSoup
import json

class CompanyReport:
    
    def __init__(self, title, link, description, source = '', scrapedReport = ''):
        self.title  = title
        self.link = link
        self.description = description
        self.source = source
        self.scrapedReport = scrapedReport
    
    def to_json(self):
        report_dict = {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "source": self.source,
            "scrapedReport": self.scrapedReport
        }
        return json.dumps(report_dict)

organic_results:CompanyReport = []

async def get_organic_data(company_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4703.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        
        response = await client.get("https://www.google.com/search?q=crisil%2C+icra%2C+careratings%2Cfitchratings+credit+report+for+"+company_name+"&gl=us&hl=en", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for el in soup.select(".g"):
            linkCrisil = el.select_one(".yuRUbf").select_one("a")["href"]
            title = el.select_one("h3").text
            description = el.select_one(".VwiC3b").text


            companyReport = CompanyReport(
                        title = title,
                        link = linkCrisil,
                        description = el.select_one(".VwiC3b").text
                    )
            
            if company_name.lower() in title.lower() or company_name.lower() in description.lower(): 
                if "mnt/winshare/Ratings/RatingList/RatingDocs" in linkCrisil:
                    companyReport.source = "crisil"
                    return companyReport
                
                if "icra.in" in linkCrisil:
                    companyReport.source = "icra"
                    return companyReport
                                    
                if "careratings" in linkCrisil:
                    companyReport.source = "careratings"
                    return companyReport
                    
                if "indiaratings" in linkCrisil:
                    companyReport.source = "indiaratings"
                    await asyncio.create_task(get_india_rating(companyReport,organic_results))
                    return companyReport

async def get_india_rating(companyObject : CompanyReport, organic_results):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4703.0 Safari/537.36"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.indiaratings.co.in/pressReleases/GetUniqueIdentifier", headers=headers)
        uniqueIdentifier = response.text
    
        pressReleaseId = companyObject.link.replace('https://www.indiaratings.co.in/pressrelease/','')
        pressReleaseUrl = 'https://www.indiaratings.co.in/pressReleases/GetPressreleaseData?pressReleaseId='+pressReleaseId+'&uniqueIdentifier='+uniqueIdentifier
    
        response = await client.get(pressReleaseUrl, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            
            soup = BeautifulSoup(json_data[0]['keyRatingDrivers'], "html.parser")
            html = soup.text
            companyObject.scrapedReport = html

            soup = BeautifulSoup(json_data[0]['ratingSensitivities'], "html.parser")
            html = soup.text
            companyObject.scrapedReport = companyObject.scrapedReport + '\n\n' + html

            soup = BeautifulSoup(json_data[0]['companyProfile'], "html.parser")
            html = soup.text
            companyObject.scrapedReport = companyObject.scrapedReport + '\n\n' + html

            organic_results.append(companyObject)
