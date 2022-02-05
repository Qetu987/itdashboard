# -*- coding: utf-8 -*-
from RPA.Browser.Selenium import Selenium
from parser import ItdashboardParser, SubAgencyParser, DownloadPdf
from excell import AgenciesXls, ExcellCheck
from pdf_reader import PdfAnalizator
import os
from local import (
    curent_department,
    list_deps,
    main_url,
    table_data,
    data_from_pdf,
)


def get_data_from_pdf():
    files = os.listdir(os.path.abspath(os.curdir))
    pdfs = [name for name in files if name.endswith('.pdf')]

    return [PdfAnalizator(name=pdf).get_data() for pdf in pdfs]


def main():
    driver = Selenium()
    driver.set_download_directory(os.path.abspath(os.curdir))
    # парсим главную страницу
    parser = ItdashboardParser(driver=driver, url=main_url)
    list_deps = parser.get_department_list()

    # записываем данные с главной страницы
    xls_agencies = AgenciesXls(page_title=curent_department)
    xls_agencies.set_data(data=list_deps)

    xls_agencies.close_xls()
    # узнаем ссылку департамента
    for dep in list_deps:
        if dep['name'] == curent_department:
            sub_url = dep['href']
            

    # парсим страницу департамента
    sub_service = SubAgencyParser(driver=driver, url=sub_url)
    table_data, download_links = sub_service.get_grid()

    # записываем данные со странички агенства
    xls_agencies1 = AgenciesXls(page_title=curent_department)
    xls_agencies1.set_data_table(data=table_data)

    xls_agencies1.close_xls()

    for link in download_links:
        sub_service = DownloadPdf(driver=driver, url=link)
        sub_service.download()
    driver.close_all_browsers()

    # получаем данные с пдф и сравниваем их с таблицей
    data_from_pdf = get_data_from_pdf()
    check = ExcellCheck(worksheet=curent_department).check_data(data=data_from_pdf)


if __name__ == '__main__':
    main()
