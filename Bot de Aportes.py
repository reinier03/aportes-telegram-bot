import telebot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ReplyKeyboardRemove
import zipfile
from flask import Flask, request
import json
import os
import threading
from random import randint
from time import sleep
import dill
import callback_querys
import requests
import time
import aportes_usefull_functions
import Auto_Publicaciones_Class



os.chdir(os.path.dirname(os.path.abspath(__file__)))

#publicaciones_auto = diccionario de tipo de publicaciones automaticas que se envian al canal desde diferentes webs
#Estructura: publicaciones_auto = { "otaku" : {"activo": True ,"frecuencia": 3, "texto_adjunto" : "#otaku" , proxima_publicacion: float(time.time())}}
publicaciones_auto = {}
canal=os.environ["canal"]
bot=telebot.TeleBot(os.environ["token"], parse_mode="html", disable_web_page_preview=True)
diccionario_publicaciones={}
lista_usuarios_baneados=[]
publicaciones_canal=True
publicaciones_usuarios=True
admin=os.environ["admin"]

try:
    grupo_vinculado_canal=os.environ["grupo"]
except:
    grupo_vinculado_canal=False
    
if not canal.isdigit() and not canal.startswith("-"):
    if not canal.startswith("@"):
        canal=f"@{canal}"
        canal=bot.get_chat(canal).id
    else:
        canal=bot.get_chat(canal).id
        
elif canal.startswith("-"):
    canal=int(canal)
    
if grupo_vinculado_canal:
    if not grupo_vinculado_canal.isdigit() and not grupo_vinculado_canal.startswith("-"):
        if not grupo_vinculado_canal.startswith("@"):
            grupo_vinculado_canal=f"@{grupo_vinculado_canal}"
            grupo_vinculado_canal=bot.get_chat(grupo_vinculado_canal).id
        else:
            grupo_vinculado_canal=bot.get_chat(grupo_vinculado_canal).id
            
    elif grupo_vinculado_canal.startswith("-"):
        grupo_vinculado_canal=int(grupo_vinculado_canal)
    

    




    
    


    
def cargar_variables():
    with open("variables.dill", "rb") as archive:
        lista=dill.load(archive)
        for key, value in lista.items():
            globals()[key]=value

    return


if os.path.isfile("variables.dill"):
    cargar_variables()

if publicaciones_usuarios==False:
    bot.send_message(admin, "<u><b>ADVERTENCIA</b></u>:\nLos aportes al canal por parte de los usuarios están desabilitados")

def guardar_variables():
    with open("variables.dill", "wb") as archive:
        lista={
            "lista_usuarios_baneados": lista_usuarios_baneados,
            "grupo_vinculado_canal" : grupo_vinculado_canal,
            "publicaciones_canal" : publicaciones_canal,
            "publicaciones_usuarios" : publicaciones_usuarios,
            "publicaciones_auto" : publicaciones_auto
        }
        dill.dump(lista, archive)
    return




bot.send_message(admin, "Estoy online bitch :)")

bot.set_my_commands([
    telebot.types.BotCommand("/help", "Ofrece ayuda sobre el funcionamiento de este bot"),
    telebot.types.BotCommand("/enviar", "Para enviar una publicación al canal"),
    telebot.types.BotCommand("/panel", "Sólo disponible para mi creador :)")
], telebot.types.BotCommandScopeAllPrivateChats())


