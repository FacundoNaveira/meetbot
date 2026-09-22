from playwright.sync_api import sync_playwright
print("Probando Playwright...")
try:
    p = sync_playwright().start()
    b = p.chromium.launch(headless=True)
    b.close()
    p.stop()
    print("TODO OK")
except Exception as e:
    print(f"ERROR: {e}")
