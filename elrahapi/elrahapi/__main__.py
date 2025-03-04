import os
import shutil
import sys
import subprocess
from dotenv import load_dotenv


load_dotenv()
PROJECT_NAME = os.getenv('PROJECT_NAME')
def startproject(project_name):
    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path, exist_ok=True)
    sub_project_path = os.path.join(project_path, project_name)
    os.makedirs(sub_project_path, exist_ok=True)

    # Initialise le dépôt Git
    try :
        subprocess.run(["git", "init", project_path])
        print(f"Git repo initialized in {project_path}")
    except Exception as e :
        print(f"Erreur lors de l'initialisation du dépôt Git: {e}")

    subprocess.run(["alembic", "init","alembic"], cwd=project_path)
    print(f"Alembic a été initialisé dans {project_path}")

    with open(f"{project_path}/__init__.py", "w") as f:
        f.write("# __init__.py\n")

    with open(f"{sub_project_path}/__init__.py", "w") as f:
        f.write("# __init__.py\n")

    settings_path = os.path.join(sub_project_path, "settings")
    os.makedirs(settings_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_settings_path = os.path.join(script_dir, "settings")
    main_path_dir = os.path.join(script_dir, "main")
    main_script_src_path = os.path.join(main_path_dir, "main.py")
    main_script_dest_path = os.path.join(sub_project_path, "main.py")
    shutil.copyfile(main_script_src_path, main_script_dest_path)
    print(f"Le ficher 'main.py' a été copié vers {main_script_dest_path}")

    main_project_files_path = os.path.join(main_path_dir,"project_files")
    if os.path.exists(main_project_files_path):
        shutil.copytree(main_project_files_path, project_path, dirs_exist_ok=True)
        print("Les fichiers .env .gitignore __main__.py ont été copiés avec succès.")
    else:
        print("Le dossier source 'main_project_files' est introuvable.")

    if os.path.exists(source_settings_path):
        shutil.copytree(source_settings_path, settings_path, dirs_exist_ok=True)
        print("Le dossier settings a été copié avec succès.")
    else:
        print("Le dossier source 'settings' est introuvable.")
    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        subprocess.run(["pip", "freeze"], stdout=f)
    print(f"Le projet {project_name} a été créé avec succès.")

def generate_loggerapp():
    """
    Copie le contenu du dossier loggerapp (source) dans le dossier 'loggerapp' du projet.
    """
    parent_dir = os.getcwd()
    project_folders = [
        f
        for f in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, f))
        and not (f.startswith("env") or f.startswith("alembic"))
        and not f.startswith(".")
    ]

    if not project_folders:
        print("Aucun projet trouvé. Veuillez d'abord créer un projet.")
        return

    project_folder = os.path.join(parent_dir, project_folders[0])
    target_loggerapp_path = os.path.join(project_folder, "loggerapp")
    os.makedirs(target_loggerapp_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_loggerapp_path = os.path.join(script_dir, "middleware/loggerapp")

    if os.path.exists(source_loggerapp_path):
        shutil.copytree(source_loggerapp_path, target_loggerapp_path, dirs_exist_ok=True)
        print(f"L'application 'loggerapp' a été copiée dans {target_loggerapp_path}.")
    else:
        print("Le dossier source 'loggerapp' est introuvable dans la bibliothèque.")


def startapp(app_name):
    parent_dir = os.getcwd()
    project_folders = [
        f
        for f in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, f))
        and not (f.startswith("env") or f.startswith("alembic"))
        and not f.startswith(".")
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



def generate_userapp():
    """
    Copie le contenu du dossier userapp (source) dans le dossier 'userapp' du projet.
    """
    parent_dir = os.getcwd()
    project_folders = [
        f
        for f in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, f))
        and not (f.startswith("env") or f.startswith("alembic"))
        and not f.startswith(".")
    ]

    if not project_folders:
        print("Aucun projet trouvé. Veuillez d'abord créer un projet.")
        return

    project_folder = os.path.join(parent_dir, project_folders[0])
    target_userapp_path = os.path.join(project_folder, "userapp")
    os.makedirs(target_userapp_path, exist_ok=True)

    # Path vers le dossier source 'userapp' dans la bibliothèque
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_userapp_path = os.path.join(script_dir, "user/userapp")

    if os.path.exists(source_userapp_path):
        shutil.copytree(source_userapp_path, target_userapp_path, dirs_exist_ok=True)
        print(f"L'application 'userapp' a été copiée dans {target_userapp_path}.")
    else:
        print("Le dossier source 'userapp' est introuvable dans la bibliothèque.")
def replace_in_file(file_path, search_word, replace_word):
    """Remplace un mot dans un fichier donné si présent."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    new_content = re.sub(re.escape(search_word), replace_word, content)

    if new_content != content:  # Vérifie si des modifications ont été faites
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"✅ Modifié : {file_path}")

def search_and_replace(directory, search_word, replace_word):
    """Parcourt récursivement un dossier et remplace un mot dans les fichiers .py."""
    if not os.path.exists(directory):
        print(f"⚠️ Dossier introuvable : {directory}")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Ne traiter que les fichiers Python
                file_path = os.path.join(root, file)
                try:
                    replace_in_file(file_path, search_word, replace_word)
                except Exception as e:
                    print(f"❌ Erreur avec {file_path}: {e}")

def cleanproject():
    """Nettoie le projet en remplaçant 'myproject' par PROJECT_NAME dans le dossier du projet."""
    project_path = os.path.join(os.getcwd(), PROJECT_NAME)  # Chemin du projet
    print(f"🔍 Nettoyage du projet {PROJECT_NAME} dans {project_path}")
    search_and_replace(project_path, "myproject", PROJECT_NAME)

def cleanapp(app_name):
    """Nettoie une application spécifique en remplaçant 'myapp' par app_name dans ses fichiers."""
    app_path = os.path.join(os.getcwd(), PROJECT_NAME, app_name)  # Chemin de l'application
    print(f"🔍 Nettoyage de l'application {app_name} dans {app_path}")
    search_and_replace(app_path, "myapp", app_name)

def cleanapp(app_name):
    pass

def cleanproject():
    pass
def main():
    if len(sys.argv) < 2:
        print("Usage: elrahapi <commande> <nom>")
        sys.exit(1)
    if len(sys.argv) > 2:
        name = sys.argv[2]
    command = sys.argv[1]

    if command == "startproject":
        startproject(name)
    elif command == "startapp":
        startapp(name)
    elif command == "generate" and name == "userapp":
        generate_userapp()
    elif command=="generate" and name=="loggerapp":
        generate_loggerapp()
    elif command=="clean-project":
        cleanproject()
    elif command=="clean-app":
        cleanapp(name)
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
