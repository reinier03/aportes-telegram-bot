import os
import dill
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import threading as t
from aportes_usefull_functions import enviar_mensajes
import aportes_usefull_functions


    
def cargar_variables():
    with open("variables.dill", "rb") as archive:
        lista=dill.load(archive)
        for key, value in lista.items():
            globals()[key]=value

    return


def guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto):
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



        
        



def recibir_querys(bot, call, lista_usuarios_baneados, publicaciones_usuarios, publicaciones_canal, canal, grupo_vinculado_canal, publicaciones_auto):
    
    
    if call.data == "admin_msg":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
                InlineKeyboardButton("Dejar de/Volver a Recibir mensajes del Canal", callback_data="Parar canal"),
                InlineKeyboardButton("Dejar de/Volver a Recibir mensajes de Usuarios", callback_data="Parar Usuarios"),
                row_width=1
        )
        bot.send_message(call.from_user.id, "¿Que pretendes hacer con los mensajes que se administran?" ,reply_markup = markup)
    

    elif call.data == "Parar canal":

        if publicaciones_canal==False:
            publicaciones_canal=True
            bot.send_message(call.from_user.id, f"He vuelto a Monitoriar las publicaciones del canal/grupo <a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a> :D \n\nCuando quieras nuevamente que deje de administrarlas vuelve a presionar el mismo botón que presionaste para desactivarlas")
            
        elif publicaciones_canal==True:
            publicaciones_canal=False
            bot.send_message(call.from_user.id, "He dejado de Monitoriar las publicaciones del canal/grupo <a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a> :( \n\nCuando quieras nuevamente que las administre vuelve a presionar el mismo botón que presionaste para desactivarlas")
            
        guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
        return






    elif call.data == "Parar Usuarios":
        if publicaciones_usuarios==False:
            publicaciones_usuarios=True
            bot.send_message(call.from_user.id, "He vuelto a empezar a recibir los aportes de los usuarios :D \n\nCuando quieras nuevamente que los deje de recibir vuelve a presionar el mismo botón que presionaste para activarlos")
        elif publicaciones_usuarios==True:
            publicaciones_usuarios=False
            bot.send_message(call.from_user.id, "He dejado de recibir los aportes de los usuarios :( \n\nCuando quieras nuevamente que los reciba vuelve a presionar el mismo botón que presionaste para desactivarlos")
        
        guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
        return



    elif call.data == "Admin Usuarios":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("Banear a un usuario 🙍‍♂️❌", callback_data="Banear Usuario"),
            InlineKeyboardButton("Desbanear a un usuario 🙍‍♂️➕", callback_data="Desbanear Usuario"),
            InlineKeyboardButton("Ver lista de usuarios baneados 👀📋", callback_data="Ver Lista"),
            InlineKeyboardButton("Ver username de usuario por ID 👀", callback_data="ver usuario"), row_width=1
        )
        
        bot.send_message(call.from_user.id, "¿Que deseas hacer con los usuarios?", reply_markup=markup)
    

    elif call.data == "Banear Usuario":
        msg=bot.send_message(call.from_user.id, "Con este panel podrás banear a un usuario para que no pueda hacer más aportes al canal\nA Continuación introduce el EL ID de dicho usuario a continuación")
        
        def banear(message):
            if not  message.text.isdigit():
                bot.send_message(message.chat.id, "Debías de enviar un ID numérico!\n\nTe devuelvo atrás")
                return
            
            # try:
            #     bot.get_chat(int(message.text)).id
            # except:
            #     bot.send_message(message.chat.id, "El usuario que has ingresado no existe, te devuelvo atrás")
            #     return
                
            lista_usuarios_baneados.append(int(message.text))
            guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
            bot.send_message(message.chat.id, "Usuario baneado exitosamente")
            return
            
            
        bot.register_next_step_handler(msg, banear)
        
        
        
        
        
        
    elif call.data=="Desbanear Usuario":
        msg=bot.send_message(call.from_user.id, "Con este panel podrás desbanear a un usuario que hayas puesto ya en la lista negra para que no pudiera aportar\nA Continuación introduce el @username o el ID de dicho usuario a continuación")
        
        def desbanear(message):
            contador=0
            if message.text.isdigit():
                message.text=int(message.text)
                for i in lista_usuarios_baneados:
                    if int(i)==message.text:
                        lista_usuarios_baneados.remove(i)
                        contador+=1
                if contador==0:
                    bot.send_message(message.chat.id, "Al parecer, no había ningún usuario con ese ID")
                
                else:
                    bot.send_message(message.chat.id, "Usuario desbaneado correctamente")
            else:
                if message.text.startswith("@"):
                    message.text=message.text.replace("@", "")
                
                for i in lista_usuarios_baneados:
                    try:
                        if bot.get_chat(i).username==message.text:
                            lista_usuarios_baneados.remove(i)
                            contador+=1
                    except:
                        bot.send_message(message.chat.id, "Al parecer hay un usuario que me bloqueó, lo eliminaré")
                        lista_usuarios_baneados.remove(i)
                        continue
                        
                if contador==0:
                    bot.send_message(message.chat.id, "Al parecer, no había ningún usuario con ese @username")
                
                else:
                    bot.send_message(message.chat.id, "Usuario baneado correctamente")
            
            guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
            return
        
        
        bot.register_next_step_handler(msg, desbanear)
        
        
        
        
    elif call.data=="Comprobar":
        if bot.get_chat_member(bot.get_chat(grupo_vinculado_canal).id, call.from_user.id).status in ("member, administrator, creator") or bot.get_chat_member(bot.get_chat(grupo_vinculado_canal).id, call.from_user.id).can_send_messages:
            if call.from_user.language_code=="es":
                bot.answer_callback_query(call.id, "¡Ya tú estabas en este lugar! ¡Ignora este mensaje que no es para ti!", True)
            else:
                bot.answer_callback_query(call.id, "You were already in this place!  Ignore this message, it is not for you!", True)
        
        elif bot.get_chat_member(bot.get_chat(canal).id, call.from_user.id).status in ("member, administrator, creator") and  bot.get_chat_member(bot.get_chat(grupo_vinculado_canal).id, call.from_user.id).status=="restricted":
            

            bot.restrict_chat_member(call.message.chat.id, call.from_user.id, None, True, True , True, True , True, False , True , False)
            if call.from_user.language_code=="es":
                if bot.get_chat(call.from_user.id).username:
                    bot.send_message(bot.get_chat(grupo_vinculado_canal).id, f"Bienvenido/a @{bot.get_chat(call.from_user.id).username}, cuéntanos de tí :)")
                    try:
                        bot.delete_message(bot.get_chat(grupo_vinculado_canal).id, call.message.message_id)
                        print("Mensaje eliminado correctamente")
                    except Exception as e:
                        print("Excepción:" + str(e))
                    
                else:
                    bot.send_message(bot.get_chat(grupo_vinculado_canal).id, f"Bienvenido/a {bot.get_chat(call.from_user.id).first_name}, cuéntanos de tí :)")
                    try:
                        bot.delete_message(bot.get_chat(grupo_vinculado_canal).id, call.message.message.id)
                        print("Mensaje eliminado correctamente")
                    except Exception as e:
                        print("Excepción:" + str(e))
            
            else:
                if bot.get_chat(call.from_user.id).username:
                    bot.send_message(bot.get_chat(grupo_vinculado_canal).id, f"Welcome @{bot.get_chat(call.from_user.id).username}, tell us about you :)")
                    try:
                        bot.delete_message(bot.get_chat(grupo_vinculado_canal).id, call.message.message.id)
                    except Exception as e:
                        print("Excepción:" + str(e))
                    
                else:
                    bot.send_message(bot.get_chat(grupo_vinculado_canal).id, f"Welcome {bot.get_chat(call.from_user.id).first_name}, tell us about you :)")
                    try:
                        bot.delete_message(bot.get_chat(grupo_vinculado_canal).id, call.message.message.id)
                    except Exception as e:
                        print("Excepción:" + str(e))
        else:
            if call.from_user.language_code=="es":
                bot.answer_callback_query(call.id, "¡Aún no eres miembro del canal/grupo!", show_alert=True)
                
            else:
                bot.answer_callback_query(call.id, "¡You aren't member of the channel/group yet!", show_alert=True)
        
        bot.answer_callback_query(call.id)
        return
    
    
    
    
        
    elif call.data=="Grupo Adjunto":
        if  not grupo_vinculado_canal == False:
            bot.send_message(call.from_user.id, f"Actualmente el grupo vinculado es <a href='{bot.get_chat(grupo_vinculado_canal).invite_link}'>{bot.get_chat(grupo_vinculado_canal).title}</a>")
            
        msg=bot.send_message(call.from_user.id, "Define a continuación el @username del grupo vinculado al canal o el ID")
        
        def grupo_vinculado(message, grupo_vinculado_canal):

            
            if not message.text.isdigit() and not message.text.startswith("@"):
                message.text="@" + message.text
            
            elif message.text.isdigit() or message.text.startswith("-"):
                message.text=int(message.text)
                
            try:
                grupo_vinculado_canal=bot.get_chat(message.text).id
                bot.send_message(message.chat.id, f"Grupo/canal {bot.get_chat(message.text).title} definido exitosamente ;)")
                
            except Exception as e:
                bot.send_message(message.chat.id, f"Al parecer, te has confundido de dirección, ese grupo no existe\n\n<u>Detalles del error</u>:{e}")
                grupo_vinculado_canal=False

            
            guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
            
            return
        
        bot.register_next_step_handler(msg, grupo_vinculado, grupo_vinculado_canal)
        
        
        
        
        
        
    elif call.data=="Ver Lista":
        texto=""
        if len(lista_usuarios_baneados)==0:
            bot.send_message(call.from_user.id, "La lista está vacía tigre")
            return
        
        for i in lista_usuarios_baneados:
            try:
                texto+=f"Usuario: @{bot.get_chat(i).username},  ID del Usuario: <code>{bot.get_chat(i).id}</code>\n"
            except:
                texto+=f"ESTE USUARIO ME BLOQUEÓ! (o no existe) > {i}\n"
            
        bot.send_message(call.from_user.id , texto)
        return


    elif call.data == "Copia de Seguridad":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
                InlineKeyboardButton("Enviar copia de seguridad 🎁", callback_data="Enviar Archivo"),
                InlineKeyboardButton("Recibir copia de seguridad ✒", callback_data="Recibir Archivo"),
                row_width=1
        )
        
        bot.send_message(call.from_user.id, "¿Qué pretendes hacer con la copia de seguridad?", reply_markup=markup)
        return
    
    elif call.data == "Enviar Archivo":
        if not os.path.isfile("variables.dill"):
            bot.send_message(call.from_user.id, "Aún no se ha hecho el archivo")
            return
        
        with open("variables.dill", "rb") as archivo:
            bot.send_document(call.from_user.id, archivo)
        
        return






    elif call.data == "Recibir Archivo":
        msg=bot.send_message(call.from_user.id, "A continuación, por favor envíeme el archivo")
        
        def recibir_archivo(message):
            if not message.document:
                bot.send_message(message.chat.id, "¡Debes de enviarme el archivo variables.dill!")
                return
            else:
                with open("variables.dill", "wb") as archivo:
                    archivo.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
            try:
                cargar_variables()
            except:
                bot.send_message(message.chat.id, "ALERTA!\nAl parecer la base de datos de usuarios baneados que me envió está corrupta!!\n\nVoy a ELIMINAR la base de datos para evitar cualquier posible error\nPor favor, asegúrese la proxima vez de enviar el archivo correcto: <b>variables.dill</b>")
                os.remove("variables.dill")
                return
            bot.send_message(message.chat.id, "Archivo cargado satisfactoriamente")
            return
        
        
        bot.register_next_step_handler(msg, recibir_archivo)
    
    
    
    
    
    
    #Ver username de usuario por ID👀
    elif call.data=="ver usuario":
        user=call.from_user.id
        msg=bot.send_message(call.from_user.id, "A continuación de este mensaje, ingresa el ID del usuario que quieres ver su <b>@username</b>")
        
        def ver_usuario_username(message):
            if not message.text.isdigit():
                bot.send_message(message.chat.id, "Debes de ingresar el ID del usuario!!\n\nTe devuelvo atrás")
                return

            else:
                try:
                    bot.send_message(message.chat.id, f"El usuario en cuestión es @{bot.get_chat(int(message.text)).username}")
                    
                except Exception as e:
                    bot.send_message(message.chat.id, f"Ha ocurrido la siguiente excepción:\n{e}")

            
        
        bot.register_next_step_handler(msg, ver_usuario_username)
        
    
        
    elif call.data == "admin_auto":
        if not publicaciones_auto.get("otaku"):
            publicaciones_auto["otaku"] = {"url" : "https://pic.re/image", "texto_adjunto" : "#otaku"}
            
        
            
                
        
        markup=InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("otaku", callback_data="p_otaku"),
        )
        
        
    
        bot.send_message(call.from_user.id, "Elige el tipo de publicacion que deseas administrar:", reply_markup=markup)
    
    elif "p_" in call.data:
        
        if "otaku" in call.data:
            
            if "_f" in call.data:
                if not publicaciones_auto["otaku"]["frecuencia"]:
                    msg = enviar_mensajes(bot, call, "A continuación elige la frecuencia con la que se enviarán los mensajes\n\nEjemplo:\n3\n\nExplicación:\nAl definir una frecuencia de n veces, publicaré de forma que se reparta esas veces equitativamente por todo el día, en el caso del ejemplo (3 veces) haré publicaciones cada 8 horas, completando así las 24 horas con 3 publicaciones\n\n\nA continuación de este mensaje escribe la frecuencia NUMÉRICA de veces que quieres que se publique")
                
                else: 
                    msg = enviar_mensajes(bot, call, f"Frecuencia actual de Publicaciones: {publicaciones_auto["otaku"]["frecuencia"]} vez/veces cada 24 horas\n\nA continuación elige la frecuencia con la que se enviarán los mensajes\n\nEjemplo:\n3\n\nExplicación:\nAl definir una frecuencia de n veces, publicaré de forma que se reparta esas veces equitativamente por todo el día, en el caso del ejemplo (3 veces) haré publicaciones cada 8 horas, completando así las 24 horas con 3 publicaciones\n\n\nA continuación de este mensaje escribe la frecuencia NUMÉRICA de veces que quieres que se publique")
                    
                
                def frecuencia_otaku(message):
                    if not message.text.isdigit():
                        bot.send_message(call.from_user.id, "¡La información enviada no era correcta, debes ingresar un NÚMERO para definir la frecuenca!")
                        return
                    
                    else:
                        publicaciones_auto["otaku"]["frecuencia"] = int(message.text)
                        bot.send_message(call.from_user.id, f"¡Muy bien!, Se publicará cada {int(24 / publicaciones_auto["otaku"]["frecuencia"])} hora(s) y {int(24 / publicaciones_auto["otaku"]["frecuencia"]) * 60 %60} minuto(s)\n\nCuando quieres empezar a publicar")
                        
                        
                    publicaciones_auto["otaku"]["activo"] = False
                    publicaciones_auto["otaku"]["proxima_publicacion"] = time.time()
                    
                    return
                        
                        
                    
                    
                
                bot.register_next_step_handler(msg, frecuencia_otaku)
                
                
            elif "_p" in call.data:
                
                if "/s" in call.data:
                    publicaciones_auto["otaku"]["activo"] = False
                    enviar_mensajes(bot, call, "¡Hilo de Publicaciones #otaku detenido!")
                    
                elif "/p" in call.data:
                    publicaciones_auto["otaku"]["activo"] = True
                    
                    contador = False
                    for i in t.enumerate():
                        if i.name=="hilo_auto_publicaciones":
                            contador=True

                    if contador == False:
                        t.Thread(name="hilo_auto_publicaciones", target=aportes_usefull_functions.auto_publicaciones, args=(publicaciones_auto, bot, canal)).start()
                        
                        
                    
                    enviar_mensajes(bot, call, "¡Hilo de Publicaciones #otaku iniciado!")
                    
                    
                
            
            
            
            else:
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("Cambiar la frecuencia", callback_data="p_otaku_f"),
                    
                )
                
                if publicaciones_auto["otaku"]["activo"] == True:
                    markup.add(InlineKeyboardButton("Dejar de Publicar", callback_data="p_otaku_p/s"))
                    
                else:
                    markup.add(InlineKeyboardButton("Empezar a Publicar", "p_otaku_p/p"))
                    
                
                bot.send_message(call.from_user.id, "Qué pretendes hacer con estas publicaciones?", reply_markup = markup)
    
        
    elif call.data=="script":
        if grupo_vinculado_canal:
            bot.send_message(call.from_user.id, f"\n<a href='{bot.get_chat(grupo_vinculado_canal).invite_link}'>Grupo Vinculado</a>: <code>{grupo_vinculado_canal}</code>\n<a href='{bot.get_chat(canal).invite_link}'>Canal</a>: <code>{canal}</code>\nSe monitorea el canal: {publicaciones_canal}\nSe recibe aportes: {publicaciones_usuarios}")
        else:
            bot.send_message(call.from_user.id, f"Grupo Vinculado': <code>{grupo_vinculado_canal}</code>\n<a href='{bot.get_chat(canal).invite_link}'>Canal</a>: <code>{canal}</code>\nSe monitorea el canal: {publicaciones_canal}\nSe recibe aportes: {publicaciones_usuarios}")
        
        
    bot.answer_callback_query(call.id)
    guardar_variables(lista_usuarios_baneados, publicaciones_usuarios , publicaciones_canal, grupo_vinculado_canal, publicaciones_auto)
    return