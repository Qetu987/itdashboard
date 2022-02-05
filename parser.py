# -*- coding: utf-8 -*-
import time


class ItdashboardParser(object):
    def __init__(self, driver, url):
        self.url = url
        self.driver = driver


    def get_page(self):
        self.driver.open_available_browser(self.url)

    
    def click_drive_in_button(self):
        self.driver.find_element('css:a.btn.btn-default.btn-lg-2x.trend_sans_oneregular').click()

    
    def get_department_list(self):
        self.get_page()
        self.click_drive_in_button()

        time.sleep(5) # ждем пока загрузится вся страница

        div = self.driver.find_element('id:agency-tiles-widget')
        divs = div.find_elements_by_css_selector('div.tuck-5')
        print(divs)
        deps = list()
        for i in divs:
            dep = dict()
            dep['name'] = i.find_element_by_css_selector('span.h4').text
            dep['sum'] = i.find_element_by_css_selector('span.h1').text
            dep['href'] = i.find_element_by_css_selector('a.btn.btn-default.btn-sm').get_attribute('href')
            deps.append(dep)
        return deps


class DownloadPdf(ItdashboardParser):
    def download(self):
        self.get_page()

        # ждем пока сайт полностью загрузится
        time.sleep(4)

        element = self.driver.find_element('id:business-case-pdf')\
            .find_element_by_tag_name('a')
        element.click()

        # ждем пока сайт сгенерит пдф и ждем само скачивание
        # 10 сек, потому что некоторые пдф не успевали скачиваться за 5 сек
        time.sleep(10)


class SubAgencyParser(ItdashboardParser):
    def click_selector_button(self):
        element = self.driver.find_element('css:select.form-control.c-select')
        element.click()
        return element


    def click_selector_all(self, element):
        select_elements = element.find_elements_by_tag_name('option')
        for element in select_elements:
            if element.text == 'All':
                element.click()


    def set_grid_drop(self):
        select_element = self.click_selector_button()
        time.sleep(1)
        self.click_selector_all(element=select_element)

    
    def get_grid_element(self):
        return self.driver.find_element('css:div.dataTables_scroll')


    def check_element_in_block(self, element):
        try:
            return element.find_element_by_tag_name('a').get_attribute('href')
        except:
            return None

    
    def generate_grid_data(self, element):
        data = list()
        download_links = list()
        # получаем шапку таблицы
        head_of_table = element.find_element_by_css_selector('div.dataTables_scrollHead')
        head_of_table = head_of_table.find_elements_by_tag_name('tr')[-1]
        elements_of_head = [title.text for title in head_of_table.find_elements_by_tag_name('th')]

        # получаем тело таблицы
        body_of_table = element.find_element_by_css_selector('div.dataTables_scrollBody')\
        .find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        for row in body_of_table:
            row_data = dict()
            # не переделываем сразу в список потому что нужно еще узнать о наличии пдф на первом столбце
            cols = row.find_elements_by_tag_name('td')
            row_data_list = [el.text for el in cols]

            for i in range(len(row_data_list)):
                row_data[elements_of_head[i]] = row_data_list[i]

            data.append(row_data)

            # проверяем, есть ли ссылка на данной строке
            link =  self.check_element_in_block(cols[0])
            if link:
                download_links.append(link)
        print('hi')
        return (data, download_links)


    def get_grid(self):
        self.get_page()
        time.sleep(10) # ждем пока прогрузится таблица, она не спешит
        self.set_grid_drop()
        time.sleep(10) # ждем пока прогрузятся все записи, они тоже не спешат
        return self.generate_grid_data(element=self.get_grid_element())
