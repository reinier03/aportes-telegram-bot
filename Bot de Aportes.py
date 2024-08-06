import telebot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from flask import Flask, request
import os
import threading
from random import randint
from time import sleep
import dill

os.chdir(os.path.dirname(os.path.abspath(__file__)))


canal=os.environ["canal"]
try:
    admin=os.environ["admin"]
except:
    admin=1413725506
lista_usuarios_baneados=[]
publicaciones_canal=True
publicaciones_usuarios=True
bot=telebot.TeleBot(os.environ["token"], parse_mode="html", disable_web_page_preview=True)
grupo_vinculado_canal=""

if os.path.isfile("variables.dill"):
    with open("variables.dill", "rb") as archive:
        lista=dill.load(archive)
        for key, value in lista.items():
            globals()[key]=value

if publicaciones_usuarios==False:
    bot.send_message(admin, "<u><b>ADVERTENCIA</b></u>:\nLos aportes al canal por parte de los usuarios están desabilitados")

def guardar_variables():
    with open("variables.dill", "wb") as archive:
        lista={
            "lista_usuarios_baneados": lista_usuarios_baneados,
            "grupo_vinculado_canal" : grupo_vinculado_canal,
            "publicaciones_canal" : publicaciones_canal,
            "publicaciones_usuarios" : publicaciones_usuarios
        }
        dill.dump(lista, archive)
    return




bot.send_message(admin, "Estoy online bitch :)")

bot.set_my_commands([
    telebot.types.BotCommand("/help", "Ofrece ayuda sobre el funcionamiento de este bot"),
    telebot.types.BotCommand("/enviar", "Para enviar una publicación al canal"),
    telebot.types.BotCommand("/panel", "Sólo disponible para mi creador :)")
])


@bot.message_handler(commands=["panel"])
def cmd_panel(message):
    if not message.chat.type == "private":
        return
    if not int(message.chat.id)==int(bot.get_chat(admin).id):
        bot.send_message(message.chat.id, f"Lo siento pero no eres mi creador @{bot.get_chat(admin).username}:)\nNo puedes acceder a esta sección")
        return
    
    panel_administrador=InlineKeyboardMarkup(row_width=1)
    panel_administrador.add(InlineKeyboardButton("Dejar de/Volver a Recibir mensajes del Canal", callback_data="Parar canal"))
    panel_administrador.add(InlineKeyboardButton("Dejar de/Volver a Recibir mensajes de Usuarios", callback_data="Parar Usuarios"))
    panel_administrador.add(InlineKeyboardButton("Banear a un usuario", callback_data="Banear Usuario"))
    panel_administrador.add(InlineKeyboardButton("Desbanear a un usuario", callback_data="Desbanear Usuario"))
    panel_administrador.add(InlineKeyboardButton("Definir Grupo Adjunto", callback_data="Grupo Adjunto"))
    panel_administrador.add(InlineKeyboardButton("Ver lista de usuarios baneados", callback_data="Ver Lista"))
    bot.send_message(admin, "Qué pretendes hacer?", reply_markup=panel_administrador)