@bot.message_handler(commands=["panel"])
def cmd_panel(message):
    if not message.chat.type == "private":
        return
    if not int(message.chat.id)==int(bot.get_chat(admin).id):
        bot.send_message(message.chat.id, f"Lo siento pero no eres mi creador @{bot.get_chat(admin).username}:)\nNo puedes acceder a esta sección")
        return
    
    panel_administrador=InlineKeyboardMarkup(row_width=1)
    panel_administrador.add(InlineKeyboardButton("Administrar Mensajes 👀📋", callback_data="admin_msg"))
    # panel_administrador.add(InlineKeyboardButton("Dejar de/Volver a Recibir mensajes del Canal", callback_data="Parar canal"))
    # panel_administrador.add(InlineKeyboardButton("Dejar de/Volver a Recibir mensajes de Usuarios", callback_data="Parar Usuarios"))
    
    panel_administrador.add(InlineKeyboardButton("Administrar Usuarios 🙍‍♂️", callback_data="Admin Usuarios"))
    # panel_administrador.add(InlineKeyboardButton("Banear a un usuario 🙍‍♂️❌", callback_data="Banear Usuario"))
    # panel_administrador.add(InlineKeyboardButton("Desbanear a un usuario 🙍‍♂️➕", callback_data="Desbanear Usuario"))
    # panel_administrador.add(InlineKeyboardButton("Ver lista de usuarios baneados 👀📋", callback_data="Ver Lista"))
    # panel_administrador.add(InlineKeyboardButton("Ver username de usuario por ID 👀", callback_data="ver usuario"))
    
    panel_administrador.add(InlineKeyboardButton("Definir Grupo Adjunto 👥", callback_data="Grupo Adjunto"))
    panel_administrador.add(InlineKeyboardButton("Copia de Seguridad 🎁", callback_data="Copia de Seguridad"))
    # panel_administrador.add(InlineKeyboardButton("Enviar copia de seguridad 🎁", callback_data="Enviar Archivo"))
    # panel_administrador.add(InlineKeyboardButton("Recibir copia de seguridad ✒", callback_data="Recibir Archivo"))
    
    panel_administrador.add(InlineKeyboardButton("Administrar Publicaciones Automáticas", callback_data="admin_auto"))
    
    panel_administrador.add(InlineKeyboardButton("Ver variables del script 👀🗒", callback_data="script"))
    bot.send_message(admin, "Qué pretendes hacer?", reply_markup=panel_administrador)





@bot.callback_query_handler(func=lambda x: True)
def cmd_process_callback(call):
    global lista_usuarios_baneados
    global publicaciones_usuarios
    global publicaciones_canal
    global canal
    global grupo_vinculado_canal
    return callback_querys.recibir_querys(bot, call, lista_usuarios_baneados, publicaciones_usuarios, publicaciones_canal, canal, grupo_vinculado_canal, publicaciones_auto)




@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    if not message.chat.type == "private":
        return
    if message.from_user.language_code=="es":
        bot.send_message(message.chat.id, f"<b>Bienvenido al Bot de Aportes de @{bot.get_chat(canal).username}</b> 😁\n\nLa idea con este bot es que los usuarios TAMBIÉN aporten contenido al canal además de los propios admins\n\n<u>Contenido Aceptado por el Bot</u>:\n<b>Imágenes</b>\n<b>Vídeos</b>\n<b>Música</b>\n<b>Documentos</b> (PDF, EPUB, etcétera)\n <b>Encuestas</b> que envíe El Usuario\n-Más allá de esos archivos, no serán aceptado a no ser que a futuro @{bot.get_chat(admin).username} lo decida-\n\nNota Importante:\nEl límite de peso de los documentos es de 50 MB mientras que para los vídeos, fotos y archivos de audio son de 20 MB, no sobrepases el límite con el peso de tus archivos o no se enviará lo que quieres compartir\n\n¿Qué esperas? Empieza llevando tu contenido a nuestro canal escribiendo /enviar :)")
        bot.send_message(message.chat.id, "Este bot está desarrollado por @mistakedelalaif\nSi quieres un bot igual o parecido contáctalo y te lo hará:)")
        
    else:
        bot.send_message(message.chat.id, f"Welcome to the Contribution Bot of @{bot.get_chat(canal).username} 😁\n\nThe idea with this bot is that users ALSO contribute content to the channel in addition to the admins themselves\n\n<u>Content Accepted by the Bot</u>:\nImages\nVideos\nMusic\nDocuments (PDF, EPUB, etc.)\nSurveys sent by the User\n-Beyond those files, they will not be accepted unless in the future @{bot.get_chat(admin ).username} decide-\n\nImportant Note:\nThe weight limit for documents is 50 MB while for videos, photos and audio files they are 20 MB, do not exceed the limit with the weight of your files or what you want to share will not be sent\n\nWhat are you waiting for?  Start by bringing your content to our channel by typing /enviar :)")
        bot.send_message(message.chat.id, "This bot is developed by @mistakedelalaif\nIf you want the same or similar bot, contact him and he will make it for you:)")
    return
    
    
    
