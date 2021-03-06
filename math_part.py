import math
import pylab
import numpy as np
from numpy import float64
from matplotlib import mlab
from matplotlib.figure import Figure
from Form import Ui_MainWindow
from tab_widg import Ui_MainWindow_tab
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
from main import second_window

class mathpart(Ui_MainWindow):
    def building(self, p, v, y, k, c, u10, u20, eps, d, x0, h, secwin):

        count_div, count_mul = 0, 0
        s1, s2 = 0, 0
        h_list = []
        S1list, S2list = [], []
        S1list.append(s1)
        S2list.append(s2)
        secwin.tableWidget.setItem(0, 6, QtWidgets.QTableWidgetItem(str(h)))
        secwin.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(x0)))
        secwin.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(u10)))
        secwin.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(u20)))

        def du1(u1, u2):
            return p + k * (u1**2 /u2) - y * u1

        def du2(u1, u2):
            return c * (u1**2) - v * u2
        
        def calc_coef_for_system(du1, du2, u1, u2, step):
            q = [[0] * 2] * 5
            res = np.array(q, dtype = np.float64)
            res[0][0] = du1(u1, u2)
            res[0][1] = du2(u1, u2)
            
            res[1][0] = du1(u1 + step * res[0][0] / 3, u2 + step * res[0][0] / 3)
            res[1][1] = du2(u1 + step * res[0][1] / 3, u2 + step * res[0][1] / 3)
            
            res[2][0] = du1(u1 + step * (res[0][0] + res[1][0]) / 6, u2 + step * (res[0][0] + res[1][0]) / 6)
            res[2][1] = du2(u1 + step * (res[0][1] + res[1][1]) / 6, u2 + step * (res[0][1] + res[1][1]) / 6)

            res[3][0] = du1(u1 + step * (res[0][0] + 3 * res[2][0]) / 8, u2 + step * (res[0][0] + 3 * res[2][0]) / 8)
            res[3][1] = du2(u1 + step * (res[0][1] + 3 * res[2][1]) / 8, u2 + step * (res[0][1] + 3 * res[2][1]) / 8)

            res[4][0] = du1(u1 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2, u2 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2)
            res[4][1] = du2(u1 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2, u2 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2)

            return res
            

        def next_point(x, u1, u2, number_r):
            nonlocal h
            secwin.tableWidget.setRowCount(number_r+1)
            x_new = x + h
            h_list.append(h)
            K = calc_coef_for_system(du1, du2, u1, u2, h)

            s1 = h * (2 * K[0][0] - 9 * K[2][0] + 8 * K[3][0] - K[4][0]) / 30
            s2 = h * (2 * K[0][1] - 9 * K[2][1] + 8 * K[3][1] - K[4][1]) / 30
            
            if self.checkBox.isChecked():
                secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(abs(s1))))
                secwin.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(abs(s2))))

            
            u1_new = u1 + h * (K[0][0] + 4 * K[3][0] + K[4][0]) / 6
            u2_new = u2 + h * (K[0][1] + 4 * K[3][1] + K[4][1]) / 6

            secwin.tableWidget.setItem(number_r, 0, QtWidgets.QTableWidgetItem(str(number_r)))
            secwin.tableWidget.setItem(number_r, 1, QtWidgets.QTableWidgetItem(str(x_new)))
            secwin.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(u1_new)))
            secwin.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(u2_new)))

            nonlocal count_div, count_mul
            if self.checkBox.isChecked():
                if abs(s1) >= eps/16 and abs(s2) >= eps/16 and abs(s1) <= eps and abs(s2) <= eps:
                    S1list.append(abs(s1))
                    S2list.append(abs(s2))
                    return x_new, u1_new, u2_new
                elif abs(s1) > eps or abs(s2) > eps:
                    count_div += 1
                    h /= 2
                    return next_point(x, u1, u2, number_r)
                elif abs(s1) < eps/16 and abs(s2) < eps/16:
                    count_mul += 1
                    h *= 2
                    S1list.append(abs(s1))
                    S2list.append(abs(s2))
                    return x_new, u1_new, u2_new
                else: 
                    S1list.append(abs(s1))
                    S2list.append(abs(s2))
                    return x_new, u1_new, u2_new
                    
            else: 
                
                return x_new, u1_new, u2_new

        self.progressBar.setMinimum(x0)
        self.progressBar.setMaximum(100)
        ax_1 = self.figure.add_subplot(211)
        ax_2 = self.figure.add_subplot(212)
        if self.checkBox_2.isChecked():
            ax_1.clear()
            ax_2.clear()
        ax_1.axis([-1, 50, -1, 2])
        ax_2.axis([-1, 50, -1, 2])
        v1, v2 = u10, u20
        x = x0
        i = 0
        secwin.label.setText("Начальное время = " + str(x))
        secwin.label_2.setText("Начальная конц. активатора = " + str(v1))
        secwin.label_3.setText("Начальная конц. ингибитора = " + str(v2))
        secwin.label_4.setText("Плотность активатора k = " + str(p))
        secwin.label_5.setText("Скорость самообразования активатора k = " + str(k))
        secwin.label_6.setText("скорость самообразования ингибитора c = " + str(c))
        secwin.label_7.setText("Естественный распад активатора v = " + str(v))
        secwin.label_8.setText("Естественный распад ингибитора y = " + str(y))
        secwin.label_9.setText("Контроль локальной погрешности Eps = " + str(eps))
        
        ax_1.set_ylabel("Inhibitor")
        ax_2.set_ylabel("Activator")
        ax_2.set_xlabel("Concetnration")
        xlist, u1list, u2list = [], [], []
        u1list.append(u10)
        u2list.append(u20)
        xlist.append(x0)
        while x < d:
            x, v1, v2 = next_point(x, v1, v2, i + 1)                    
            secwin.tableWidget.setItem(i + 1, 6, QtWidgets.QTableWidgetItem(str(h)))
            secwin.tableWidget.setItem(i + 1, 7, QtWidgets.QTableWidgetItem(str(count_div)))
            secwin.tableWidget.setItem(i + 1, 8, QtWidgets.QTableWidgetItem(str(count_mul)))           
            self.progressBar.setValue(i)
            xlist.append(x)
            u1list.append(v1)
            u2list.append(v2)
            i += 1
        if self.checkBox.isChecked():
            ax_1.plot(xlist, u1list, '-b', label = 'С контролем ЛП')
        else:
            ax_1.plot(xlist, u1list, '-y')
        if self.checkBox.isChecked():
            ax_2.plot(xlist, u2list, '-r', label = 'С контролем ЛП')
        else:
            ax_2.plot(xlist, u2list, '-y')
        if self.checkBox.isChecked():
            secwin.label_10.setText("Максимальная оценка ЛП 1 = " + str(round(max(S1list), 9)))
            secwin.label_11.setText("Максимальная оценка ЛП 2 = " + str(round(max(S2list), 9)))
            secwin.label_14.setText("Делений шага = " + str(count_div))
            secwin.label_15.setText("Удвоений шага = " + str(count_mul))
        secwin.label_12.setText("Максимальный шаг = " + str(max(h_list)))
        secwin.label_13.setText("Минимальный шаг = " + str(min(h_list)))
        ax_1.legend()
        ax_2.legend()
        ax_1.grid(True)
        ax_2.grid(True)
        self.canvas.draw()
        
        