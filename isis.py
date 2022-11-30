import sys  # recursos do sistema
import os  # recursos do sistema operacional
import numpy as np  # cientifica matematica
import winsound  # recursos windows de som, para avisar os precessos em andamento (carga, escuta, resposta)

from datetime import datetime  # recursos de data
# automação de telas/processos windows (trabalho na camada de mensagens do sistema operacional)
from pywinauto.application import Application
import string  # texto

import pyttsx3 as fala  # conversao de texto para audio

winsound.Beep(2200, 30)
print("\n> Importando recursos de fala..............: " + str(datetime.now()))

print("> Importando recursos de recognição..........: " + str(datetime.now()))
import speech_recognition as sr  # reconhecimento de fala com i.a

winsound.Beep(2200, 30)

print("> Importando recursos de conversação.........: " + str(datetime.now()))

from chatterbot import ChatBot  # recursos de chatbot com i.a
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

winsound.Beep(2200, 30)

print("> Importando recursos de visão computacional..: " + str(datetime.now()))
import cv2  # visao computacional

winsound.Beep(2200, 30)
##

rec = sr.Recognizer()  # tratamento do reconhecimento de fala

###tratamento da robo
##bot - ChatBot('ISIS') #inicia o Bot no ambiente

bot = ChatBot('ISIS',
              storage_adapter='chatterbot.storage.SQLStorangeAdapter',

              logic_adapters=[
                  'chatterbot.logic.MathematicalEvaluation',
                  # 'chatterbot.logic.TimeLogicAdapter',
                  'chatterbot.logic.BestMatch',
              ],
              # filters=[filters.get_recent_repeated_responses]
              database_uri='sqlite:///database.db'
              )
###

winsound.Beep(2200, 30)

# carga inicial de vocabulario, aqui deve-se incluir aquele que for mais apropriado para necessidade
# pode ser arquivos com frases ou direcionado para ações especificas
chats = ['Como vai?', 'Tudo legal', 'Você pode me ajudar?', 'Claro que posso! Diga?', 'Você conhece ÍSIS?',
         'Ouvi dizer']
chats += ['Oi!', 'Olá pessoa Humana!', 'Odia esta bom', 'Dias assim são bons', 'Você sabe sobre muita coisa?',
          'Posso ajudar?']
chats += ['Você gosta?', 'Gosto não se discute', 'Já ouviu falar?', 'Depende, posso pesquisar...']
chats += ['Desligar', 'Já vai? Até logo!', 'Você sabe se vai chover amanhã?', 'Vamos ver o clima...']
chats += ['Entender', 'Sempre refletindo', 'Bom dia', 'Olá ser humano! Tenha um bom dia.']
chats += ['Orientador UNESP?', 'Professor Dorival']

# manda a robo treinar com o vocabulario inicial
print('> Iniciando vocabulário neural..........: ' + str(datetime.now()))

# treinamento do bot
trainer = ListTrainer(bot)
trainer.train(chats)

###exemplos de treino alternativos
#trainer = ChatterBotCorpusTrainer(ChatBot)
#trainer.train(chats)
#trainer.train("chatterbot.corpus.english") portuguese

#bot.set_trainer(ListTrainer)
#bot.train(chats) #executa o treino com o vocabulario fornecido

##

# tratamento de voz
voz = fala.init('sapi5')
ids = voz.getProperty('voices')  # vozes disponiveis

rate = voz.getProperty('rate')  # velocidade
print('> Velocidade de fala...................: ' + str(rate))
voz.setProperty('rate', rate + 75) #ajusta velocidade da voz, buscando algo mais 'natural' +20

volume = voz.getProperty('volume')
print('> Volume de voz........................: ' + str(volume))
voz.setProperty('volume', 5.0)  # ajusta o volume maximo

###

###funçao de visão computacional simples para detecção de objetos cor verde,
###também pode-se alterar para a necessidade em especifico
def cv():
    # Iniciamos camera
    captura = cv2.VideoCapture(0)

    while (1):

        # Captura img em RGB -> HSV
        _, image = captura.read()
        hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

        # Faixa de cores desejadas
        verde_baixos = np.array([49, 50, 50], dtype=np.uint8)  # 49 50 50
        verde_altos = np.array([80, 255, 255], dtype=np.uint8)  # 80 255 255

        # mascara com essa faixa de cores
        mask = cv2.inRange(hsv, verde_baixos, verde_altos)

        # encontrar a area onde o objeto esta
        moments = cv2.moments(mask)
        area = moments['m00']

        if (area > 200000):
            # centro do objeto detectado
            x = int(moments['m10'] / moments['m00'])
            y = int(moments['m01'] / moments['m00'])

            # Mostramos coordenadas
            # print("x = ", x)
            # print("y = ", y)

            # retangulo de detecção
            cv2.rectangle(imagem, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), 2)
            cv2.putText(imagem, "pos x,y:" + str(x) + " , " + str(y), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 1)
            #cv2.FRONT_HERSHEY_SIMPLEX

        # mascara x original
        ##cv2.imshow('mask', mask)
        cv2.imshow('Câmera Atual do Dispositivo', imagem)

        # tecla = cv2.waitKey(5) & 0xFF = shutdown
        if cv2.waitKey(1) & 0xFF == ord('q'):
            captura.release()
            break
    # libera janela
    cv2.destroyAllWindows()
###---
if __name__ == "__main__":
    main()
###----

