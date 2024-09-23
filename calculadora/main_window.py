from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QKeyEvent, QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QToolTip
# from calculadora.display import DisplayCalc
from variables import DARKER_PRIMARY_COLOR, PRIMARY_COLOR, DARKEST_PRIMARY_COLOR
import utils
from typing import TYPE_CHECKING, Any

# Isso evita importação circular. Não é tão necessário agora, mas já é um problema a menos para resolver.
if TYPE_CHECKING:
    from display import DisplayCalc, InfoDisplayCalc

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        # O atributo parent significa que esta janela pode ter uma janela pai. Neste caso, esta não terá um.
        super().__init__(parent, *args, **kwargs)

        # Cria o widget
        self.principal = QWidget()
        self.vLayout = QVBoxLayout()
        self.principal.setLayout(self.vLayout)
        self.setCentralWidget(self.principal)
        # Título
        self.setWindowTitle('Calculadora Simples 0.9 (Beta)')

    def addVLayout(self,widget):
        self.vLayout.addWidget(widget)

    def adjustFixedSize(self):
        # Use isto para ajustar os widgets à janela. Deve ser a última coisa a ser feita. Em outras palavras, /
        # se você mudar o tamanho da fonte, vai mudar o tamanho do widget também.
        self.adjustSize()
        self.setFixedSize(self.width(),self.height())

    def addLabel(self,labelName: str | QLabel = 'Label1', fontSize = 12, orientation: str = None):
        # É possível usar o "typing.Union" para unir tipos diferentes para um argumento
        if isinstance(labelName, str):
            # Esta condição é necessária para converter o tipo para QLabel, sendo assim, ser lido como um widget.
            labelName = QLabel(labelName)
        labelName.setStyleSheet(f'font-size: {fontSize}px;')
        valid_orientations = {'left': Qt.AlignmentFlag.AlignLeft, 'right': Qt.AlignmentFlag.AlignRight,
                             'center': Qt.AlignmentFlag.AlignCenter}
        if orientation in valid_orientations:
            labelName.setAlignment(valid_orientations[orientation])
        else:
            raise ValueError(f"Orientação inválida: {orientation}. O campo 'orientation' aceita apenas estas palavras: \
            'left', 'right', 'center'.")
        self.addVLayout(labelName)

# O PyCharm sugere que um método pode ser estático quando ele não utiliza a instância da classe (ou seja, não acessa /
    # atributos ou outros métodos da instância). Métodos estáticos são definidos usando o decorador @staticmethod e /
    # não recebem o parâmetro self.

    def makeMsgBox(self, text = 'Ocorreu algo inesperado.'):
        # messageBox = QMessageBox()
        return QMessageBox(self)
