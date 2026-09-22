import time
import argparse
from playwright.sync_api import sync_playwright, TimeoutError

def join_meet(meet_url, visible=False):
    user_data_dir = "./perfil_meet"
    
    with sync_playwright() as p:
        modo = "visible" if visible else "headless"
        print(f"Iniciando navegador en modo {modo}...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=not visible,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu"
            ]
        )
        
        page = context.new_page()
        
        # (Opcional) Bloquear carga de medios/imágenes innecesarios para ahorrar RAM en el Free Tier
        # page.route("**/*", lambda route: route.continue_() if route.request.resource_type not in ["image", "media", "font"] else route.abort())

        print(f"Navegando a la reunión: {meet_url}")
        page.goto(meet_url)
        
        # Esperamos a que la página cargue los elementos principales
        page.wait_for_load_state("networkidle")
        time.sleep(5)  # Pausa adicional para dar tiempo a que el DOM de Meet se estabilice
        
        # 1. Apagar Micrófono y Cámara
        print("Apagando micrófono y cámara usando atajos de teclado...")
        # En Google Meet, los atajos Ctrl+D (Mic) y Ctrl+E (Cam) son muy estables.
        page.keyboard.press("Control+d") 
        time.sleep(1)
        page.keyboard.press("Control+e")
        time.sleep(2)
            
        print("Intentando unirse a la reunión...")
        
        # 2. Encontrar el botón de unirse
        join_texts = ["Unirse ahora", "Solicitar unirse", "Join now", "Ask to join"]
        joined = False
        
        for text in join_texts:
            try:
                # Buscamos botones cuyo texto coincida
                button = page.locator(f'button:has-text("{text}")').first
                button.wait_for(state="visible", timeout=3000)
                button.click()
                print(f"¡Clic exitoso en el botón: '{text}'!")
                joined = True
                break
            except TimeoutError:
                continue
            except Exception as e:
                print(f"Error al intentar hacer clic en '{text}': {e}")
                
        if not joined:
            print("ADVERTENCIA: No se encontró el botón para unirse. Podría ser necesario actualizar los selectores o ya estás dentro.")
        else:
            print("✅ Solicitud enviada o unido a la reunión con éxito.")

        # 3. Mantener el proceso activo
        print("Bot activo. Manteniendo la conexión abierta...")
        print("El script terminará automáticamente si haces 'Switch' desde otro dispositivo, o por el límite del cron.")
        try:
            while True:
                time.sleep(20) # Revisar cada 20 segundos
                
                # Textos que indican que la llamada terminó o el bot fue reemplazado por otro dispositivo
                disconnect_indicators = [
                    "Volver a la pantalla de inicio", 
                    "Return to home screen", 
                    "Abandonaste la reunión", 
                    "You left the meeting",
                    "Te has unido desde otro dispositivo",
                    "You joined from another device"
                ]
                
                bot_kicked = False
                for text in disconnect_indicators:
                    try:
                        # Buscamos si aparece alguno de estos mensajes en la pantalla
                        if page.locator(f'text="{text}"').first.is_visible():
                            bot_kicked = True
                            break
                    except Exception:
                        pass
                
                if bot_kicked:
                    print("\n[!] Detectado: El bot fue desconectado (entraste desde tu PC/Celular o la llamada finalizó). Apagando proceso...")
                    break
                    
        except KeyboardInterrupt:
            print("\nSaliendo de la reunión manualmente...")
        finally:
            try:
                context.close()
            except Exception:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot de Auto-Asistencia para Google Meet")
    parser.add_argument("url", help="URL de la reunión de Google Meet")
    parser.add_argument("--visible", action="store_true", help="Muestra el navegador (ideal para pruebas locales)")
    args = parser.parse_args()
    
    join_meet(args.url, visible=args.visible)