#Loop 'robotico'
#inicia captura de audio
def main():

    ###vars iniciais
    n = 0  # contador
    dtnas = "2020 03 03 13:33:00.000000"  # dt de 'nascimento'
    action = 0  # define ação

    with sr.Microphone() as s:

        # limpa ruido
        rec.adjust_for_ambient_noise(s)

    # loop de dialogo
    while True:
        rec.adjust_for_ambient_noise(s)
        if (n == 0):
            print("\n\n!!!!! INICIANDO ÍSIS = PROTÓTIPO COMPUTACIONAL MAKE !!!!!! ... [modo log] ...\n\n")
            voz.say("Oi eu sou a PROTÓTIPO ÍSIS, como posso ajudar?")
            voz.runAndWait()

            ##estrutura de segurança do bloco de execução, tratando exceções
            try:
                time = datetime.now()

                print('ouvindo......:' + str(time))
                winsound.Beep(2200, 30)

                # captura o audio
                rec.adjust_for_ambient_noise(s)

                audio = rec.listen(s)

                time = time.now()

                print('processando..:' + str(time))
                winsound.Beep(1000, 30)

                # processa via google open
                # call api para idioma pt-br/en
                # existem outras formas e calls, pode-se alterar caso necessário
                # exemplo:
                # lib sphinx para off-line, en pt-br ainda em testes/desenvolvimento
                # audio_capt = rec.recognize_sphinx (audio)

                audio_capt = rec.recognize_google(audio, language='pt')

                time = datetime.now()
                print('respondendo..: ' + str(time) + '\n')

            except sr.UnknownValueError:
                voz.say("Desculpe. Eu não consegui compreender...")
                voz.runAndWait()
                n += 1
                continue

            except sr.RequestError as e:
                voz.say("Desculpe. Mas estamos sem conexão no momento...")
                voz.runAndWait()
                n += 1
                continue

            except (KeyboardInterrupt, EOFError, SystemExit):
                voz.say("Desculpe. Identifiquei um desligamento inesperado.")
                voz.runAndWait()
                print("\n\n!!!!!! DESLIGANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER !!!!!!")
                exit()

                # imprime o que foi dito
                print("Ser humano diz ... -> " + audio_capt + "\n")

                # upper pra facilitar os ifs
                audio_capt = audio_capt.upper()

                ###tratamento de ações executadas pelo protótipo, pode-se incluir quantas desejar

                #verifica p que foi dito e executa ação em WINDOWS (você pode definir palavras chaves para suas proprias ações e também outros sistemas operacionais)

                if(audio_capt.find('DESLIGAR') >= 0):
                    print("\n\n||||| DESLIGANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER ||||| \n ||||| Andre Medeiros "
                    # + str(n) + "\n"

                    voz.say("Desligando...")
                    voz.runAndWait()

                    #fim dialogo
                    exit()

                if (audio_capt.find('YOUTUBE' >= 0):
                    busca = audio_capt[audio_capt.find('YOUTUBE')+8:]
                        print("\nAção executada: Procurando videos com o tema... " + busca + "\n")
                        #abre o caminho/path
                            os.startfile("https://www.youtube.com/results?search_query=" + busca)
                            action = 1
                if (audio_capt.find('OUTLOOK') >= 0):
                    print ("\nAção executada: Abrindo e-mail...\n")
                        os.startfile("Outlook.exe")
                        action = 1
                if (audio_capt.find('GMAIL') >= 0):
                    print("\nAção executada: Abrindo Gmail... \n")
                        os.startfile("http://gmail.com")
                        action = 1
                if (audio_capt.find('CBN') >= 0):
                    print("\nAção executada: Abrindo radio on-line...\n")
                        os.startfile("http://cbn.globoradio.globo.com/servicos/estudio-ao-vivo/ESTUDIO-AO-VIVO.htm?praca=SP")
                        action = 1

                if (audio_capt.find('PESQUISA') >= 0):
                    busca = audiio_capt[audio_capt.find("PESQUISA") + 9:]
                    print("\nAção executada: Pesquisando no Google sobre... " + busca + "\n")

                    #abre o caminho invocando o browser padrao
                        os.startfile("https://www.google.com.br/search?hl=pt-BR&q=" + busca))
                        action = 1

                if (audio_capt.find('TEMPO') >= 0) or (audio_capt.find('CLIMA') >= 0):
                    print("\nAção executada: Verificando as condições climáticas...\n")
                    #abre o caminho invocando o browser padrao
                    os.startfile('https://www.ipmetradar.com.br/')
                    action = 1

                if(audio_capt.find('ATIVAR CAMERA' >= 0) or (audio_capt.find('ATIVAR CÂMERA') >= 0) or (audio_capt.find('ATIVAR A CÂMERA') >= 0):
                   voz.say("Ativando câmera para identificar objetos")
                    voz.runAndWait()
                    ###inicia camera
                    cv()
                    action = 1

                if (audio_capt.find('DIGITE') >= 0):
                    )

")




####
if (audio_capt.find('DIGITE') >= 0):
    repetir = audio_capt[audio_capt.find('DIGITE')+5=6:]

    print("\nAção executada: Repetindo a frase ..." + repetir + "\n")

    ##TESTE - automação com pywinauto - escrever o que foi dito pelo humano num arquivo .txt
    app = Application().start("notepad.exe")

    # 'digita' o texto capturado pelo audio
    app.UnititledNotepad.Edit.type_keys(repetir, with_spaces = True)
    ##-------
if (audio_capt.find('ATIVAR CAMERA') >= 0) or (audio_capt.find('ATIVAR CÂMERA') >= 0)

    voz.say("Ativando câmera para identificar objetos")
    voz.runAndWait()

    ###inicia camera
    cv()
    action = 1