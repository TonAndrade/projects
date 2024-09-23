from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from sys import argv
from main_window import MainWindow, MainButton, GridButtons, Button
from variables import WINDOW_ICON
from display import DisplayCalc, InfoDisplayCalc

# todo - comentários mentem
# todo - Use o Pyinstaller para empacotar o projeto. Use o noconfirm para ignorar avisos. Use o onefile para mesclar
#  os arquivos do app num arquivo só. Use o --add-data para adicionar coisas que estão em pastas específicas. Use o
#  --icon para adicionar o caminho do ícone. Use o --noconsole caso queira remover retornos do console. O --log-level
#  define o nível de log caso algo ocorra (WARN ou INFO). Os parâmetros devem ser inseridos antes do nome do arquivo.
#  Use o --distpath para definir o local da instalação (--distpath 'local').
#  Use o --specpath para definir o local do spec e reconstruir o projeto com as configs predefinidas./
    # pyinstaller 'nomeProjeto.py'  Caso não queira configurar nada.
    # pyinstaller --name='nome_do_aplicativo' --noconfirm --onefile --icon='./calculadora/files/icon.png --noconsole'
# todo - Use o pipreqs ./nomeProjeto para adicionar o requirements separadamente

if __name__ == '__main__':
    # A maioria das configurações de estilos devem ser colocadas após o objeto da aplicação (app). Isso deve-se ao fato /
    # do objeto QApplication ser responsável por inicializar o ambiente gráfico da aplicação. Sem ele, a aplicação /
    # não teria um contexto gráfico para aplicar estilos ou outras configurações visuais.
    app = QApplication(argv)
    janela = MainWindow()
    # Para que o ícone seja reconhecido, o path do arquivo precisa ser convertido em string.
    icon = QIcon(str(WINDOW_ICON))
    # Após converter o caminho do arquivo em string, é necessário chamá-lo através da janela (Windows) ou app (Mac)
    janela.setWindowIcon(icon)
    # janela.addLabel('texto ',20, 'right')
    # Informação acima do display
    infoCalc = InfoDisplayCalc('Info  ')
    janela.addVLayout(infoCalc)
    # O display
    display = DisplayCalc()
    janela.addVLayout(display)
    # Botões em grade
    gridButtons = GridButtons(display, infoCalc, janela)
    # Use o setDisplayHolderText para definir valores invisíveis como placeholder.
    # display.setPlaceholderText('0')
    # Lembre-se de adicionar os widgets após o layout da grade e adicionar a grade após o display. A ordem importa.
    janela.vLayout.addLayout(gridButtons)
    # gridButtons.addWidget(MainButton('C'),0,0)
    # Use o setFixedSIze através da janela para desativar o botão de maximizar.
    janela.adjustFixedSize()

    janela.show()
    app.exec()

