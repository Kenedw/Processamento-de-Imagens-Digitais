 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys
from math import sqrt
import numpy as np
from PIL import Image

##########################
#Primeiro Trabalho de PDI#
##########################


def abreImagem(destino):
	imagem = Image.open(destino)
	return imagem

def salvaImagem(imagem, destino):
	imagem.save(destino, 'png')

def criaImagem(i,j):
	imagem = Image.new("RGB",(i,j))
	return imagem

def pegaPixel(imagem,i,j):
	width, height = imagem.size
	if((i>width) or (j>height)):
		return None
	pixel = imagem.getpixel((i,j))
	return pixel

#1.1 - Conversão RGB-YIQ-RGB
def RGB_YIQ_RGB(imagem):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			#RGB PARA YIQ
			y = r * 0.299 + g * 0.587 + b * 0.114
			i = r * 0.596 - g * 0.275 - b * 0.321
			q = r * 0.212 - g * 0.523 + b * 0.311
			#YIQ PARA RGB
			r = 1*y + 0.956*i + 0.621*q
			g = 1*y - 0.272*i - 0.647*q
			b = 1*y - 1.105*i + 1.702*q

			#Tratando os limites
			r = min(max(r,0),255) 
			g = min(max(g,0),255)
			b = min(max(b,0),255)

			#print(r,g,b)
			pixels[k,j] = (int(r),int(g),int(b))

	return new

#1.2 - Exibição de bandas individuais (R, G e B) como imagens monocromáticas ou coloridas (em tons de R, G ou B, respectivamente)

def Mono(imagem):
	width, height = imagem.size
	newR = criaImagem(width,height)
	newB = criaImagem(width,height)
	newG = criaImagem(width,height)

	red = newR.load()
	green= newB.load()
	blue = newG.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]

			cinzaR = r * 0.299 + r * 0.587 + r * 0.114
			cinzaG = g * 0.299 + g * 0.587 + g * 0.114 
			cinzaB = b * 0.299 + b * 0.587 + b * 0.114 


			#r = min(max(r,0),255)
			red[k,j]	= (int(cinzaR),int(cinzaR),int(cinzaR))
			green[k,j]	= (int(cinzaG),int(cinzaG),int(cinzaG))
			blue[k,j]	= (int(cinzaB),int(cinzaB),int(cinzaB))

			#pixels[k,j] = (int(cinza),int(cinza),int(cinza))

	return newR, newB, newG

def Banda_RGB(imagem):
	width, height = imagem.size

	newR = criaImagem(width,height)
	newB = criaImagem(width,height)
	newG = criaImagem(width,height)

	red = newR.load()
	green= newB.load()
	blue = newG.load()

	for i in range(0,3):
		for k in range(0,width):
			for j in range(0,height):

				pixel = pegaPixel(imagem, k, j)

				r = pixel[0]
				g = pixel[1]
				b = pixel[2]
					
				if(i==0):
					g = 0
					b = 0			
					red[k,j] = (int(r),int(g),int(b))
				if(i==1):
					r = 0
					b = 0
					green[k,j] = (int(r),int(g),int(b))
				if(i==2):
					r = 0
					g = 0
					blue[k,j] = (int(r),int(g),int(b))

	return newR, newB, newG

def Negativo(imagem):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			
			r = (-1*r+255)
			g = (-1*g+255)
			b = (-1*b+255)

			pixels[k,j] = (int(r),int(g),int(b))

	return new

#1.4 - Brilho Aditivo
def BrilhoAditivo(imagem,c):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]

			r = r+c
			g = g+c
			b = b+c

			#Tratando os limites
			r = min(max(r,0),255)
			g = min(max(g,0),255)
			b = min(max(b,0),255)

			pixels[k,j] = (int(r),int(g),int(b))

	return new

#1.5 - Brilho Multiplicativo
def BrilhoMultiplicativo(imagem,d):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]

			r = r*d
			g = g*d
			b = b*d

			#Tratando os limites
			r = min(max(r,0),255)
			g = min(max(g,0),255)
			b = min(max(b,0),255)

			pixels[k,j] = (int(r),int(g),int(b))

	return new

#1.8 - Limiarização com limiar m escolhido pelo usuário.
def Limiarizacao(imagem,m):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	for k in range(0,width):
		for j in range(0,height):

			pixel = pegaPixel(imagem, k, j)

			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			# result = (false,true)[condition]
			r = (255,0)[r<=m]
			g = (255,0)[g<=m]
			b = (255,0)[b<=m]

			pixels[k,j] = (int(r),int(g),int(b))
	return new