@bot.message_handler(commands=["enviar"])
def cmd_ingresar(message):
    global diccionario_publicaciones
    if not message.chat.type == "private":
        return
        
    if publicaciones_usuarios==False:
        if message.from_user.language_code=="es":
            bot.send_message(message.chat.id, f"Lo siento :( Mi creador @{bot.get_chat(admin).username} me quitó el acceso a los mensajes TEMPORALMENTE, por alguna razón (sabrá Dios cual)\n\n<b>Vuelve más tarde</b> para comprobar si estoy autorizado a empezar a recibir aportes nuevamente (o pregúntale)")
            
        else:
            bot.send_message(message.chat.id, f"Sorry :( My creator @{bot.get_chat(admin).username} removed my access to messages TEMPORARILY, for some reason (only God knows why)\n\nPlease come back later to check If I am authorized to start receiving contributions again (or ask)")
            
        return
        
    for i in lista_usuarios_baneados:
        if i == bot.get_chat(message.from_user.id).id:
            bot.send_message(message.chat.id, f"Al parecer mi administrador @{bot.get_chat(admin).username} te baneó por alguna razón y ya no puedes hacer aportes al canal @{bot.get_chat(canal).username}\nTe habrás portado mal seguramente, ni idea, soy solamente un bot 😐\n\nVe a hablar con él y pídele explicación👇👇", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("El Administrador", url=f"https://t.me/{bot.get_chat(admin).username}")))
            return
    
    if message.text.split(" "):
        canal_destino = int(message.text.split(" ")[1])
        
        
    else:
                    
        bot.send_message(message.chat.id, f"¿A cuál de los canales planeas hacer el aporte?\n\n<a href='{bot.get_chat(-1001161864648).username}'>{bot.get_chat(-1001161864648).title}</a> (Toca para ver más información)\n<a href='{bot.get_chat(-1001795230328).username}'>{bot.get_chat(-1001795230328).title}</a> (Toca para ver más información)\n\n", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(bot.get_chat(-1001161864648).title, callback_data="canal:-1001161864648")][InlineKeyboardButton(bot.get_chat(-1001795230328).title, callback_data="canal:-1001795230328")]]))
        
        @bot.callback_query_handler(func=lambda call: "canal:" in call.data)
        def extraer(call):
            canal_destino = int(call.data.split(":")[1])
            return canal_destino
    
    markup=ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=2,
        input_field_placeholder="¿Quieres mostrar tu nombre en el #aporte?"
    )
    markup.add("Si", "No")
    msg=bot.send_message(message.chat.id, "¿Quieres mostrar tu nombre en el aporte?\n\n(Presiona en '<b>Si</b>' Para que se envíe tu usuario como autor'\nPresiona <b>No</b>' Para que sea un aporte anónimo)", reply_markup=markup)
    bot.register_next_step_handler(msg, hacer_aporte, canal_destino)
    
def hacer_aporte(message, canal_destino):
    mostrar_nombre=""
    if message.text=="Si":
        bot.send_message(message.chat.id, "Muy bien, mostraré tu nombre en la publicación", reply_markup=ReplyKeyboardRemove())
        mostrar_nombre=True
    elif message.text=="No":
        bot.send_message(message.chat.id, "Muy bien, no mostraré tu nombre en la publicación", reply_markup=ReplyKeyboardRemove())
        mostrar_nombre=False
    else:
        bot.send_message(message.chat.id, "No has elegido ninguna de las dos opciones, voy entonces a suponer que quieres que muestre tu nombre", reply_markup=ReplyKeyboardRemove())
        mostrar_nombre=True
    
    
    msg=bot.send_message(message.chat.id, f"Perfecto! Acontinuación <b>ENVÍAME</b> lo que quieres que se publique :) \n\n<u>Contenido Aceptado por el Bot</u>:\n<b>Imágenes</b>\n<b>Vídeos</b>\n<b>Música</b>\n<b>Documentos</b> (PDF, EPUB, etcétera)\n <b>Encuestas</b> que envíe El Usuario\n-Más allá de esos archivos, no serán aceptado a no ser que a futuro @{bot.get_chat(admin).username} lo decida-\n\nNota Importante:\nEl límite de peso de los documentos es de 50 MB mientras que para los vídeos, fotos y archivos de audio son de 20 MB, no sobrepases el límite con el peso de tus archivos o no se enviará lo que quieres compartir")
    bot.register_next_step_handler(msg, recibir_publicacion, mostrar_nombre, canal_destino)
    
    
