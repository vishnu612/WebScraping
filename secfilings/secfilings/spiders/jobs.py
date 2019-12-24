# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from scrapy.loader import ItemLoader

from secfilings.items import parse_ndseclisting_Item
from secfilings.items import parse_dseclisting_Item

class JobsSpider(Spider):
    name = 'jobs'
    allowed_domains = ["sec.gov"]
    start_urls = ['https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=4']
    

    def parse(self, response):
        base_url = "https://sec.gov"
        listings = response.xpath('//a[text()="4"]')
        for listing in listings:
            link = listing.xpath('.//@href').extract_first()
            
            CIK = link[21:link.rfind('/')]
            new_link = base_url+link
           
            yield Request(new_link,
                                callback=self.parse_listing,
                                meta={'link': link,
                                        'base_url' : base_url,
                                        'CIK' : CIK})

    def parse_listing(self, response):
        link = response.meta['link']
        base_url = response.meta['base_url']
        CIK = response.meta['CIK']
        
        htmllink = response.xpath('//a[contains(text(),"html")]/@href').extract_first()
        
        seclink = base_url + htmllink
        
        yield Request(seclink,
                                callback=self.parse_seclisting,
                                meta={'link': link,
                                        'base_url' : base_url,
                                        'CIK' : CIK})
                                        
    def parse_seclisting(self, response):
        CIK = response.meta['CIK']
        fData = response.xpath('//tbody')
        
        if len(fData) > 0:
        
            fData1 = response.xpath('//tbody')[0]
            rows1 = fData1.xpath('.//tr')
            
            tbody = fData1.xpath('.//*[@class="FormData"]/text()')        
                    
            if len(response.xpath('///tbody')) > 1:
                
                fData2 = response.xpath('//tbody')[1]
                rows2 = fData2.xpath('.//tr')
                
                for rw1 in rows1:
                    columns1 = rw1.xpath('.//td')
                    
                    items = parse_ndseclisting_Item()
                    
                    nDTitleofSecurity = columns1[0].xpath('.//text()').extract()
                    nDTransactionDate = columns1[1].xpath('.//text()').extract()
                    nDTransactionCode = columns1[3].xpath('.//text()').extract()
                    nDSecurityAmt = columns1[5].xpath('.//text()').extract()
                    nDSecuritiesAnD = columns1[6].xpath('.//text()').extract()
                    nDPrice = columns1[7].xpath('.//text()').extract()
                    nDAmountOfSecOwned = columns1[8].xpath('.//text()').extract()
                    nDOwnership = columns1[9].xpath('.//text()').extract()
                    
                    nDTitleofSecurity = [ elem for elem in nDTitleofSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    nDTransactionDate = [ elem for elem in nDTransactionDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDTransactionCode = [ elem for elem in nDTransactionCode if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDSecurityAmt = [ elem for elem in nDSecurityAmt if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDSecuritiesAnD = [ elem for elem in nDSecuritiesAnD if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDPrice = [ elem for elem in nDPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDAmountOfSecOwned = [ elem for elem in nDAmountOfSecOwned if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDOwnership = [ elem for elem in nDOwnership if '(' not in elem and '\n' not in elem and '$' not in elem]
                    
                    items['CIK'] = CIK
                    items['TitleOfSecurity'] = nDTitleofSecurity
                    items['TransactionDate'] =  nDTransactionDate
                    items['TransactionCode'] =  nDTransactionCode
                    items['Amount'] =  nDSecurityAmt
                    items['SecuritiesAcquirednDisposed'] = nDSecuritiesAnD
                    items['Price'] = nDPrice
                    items['AmountOfSecurityOwned'] = nDAmountOfSecOwned
                    items['OwnershipForm'] = nDOwnership
                    
                    yield items
                    
                for rw2 in rows2:
                    columns2 = rw2.xpath('.//td')
                    
                    items = parse_dseclisting_Item()
                    
                    dTitleofDerSecurity = columns2[0].xpath('.//text()').extract()
                    dConvExerPrice = columns2[1].xpath('.//text()').extract()
                    dTransactionDate = columns2[2].xpath('.//text()').extract()
                    dTransactionCode = columns2[4].xpath('.//text()').extract()
                    dSecuritiesA = columns2[6].xpath('.//text()').extract()
                    dSecuritiesD = columns2[7].xpath('.//text()').extract()
                    dExpirationDate = columns2[9].xpath('.//text()').extract()
                    dTitleofSecurity = columns2[10].xpath('.//text()').extract()
                    dAmtOrNumOfShares = columns2[11].xpath('.//text()').extract()
                    dPrice = columns2[12].xpath('.//text()').extract()
                    dNumberOfSecOwned = columns2[13].xpath('.//text()').extract()
                    dOwnership = columns2[14].xpath('.//text()').extract()
                    
                    dTitleofDerSecurity = [ elem for elem in dTitleofDerSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    dConvExerPrice = [ elem for elem in dConvExerPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTransactionDate = [ elem for elem in dTransactionDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTransactionCode = [ elem for elem in dTransactionCode if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dSecuritiesA = [ elem for elem in dSecuritiesA if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dSecuritiesD = [ elem for elem in dSecuritiesD if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dExpirationDate = [ elem for elem in dExpirationDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTitleofSecurity = [ elem for elem in dTitleofSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    dAmtOrNumOfShares = [ elem for elem in dAmtOrNumOfShares if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dPrice = [ elem for elem in dPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dNumberOfSecOwned = [ elem for elem in dNumberOfSecOwned if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dOwnership = [ elem for elem in dOwnership if '(' not in elem and '\n' not in elem and '$' not in elem]
                    
                    items['CIKDer'] = CIK
                    items['TitleofDerivativeSecurity'] = dTitleofDerSecurity
                    items['ConversionExercisePrice'] = dConvExerPrice
                    items['TransactionDateDer'] = dTransactionDate
                    items['TransactionCodeDer'] = dTransactionCode
                    items['SecuritiesAcquired'] = dSecuritiesA
                    items['SecuritiesDisposed'] = dSecuritiesD
                    items['ExpirationDate'] = dExpirationDate
                    items['TitleOfSecurityDer'] = dTitleofSecurity
                    items['AmountDer'] = dAmtOrNumOfShares
                    items['PriceDer'] = dPrice
                    items['AmountOfSecurityOwnedDer'] = dNumberOfSecOwned
                    items['OwnershipFormDer'] = dOwnership                  
                    
                    yield items
            
            elif len(tbody) >  2:
                       
                for rw1 in rows1:
                    columns1 = rw1.xpath('.//td')
                    
                    items = parse_ndseclisting_Item()
                    
                    nDTitleofSecurity = columns1[0].xpath('.//text()').extract()
                    nDTransactionDate = columns1[1].xpath('.//text()').extract()
                    nDTransactionCode = columns1[3].xpath('.//text()').extract()
                    nDSecurityAmt = columns1[5].xpath('.//text()').extract()
                    nDSecuritiesAnD = columns1[6].xpath('.//text()').extract()
                    nDPrice = columns1[7].xpath('.//text()').extract()
                    nDAmountOfSecOwned = columns1[8].xpath('.//text()').extract()
                    nDOwnership = columns1[9].xpath('.//text()').extract()
                    
                    nDTitleofSecurity = [ elem for elem in nDTitleofSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    nDTransactionDate = [ elem for elem in nDTransactionDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDTransactionCode = [ elem for elem in nDTransactionCode if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDSecurityAmt = [ elem for elem in nDSecurityAmt if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDSecuritiesAnD = [ elem for elem in nDSecuritiesAnD if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDPrice = [ elem for elem in nDPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDAmountOfSecOwned = [ elem for elem in nDAmountOfSecOwned if '(' not in elem and '\n' not in elem and '$' not in elem]
                    nDOwnership = [ elem for elem in nDOwnership if '(' not in elem and '\n' not in elem and '$' not in elem]
                    
                    items['CIK'] = CIK
                    items['TitleOfSecurity'] = nDTitleofSecurity
                    items['TransactionDate'] =  nDTransactionDate
                    items['TransactionCode'] =  nDTransactionCode
                    items['Amount'] =  nDSecurityAmt
                    items['SecuritiesAcquirednDisposed'] = nDSecuritiesAnD
                    items['Price'] = nDPrice
                    items['AmountOfSecurityOwned'] = nDAmountOfSecOwned
                    items['OwnershipForm'] = nDOwnership
                    
                    yield items
                
            else:
                
                fData2 = response.xpath('//tbody')[0]
                rows2 = fData2.xpath('.//tr')
                
                for rw2 in rows2:
                    columns2 = rw2.xpath('.//td')
                    
                    items = parse_dseclisting_Item()
                    
                    dTitleofDerSecurity = columns2[0].xpath('.//text()').extract()
                    dConvExerPrice = columns2[1].xpath('.//text()').extract()
                    dTransactionDate = columns2[2].xpath('.//text()').extract()
                    dTransactionCode = columns2[4].xpath('.//text()').extract()
                    dSecuritiesA = columns2[6].xpath('.//text()').extract()
                    dSecuritiesD = columns2[7].xpath('.//text()').extract()
                    dExpirationDate = columns2[9].xpath('.//text()').extract()
                    dTitleofSecurity = columns2[10].xpath('.//text()').extract()
                    dAmtOrNumOfShares = columns2[11].xpath('.//text()').extract()
                    dPrice = columns2[12].xpath('.//text()').extract()
                    dNumberOfSecOwned = columns2[13].xpath('.//text()').extract()
                    dOwnership = columns2[14].xpath('.//text()').extract()
                    
                    dTitleofDerSecurity = [ elem for elem in dTitleofDerSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    dConvExerPrice = [ elem for elem in dConvExerPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTransactionDate = [ elem for elem in dTransactionDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTransactionCode = [ elem for elem in dTransactionCode if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dSecuritiesA = [ elem for elem in dSecuritiesA if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dSecuritiesD = [ elem for elem in dSecuritiesD if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dExpirationDate = [ elem for elem in dExpirationDate if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dTitleofSecurity = [ elem for elem in dTitleofSecurity if not elem.startswith('(') and '\n' not in elem and '$' not in elem]
                    dAmtOrNumOfShares = [ elem for elem in dAmtOrNumOfShares if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dPrice = [ elem for elem in dPrice if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dNumberOfSecOwned = [ elem for elem in dNumberOfSecOwned if '(' not in elem and '\n' not in elem and '$' not in elem]
                    dOwnership = [ elem for elem in dOwnership if '(' not in elem and '\n' not in elem and '$' not in elem]
                    
                    items['CIKDer'] = CIK
                    items['TitleofDerivativeSecurity'] = dTitleofDerSecurity
                    items['ConversionExercisePrice'] = dConvExerPrice
                    items['TransactionDateDer'] = dTransactionDate
                    items['TransactionCodeDer'] = dTransactionCode
                    items['SecuritiesAcquired'] = dSecuritiesA
                    items['SecuritiesDisposed'] = dSecuritiesD
                    items['ExpirationDate'] = dExpirationDate
                    items['TitleOfSecurityDer'] = dTitleofSecurity
                    items['AmountDer'] = dAmtOrNumOfShares
                    items['PriceDer'] = dPrice
                    items['AmountOfSecurityOwnedDer'] = dNumberOfSecOwned
                    items['OwnershipFormDer'] = dOwnership                    
                    
                    yield items
        else:          
            pass

