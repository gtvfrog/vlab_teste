# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 07:47:47 2021

@author: gtvol
"""


#Importações
import cv2
import pytesseract
from pytesseract import Output
import difflib

#Video capture
video = cv2.VideoCapture('Video.mp4')

frame_width = int(video.get(3))
frame_height = int(video.get(4))

out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

#Quantidade de frames auxiliares
frames = 50

#Algumas palavras encontradas por erro
dicionario = ['CLINICA','PRIORITE','ABZTIOB','ATOR','TEST','PILI','ARSE','MEAS','ACES','MARL','FUELS','SNMP','AOAC','SNPM','AULD','NOUCAES','PRIORTTE','ROHE',"NOCRES","PRIORITE","PRIOR","CONC","NURSE",'NURSE',"SUNG","PCNA",'EDMAN','AMOR',"SITE","CLEA",'PCNA','JOON',"TOTES","URES","CRES","WOES","YODA","YORI","NARS","CLINIC","TONE","ORONE","SARE","CUNICA","RIOR","ALAN","NOUCRES","NOUCARS","NCCRES","OZONE","RIORTTE","IONE","TOSS","CUINICA","ODOM","METS","SONS","LOPS","PRIORI","IEEE",'MINS','ODDIE','YORE','SINS','LAGS','HUTS']
#Nomes encontrados
nomes = []

#Expressão regular
pattern = re.compile("[A-Z]+")
#Salva coordenadas de onde foi encontrado os nomes
coordenadas_nomes = []

while(True):
    frameId = int(round(video.get(1)))
    
    ret, frame = video.read()

    if ret == True:
        #Aplica limiar na imagem para o uso do pytesseract
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image,127,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C | cv2.THRESH_BINARY)
        #teste limiar
        #threshold_img = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)

        #Pinta box recentes da variavel frames para evitar deslises de algum frame ter erros na localizacao do nome
        for i in range(len(coordenadas_nomes)):        
            (x, y, w, h) = coordenadas_nomes[i][1]
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0,0), -1)
        #Exclui coordenadas antigas
        coordenadas_nomes = [e for e in coordenadas_nomes if not e[0]+frames<frameId ]
        
        #configuração do pytesseract
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(threshold_img[1], output_type=Output.DICT, config=custom_config)
       
        
        total_boxes = len(details['text'])
        for sequence_number in range(total_boxes):
            #Caso o nome já esteja salvo já faz o quadrado
            if(details['text'][sequence_number] in nomes):
                (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
            else:
                #Caso tenha palavras com letras minusculas e com tamanho menores que 3 são desconsideradas
                if int(len(details['text'][sequence_number]))>3 and pattern.fullmatch(details['text'][sequence_number]):
                        #Se a palavra encontrada estiver no dicionario de palavras erradas são desconsideradas
                        if not details['text'][sequence_number] in dicionario:
                            #É feito tambem uma varredura pra verificar se nao tem nenhuma palavra similiar as palavras erradas
                            for i in range(len(dicionario)):
                                similarity = difflib.SequenceMatcher(None, dicionario[i], details['text'][sequence_number]).ratio()
                                if(similarity>0.1):  
                                    #Caso tenha é adicionado essa palavra semelhante tambem
                                    dicionario.append(details['text'][sequence_number])
                                    break
                            #Vericado se a palavra encontrada é similiar com algum nome já salvo       
                            for i in range(len(nomes)):
                                similarity = difflib.SequenceMatcher(None, nomes[i], details['text'][sequence_number]).ratio()
                                if(similarity>0.4):
                                    #Caso seja semelhante é criado o quadrado e adicionado aos nomes
                                    (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
                                    nomes.append(details['text'][sequence_number])
                                    break
                            
                            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
                            nomes.append(details['text'][sequence_number])
                            coordenadas_nomes.append([frameId,(x, y, w, h)])
                            # print(details['text'][sequence_number])
        #show frame
        cv2.imshow("Anonimus", frame)
        #write frame
        out.write(frame)
        #Q para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   
    else:
        break
video.release()
out.release()
cv2.destroyAllWindows()
