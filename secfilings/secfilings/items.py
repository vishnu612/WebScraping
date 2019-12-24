# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#class SecfilingsItem(scrapy.Item):
#    pass
class parse_ndseclisting_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fields_to_export = ['CIK','TitleOfSecurity', 'TransactionDate','TransactionCode','Amount','SecuritiesAcquirednDisposed','Price','AmountOfSecurityOwned','OwnershipForm']
    TitleOfSecurity = scrapy.Field()
    TransactionDate = scrapy.Field()
    TransactionCode = scrapy.Field()
    Amount = scrapy.Field()
    SecuritiesAcquirednDisposed = scrapy.Field()
    Price = scrapy.Field()
    AmountOfSecurityOwned = scrapy.Field()
    OwnershipForm = scrapy.Field()
    CIK = scrapy.Field()
    
class parse_dseclisting_Item(scrapy.Item):
    fields_to_export = ['CIKDer','TitleofDerivativeSecurity','ConversionExercisePrice','TransactionDateDer','TransactionCodeDer','SecuritiesAcquired','SecuritiesDisposed','ExpirationDate','TitleOfSecurityDer','AmountDer','PriceDer','AmountOfSecurityOwnedDer','OwnershipFormDer']
    TitleofDerivativeSecurity = scrapy.Field()
    ConversionExercisePrice = scrapy.Field()
    TransactionDateDer = scrapy.Field()
    TransactionCodeDer = scrapy.Field()
    SecuritiesAcquired = scrapy.Field()
    SecuritiesDisposed = scrapy.Field()
    ExpirationDate = scrapy.Field()
    TitleOfSecurityDer = scrapy.Field()
    AmountDer = scrapy.Field()
    PriceDer = scrapy.Field()
    AmountOfSecurityOwnedDer = scrapy.Field()
    OwnershipFormDer = scrapy.Field()
    CIKDer = scrapy.Field()