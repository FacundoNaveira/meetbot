from playwright.sync_api import sync_playwright

def setup_account():
    with sync_playwright() as p:
        user_data_dir = "./perfil_meet"
        print(f"Abriendo navegador. Se guardará la sesión en: {user_data_dir}")
        
        # Lanzar contexto persistente
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # Necesitamos ver la ventana para loguearnos
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.new_page()
        page.goto("https://accounts.google.com/")
        
        print("\n" + "="*60)
        print(" ACCIÓN REQUERIDA ".center(60, "="))
        print("1. En el navegador que se abrió, inicia sesión en tu cuenta de Google.")
        print("2. Resuelve cualquier verificación en dos pasos (2FA).")
        print("3. Cuando veas la página de bienvenida de tu cuenta, vuelve aquí.")
        print("="*60 + "\n")
        
        input("Presiona ENTER aquí en la consola SOLO CUANDO hayas terminado el login...")
        
        try:
            context.close()
        except Exception:
            pass # Ignoramos el error si cerraste la ventana a mano
            
        print("✅ Sesión guardada exitosamente.")
        print(f"Ahora puedes copiar la carpeta '{user_data_dir}' a tu servidor de Oracle Cloud.")

if __name__ == "__main__":
    setup_account()