#1.7 Filtro mediana m x n
def MeanMid(numbers):
		A = numbers[(len(numbers)//2)]
		B = numbers[((len(numbers)+1)//2)]
		return tuple([(A[i]+B[i])//2 for i in range(len(A))])
		 

def FiltroMediana(imagem,m,n):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()

	Ntotal = m*n
	NtotalMedian = int(Ntotal/2)+1
	window = [] 

	for k in range(0,width): #movimento na imagem
		for j in range(0,height):
			for h in range(0,m): #movimento na janela do filtro
				for g in range(0,n):
					PosW = ((m//2)-h,h)[h<(m//2)]
					PosH = ((n//2)-g,g)[g<(n//2)]
					if(((k+PosW)<width and (k+PosW)>=0 and (j+PosH)<height and (j+PosH)>=0)):
						pixel = pegaPixel(imagem, k+PosW, j+PosH)
						window.append(pixel)
					# else:
					# 	window.append((0,0,0))
			window.sort()
			
			if (Ntotal % 2 == 0):
				pixels[k,j] = (MeanMid(window))		
			else:
				pixels[k,j] = (window[(len(window)//2)])
			window.clear()
	return new

#1.6. Convolução m x n com bias (viés, offset). Testar com filtros Média e Sobel
# def Convolution(imagem):
# 	width, height = imagem.size
# 	new = criaImagem(width,height)
# 	pixels = new.load()

# 	for k in range(0,width): #movimento na imagem
# 		for j in range(0,height):
# 			if(k>=width//2 and j>=height//2):
# 				return new
# 			pixels[width-k-1,height-j-1],pixels[k,j] = pegaPixel(imagem,k,j),pegaPixel(imagem,width-k-1,height-j-1)
# 	return new

def ConvolutionWindow(window,width):
	for k in range(0,width):
		if(k>=width//2):
			return window
		window[width-k-1],window[k] = window[k],window[width-k-1]
	return window

def Mean(numbers):
	soma=[0,0,0]
	for i in numbers:
		for j in range(len(i)):
			soma[j] = soma[j] + i[j]
	return tuple([i//len(numbers) for i in soma])

def FiltroMedia(imagem,m,n):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()
	window = [] 

	for k in range(0,width): #movimento na imagem
		for j in range(0,height):
			for h in range(0,m): #movimento na janela do filtro
				for g in range(0,n):
					PosW = ((m//2)-h,h)[h<(m//2)]
					PosH = ((n//2)-g,g)[g<(n//2)]
					if(((k+PosW)<width and (k+PosW)>=0 and (j+PosH)<height and (j+PosH)>=0)):
						pixel = pegaPixel(imagem, k+PosW, j+PosH)
						window.append(pixel)
					# else:
					# 	window.append((0,0,0))
			window = ConvolutionWindow(window,len(window))
			pixels[k,j] = (Mean(window))		
			window.clear()
	return new

def edgeH(window):
	result = []
	matrix = [1,2,1,0,0,0,-1,-2,-1]
	for idx,i in enumerate(window):
		aux = [0,0,0]
		for j in range(0,3):
			aux[j] = min(max(0,i[j]*matrix[idx]),255)
		result.append(tuple(aux))
	return result

def edgeV(window):
	result = []
	matrix = [-1,0,1,-2,0,2,-1,0,1]
	for idx,i in enumerate(window):
		aux = [0,0,0]
		for j in range(3):
			aux[j] = min(max(0,i[j]*matrix[idx]),255)
		result.append(tuple(aux))
	return result

def MeanSQRT(window):
	SomaR=0
	SomaG=0
	SomaB=0

	for j in range(0,len(window)):
		SomaR += window[j][0]*window[j][0]
		SomaG += window[j][1]*window[j][1]
		SomaB += window[j][2]*window[j][2]

	somaR = int(sqrt(SomaR/len(window)))
	SomaG = int(sqrt(SomaG/len(window)))
	SomaB = int(sqrt(SomaB/len(window)))

	return (somaR,SomaG,SomaB)

def FiltroSobel(imagem):
	width, height = imagem.size
	new = criaImagem(width,height)
	pixels = new.load()
	window = [] 

	for k in range(0,width): #movimento na imagem
		for j in range(0,height):
			for h in range(0,3): #movimento na janela do filtro
				for g in range(0,3):
					PosW = (1-h,h)[h<1]
					PosH = (1-g,g)[g<1]
					if(((k+PosW)<width and (k+PosW)>=0 and (j+PosH)<height and (j+PosH)>=0)):
						pixel = pegaPixel(imagem, k+PosW, j+PosH)
						window.append(pixel)
					else:
						window.append((0,0,0))
			window = ConvolutionWindow(window,len(window))
			windowH = edgeH(window)
			windowV = edgeV(window)
			pixels[k,j] = (MeanSQRT(windowH+windowV))		
			window.clear()
	return new

if __name__ == "__main__":

		fileInput = sys.argv[1]
		fileOutput = sys.argv[2]
		
		while(True):
			imagem = abreImagem(fileInput)
			MenuSelect = input(
			" _____                                           _          ____  _     _ _       _      _        _                           \n"
			+"|  _  |___ ___ ___ ___ ___ ___ ___ _____ ___ ___| |_ ___   |    \|_|___|_| |_ ___| |   _| |___   |_|_____ ___ ___ ___ ___ ___ \n"
			+"|   __|  _| . |  _| -_|_ -|_ -| .'|     | -_|   |  _| . |  |  |  | | . | |  _| .'| |  | . | -_|  | |     | .'| . | -_|   |_ -|\n"
			+"|__|  |_| |___|___|___|___|___|__,|_|_|_|___|_|_|_| |___|  |____/|_|_  |_|_| |__,|_|  |___|___|  |_|_|_|_|__,|_  |___|_|_|___|\n"
			+"                                                                   |___|                                     |___|            \n\n\n\n"		
			+"\t+---+-------------------------------------------------------+\n"
			+"\t|   |           Digite o numero da opção desejada           |\n"
			+"\t+---+-------------------------------------------------------+\n"
			+"\t| 1 | RGB-YIQ-RGB                                           |\n"
			+"\t| 2 | Mono R G B                                            |\n"
			+"\t| 3 | Banda R G B                                           |\n"
			+"\t| 4 | Negativo                                              |\n"
			+"\t| 5 | BrilhoAditivo                                         |\n"
			+"\t| 6 | Brilho Multiplicativo                                 |\n"
			+"\t| 7 | Limiarização                                          |\n"
			+"\t| 8 | Filtro Mediana                                        |\n"
			+"\t| 9 | Filtro Media                                          |\n"
			+"\t| 10| Filtro Sobel                                          |\n"
			+"\t| 0 | Sair                                                  |\n"
			+"\t+---+-------------------------------------------------------+\n"
			)
			if(MenuSelect == '1'):
				#RGB_YIQ_RGB
				RGB_YIQ_RGB = RGB_YIQ_RGB(imagem)
				salvaImagem(RGB_YIQ_RGB, 'saida/'+fileOutput+'_RGB-YIQ-RGB.png')
				print("Filtro RGB-YIQ-RGB aplicado com sucesso.")
			elif(MenuSelect == '2'):
				#Monocromática
				[MonoR, MonoG, MonoB] = Mono(imagem)
				salvaImagem(MonoR, 'saida/'+fileOutput+'_MonoR.png')
				salvaImagem(MonoG, 'saida/'+fileOutput+'_MonoG.png')
				salvaImagem(MonoB, 'saida/'+fileOutput+'_MonoB.png')
				print("Filtro Monocromatico aplicado com sucesso.")
			elif(MenuSelect == '3'):
				#Bandas Red, Green e Blue
				[Banda_R,Banda_G,Banda_B] = Banda_RGB(imagem)
				salvaImagem(Banda_R,'saida/'+fileOutput+'_Banda_R.png')
				salvaImagem(Banda_G,'saida/'+fileOutput+'_Banda_G.png')
				salvaImagem(Banda_B,'saida/'+fileOutput+'_Banda_B.png')
				print("Filtro Red aplicado com sucesso.")
			elif(MenuSelect == '4'):
				#Negativo
				Negativo = Negativo(imagem)
				salvaImagem(Negativo,'saida/'+fileOutput+'_Negativo.png')
				print("Filtro Negativo aplicado com sucesso.")
			elif(MenuSelect == '5'):
				#Brilho Aditivo
				c = int(input("Valor do aditivo: "))
				BrilhoAditivo = BrilhoAditivo(imagem,c)
				salvaImagem(BrilhoAditivo,'saida/'+fileOutput+'_BrilhoAditivo_'+str(c)+'.png')
				print("Filtro de Brilho Aditivo aplicado com sucesso.")
			elif(MenuSelect == '6'):
				#Brilho Multiplicativo
				d = int(input("Valor do multiplicativo: "))
				BrilhoAditivo = BrilhoMultiplicativo(imagem,d)
				salvaImagem(BrilhoAditivo,'saida/'+fileOutput+'_brilhoMultiplicativo_'+str(d)+'.png')
				print("Filtro de Brilho Multiplicativo aplicado com sucesso.")
			elif(MenuSelect == '7'):
				#Limiarização
				m = int(input("Valor do limiar: "))
				Limiarizacao = Limiarizacao(imagem,m)
				salvaImagem(Limiarizacao,'saida/'+fileOutput+'_LimiarM_'+str(m)+'.png')
				print("Filtro de Limiarizacao aplicado com sucesso.")
			elif(MenuSelect == '8'):
				#Filtro da mediana
				m = input("Entre com o valor da linha: ")
				n = input("Entre com o valor da coluna: ")
				FiltroMediana = FiltroMediana(imagem,int(m),int(n))
				salvaImagem(FiltroMediana,'saida/'+fileOutput+'_FiltroMediana_'+m+'X'+n+'.png')
			elif(MenuSelect == '9'):
				#Filtro da media
				m = input("Entre com o valor da linha: ")
				n = input("Entre com o valor da coluna: ")
				FiltroMedia = FiltroMedia(imagem,int(m),int(n))
				salvaImagem(FiltroMedia,'saida/'+fileOutput+'_FiltroMedia_'+m+'X'+n+'.png')
			elif(MenuSelect == '10'):
				#Filtro sobel
				FiltroSobel = FiltroSobel(imagem)
				salvaImagem(FiltroSobel,'saida/'+fileOutput+'_FiltroSobel.png')
			elif(MenuSelect == '0'):
				print("Programa finalizado com sucesso.")
				break;
