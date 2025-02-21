import threading as t
import time
import os
import requests
import telebot
import Auto_Publicaciones_Class


admin = os.environ["admin"]



def enviar_mensajes(bot, call, texto, markup=False , msg=False, delete=False):
    """
    msg = objeto Message para editar\n
    delete = Si es True se eliminará el mensaje anterior y se enviará el actual, en lugar de editar el mensaje anterior especificado , es necesario ingresar el msg
    """
    
    

    if "CallbackQuery" in str(type(call)):
        
        try:
            if markup == False:
                
                
                if msg != False or delete == True:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
                    
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, call.message.chat.id, msg.message_id)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                            
                            mensaje = bot.send_message(call.message.chat.id , texto)
                else:
                    
                    try:
                        mensaje = bot.edit_message_text(texto, call.message.chat.id, call.message.message_id)
                    except Exception as e:
                        
                        if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                            
                            return
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
        
        
            
            else:
                
                
                if msg != False:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, call.message.chat.id, msg.message_id , reply_markup=markup)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(call.message.chat.id , texto , reply_markup=markup)
                else:
                
                    try:
                        mensaje = bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup)
                        
                    except Exception as e:
                        
                        if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                            
                            return
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
        except Exception as error:
            mensaje = bot.send_message(call.message.chat.id, f"¡Ha ocurrido un error intentando enviar el mensaje!\n\nDescripción del error:\n{error}")
                    
    else:
        
        try:
            #si no es un callback y por el contrario es un mensaje....
            message = call
            
            #si no hay markup
            if markup == False:
                
                #si hay msg de ID
                if msg != False or delete == True:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, message.chat.id, msg.message_id)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(message.chat.id , texto)
                
                #si NO hay msg de ID
                else:
                    mensaje = bot.send_message(message.chat.id, texto)
            
            #si hay markup
            else:
                
                if msg != False:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, message.chat.id, msg.message_id , reply_markup=markup)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(message.chat.id , texto , reply_markup=markup)
                        
                else:
                    
                    mensaje = bot.send_message(message.chat.id, texto, reply_markup=markup)
                    
        except Exception as error:
            mensaje = bot.send_message(call.message.chat.id, f"¡Ha ocurrido un error intentando enviar el mensaje!\n\nDescripción del error:\n{error}")
           
        
            
    return mensaje




        
    
    
    
    

def auto_publicaciones(publicaciones_auto, bot, canal=os.environ["canal"]):
    while True:
        #-------------comprobación---------------
        contador = []
        for key, item in publicaciones_auto.items():
            if item.activo == True:
                contador.append(item)
                
        if len(contador) == 0:
            break
        
        for key, item in  publicaciones_auto.items():
            if item.activo == True and time.time() >= item.proxima_publicacion:
                
                #otaku-------------------------------------
                if key == "otaku":
                    contenido = item.enviar_info()
                    
                    if not os.path.isfile(contenido):
                        bot.send_message(os.environ["admin"], f"Ha ocurrido un error intentando adquirir el contenido para #otaku\n\nDescripción:\n{str(contenido)}")
                        continue
                    else:
                        
                        contador = 0
                        
                        while True:
                            
                            try:
                                
                            
                                contenido = publicaciones_auto.get("otaku").enviar_info()
                                if not os.path.isfile(contenido):
                                    bot.send_message(os.environ["admin"], f"Ha ocurrido un error intentando adquirir el contenido para #otaku\n\nDescripción:\n{str(contenido)}")
                                    return
                                
                                
                                bot.send_photo(canal , telebot.types.InputFile(contenido) , caption=publicaciones_auto.get("otaku").texto_adjunto)
                                
                                break
                            
                            except Exception as e:
                                if "non-empty" in str(e):
                                    if contador >= 5:
                                        bot.send_message(os.environ["admin"], f"Ha ocurrido un error intentando adquirir el contenido para #otaku\n\nDescripción:\n{str(e)}")
                                        return

                                    contador+=1
                                    continue
                                
                                else:
                                    bot.send_message(os.environ["admin"], f"Ha ocurrido un error intentando adquirir el contenido para #otaku\n\nDescripción:\n{str(e)}")
                                    return
                
                        try:
                            os.remove(contenido)
                        
                        except Exception as e:
                            bot.send_message(os.environ["admin"], f"Ha ocurrido un error intentando eliminar la publicacion #otaku\n\nDescripción:\n{str(e.args)}")
                            
                        item.proxima_publicacion = time.time() + item.tiempo_espera
                        
                #otaku-end-------------------------
                            
        
        time.sleep(30)
        
        
    bot.send_message(admin, "¡Alerta!\n¡El hilo de Publicaciones ha parado!")    
    return