import os
import shutil
import sys
import subprocess




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

    env_src_path = os.path.join(main_path_dir, ".env")
    env_dest_path = os.path.join(project_path, ".env")
    shutil.copyfile(env_src_path, env_dest_path)
    print(f"Le ficher '.env' a été copié vers {env_dest_path}")

    main_project_files_path = os.path.join(main_path_dir,"main_project_files")
    if os.path.exists(main_project_files_path):
        shutil.copytree(main_project_files_path, project_path, dirs_exist_ok=True)
        print("Les fichiers .gitignore __main__.py et README.md ont été copiés avec succès.")
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

    project_folder = get_project_folder()
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
    project_folder = get_project_folder()
    app_path = os.path.join(project_folder, app_name)
    os.makedirs(app_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    sqlapp_path = os.path.join(script_dir, "sqlapp")

    if os.path.exists(sqlapp_path):
        shutil.copytree(sqlapp_path, app_path, dirs_exist_ok=True)
        print(f"L'application {app_name} a été créée avec succès.")
    else:
        print("Le dossier 'sqlapp' est introuvable.")


def get_project_folder():
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

    return os.path.join(parent_dir, project_folders[0])

def generate_userapp(ending):
    """
    Copie le contenu du dossier userapp (source) dans le dossier 'userapp' du projet.
    """
    project_folder=get_project_folder()
    user_app_name= f"userapp_{ending}"
    target_userapp_path = os.path.join(project_folder,user_app_name)
    os.makedirs(target_userapp_path, exist_ok=True)

    # Path vers le dossier source 'userapp' dans la bibliothèque
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_userapp_path = os.path.join(script_dir, "user/userapp")

    if os.path.exists(source_userapp_path):
        shutil.copytree(source_userapp_path, target_userapp_path, dirs_exist_ok=True)
        print(f"L'application 'userapp' a été copiée dans {target_userapp_path}.")
    else:
        print("Le dossier source 'userapp' est introuvable dans la bibliothèque.")

def run():
    project_folder=os.getcwd()
    main_entry=os.path.join(project_folder,"__main__.py")
    subprocess.run(["python",main_entry])

def main():
    if len(sys.argv) < 2:
        print("Usage: elrahapi <commande> <nom>")
        sys.exit(1)
    if len(sys.argv) > 2:
        name = sys.argv[2]
        command = sys.argv[1]
        ending=sys.argv[3]

    if command == "startproject":
        startproject(name)
    elif command == "startapp":
        startapp(name)
    elif command == "generate" and name == "userapp" and ending:
        generate_userapp(ending)
    elif command=="generate" and name=="loggerapp":
        generate_loggerapp()
    elif command == "run":
        run()
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
