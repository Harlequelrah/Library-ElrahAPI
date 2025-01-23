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
    subprocess.run(["git", "init", project_path])
    print(f"Git repo initialized in {project_path}")
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

    # Créer l'environnement virtuel directement dans le dossier du projet (pas dans 'settings')
    env_path = os.path.join(project_path, "env")
    subprocess.run(["virtualenv", env_path])
    print(f"Environnement virtuel créé dans {env_path}")
    requirements_src_path = os.path.join(settings_path, "requirements.txt")
    requirements_dest_path = os.path.join(project_path, "requirements.txt")
    shutil.move(requirements_src_path, requirements_dest_path)
    print(f"Le ficher 'requirements.txt' a été déplacé vers {requirements_dest_path}")

    # Installation des dépendances avec pip
    requirements_file = os.path.join(project_path, "requirements.txt")
    if os.path.exists(requirements_file):
        print(f"Installation des dépendances à partir de {requirements_file}...")
        subprocess.run(
            [
                os.path.join(env_path, "Scripts", "pip"),
                "install",
                "-r",
                requirements_file,
            ]
        )
    else:
        print("Le fichier requirements.txt n'a pas été trouvé.")

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

    # Path vers le dossier source 'userapp' dans la bibliothèque
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
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
