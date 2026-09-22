# Documentación y Configuración del Bot

## 1. Instalación de Dependencias
Asegúrate de tener Python instalado y crea un entorno virtual (recomendado). Luego instala los requerimientos:

```bash
# Crear entorno virtual (opcional pero recomendado)
python3 -m venv env
source env/bin/activate

# Instalar dependencias
pip install playwright
playwright install chromium
```
*(En el servidor de Oracle, es posible que necesites dependencias adicionales de sistema operativo para playwright, ejecútalas con: `playwright install-deps` si te marca error).*

## 2. Autenticación y Cuentas (Guardar Sesión)
El bot utiliza un perfil persistente para entrar sin problemas y saltarse los bloqueos de bots y el 2FA de Google.

### Iniciar sesión por primera vez
Para guardar tu sesión, ejecuta el script de configuración en tu entorno local:
```bash
python3 auth_setup.py
```
Esto abrirá un navegador visible. Inicia sesión normalmente con tu cuenta de Google, resuelve cualquier 2FA, y cuando estés dentro, vuelve a la terminal y **presiona ENTER** para guardar la sesión. Todo se guardará en la carpeta `perfil_meet`.

### Cómo cambiar de cuenta (Borrar credenciales)
Si iniciaste sesión con una cuenta de prueba y quieres cambiar a la tuya (o viceversa), **DEBES borrar la carpeta anterior** para no dejar registros y generar una limpia:

```bash
# 1. Borrar la carpeta con las credenciales viejas
rm -rf perfil_meet

# 2. Volver a ejecutar el setup para loguearte con la nueva cuenta
python3 auth_setup.py
```

## 3. Pruebas Locales (Correr el Bot)
Para probar que el bot funciona correctamente en tu PC antes de mandarlo al servidor, usa el flag `--visible` para que puedas ver cómo abre el navegador, apaga el micrófono y entra a la llamada.

```bash
python3 meet_bot.py "https://meet.google.com/tu-enlace-aqui" --visible
```
*Nota: El bot es capaz de detectar si haces "Switch" (Cambiar aquí) desde tu celular u otra PC. Si entras con la misma cuenta a la misma llamada, el bot se apagará automáticamente.*

## 4. Configuración del Cron en Linux (Producción)
En tu servidor Linux (Oracle Cloud), el bot debe ejecutarse en modo headless (invisible, no uses el flag `--visible`).

Para ejecutar el bot automáticamente de lunes a viernes a las **19:15** y cerrarlo a las **22:00**, abre el editor de cron:
```bash
crontab -e
```

### Opción 1: Usando `timeout` (Recomendada)
El comando `timeout` ejecuta un proceso y lo "mata" automáticamente cuando pasa cierto tiempo. Desde las 19:15 hasta las 22:00 hay 165 minutos (2 horas y 45 minutos).

```cron
# M-V a las 19:15 (7:15 PM), lo ejecuta y lo cierra pasados 165 minutos (a las 22:00 exactas)
15 19 * * 1-5 timeout 165m /usr/bin/python3 /ruta/absoluta/a/tu/proyecto/meet_bot.py "https://meet.google.com/abc-defg-hij" >> /ruta/absoluta/a/tu/proyecto/bot.log 2>&1
```

### Opción 2: Usando dos tareas cron (Iniciar y Matar)
Si prefieres iniciar y matar explícitamente:
```cron
# Iniciar a las 19:15 (7:15 PM) de lunes a viernes
15 19 * * 1-5 /usr/bin/python3 /ruta/absoluta/a/tu/proyecto/meet_bot.py "https://meet.google.com/abc-defg-hij" >> /ruta/absoluta/a/tu/proyecto/bot.log 2>&1 &

# Matar el proceso a las 22:00 (10:00 PM) de lunes a viernes
0 22 * * 1-5 pkill -f "meet_bot.py"
```

## 5. Mantenimiento: Selectores CSS/XPath
Si Google Meet actualiza su interfaz y los textos de "Unirse ahora" / "Solicitar unirse" cambian:

1. Abre Google Meet, haz clic derecho en el botón de unirse y elige **"Inspeccionar"**.
2. Busca el texto interno o el `aria-label`.
3. Actualiza el arreglo `join_texts` en `meet_bot.py` o cambia el selector:
   - `page.locator('button[aria-label="Solicitar unirse"]')`

*Nota:* Para el micrófono y cámara, el código usa `Ctrl+d` y `Ctrl+e` ya que han probado ser los más resilientes a cambios de interfaz.