@bot.callback_query_handler(func=lambda x: True)
def cmd_callbacks(call):
    global publicaciones_canal
    global publicaciones_usuarios
        
    if call.data == "Parar canal":
        if publicaciones_canal==False:
            publicaciones_canal=True
            bot.send_message(call.from_user.id, "He vuelto a Monitoriar las publicaciones del canal :D \n\nCuando quieras nuevamente que deje de administrarlas vuelve a presionar el mismo botón que presionaste para desactivarlas")
            
        elif publicaciones_canal==True:
            publicaciones_canal=False
            bot.send_message(call.from_user.id, "He dejado de Monitoriar las publicaciones del canal :( \n\nCuando quieras nuevamente que las administre vuelve a presionar el mismo botón que presionaste para desactivarlas")
            
        guardar_variables()
        return
    
    
    
    
    
    
    if call.data == "Parar Usuarios":
        if publicaciones_usuarios==False:
            publicaciones_usuarios=True
            bot.send_message(call.from_user.id, "He vuelto a empezar a recibir los aportes de los usuarios :D \n\nCuando quieras nuevamente que los deje de recibir vuelve a presionar el mismo botón que presionaste para activarlos")
        elif publicaciones_usuarios==True:
            publicaciones_usuarios=False
            bot.send_message(call.from_user.id, "He dejado de recibir los aportes de los usuarios :( \n\nCuando quieras nuevamente que los reciba vuelve a presionar el mismo botón que presionaste para desactivarlos")
        
        guardar_variables()
        return





    if call.data == "Banear Usuario":
        msg=bot.send_message(call.from_user.id, "Con este panel podrás banear a un usuario para que no pueda hacer más aportes al canal\nA Continuación introduce el EL ID de dicho usuario a continuación")
        
        def banear(message):
            
            try:
                bot.get_chat(int(message.text)).id
            except:
                bot.send_message(message.chat.id, "El usuario que has ingresado no existe, te devuelvo atrás")
                return
                
            lista_usuarios_baneados.append(bot.get_chat(message.text).id)
            guardar_variables()
            bot.send_message(message.chat.id, "Usuario baneado exitosamente")
            return
            
            
        bot.register_next_step_handler(msg, banear)
        
        
        
        
        
        
    if call.data=="Desbanear Usuario":
        msg=bot.send_message(call.from_user.id, "Con este panel podrás desbanear a un usuario que hayas puesto ya en la lista negra para que no pudiera aportar\nA Continuación introduce el @username de dicho usuario a continuación")
        
        def banear(message):
            if message.text.startswith("@"):
                message.text.replace("@", "")
                
            try:
                bot.get_chat(message.text)
            except:
                bot.send_message(message.chat.id, "El usuario que has ingresado no existe, te devuelvo atrás")
                return
            
            for i in lista_usuarios_baneados:
                if i==message.text:
                    lista_usuarios_baneados.remove(i)
            guardar_variables()
            return
        
        
        
        
        
        
    if call.data=="Grupo Adjunto":
        if  not grupo_vinculado_canal == "":
            bot.send_message(call.from_user.id, f"Actualmente el grupo vinculado es @{bot.get_chat(grupo_vinculado).username}")
            
        msg=bot.send_message(call.from_user.id, "Define a continuación el @username del grupo vinculado al canal \n\nNota:\nEsto les da la condición a los usuarios de unirse a un grupo para poder aportar al canal principal. Si no quieres establecer esta condición para aportar, escribe un @username incorrecto a propósito\n\n")
        
        def grupo_vinculado(message):
            global grupo_vinculado_canal

            if not message.text.startswith("@"):
                message.text="@" + message.text
            try:
                grupo_vinculado_canal=bot.get_chat(message.text).username
                
            except:
                bot.send_message(message.chat.id, "Al parecer, te has confundido de dirección, ese grupo no existe\n\n<b>Eliminaré la condición de unirse a un grupo para publicar</b>")
                grupo_vinculado_canal=""
                guardar_variables()
                return
            
            guardar_variables()
            bot.send_message(message.chat.id, "Grupo definido exitosamente ;)")
            return
        
        bot.register_next_step_handler(msg, grupo_vinculado)
        
        
        
        
        
        
    elif call.data=="Ver Lista":
        texto=""
        if len(lista_usuarios_baneados)==0:
            bot.send_message(call.from_user.id, "La lista está vacía tigre")
            return
        
        for i in lista_usuarios_baneados:
            try:
                texto+=f"Usuario: @{bot.get_chat(i).username},  ID del Usuario: <code>{bot.get_chat(i).id}</code>\n"
            except:
                texto+=f"ESTE USUARIO ME BLOQUEÓ! > {i}\n"
            
        bot.send_message(call.from_user.id , texto)
        return


