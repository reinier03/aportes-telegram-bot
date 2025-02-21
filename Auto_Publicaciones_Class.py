import time
import requests
import os

class Auto_Publicacion():
    def __init__(self, tipo, texto_adjunto ,activo=False, frecuencia=3, proxima_publicacion=time.time(), tiempo_espera = False):
    
        self.tipo = tipo
        self.activo = activo
        self.frecuencia = frecuencia
        self.texto_adjunto = texto_adjunto
        self.proxima_publicacion = proxima_publicacion
        self.tiempo_espera = int((24 / self.frecuencia) * 60 * 60)
        
        
        
        
        
        
class Otaku(Auto_Publicacion):
    def __init__(self, tipo="otaku", texto_adjunto="#otaku" ,activo=False, frecuencia=3, proxima_publicacion=time.time(), tiempo_espera = False):
        self.tipo = "otaku"
        super().__init__(tipo, texto_adjunto ,activo=False, frecuencia=3, proxima_publicacion=time.time(), tiempo_espera = False)
        self.texto_adjunto = f"#otaku\n\n@LastHopePosting\n\nPara realizar aportes al canal escriba al bot @lastaportes_bot"
        
        
        
        
    def enviar_info(self):
        try:
            res = requests.get("https://pic.re/image")
            with open("otaku.png", "wb") as foto:
                foto.write(res.content)
            
            
            
            
        except Exception as e:
            return e.args
        
        res=os.path.abspath(foto.name)
        time.sleep(1)
        return res
    
    