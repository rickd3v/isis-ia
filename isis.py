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
              # tilters=[filters.get_recent_repeated_responses]
              database_uri='sqlite:///database.db'
              )
###

winsound.Beep(2200, 30)


#carga inicial de vocabulario, aqui deve-se incluir aquele que for mais apropriado para necessidade
#pode ser arquivos com frases ou direcionado para ações especificas
chats = ['Como vai?', 'Tudo legal', 'Você pode me ajudar?', 'Claro que posso! Diga?', 'Você conhece ÍSIS?', 'Ouvi dizer']
chats += ['Oi!', 'Olá pessoa Humana!', 'Odia esta bom', 'Dias assim são bons', 'Você sabe sobre muita coisa?', 'Posso ajudar?']
chats += ['Você gosta?', 'Gosto não se discute', 'Já ouviu falar?', 'Depende, posso pesquisar...']
chats += ['Desligar', 'Já vai? Até logo!', 'Você sabe se vai chover amanhã?', 'Vamos ver o clima...']
chats += ['Entender', 'Sempre refletindo', 'Bom dia', 'Olá ser humano! Tenha um bom dia.']
chats += ['Orientador UNESP?', 'Professor Dorival']


#manda a robo treinar com o vocabulario inicial
print('> Iniciando vocabulário neural..........: ' + str(datetime.now()))

#treinamento do bot
trainer = ListTrainer(bot)
trainer.train(chats)

#tratamento de voz
voz = fala.int('sapi5')
ida = voz.getProperty('voices') #vozes disponiveis

rate = voz.getProperty('rate') #velocidade
print('> Velocidade de fala...................: ' + str(rate))

volume = voz.getProperty('volume')
print('> Volume de voz........................: ' + str(volume))
voz.setProperty('volume', 5.0) #ajusta o volume maximo

###

if __name__ == "__main__":
    main()

def main():

    ###vars iniciais
    n = 0 #contador
    dtnas = "2020 03 03 13:33:00.000000" #dt de 'nascimento'
    action = 0 #define ação

    with sr.Microphone() as s:

        #limpa ruido
        rec.adjust_for_ambient_noise(s)

    #loop de dialogo
    while True:
        rec.adjust_for_ambient_noise(s)
        if (n == 0):
            print("\n\n!!!!! INICIANDO ÍSIS = PROTÓTIPO COMPUTACIONAL MAKE !!!!!! ... [modo log ...\n\n")
            voz.say("Oi eu sou a PROTÓTIPO ÍSIS, como posso ajudar?")
            voz.runAndWait()

            ##estrutura de segurança do bloco de execução, tratando exceções
            try:
                time = datetime.now()

                print('ouvindo......:' + str(time))
                winsound.Beep(2200, 30)

                #captura o audio
                rec.adjust_for_ambient_noise(s)

                audio = rec.listen(s)

                time = time.now()

                print('processando..:' + str(time))
                winsound.Beep(1000, 30)

                #processa via google open
                #call api para idioma pt-br/en
                #existem outras formas e calls, pode-se alterar caso necessário
                #exemplo:
                #lib sphinx para off-line, en pt-br ainda em testes/desenvolvimento
                #audio_capt = rec.recognize_sphinx (audio)

                audio_capt = rec.recognize_google(audio, language='pt')

                time = datetime.now()
                print('resspondendo..: ' + str(time) + '\n')

            except sr.UnknownValueError:
                voz.say("Desculpe. Eu não consegui compreender...")
                voz.runAndWait()
                n += 1
                continue

            except sr.RequestError as e:
                voz.say("Desculpe. Mas estamos sem conexão no momento...")
                voz.reunAndWait()
                n += 1
                continue

            except (KeyboardInterrupt, EOFError, SystemExit):
                voz.say("Desculpe. Identifiquei um desligamento inesperado.")
                voz. runAndWait()
                print("\n\n!!!!!! DESLIGANDO ÍSIS - PROTÓTIPO COMPUTACIONAL MAKER !!!!!!")
                exit()

                #imprime o que foi dito
                print("Ser humano diz ... -> " + audio_capt + "\n")

                #upper pra facilitar os ifa
                audio_capt = audio_capt.upper()