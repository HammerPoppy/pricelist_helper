import csv
import time

import pyautogui as pag
import pyperclip
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QAction


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):

    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(400, 800))  # Устанавливаем размеры
        self.setWindowTitle("pricelist helper")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        # table
        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(3)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Done"])

        with open('pl.csv', 'r') as csvfile:

            with open('pl.csv') as f:
                row_count = sum(1 for _ in f)

            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            self.table.setRowCount(row_count)

            for row in reader:
                i = 0
                for item in row:
                    self.table.setItem(reader.line_num - 1, i, QTableWidgetItem("".join(item)))
                    i += 1

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)

        self.table.selectRow(0)

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        grid_layout.addWidget(self.table, 0, 0, 1, 3)  # Добавляем таблицу в сетку

        # button 1
        button = QPushButton('proceed', self)
        button.clicked.connect(self.proceed)

        grid_layout.addWidget(button, 1, 0)

        # button 2
        button = QPushButton('done', self)
        button.clicked.connect(self.markDone)

        grid_layout.addWidget(button, 1, 1)

        # button 3
        button = QPushButton('missing', self)
        button.clicked.connect(self.markMissing)

        grid_layout.addWidget(button, 1, 2)

        # button 4
        button = QPushButton('save', self)
        button.clicked.connect(lambda: self.save('pl.csv'))

        grid_layout.addWidget(button, 1, 3)

        QAction("Quit", self).triggered.connect(self.closeEvent)

        #for i in range(20):
        #    print(pag.position())
        #    time.sleep(1)



    @pyqtSlot()
    def proceed(self):
        name = self.table.selectionModel().selectedRows()[0].data()
        original_pos = pag.position()

        pag.click(-1000, 605)
        pag.moveTo(original_pos)

        pag.write(name)
        time.sleep(2)
        pag.press('enter')
        time.sleep(1)
        pag.keyDown('ctrl')
        pag.press('w')
        pag.keyUp('ctrl')

        selection = self.table.selectedItems()
        price = selection[1].text()
        print(price)
        pyperclip.copy(price)

    @pyqtSlot()
    def save(self, path):
        with open(path, 'w') as stream:
            writer = csv.writer(stream, delimiter=';', quotechar='"', lineterminator='\n')
            for row in range(self.table.rowCount()):
                rowdata = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')

                writer.writerow(rowdata)
            print("save complete: " + path)

    @pyqtSlot()
    def markDone(self):
        range = self.table.selectedItems()
        for item in range:
            if item.text() == 'false' or item.text() == 'missing':
                item.setText('true')

        selection = self.table.selectionModel().selectedRows()
        if len(selection) > 0:
            self.table.selectRow(selection[-1].row() + 1)

        self.save('pl.csv')

    @pyqtSlot()
    def markMissing(self):
        range = self.table.selectedItems()
        for item in range:
            if item.text() == 'false' or item.text() == 'true':
                item.setText('missing')

        selection = self.table.selectionModel().selectedRows()
        if len(selection) > 0:
            self.table.selectRow(selection[-1].row() + 1)

        self.save('pl.csv')

    def closeEvent(self, event):
        self.save('pl_exit_save.csv')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