def recibir_publicacion(message, mostrar_nombre, canal_destino):
    global diccionario_publicaciones
    if message.content_type=="text":
        bot.send_message(message.chat.id, "No está permitido que sea <b>Solamente texto</b>....\nEnvía una foto, un vídeo o una canción que quieras compartir con los demás :) \n\nEscribe nuevamente /enviar para intentarlo nuevamente")
        return


    diccionario_publicaciones[message.chat.id]=[]
    #El elemento 0 de diccionario_publicaciones[message.chat.id] será el nombre del archivo y el 1 será el enlace y el 2 será el tipo de archivo
        
    try:
        if message.content_type=="photo":   
            diccionario_publicaciones[message.chat.id].append(f"{randint(1,100)}_{os.path.basename(bot.get_file(message.photo[-1].file_id).file_path)}")
            diccionario_publicaciones[message.chat.id].append(bot.get_file(message.photo[-1].file_id).file_path)
            diccionario_publicaciones[message.chat.id].append("photo")
        
        elif message.content_type=="audio":
            try:
                extension=os.path.basename(bot.get_file(message.audio.file_id).file_path).split(".")[-1]
                diccionario_publicaciones[message.chat.id].append(f"{message.audio.performer} - {message.audio.title}.{extension}")
            except:
                contador=0
                for i in message.audio.file_name:
                    if not i.isdigit():
                        break
                    else:
                        contador+=1
                    
                diccionario_publicaciones[message.chat.id].append(f"{message.audio.file_name[contador:]}")
                
            diccionario_publicaciones[message.chat.id].append(bot.get_file(message.audio.file_id).file_path)
            diccionario_publicaciones[message.chat.id].append("audio")
        
        elif message.content_type=="video":
            diccionario_publicaciones[message.chat.id].append(f"{randint(1,100)}_{os.path.basename(bot.get_file(message.video.file_id).file_path)}")
            diccionario_publicaciones[message.chat.id].append(bot.get_file(message.video.file_id).file_path)
            diccionario_publicaciones[message.chat.id].append("video")
        
        
        elif message.content_type=="document":
            diccionario_publicaciones[message.chat.id].append(f"{randint(1,100)}_{os.path.basename(bot.get_file(message.document.file_id).file_path)}")
            diccionario_publicaciones[message.chat.id].append(bot.get_file(message.document.file_id).file_path)
            diccionario_publicaciones[message.chat.id].append("document")
            
        elif message.content_type=="poll":
            bot.forward_message(canal, message.chat.id , message.message_id)
            bot.send_message(message.chat.id, "Encuesta enviada exitosamente :) revisa el canal para que veas la publicación\n\n¡Gracias por tu #aporte! :D")
            return
        
        else:
            bot.send_message(message.chat.id, "Al parecer, el contenido que planeas enviar no está entre los que acepto, por favor, consulta nuevamente la ayuda ingresando /help para más información :)")
            return
        
    except Exception as e:
        bot.send_message(message.chat.id, f"<b>Ha ocurrido un error🙈</b>\nMUY posiblemente ese error haya sido debido a que el archivo que has enviado sea muy grande\n\nEl límite de peso de los documentos es de 50 MB mientras que para los vídeos, fotos y archivos de audio son de 20 MB, no sobrepases el límite con el peso de tus archivos\n\n<u>Descripción del error</u>:\n{e}\n\nElige otro archivo más pequeño y escríbeme /enviar nuevamente :(")
        return



    # nombre = diccionario_publicaciones[message.chat.id][0]
    # enlace= tipo_archivo=diccionario_publicaciones[message.chat.id][2]
    # tipo_archivo = diccionario_publicaciones[message.chat.id][2]
    
    with open(diccionario_publicaciones[message.chat.id][0], "wb") as archive:
        archive.write(bot.download_file(diccionario_publicaciones[message.chat.id][1]))
        
    with open(diccionario_publicaciones[message.chat.id][0], "rb") as archive:
        if message.caption:
            if diccionario_publicaciones[message.chat.id][2]=="photo":
                if mostrar_nombre==False:
                    bot.send_photo(canal_destino, photo=archive , caption=f"{message.caption}\n\n#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_photo(canal_destino, photo=archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            elif diccionario_publicaciones[message.chat.id][2]=="video":
                if mostrar_nombre==False:
                    bot.send_video(canal_destino, archive , caption=f"{message.caption}\n\n#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_video(canal_destino, archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            elif diccionario_publicaciones[message.chat.id][2]=="audio":
                if mostrar_nombre==False:
                    bot.send_audio(canal_destino, archive , caption=f"{message.caption}\n\n#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_audio(canal_destino, archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            else:
                if mostrar_nombre==False:
                    bot.send_document(canal_destino, archive , caption=f"{message.caption}\n\n#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_document(canal_destino, archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
            
        else: #Si no tiene texto, adjunto, lo mismo pero sin el texto
            
            if diccionario_publicaciones[message.chat.id][2]=="photo":
                if mostrar_nombre==False:
                    bot.send_photo(canal_destino, photo=archive , caption=f"#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_photo(canal_destino, photo=archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            
            elif diccionario_publicaciones[message.chat.id][2]=="video":
                if mostrar_nombre==False:
                    bot.send_video(canal_destino, archive , caption=f"#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_video(canal_destino, archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            elif diccionario_publicaciones[message.chat.id][2]=="audio":
                if mostrar_nombre==False:
                    bot.send_audio(canal_destino, archive , caption=f"#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_audio(canal_destino, archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            else:
                if mostrar_nombre==False:
                    bot.send_document(canal_destino, archive , caption=f"#aporte (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                else:                        
                    bot.send_photo(canal_destino, archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
        


            
        
        #Luego de cerrado el archivo, borraré el documento
    os.remove(diccionario_publicaciones[message.chat.id][0])  
    del diccionario_publicaciones[message.chat.id]               
    bot.send_message(message.chat.id, f"Mensaje enviado exitosamente :) Revisa el canal @{bot.get_chat(canal).username} para que veas la publicación\n\n¡Gracias por tu #aporte! :D")
    return



            

@bot.channel_post_handler(func=lambda message: int(message.chat.id) == bot.get_chat(canal).id and publicaciones_canal==True or message.chat.id == -1001795230328, content_types=["photo", "video", "document", "audio"])
#-1001795230328 > @LastHentai
def cmd_recibir_mensajes_canal(message):
    if not (message.content_type=="video" or message.content_type=="photo" or message.content_type=="audio" or message.content_type=="document"):
        return
    try:
        if message.caption:
            message.caption = message.caption.split("http")[0]
            bot.edit_message_caption(f"{message.caption}\n\n@{bot.get_chat(message.chat.id).username}\n\nPara realizar aportes al canal escriba al bot <a href='https://t.me/{bot.user.username}?enviar={message.chat.id}'>@{bot.user.username}</a>", message.chat.id , message.message_id)
        else:
            bot.edit_message_caption(f"@{bot.get_chat(message.chat.id).username}\n\nPara realizar aportes al canal escriba al bot <a href='https://t.me/{bot.user.username}?enviar={message.chat.id}'>@{bot.user.username}</a>", message.chat.id , message.message_id)
    except:
        pass
    
    return


@bot.message_handler(commands=["host"])
def cmd_host(message):
    
    bot.send_message(message.chat.id, "Hora del host: " + str(time.localtime()))
    
    try:
        bot.send_message(message.chat.id, request.host_url)
    except:
        bot.send_message(message.chat.id, "No pude hayar la URL :(")
        
        
    


@bot.message_handler(content_types="new_chat_members", func=lambda message: message.chat.id==grupo_vinculado_canal)
def cmd_control_group(message):
    print("Entró por el caption de los nuevos miembros del grupo")
    for member in message.new_chat_members:
        if not bot.get_chat_member(canal , member.id).status in ("member, administrator, creator"):
            if bot.get_chat(canal).username:
                enlace=f"https://t.me/{bot.get_chat(canal).username}"
            else:
                enlace=bot.get_chat(canal).invite_link
                
            if member.language_code=="es":
                markup=InlineKeyboardMarkup(row_width=1)
                markup.add(InlineKeyboardButton(text="Únete al canal aquí 🎯", url=enlace))
                markup.add(InlineKeyboardButton(text="Comprobar ✨", callback_data="Comprobar"))
                
                if member.username:
                    bot.send_message(message.chat.id, f"Lo siento @{member.username} al parecer no eres miembro del canal @{bot.get_chat(canal).username}.\n\nÚnete al canal y vuelve a intentar unirte aquí presionando en '<b>Comprobar ✨</b>' :)", reply_markup=markup)
                    bot.restrict_chat_member(message.chat.id, member.id, can_send_messages=False)
                
                else:
                    bot.send_message(message.chat.id, f"Lo siento @{member.first_name} al parecer no eres miembro del canal @{bot.get_chat(canal).username}.\n\nÚnete al canal y vuelve a intentar unirte aquí presionando en '<b>Comprobar ✨</b>' :)", reply_markup=markup)
                    bot.restrict_chat_member(message.chat.id, member.id, can_send_messages=False)
            
            else:
                markup=InlineKeyboardMarkup(row_width=1)
                markup.add(InlineKeyboardButton(text="Join to channel here 🎯", url=enlace))
                markup.add(InlineKeyboardButton(text="Check ✨", callback_data="Comprobar"))
                
                if member.username:
                    bot.send_message(message.chat.id, f"Sorry @{member.username} looks like you are not member of <a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>.\n\nJoin yourself here and come back again to join to this group pressing '<b>Check ✨</b>' :)", reply_markup=markup)
                    bot.restrict_chat_member(message.chat.id, member.id, can_send_messages=False)
                    
                else:
                    bot.send_message(message.chat.id, f"Sorry @{member.first_name} looks like you are not member of <a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>.\n\nJoin yourself here and come back again to join to this group pressing '<b>Check ✨</b>' :)", reply_markup=markup)
                    bot.restrict_chat_member(message.chat.id, member.id, can_send_messages=False)
        
        else:
            if message.from_user.language_code=="es":
                bot.send_message(message.chat.id, f"Bienvenido/a {bot.get_chat(member.id).first_name} que te trae por aquí :)")

            else:
                bot.send_message(message.chat.id, f"Welcome {bot.get_chat(member.id).first_name} tell us something about you :)")
            
    return



@bot.message_handler(func=lambda x: True, )
@bot.message_handler(content_types=['audio','video', 'document'])
def cmd_recibir_cualquier_mensaje(message):
    


    if message.chat.id==grupo_vinculado_canal and message.text in ["https", "http" ,".com", ".net", ".org"]:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.from_user.id, f"<u>ES:</u>\nNo puedes enviar spam a <a href='{bot.get_chat(grupo_vinculado_canal).invite_link}'>{bot.get_chat(grupo_vinculado_canal).title}</a>!\n\n<u>EN:</u>\nYou can't send spam to <a href='{bot.get_chat(grupo_vinculado_canal).invite_link}'>{bot.get_chat(grupo_vinculado_canal).title}</a>!")
            
        except:
            return
    
    elif not message.chat.type == "private":
        return
    
    
    
    if str(message.chat.id) == str(admin) and not message.content_type == "text":
        
    
        
        match message.content_type:
            case "video":
                nombre = "video_{}.{}".format(message.from_user.id, message.video.mime_type.split("/")[-1])
                tipo=message.video
                
            case "document":
                nombre = "document_{}.{}".format(message.from_user.id, message.document.mime_type.split("/")[-1])
                tipo = message.document
                
            case "audio":
                nombre = "audio_{}.{}".format(message.from_user.id, message.audio.mime_type.split("/")[-1])
                tipo = message.audio

        
        with open(nombre, "wb") as archivo:
            try:
                archivo.write(bot.download_file(bot.get_file(tipo.file_id).file_path))
                
            except Exception as e:
                
                bot.send_message(message.chat.id, f"Ha ocurrido un error\n\nDescripcion:\n{e}")
                
                return
                # file_path = bot.get_file(tipo.file_id).file_path
                # download_url = "https://api.telegram.org/file/bot{}/{}".format(os.environ["token"], file_path)


                # # Descarga por streaming
                # response = requests.get(download_url, stream=True)
                # response.raise_for_status() # Lanza una excepción para errores HTTP

                # # Ruta donde guardar el archivo


                # for chunk in response.iter_content(chunk_size=8192): # Tamaño del chunk
                #     archivo.write(chunk)
                    
        
            
            def comprimir_y_dividir_imagen(ruta_imagen, ruta_destino, tamano):
                
                breakpoint()

                """Comprime una imagen y divide el zip resultante en partes.

                Args:
                    ruta_imagen: Ruta de la imagen a comprimir.
                    ruta_destino: Directorio donde guardar las partes del zip.
                    num_partes: Número de partes en las que dividir el zip.
                """
                


                nombre_zip = os.path.basename(ruta_imagen) + ".zip"
                ruta_zip = os.path.join(ruta_destino, nombre_zip)

                with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(ruta_imagen, os.path.basename(ruta_imagen))

                tamano_zip = os.path.getsize(ruta_zip)
                tamano_parte = tamano

                
                with open(ruta_zip, "rb") as f:
                    data = f.read()

                for i in range(int(tamano_zip / tamano_parte) + 1):
                    inicio = i * tamano_parte
                    fin = min((i + 1) * tamano_parte, tamano_zip)
                    with open(f"{ruta_zip}.part.{i+1:03d}", "wb") as outfile:
                        outfile.write(data[inicio:fin])
                    

                    with open(f"{ruta_zip}.part.{i+1:03d}", "rb") as outfile:
                        bot.send_document(message.chat.id, telebot.types.InputFile(outfile.name))
                        nombre_Del=outfile.name
                        
                        
                    os.remove(nombre_Del)
                    os.remove(ruta_zip)

                





            # Ejemplo de uso
            try:
                comprimir_y_dividir_imagen(os.path.abspath(archivo.name), ".", 1_048_576 * 15)
                
            except Exception as e:
                
                bot.send_message(message.chat.id, f"Ha ocurrido un error\n\nDescripcion:\n{e}")
            
            
        try:
            os.remove(nombre)
            
        except Exception as e:
                
                bot.send_message(message.chat.id, f"Ha ocurrido un error intentando borrar el archivo de compresion\n\nDescripcion:\n{e}")
        return
                        
        
    if message.from_user.language_code == "es" and message.chat:           
        
        bot.send_message(message.chat.id, "Oye Mastodonte, tienes que enviarme algún comando para yo poder hacer algo 🤨\n\nEnvíame /help para empezar :)")
    else:
        bot.send_message(message.chat.id, "Hey Bulldog, you must send me some command for do something 🤨\n\nSend to me /help to start :)")

    return




try:
    print(f"La dirección del servidor es:{request.host_url}")
except:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Hello World"

    def flask():
        app.run(host="0.0.0.0", port=5000)

    
    @app.route("/webhook", methods=["GET", "POST"])
    def webhook():
        if request.method.lower() == "post":
            try:
                bot.send_message(admin, "¡¡Un mensaje entrante de la web!!\n\n<u>Contenido del mensaje</u>:\n" + str(json.loads(request.data)))
                
                return "¡Mensaje enviado!"
            
            except:
                pass
            
                return "¡Error Enviando el Mensaje!"
            
        else:
            
            return "<h2>Este no es lugar para un forastero...</h2>"
            
            
            



try:
    print(f"La dirección del servidor es:{request.host_url}")
except:
    hilo_flask=threading.Thread(name="hilo_flask", target=flask)
    hilo_flask.start()


    
try:
    bot.remove_webhook()
except:
    pass

sleep(2)

bot.infinity_polling()
