import os
import shutil
import sys
import subprocess


def startproject(project_name):
    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path, exist_ok=True)

    # Initialise le dépôt Git
    subprocess.run(["git", "init", project_path])
    print(f"Git repo initialized in {project_path}")

    with open(f"{project_path}/__init__.py", "w") as f:
        f.write("# __init__.py\n")

    sub_project_path = os.path.join(project_path, project_name)
    os.makedirs(sub_project_path, exist_ok=True)

    settings_path = os.path.join(sub_project_path, "settings")
    os.makedirs(settings_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_settings_path = os.path.join(script_dir, "settings")
    main_path_dir = os.path.join(script_dir, "main")

    if os.path.exists(source_settings_path):
        shutil.copytree(source_settings_path, settings_path, dirs_exist_ok=True)
        print("Le dossier settings a été copié avec succès.")
    else:
        print("Le dossier source 'settings' est introuvable.")

    if os.path.exists(main_path_dir):
        shutil.copytree(main_path_dir, sub_project_path, dirs_exist_ok=True)
        print("Le ficher main  a été copié avec succès.")
    else:
        print("Le dossier source 'main' est introuvable.")

    # Création de l'environnement virtuel dans le dossier settings
    env_path = os.path.join(settings_path, "env")
    subprocess.run(["virtualenv", env_path])
    print(f"Environnement virtuel créé dans {env_path}")

    # Installation des dépendances avec pip
    requirements_file = os.path.join(settings_path, "requirements.txt")
    print(f"Installation des dépendances à partir de {requirements_file}...")
    subprocess.run(
        [os.path.join(env_path, "Scripts", "pip"), "install", "-r", requirements_file]
    )

    print(f"Le projet {project_name} a été créé avec succès.")


def startapp(app_name):
    parent_dir = os.getcwd()
    project_folders = [
        f
        for f in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, f)) and not f.startswith(".")
    ]

    if not project_folders:
        print("Aucun projet trouvé. Veuillez d'abord créer un projet.")
        return

    project_folder = os.path.join(parent_dir, project_folders[0])
    app_path = os.path.join(project_folder, app_name)
    os.makedirs(app_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    sqlapp_path = os.path.join(script_dir, "sqlapp")

    if os.path.exists(sqlapp_path):
        shutil.copytree(sqlapp_path, app_path, dirs_exist_ok=True)
        print(f"L'application {app_name} a été créée avec succès.")
    else:
        print("Le dossier 'sqlapp' est introuvable.")


def generate_appuser():
    parent_dir = os.getcwd()
    project_folders = [
        f
        for f in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, f)) and not f.startswith(".")
    ]

    if not project_folders:
        print("Aucun projet trouvé. Veuillez d'abord créer un projet.")
        return

    project_folder = os.path.join(parent_dir, project_folders[0])
    appuser_path = os.path.join(project_folder, "appuser")
    os.makedirs(appuser_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    appuser_source = os.path.join(script_dir, "appuser")

    if os.path.exists(appuser_source):
        shutil.copytree(appuser_source, appuser_path, dirs_exist_ok=True)
        print("Le contenu de 'appuser' a été copié avec succès.")
    else:
        print("Le dossier source 'appuser' est introuvable.")


def main():
    if len(sys.argv) < 2:
        print("Usage: harlequelrah_fastapi <commande> <nom>")
        sys.exit(1)
    if len(sys.argv) > 2:
        name = sys.argv[2]
    command = sys.argv[1]

    if command == "startproject":
        startproject(name)
    elif command == "startapp":
        startapp(name)
    elif command == "generate" and name == "appuser":
        generate_appuser()
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
