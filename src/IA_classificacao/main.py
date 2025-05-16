from teachableMachine.prever import prever
import FreeSimpleGUI as sg
import os


layout = [ 
    [sg.Text('Bem vindo ao Classificador de Fissuras SOD', key='-IN-')],
    [sg.Text('Comece inserindo sua imagem:', key='-INS-'), 
     sg.In(key='-FILE-', enable_events=True, visible=False),
     sg.FileBrowse(button_text='Insira sua imagem aqui', file_types=(("Image Files", ["*.jpg", ".png", ".jpeg"]),))],
    [sg.Text('Classificação do modelo', key='-TXT-', visible=False)],
    [sg.Text('', key='-Class-', visible=False)],
    [sg.Text('', key='-Conf-', visible=False)],

]

window = sg.Window('Visualizador de Imagens', layout, resizable=True, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    caminho_arquivo = values['-FILE-']
    if event == '-FILE-': # Se um arquivo for selecionado
        if os.path.exists(caminho_arquivo):
            classificacao, confianca = prever(caminho_arquivo)
            window['-TXT-'].update(visible=True)
            texto_resultado = f"A fissura é do tipo: {classificacao}"
            texto_confianca = f"Nível de confiança: {confianca:.2%}"
            window['-Class-'].update(texto_resultado, visible=True)
            window['-Conf-'].update(texto_confianca, visible=True)


