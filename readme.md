# Itdashboard_bot

:shipit: для установки [прочитать](./install.md)


## О проекте
в проекте используется [rpaframework](https://rpaframework.org/) 
<br>

## Классы
Для работы бота используются классы распределенные по файлам распределенными по категориям.
<br>

[task.py](./task.py) главный файл содержащий в себе функцию ***main.py*** запуск всех сторонних классов.

[parser.py](./parser.py) файл содержащий классы реализующие парсинг данных и скачивание пдф файлов.

[excell.py](./excell.py) файл содержащий классы реализующие создание, открытие и обработку excell файлов.

[pdf_reader.py](./pdf_reader.py) файл содержащий классы реализующие создание, открытие и обработку pdf файлов.

[local.py](./local.py) файл содержащий локальные настройки и переменные для частичного тестирования ф-ций.

## минусы
Код не отработал на [robocorp](https://cloud.robocorp.com/) потому что привысил время работы (более 3х минут)

## Улучшение кода
Для прохождения теста нужно было использовать многопоточность, так как самое длительное действие это расчет пдф файлов и скачивание пдф файлов, так как нужно ждать полной загрузки страницы и ожидать загрузку файла
 <br>
 многопоточность сократила бы время работы бота от +- 15-ти минут  до +- 2-х минут
 <br>
 на многопоточность нехватило времени)
