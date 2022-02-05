from RPA.Excel.Files import Files


class AgenciesXls(object):
    def __init__(self, page_title):
        self.xls_file = Files()
        self.page_title = 'Agencies'
        self.subservis_page_title = page_title
        self.name_xls = 'Agencies.xls'

    
    def create_file(self):
        self.xls_file.create_workbook(path=self.name_xls, fmt='xls')

    

    def open_file(self):
        self.xls_file.open_workbook(path=self.name_xls)


    def create_sheet(self, title):
        self.xls_file.workbook.create_worksheet(title)


    def create_header(self):
        self.create_file()
        self.create_sheet(title=self.page_title)
        self.xls_file.set_worksheet_value(row=1, column=1, value='Title')
        self.xls_file.set_worksheet_value(row=1, column=2, value='Sum')


    def close_xls(self):
        self.xls_file.save_workbook()


    def cteate_table_header(self, head):
        self.create_sheet(title=self.subservis_page_title)
        for i in range(len(head)):
            self.xls_file.set_worksheet_value(row=1, column=i+1, value=head[i])


    def set_data_table(self, data):
        self.open_file()
        head = list(data[0].keys())
        self.cteate_table_header(head=head)
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.xls_file.set_worksheet_value(row=i+2, column=j+1, value=data[i].get(head[j]))


    def set_data(self, data):
        self.create_header()
        for i in range(len(data)):
            self.xls_file.set_worksheet_value(row=i+2, column=1, value=data[i].get('name'))
            self.xls_file.set_worksheet_value(row=i+2, column=2, value=data[i].get('sum'))


class ExcellCheck(object):
    def __init__(self, worksheet):
        self.xls_file = Files()
        self.name_xls = 'Agencies.xls'
        self.worksheet = worksheet

    
    def open_file(self):
        self.xls_file.open_workbook(path=self.name_xls)

    
    def check_data(self, data):
        self.open_file()
        excell_data = self.xls_file.read_worksheet(self.worksheet)

        ans = dict()
        for element in data:
            for row in excell_data:
                if element['Unique Investment Identifier (UII)'] == row['A'] and \
                    element['Name of this Investment'] == row['C']:
                    print('Investment %s with UII %s in Excell table' % (element['Name of this Investment'], element['Unique Investment Identifier (UII)']))
                    ans[element['Unique Investment Identifier (UII)']] = True
        return ans