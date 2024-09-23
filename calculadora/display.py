# Use o LineEdit para criar campos de texto em linha. Use o TextEdit para criar campos de texto de várias linhas.
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, Signal
import variables as var
from utils import isEmpty, isNumOrDot
from os import system, name
from time import sleep


# Use o TYPING_CHECKING para checar tipos.
# Se fizer desta forma, não vai funcionar. Requer aspas simples para definir como tipo.
# exemplo: Button

class DisplayCalc(QLineEdit):
    signalRequest = Signal()
    delRequest = Signal()
    escRequest = Signal()
    inputRequest = Signal()
    opRequest = Signal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para que o método funcione, chame-o pelo init da classe principal.
        self.configStyle()
    def configStyle(self):
        self.setStyleSheet(f'font-size: {var.MAX_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setMinimumHeight(var.MAX_FONT_SIZE * 2)
        self.setMinimumWidth(var.MIN_WIDGET_WIDTH)
        # Evite passar os valores desta forma. Só fizemos desta forma para não repetir a mesma variável.
        self.setTextMargins(*[var.DEFAULT_STRING_MARGIN for _ in range (4)])

    # Este método só funciona em QLineEdit
    def keyPressEvent(self, event: QKeyEvent):
        focus_ = DisplayCalc()
        focus_.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        text = event.text().strip()
        # Variável para detectar qual tecla foi pressionada.
        key = event.key()
        # Constante para definir teclas do teclado. Neste caso, o Enter ou semelhante a ele (Return).
        KEYS = Qt.Key
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDel = key in [KEYS.Key_Delete, KEYS.Key_Backspace, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape]
        isOp = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk,KEYS.Key_P]
        # if key == KEYS.Key_Enter or key == KEYS.Key_Return:]
        if isEnter or text == '=':
            # Emitir um signal.
            self.signalRequest.emit()
            return event.ignore()
        if isDel:
            # Emitir um signal.
            focus_.setFocus()
            self.delRequest.emit()
            return event.ignore()
        if isEsc or text.lower() == 'c':
            # Emitir um signal.
            self.escRequest.emit()
            self.clear()
            sleep(0.2)
            system('cls' if name == 'nt' else 'clear')
            return event.ignore()
        if isOp:
            if text.lower() == 'p':
                text = 'x²'
                self.text()
            self.opRequest.emit(text)
            return event.ignore()
        if text.isdigit() or text == '.':
            QLineEdit.keyPressEvent(self, event)
            # O método event.ignore() é usado em eventos do Qt para indicar que o evento não foi tratado pelo widget /
            # atual. Quando você chama ignore() em um evento, está dizendo ao Qt que o evento deve ser passado para o /
            # próximo widget na cadeia de eventos para ser processado.
            # Por exemplo, se você estiver implementando um método de evento de tecla (keyPressEvent) e chamar /
            # event.ignore(), o Qt tentará passar o evento de tecla para o próximo widget que pode processá-lo. Isso /
            # é útil quando você deseja que outros widgets ou o sistema de gerenciamento de eventos do Qt tenham a /
            # chance de lidar com o evento.
            # Embora event.ignore() não retorne um valor, o uso de return dessa forma é uma prática para garantir que /
            # o método termine imediatamente após essa chamada.
        # O return logo abaixo permite que quaisquer teclas podem ser pressionadas sem exceção.
        # return super().keyPressEvent(event)
        # Já este outro return abaixo garante o término do método caso não haja mais nada a ser digitado.
        if isEmpty(text):
            return event.ignore()
        if isNumOrDot(text):
            # Emitir um signal.
            self.inputRequest.emit()
            return event.ignore()
    # Os métodos abaixo definem o foco no display permanentemente.
    def ensureFocus(self):
        if not self.hasFocus():
            self.setFocus()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setFocus()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setFocus()

class InfoDisplayCalc(QLabel):
    # Os atributos abaixo representam *args e **kwargs respectivamente, mas de forma menos amigável.
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.infoStyle()
    def infoStyle(self):
        self.setStyleSheet(f'font-size: {var.MIN_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