class MainButton(QPushButton):

    '''def __init__(self,*args,**kwargs):
        # Neste caso, é necessário usar o args e o kwargs para inserir parâmetros.
        super().__init__(*args,**kwargs)
        self.configStyleButton()

    def configStyleButton(self):
        font_ = self.font()
        font_.setPixelSize(MED_FONT_SIZE)
        font_.setBold(True)
        self.setMinimumSize(60,60)
        # Estilos são sobrescritos caso sejam chamados mais de uma vez.
        self.setStyleSheet(f'font-size: {MED_FONT_SIZE}px;')
        self.setProperty('cssClass','specialButton')

    qss = f"""
        QPushButton[cssClass="specialButton"] {{
        # Colocar duas chaves dentro de uma f-string significa que o conteúdo dentro da segunda chave será lido.
            color: #fff;
            background: {PRIMARY_COLOR};
            border-radius: 5px;
        }}
        QPushButton[cssClass="specialButton"]:hover {{
            color: #fff;
            background: {DARKER_PRIMARY_COLOR};
        }}
        QPushButton[cssClass="specialButton"]:pressed {{
            color: #fff;
            background: {DARKEST_PRIMARY_COLOR};
        }}
    """

    def setupStyle(self):
        # Adiciona um tema padrão para a janela. Perceba que o final deve ser "pyside6" para não haver erros.
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        # Sobrepõe com qss adicional.
        self.setStyleSheet(self.styleSheet() + qss)'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty('cssClass', 'specialButton')
        self.setMinimumSize(75,75)
        self.updateStyle()

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            QPushButton[cssClass="specialButton"] {{
                color: #fff;
                background: {DARKER_PRIMARY_COLOR};
                border-radius: 5px;
                font-weight: bold;
                font-size: 28px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.updateStyle()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet(f"""
            QPushButton[cssClass="specialButton"] {{
                color: #fff;
                background: {DARKEST_PRIMARY_COLOR};
                border-radius: 5px;
                font-weight: bold;
                font-size: 28px;
            }}
        """)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.updateStyle()
        super().mouseReleaseEvent(event)

    def updateStyle(self):
        self.setStyleSheet(f"""
            QPushButton[cssClass="specialButton"] {{
                color: #fff;
                background: {PRIMARY_COLOR};
                border-radius: 5px;
                font-weight: bold;
                font-size: 28px;
            }}
        """)

class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setMinimumSize(75,75)
        self.setStyleSheet(f'font-size: 28px; border-color: {PRIMARY_COLOR}')
        # self.setCheckable(True)

class GridButtons(QGridLayout):
    def __init__(self, display: 'DisplayCalc', info: 'InfoDisplayCalc', window: MainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ['C','⌫','x²','/'],
            ['7','8','9','*'],
            ['4','5','6','-'],
            ['1','2','3','+'],
            ['%','0','.','='],
        ]
        display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.display = display
        self.info = info
        self.window = window
        # O Getter e Setter de equation será útil, pois será definido um valor a info e isso pode se repetir.
        # Esta variável sustenta o getter (property)
        self._equation = ''
        self._equationInitialValue = 'Sua equação'
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    @equation.setter
    def equation(self,value):
        # Quando definir um valor em "value", este será mostrado no infoCalc.
        self._equation = value
        self.info.setText(value)

    def connectRequest(self, signal, *args):
        if signal == 'enter'.lower():
            self.display.signalRequest.connect(lambda: print(f'Requisição de {signal} vindo de: '
                                                             f'{self.__class__.__name__}'))
        if signal == 'del'.lower():
            self.display.delRequest.connect(self._backspace)
        if signal == 'esc'.lower():
            self.display.escRequest.connect(lambda: print(f'Requisição de {signal} vindo de: '
                                                          f'{self.__class__.__name__}'))
        if signal == 'num':
            self.display.inputRequest.connect(lambda: print(f'Requisição de {signal} vindo de: '
                                                            f'{self.__class__.__name__}'))
        if signal == 'op':
            self.display.opRequest.connect(lambda: print(f'Requisição de {signal} vindo de: ',
                                                         f'{self.__class__.__name__}'))

    def _makeGrid(self):
        self.connectRequest('enter')
        self.connectRequest('del')
        self.connectRequest('esc')
        self.connectRequest('num')
        self.connectRequest('op')
        for i, row in enumerate(self._gridMask):
            for j, item in enumerate(row):
                button = Button(item)
                if i==0 and j==0:
                    continue
                if not utils.isNumOrDot(item):
                    button.setStyleSheet(f'font-size: 28px; font-weight: bold;')
                    self._configSpecialButton(button)
                self.addWidget(button,i,j)
                buttonSlot = self._makeSlot(self.clickedInfoCalc, button)
                self._connectButtonClicked(button, buttonSlot)
        # O botão C precisa ser criado depois e deve ter seu próprio slot, já que pertence a outra classe.
        buttonC = MainButton('C')
        # buttonC.setStyleSheet('font-size: 28px; font-weight: bold;')
        self.addWidget(buttonC, 0, 0)
        buttonC.clicked.connect(self._clear)

    @staticmethod
    def _connectButtonClicked(button,slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        tooltipFont = QFont('Arial', 14)
        QToolTip.setFont(tooltipFont)
        text = button.text()
        buttonSlot = self._makeSlot(self._clear)
        # Caso o botão seja o correspondente, limpe o display.
        if text == 'C':
            self._connectButtonClicked(button, buttonSlot)
            # button.clicked.connect(self.display.clear)
            button.clicked.connect(self._clear)
        if text == '◄' or text == '⌫':
            # Para apagar os números digitados, simplesmente uso o backspace (sem os parênteses)
            self._connectButtonClicked(button, self._backspace)
            self.display.setFocus()
        if text in '+-*/x²%':
            if text == '%':
                button.setToolTip('Resto da divisão.')
            self._connectButtonClicked(button, self._makeSlot(self._operatorClicked, button))
        if text == '=':
            self._connectButtonClicked(button, self._equal)
    @staticmethod
    def _makeSlot(func, *args, **kwargs):   #type: ignore
        @Slot(bool)
        def realSlot(_):
            func(*args,**kwargs)
        return realSlot

    def clickedInfoCalc(self,button_):
        buttonString = button_.text()
        newDisplayText = self.display.text() + buttonString     #Mostra o valor resultante após apertar o botão.
        if not utils.isValidNumber(newDisplayText):
            return
        self.display.insert(buttonString)
        print(buttonString)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    # O uso do lambda em _clear:
    # Caso queira adicionar mensagens extras ao clicar no botão, deve ser criado um argumento dentro do _clear e um /
    # lambda para chamar diretamente.
    # No PyQt, quando você conecta um sinal a um slot (função), o slot é chamado sem argumentos adicionais, a menos que /
    # o sinal em si passe argumentos. Neste caso, você queria passar uma mensagem específica para o método _clear /
    # quando o botão “C” fosse clicado.
    # Ao tentar conectar o botão “C” diretamente ao método _clear com um argumento, isso não funcionou porque /
    # _makeSlot provavelmente não estava configurado para passar argumentos adicionais corretamente. Além disso, o /
    # método _clear esperava um argumento (msg), mas a conexão direta não fornecia isso.

    def _operatorClicked(self, button: Any | QKeyEvent):
        buttonText = button.text()          # Pegar o texto que está no botão. Neste caso, +-*/ etc.
        displayText = self.display.text()   # Pegar o texto que está no display. Neste caso, o número da esquerda (left).
        self.display.clear()
        KEYS = Qt.Key
        isNegative = button in [KEYS.Key_Minus]
        if isNegative:
            self.info.setText(displayText * -1)
            return
        if not utils.isValidNumber(displayText):
            # Este if verifica se o valor à esquerda é um número e se o valor à esquerda inexiste. Evita entradas inválidas.
            # Se o objetivo é garantir que sempre haja um número válido no display antes de prosseguir, a remoção de /
            # left faz sentido. Caso contrário, manter a verificação de self._left permite maior flexibilidade na /
            # continuidade das operações.
            self.info.setText(f'Nada para mostrar.')
            return
        if self._left is None:
            # Este if define o número à esquerda da equação.
            self._left = float(displayText)
        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
        print('Operador',buttonText)

    @Slot()
    def _equal(self):
        displayText = self.display.text()
        if not utils.isValidNumber(displayText) or self._left is None:
            self.info.setText(f'Nada para calcular.')
            return
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 0
        try:
            if 'x²' in self.equation:
                # Neste caso podemos usar o pow simplesmente para evitar o uso do eval.
                result = pow(self._left, self._right)
                self.info.setText(f'{self._left} {self._op} {self._right} = {result}')
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self.info.setText(f'Divisão por zero não permitida.')
        except OverflowError:
            self.info.setText(f'Número muito grande (Overflow).')
        # print(result)
        self.display.clear()
        # A linha logo abaixo é que vai mostrar o resultado.
        self.info.setText(f'{self.equation} = {result}')
        # é possível mostrar o resultado dentro de equation, mas isso pode nos trazer complicações posteriores.
        self._left = None
        self._right = None

    @Slot()
    # Este método define o foco exclusivamente ao backspace.
    def _backspace(self):
        self.display.backspace()
        self.display.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.display.setFocus()
    def _showError(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        # Exibe um texto exatamente na forma que foi definido. Ele é exibido após a chamada do método que chamou este.
        # msgBox.setInformativeText('''Lorem
        # Ipsum''')
        # Ícone que será exibido na mensagem.
        msgBox.setIcon(msgBox.Icon.Warning)
        # Botões que podem ser adicionados na caixa de diálogo. Para traduzi-los, use o QtTranslator.
        '''msgBox.setStandardButtons(
            msgBox.StandardButton.Ok |  # Para adicionar mais botões na mesma mensagem, use o sinal do pipe.
            msgBox.StandardButton.No
        )'''
        # Altera o nome do botão em questão.
        msgBox.button(msgBox.StandardButton.Ok).setText('Tudo bem.')
        # Ativa algo ao clicar em tal botão da mensagem.
        result = msgBox.exec()
        if result == msgBox.StandardButton.Ok:
            print('Clicou em OK.')
