import os
import base64

import win32api
import win32print
from win32com import client

# from fabs.driversRelate.singleton import singleton
# from fabs.driversRelate.driverbase import DriverBase

# @singleton
class PrinterDriver(DriverBase):
    def __init__(self):
        self.GHOSTSCRIPT_PATH = 'C:\\Program Files\\gs\\gs9.21\\bin\\gswin32c.exe'
        self. GSPRINT_PATH = 'C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe'
        self.defaultPrinter = win32print.GetDefaultPrinter()
        self.filePath = os.environ['TMP']+'\\test.docx'

    def printer(self, ls, fileType,targetPrinter=self.defaultPrinter):
        if fileType == 'word':
            self.filePath +='\\tmp.docx'
            decodeFile(ls)
            self.wordPrinter(targetPrinter)
        elif fileType == 'excel':
            self.filePath += '\\tmp.xlsx'
            decodeFile(ls)
            self.excelPrinter(targetPrinter)
        elif fileType == 'pdf':
            self.filePath +='\\tmp.pdf'
            decodeFile(ls)
            self.pdfPrinter(targetPrinter)
        else:
            return 'unsupported file type'

        return 'success'
        
        self.wordPrinter(self.defaultPrinter)

    def decodeFile(self, ls, fileType):
        outFile = open(self.filePath,'wb')
        data = base64.b64decode(ls)
        outFile.write(data)
        outFile.close()
        

    def getPrinters(self):
        # self.write_message('HH', '22', '33')
        # self.handler.write_message('HH')
        return win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None, 1)
    
    def wordPrinter(self, targetPrinter):
        try:
            document = client.Dispatch('Kwps.application')
            doc = document.Documents.Open(self.filePath)
            if not targetPrinter == self.defaultPrinter:
                win32print.SetDefaultPrinter(targetPrinter)
            doc.printOut()
        except:
            return 'failed'
        finally:
            doc.Close()
            document.Quit()
            if not targetPrinter == self.defaultPrinter:
                win32print.SetDefaultPrinter(self.defaultPrinter)
        return 'success'
    
    def excelPrinter(self,targetPrinter):
        try:
            document = client.Dispatch('Ket.application')
            excel = document.Workbooks.Open(self.filePath)
            if targetPrinter != self.defaultPrinter:
                win32print.SetDefaultPrinter(targetPrinter)
            excel.printOut()
        except:
            return 'failed'
        finally:
            excel.Close()
            document.Quit()
            if not targetPrinter == self.defaultPrinter:
                win32print.SetDefaultPrinter(self.defaultPrinter)
        return 'success'

    def pdfPrinter(self,targetPrinter):
        try:
            win32api.WinExec('"'+self.GSPRINT_PATH + '" -ghostscript "'
                     + self.GHOSTSCRIPT_PATH+'" -printer "'
                     + self.targetPrinter+'" ' + self.filePath,0)
        except:
            return 'failed'

        return 'success'

