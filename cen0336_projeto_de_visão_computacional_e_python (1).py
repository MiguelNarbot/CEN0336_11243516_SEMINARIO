# -*- coding: utf-8 -*-
"""CEN0336 - Projeto de visão computacional e Python

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eQ1_nDSZdc0ORoLobn4knW7-j9dhFVox

#Projeto de Rede Neural Convolucional, utilizando Keras

Nomes: Miguel Ângelo Cyrillo Narbot N°USP: 11243516 / Giovanni Theodoro Costa N°USP:11323370
"""

from keras.layers import Input, Lambda, Dense, Flatten  #aqui está toda a estrutura de library que iremos precisar para rodar esse modelo convolucional. 
from keras.models import Model   #entre as bibliotecas encontram-se numpy, glob, matplotlib e Keras (biblioteca aberta de Deep Learning)
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

IMAGE_SIZE=[640,640]  #tamanho das iamgens que iremos utilizar

train_directory='/content/Animais/train'     #aqui coloca-se os diretorios (locais) em que encontram-se as nossas imagens.  
test_directory='/content/Animais/test'
val_directory='/content/Animais/valid'

vgg=VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top = False)

for layer in vgg.layers:
  layer.trainable = False

folders =glob('/content/Animais/train/*')
len(folders)

x=Flatten()(vgg.output)
prediction = Dense(4, activation='softmax')(x)

model=Model(inputs=vgg.input, outputs=prediction)
model.summary()  #parametros do dataset. Vide tabela que será criada abaixo.

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#daremos as caracteristicas ao dataset. Portanto, aqui estão os parâmetros, das features, do treinamento e teste
from keras.preprocessing.image import ImageDataGenerator 

train_datagen=ImageDataGenerator(rescale=1./255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set=train_datagen.flow_from_directory(train_directory,
                                             target_size=(640, 640),
                                             batch_size=32,
                                             class_mode='categorical')

test_set=test_datagen.flow_from_directory(test_directory,
                                          target_size=(640, 640),
                                          batch_size=32,
                                           class_mode='categorical')

print(len(training_set))
print(len(test_set))

r = model.fit_generator(
    training_set,
    validation_data=test_set,
    epochs=5,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)

test_set.class_indices #como saber quais os indices introduzidos a cada classe? Essa função possibilita que isso venha a se expor.

plt.plot(r.history['loss'],label='train loss')  #a função plot, está disponível na biblioteca matplotlib. Ele permite sabermos como se comporta nosso treinamento
plt.plot(r.history['val_loss'],label='val loss') #No caso, abaixo vemos a análise estatística "loss" (perdas). Nota-se os gráficos do "train loss" e "val loss" caminham juntos. Isso delimita que o modelo e as configurações do mesmo, junto ao dataset, se encontram adequadas.  
plt.legend()
plt.show

plt.plot(r.history['accuracy'],label='train acc') #aqui os gráfico será plotado (plot)
plt.plot(r.history['val_accuracy'],label='val acc')
plt.legend() #aqui entra a biblioteca matplotlib
plt.show

model.save('animals.h5') #esse arquivo é o do saalvamento

"""#Teste do dataset"""

from io import BytesIO  #todas as bibliotecas usadas para o teste
import cv2
import imghdr
import os
import tensorflow as tf
import keras
from tensorflow.keras.utils import load_img, img_to_array

dir_path='/content/Animais/test sem folder' #aqui quero saber quais os arquivos tem na pasta
for i in os.listdir(dir_path ):
  print(i)

"""Observação: essa é apenas uma maneira de realizar a validação. Exitem outras, inclusive expostas pelo Keras."""

dir_path='/content/Animais/test sem folder' #nessa parte são realizado os testes
for i in os.listdir(dir_path ):
  img=tf.keras.utils.load_img(dir_path+'//'+ i) #captação de todas as imagens da pasta
  plt.imshow(img)
  plt.show()

  x=img_to_array(img)
  x=np.expand_dims(x,axis=0)
  images=np.vstack([x])
  val=model.predict(images)  
  if (val == 2).all():  #2 pois a saida (indice) do tamandua (classe) é 2. Veja acima!
    print('É tamanduá') #se for tamanduá printar "É tamandua". Se não (else), print não é tamandua
  else:
    print('Não é tamanduá')