@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    if not message.chat.type == "private":
        return
    bot.send_message(message.chat.id, f"<b>Bienvenido al Bot de Aportes de @{bot.get_chat(canal).username}</b> 😁\n\nLa idea con este bot es que los usuarios TAMBIÉN aporten contenido al canal además de los propios admins\n\n<u>Contenido Aceptado por el Bot</u>:\n<b>Imágenes</b>\n<b>Vídeos</b>\n<b>Música</b>\n<b>Documentos</b> (PDF, EPUB, etcétera)\n <b>Encuestas</b> que envíe El Usuario\n-Más allá de esos archivos, no serán aceptado a no ser que a futuro @{bot.get_chat(admin).username} lo decida-\n\nNota Importante:\nEl límite de peso de los documentos es de 50 MB mientras que para los vídeos, fotos y archivos de audio son de 20 MB, no sobrepases el límite con el peso de tus archivos o no se enviará lo que quieres compartir\n\n¿Qué esperas? Empieza llevando tu contenido a nuestro canal escribiendo /enviar :)")
    return
    
    
    
@bot.message_handler(commands=["enviar"])
def cmd_ingresar(message):
    if not message.chat.type == "private":
        return
        
    if publicaciones_usuarios==False:
        bot.send_message(message.chat.id, f"Lo siento :( Mi creador @{bot.get_chat(admin).username} me quitó el acceso a los mensajes TEMPORALMENTE, por alguna razón (sabrá Dios cual)\n\n<b>Vuelve más tarde</b> para comprobar si estoy autorizado a empezar a recibir aportes nuevamente (o pregúntale)")
        return
    if not grupo_vinculado_canal == "" and (bot.get_chat_member(chat_id=bot.get_chat(f"@{grupo_vinculado_canal}").id, user_id=message.from_user.id).status == "left" or bot.get_chat_member(chat_id=bot.get_chat(f"@{grupo_vinculado_canal}").id, user_id=message.from_user.id).status == "kicked"):
        bot.send_message(message.chat.id, "Para poder enviar aportes debes de estar en el grupo vinculado al canal, por favor, únete a el y luego regresa aquí nuevamente :)", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Únete aquí :)", url=f"https://t.me/{bot.get_chat(f'@{grupo_vinculado_canal}').username}")))
        return
        
    for i in lista_usuarios_baneados:
        if i == bot.get_chat(message.from_user.id).id:
            bot.send_message(message.chat.id, f"Al parecer mi administrador @{bot.get_chat(admin).username} te baneó por alguna razón y ya no puedes hacer aportes al canal @{bot.get_chat(canal).username}\nTe habrás portado mal seguramente, ni idea, soy solamente un bot 😐\n\nVe a hablar con él y pídele explicación👇👇", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("El Administrador", url=f"https://t.me/{bot.get_chat(admin).username}")))
            return
            
    msg=bot.send_message(message.chat.id, "Muy bien, a continuación envíame lo que quieres que se publique :)")
    bot.register_next_step_handler(msg, recibir_publicacion)
    
    
