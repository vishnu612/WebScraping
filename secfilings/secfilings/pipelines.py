# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from pydispatch import dispatcher

def item_type(item):
    # The CSV file names are used (imported) from the scrapy spider.
    return type(item).__name__.replace('_Item','')

class SecfilingsPipeline(object):
    fileNamesCsv = ['parse_ndseclisting','parse_dseclisting']
    
    def __init__(self):
        self.files = {}
        self.exporters = {}
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        
    def spider_opened(self, spider):
        self.files = dict([ (name, open(name+'.csv','wb')) for name in self.fileNamesCsv ])
        for name in self.fileNamesCsv:
            self.exporters[name] = CsvItemExporter(self.files[name])

            
            if name == "NonDerivatives":
                self.exporters[name].fields_to_export = ['CIK','TitleOfSecurity', 'TransactionDate','TransactionCode','Amount','SecuritiesAcquirednDisposed','Price','AmountOfSecurityOwned','OwnershipForm']
                self.exporters[name].start_exporting()


            if name == "Derivatives":
                self.exporters[name].fields_to_export = ['CIKDer','TitleofDerivativeSecurity','ConversionExercisePrice','TransactionDateDer','TransactionCodeDer','SecuritiesAcquired','SecuritiesDisposed','ExpirationDate','TitleOfSecurityDer','AmountDer','PriceDer','AmountOfSecurityOwnedDer','OwnershipFormDer']
                self.exporters[name].start_exporting()


    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    
    def process_item(self, item, spider):
        typesItem = item_type(item)
        if typesItem in set(self.fileNamesCsv):
            self.exporters[typesItem].export_item(item)
        return item

