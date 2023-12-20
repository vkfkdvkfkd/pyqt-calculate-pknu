import sys
import math
from PyQt5.QtWidgets import *


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.list = []

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_window = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation_solution = QLabel("")
        self.equation_solution = QLineEdit("")

        ### layout_equation_solution 레이아웃에 입출력 위젯을 추가
        layout_equation_solution.addRow(label_equation_solution, self.equation_solution)

        ### 이항 연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_modular = QPushButton("%")

        ### 단항 연산 버튼 생성
        button_inverse = QPushButton("1/x")
        button_square = QPushButton("x^2")
        button_square_root = QPushButton("√x")

        ### 기타 기능 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clear_entry = QPushButton("CE")
        button_backspace = QPushButton("<-")
        button_dot = QPushButton(".")
        button_abs = QPushButton("+/-")

        ### 숫자 버튼 생성 및 layout_window에 추가
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.button_number_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_window.addWidget(number_button_dict[number], x+2, y)
            elif number==0:
                layout_window.addWidget(number_button_dict[number], 5, 1)

        ### 버튼을 layout_window에 추가
        layout_window.addWidget(button_modular, 0, 0)
        layout_window.addWidget(button_clear_entry, 0, 1)
        layout_window.addWidget(button_clear, 0, 2)
        layout_window.addWidget(button_backspace, 0, 3)

        layout_window.addWidget(button_inverse, 1, 0)
        layout_window.addWidget(button_square, 1, 1)
        layout_window.addWidget(button_square_root, 1, 2)
        layout_window.addWidget(button_division, 1, 3)
        
        layout_window.addWidget(button_product, 2, 3)
        layout_window.addWidget(button_minus, 3, 3)
        layout_window.addWidget(button_plus, 4, 3)

        layout_window.addWidget(button_abs, 5, 0)
        layout_window.addWidget(button_dot, 5, 2)
        layout_window.addWidget(button_equal, 5, 3)

        ### 버튼을 클릭 시
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_modular.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))

        button_inverse.clicked.connect(lambda state, operation = "1/x": self.button_unary_operator_clicked(operation))
        button_square.clicked.connect(lambda state, operation = "x^2": self.button_unary_operator_clicked(operation))
        button_square_root.clicked.connect(lambda state, operation = "√x": self.button_unary_operator_clicked(operation))

        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_clear_entry.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)
        button_dot.clicked.connect(self.button_dot_clicked)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_window)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def button_number_clicked(self, num):
        equation = self.equation_solution.text()
        if equation == "0":
            self.equation_solution.setText(equation.replace("0", str(num)))
        else:
            equation += str(num)
            self.equation_solution.setText(equation)

    def button_dot_clicked(self):
        equation = self.equation_solution.text()
        if equation == "":
            equation += str("0.")
            self.equation_solution.setText(equation)            
        if "." not in equation:
            equation += str(".")
            self.equation_solution.setText(equation)       

    def button_operation_clicked(self, operation):
        equation = self.equation_solution.text()
        if equation == "" and len(self.list) == 0:
            equation = "0"
            self.list.append(equation)
            self.list.append(operation)
        elif equation == "" and self.list[-1] in "+-*/%":
            self.list.pop()
            self.list.append(operation)
        elif equation != "" and len(self.list) >= 2:
            self.list.append(equation)
            postfix = self.Infix2Postfix(self.list)
            equation = str(self.evalPostfix(postfix))
            self.list = []
            self.list.append(equation)
            self.list.append(operation)
        else:
            self.list.append(equation)
            self.list.append(operation)
        self.equation_solution.setText("")
        
    def button_unary_operator_clicked(self, operation):
        equation = float(self.equation_solution.text())
        if operation == "1/x":
            solution = 1 / equation
            self.equation_solution.setText(str(solution))
        elif operation == "x^2":
            solution = equation ** 2
            self.equation_solution.setText(str(solution))
        elif operation == "√x":
            solution = math.sqrt(equation)
            self.equation_solution.setText(str(solution))

    def button_equal_clicked(self):
        value = self.equation_solution.text()
        self.list.append(value)
        equation = self.Infix2Postfix(self.list)
        solution = self.evalPostfix(equation)
        self.list = []
        self.equation_solution.setText(str(solution))

    def button_clear_clicked(self):
        self.list = []
        self.equation_solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation_solution.text()
        equation = equation[:-1]
        self.equation_solution.setText(equation)
    
    def button_abs_clicked(self):
        equation = self.equation_solution.text()
        if equation == "":
            self.equation_solution.setText("0")
        elif "-" not in equation:
            self.equation_solution.setText("-" + equation)
        else:
            self.equation_solution.setText(equation.replace("-", ""))

    def Infix2Postfix(self, expr):
        stack = []
        output = []
        for term in expr:
            if term in "+-*/%":   
                stack.append(term)
            else:
                output.append(term)
        while len(stack) != 0:
            output.append(stack.pop())
        return output

    def evalPostfix(self, expr):
        stack = []
        for token in expr:
            if token in "+-*/%":
                val2 = stack.pop()
                val1 = stack.pop()
                if token == "+": stack.append(val1 + val2)
                elif token == "-": stack.append(val1 - val2)
                elif token == "*": stack.append(val1 * val2)
                elif token == "/": stack.append(val1 / val2)
                elif token == "%": stack.append(val1 % val2)
            else:
                stack.append(float(token))
        return stack.pop()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