def recibir_publicacion(message):
    if message.content_type=="text":
        bot.send_message(message.chat.id, "No está permitido que sea <b>Solamente texto</b>....\nEnvía una foto, un vídeo o una canción que quieras compartir con los demás :) \n\nEscribe nuevamente /ingresar para intentarlo nuevamente")
        return
    

    if message.content_type=="photo":   
        nombre_archivo=f"{randint(1,100)}_{os.path.basename(bot.get_file(message.photo[-1].file_id).file_path)}"
    
    elif message.content_type=="audio":
        try:
            nombre_archivo=f"{message.audio.performer} - {message.audio.title}"
        except:
            contador=0
            for i in message.audio.file_name:
                if not i.isdigit():
                    break
                else:
                    contador+=1
                
        nombre_archivo=f"{message.audio.file_name[contador:]}"
    
    elif message.content_type=="video":
        nombre_archivo=f"{randint(1,100)}_{os.path.basename(bot.get_file(message.video.file_id).file_path)}"
    
    
    elif message.content_type=="document":
        nombre_archivo=f"{randint(1,100)}_{os.path.basename(bot.get_file(message.document.file_id).file_path)}"
        
    elif message.content_type=="poll":
        bot.forward_message(canal, message.chat.id , message.message_id)
        bot.send_message(message.chat.id, "Encuesta enviada exitosamente :) revisa el canal para que veas la publicación\n\n¡Gracias por tu #aporte! :D")
        return
    
    else:
        bot.send_message(message.chat.id, "Al parecer, el contenido que planeas enviar no está entre los que acepto, por favor, consulta nuevamente la ayuda ingresando /help para más información :)")
        return
    
    with open(nombre_archivo, "wb") as archive:
        if message.content_type=="photo":   
            archive.write(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
        
        elif message.content_type=="audio":
            archive.write(bot.download_file(bot.get_file(message.audio.file_id).file_path))
        
        elif message.content_type=="video":
            archive.write(bot.download_file(bot.get_file(message.video.file_id).file_path))
        
        elif message.content_type=="document":
            archive.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
        

        
        
    with open(nombre_archivo, "rb") as archive:
        if message.caption: #Si tiene texto adjunto:
            if message.content_type=="photo":
                #Si es una foto:
                bot.send_photo(canal, photo=archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            
            elif message.content_type=="video":
                bot.send_video(canal, video=archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)", timeout=80)
                
            elif message.content_type=="audio":
                bot.send_audio(canal, audio=archive , caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            else:
                bot.send_document(canal , archive, caption=f"{message.caption}\n\n#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
            
        else: #Si no tiene texto, adjunto, lo mismo pero sin el texto
            
            if message.content_type=="photo":
                #Si es una foto:
                bot.send_photo(canal, photo=archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            
            elif message.content_type=="video":
                bot.send_video(canal, video=archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            elif message.content_type=="audio":
                bot.send_audio(canal, audio=archive , caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
                
            else:
                bot.send_document(canal , archive, caption=f"#aporte de @{bot.get_chat(message.from_user.id).username} (<code>{bot.get_chat(message.from_user.id).id}</code>)\nPara hacer tu aporte escríbeme a @{bot.user.username} ;)")
    
    #Luego de cerrado el archivo, borraré el documento
    os.remove(nombre_archivo)
    bot.send_message(message.chat.id, f"Mensaje enviad exitosamente :) Revisa el canal @{bot.get_chat(canal).username} para que veas la publicación\n\n¡Gracias por tu #aporte! :D")
    return



            

@bot.channel_post_handler(func=lambda message: int(message.chat.id) == bot.get_chat(canal).id and publicaciones_canal==True, content_types=["photo", "video", "document", "audio"])
def cmd_recibir_mensajes_canal(message):
    if not (message.content_type=="video" or message.content_type=="photo" or message.content_type=="audio" or message.content_type=="document"):
        return
    try:
        if message.caption:
            bot.edit_message_caption(f"{message.caption}\n\n@{bot.get_chat(canal).username}\n\nPara realizar aportes al canal escriba al bot @{bot.user.username}", canal , message.message_id)
        else:
            bot.edit_message_caption(f"@{bot.get_chat(canal).username}\n\nPara realizar aportes al canal escriba al bot @{bot.user.username}", canal , message.message_id)
    except:
        pass
    
    return


@bot.message_handler(func=lambda x: True)
def cmd_recibir_cualquier_mensaje(message):
    if not message.chat.type == "private":
        return
    bot.send_message(message.chat.id, "Oye Mastodonte, tienes que enviarme algún comando para yo poder hacer algo 🤨\n\nEnvíame /help para empezar :)")




if __name__== "__main__":

    app=Flask(__file__)

    @app.route("/")
    def index():
        if request.headers.get("content-type") == "application/json":
            update=telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
            bot.process_new_updates([update])
            return "OK", 200
        return "Hello World"

    def run():
        app.run("0.0.0.0", port=5000)
        
    try:
        request.host_url()
    except:
        threading.Thread(name="hilo_flask", target=run).run()
        
        

    bot.remove_webhook()
    sleep(2)
    bot.set_webhook(f"{os.environ['nombre_link']}")
