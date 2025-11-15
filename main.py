# main.py

from sistema import SistemaHotDog

if __name__ == "__main__":
    # Aquí usas las URLs de tu repo en GitHub
    USERNAME = "FernandoSapient"
    REPOSITORY = "BPTSP05_2526-1"
    BRANCH = "main"
    MENU_PATH = "menu.json"
    ING_PATH = "ingredientes.json"

    MENU_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{MENU_PATH}"
    ING_URL = f"https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{ING_PATH}"

    sistema = SistemaHotDog(MENU_URL, ING_URL)
    sistema.ejecutar()
