from RPA.PDF import PDF


class PdfAnalizator(object):
    def __init__(self, name):
        self.name = name
        self.pdf = PDF()

    
    def open_pdf(self):
        return self.pdf.get_text_from_pdf(self.name)

    
    def get_data(self):
        text = self.open_pdf()[1]

        # +3 для того чтоб не захватывать в строку символы левого сепаратора
        left_sep = text.index('1. ') + 3
        right_index = text.index('Section B: Investment Detail')

        text = text[left_sep:right_index].split('2. ')

        data = dict()
        for element in text:
            key, value = element.split(': ')
            data[key] = value
        return data