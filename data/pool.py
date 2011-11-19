import StringIO
import BeautifulSoup
import csv

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.cmapdb import CMapDB

from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

from pdfminer.converter import XMLConverter, TextConverter, HTMLConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf

codec = 'utf-8'
laparams = LAParams()
outfile = None
outtype = None
outdir = None
outfp = StringIO.StringIO()
pagenos = set((0,))
maxpages = 1
password = ''
caching = True
debug = 1
layoutmode = 'normal'
scale = 1

PDFDocument.debug = debug
PDFParser.debug = debug
CMapDB.debug = debug
PDFResourceManager.debug = debug
PDFPageInterpreter.debug = debug
PDFDevice.debug = debug

fp = open('pooloct2011.pdf', 'rb')
rsrcmgr = PDFResourceManager(caching=caching)
# device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, outdir=outdir)
#device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                       layoutmode=layoutmode, laparams=laparams, outdir=outdir)
process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=password,
                    caching=caching, check_extractable=True)

outfp.seek(0)

v = BeautifulSoup.BeautifulSoup("".join(outfp.readlines()))
#column1 = [x for x in v.findAll('div') if '56' in dict(x.attrs).get('style', '')]
column2 = [x for x in v.findAll('div') if '167' in dict(x.attrs).get('style', '')]
column3 = [x for x in v.findAll('div') if '284' in dict(x.attrs).get('style', '') or '288' in dict(x.attrs).get('style', '')]
column4 = [x for x in v.findAll('div') if '362' in dict(x.attrs).get('style', '')]
#column5 = [x for x in v.findAll('div') if '427' in dict(x.attrs).get('style', '')]


def top(source):
    return dict([x.strip().split(":") for x in dict(source.attrs).get('style', '').split(';') if x]).get('top','')

def merge(source, *lsts):
    elem = [source.text.encode('utf-8')]
    source_top = top(source) 
    if source_top != "":
        for lst in lsts:
            for x in lst:                
                x_top = top(x)
                if source_top == x_top:
                    elem.append(x.text.encode('utf-8'))
    return elem

pools = []
for x in column2:
    pool = merge(x, column3, column4)
    if len(pool) >= 3 and len(pool) <= 4:
        pools.append(pool)
poolWriter = csv.writer(open('pools.csv', 'wb'), delimiter=',')
for x in pools:
    poolWriter.writerow(x)


