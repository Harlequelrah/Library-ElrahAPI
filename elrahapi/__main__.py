import os
import shutil
import sys
import subprocess

from elrahapi.security.secret import define_algorithm_and_key


def repline(file, line, line_content):
    with open(file, "r") as ficher:
        a = ficher.readlines()
    with open(file, "w") as ficher:
        ficher.writelines(a[0 : line - 1])
        ficher.write(line_content)
        ficher.writelines(a[line:])


def update_env_with_secret_and_algorithm(env_file: str, algorithm: str = "HS256"):
    algo, key = define_algorithm_and_key(algorithm=algorithm)
    with open(env_file, "r") as f:
        lines = f.readlines()
    secret_key_line = None
    algorithm_line = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("SECRET_KEY"):
            secret_key_line = idx + 1
        if line.strip().startswith("ALGORITHM"):
            algorithm_line = idx + 1
    if secret_key_line:
        repline(env_file, secret_key_line, f"SECRET_KEY={key}\n")
    if algorithm_line:
        repline(env_file, algorithm_line, f"ALGORITHM={algo}\n")


def generate_secret_key(env_src_path:str | None =None,algorithm: str = "HS256") -> str:
    if env_src_path is None :
        project_folder = os.getcwd()
        env_src_path = os.path.join(project_folder, ".env")
    update_env_with_secret_and_algorithm(env_src_path, algorithm)
    print("SECRET_KEY and ALGORITHM have been generated and added to the .env file")


def startproject(project_name):
    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path, exist_ok=True)
    apps_dir = os.path.join(project_path, project_name)
    os.makedirs(apps_dir, exist_ok=True)

    # Initialise le dépôt Git
    try:
        subprocess.run(["git", "init", project_path])
        print(f"Git repo initialized in {project_path}")
    except Exception as e:
        print(f"Error initializing the Git repository: {e}")

    subprocess.run(["alembic", "init", "alembic"], cwd=project_path)
    print(f"Alembic has been initialized in {project_path}")

    with open(f"{project_path}/__init__.py", "w") as f:
        f.write("# __init__.py\n")

    with open(f"{apps_dir}/__init__.py", "w") as f:
        f.write("# __init__.py\n")

    settings_path = os.path.join(apps_dir, "settings")
    os.makedirs(settings_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_settings_path = os.path.join(script_dir, "settings")
    main_path_dir = os.path.join(script_dir, "main")
    main_script_src_path = os.path.join(main_path_dir, "main.py")
    main_script_dest_path = os.path.join(apps_dir, "main.py")
    shutil.copyfile(main_script_src_path, main_script_dest_path)
    print(f"The file 'main.py' has been copied to {main_script_dest_path}")

    env_src_path = os.path.join(main_path_dir, ".env")
    env_dest_path = os.path.join(project_path, ".env")
    print(f"{env_src_path,env_dest_path=}")
    shutil.copyfile(env_src_path, env_dest_path)
    print(f"The '.env' file has been copied to {env_dest_path}")

    example_env_src_path = os.path.join(main_path_dir, ".env.example")
    example_env_dest_path = os.path.join(project_path, ".env.example")
    shutil.copyfile(example_env_src_path, example_env_dest_path)
    print(f"The file '.env.example' has been copied to {example_env_dest_path}")

    with open(env_dest_path, "r") as f:
        lines = f.readlines()
    with open(env_dest_path, "w") as f:
        for line in lines:
            if line.strip().startswith("PROJECT_NAME="):
                f.write(f"PROJECT_NAME={project_name}\n")
            else:
                f.write(line)
    main_project_files_path = os.path.join(main_path_dir, "main_project_files")
    if os.path.exists(main_project_files_path):
        shutil.copytree(main_project_files_path, project_path, dirs_exist_ok=True)
        print(
            "The files .gitignore, __main__.py, and README.md have been copied successfully."
        )
    else:
        print("The source folder 'main_project_files' was not found.")

    if os.path.exists(source_settings_path):
        shutil.copytree(source_settings_path, settings_path, dirs_exist_ok=True)
        print("The 'settings' folder has been copied successfully.")
    else:
        print("The source folder 'settings' was not found.")
    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        subprocess.run(["pip", "freeze"], stdout=f)
    print(f"The project {project_name} has been created successfully.")
    generate_secret_key(env_src_path=env_dest_path)


def startapp(app_name):
    apps_dir_folder = get_apps_dir()
    app_path = os.path.join(apps_dir_folder, app_name)
    os.makedirs(app_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    sqlapp_path = os.path.join(script_dir, "sqlapp")

    if os.path.exists(sqlapp_path):
        shutil.copytree(sqlapp_path, app_path, dirs_exist_ok=True)
        print(f"The application {app_name} has been created successfully.")
    else:
        print("The 'sqlapp' folder was not found.")

def get_apps_dir():
    parent_dir = os.getcwd()
    env_path = os.path.join(parent_dir, ".env")
    project_name = None

    if not os.path.exists(env_path):
        print("No .env file found in the current directory.")
        return

    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith("PROJECT_NAME"):
                project_name = line.split("=", 1)[-1].strip()
                break
    if not project_name:
        print("PROJECT_NAME not found in .env file.")
        return

    apps_dir_folder = os.path.join(parent_dir, project_name)
    if not os.path.isdir(apps_dir_folder):
        print(f"Apps dirs '{apps_dir_folder}' not found.")
        return

    return apps_dir_folder


def run():
    project_folder =  os.getcwd()
    main_entry = os.path.join(project_folder, "__main__.py")
    subprocess.run(["python", main_entry])


def main():
    if len(sys.argv) < 2:
        print("Usage: elrahapi <commande> <name>")
        sys.exit(1)
    if len(sys.argv) >= 2:
        command = sys.argv[1]
    if len(sys.argv) >= 3:
        name = sys.argv[2]
    if command == "run":
        run()
    if command == "startproject":
        startproject(name)
    elif command == "startapp":
        startapp(name)
    elif command == "generate_secret_key":
        if len(sys.argv) == 2:
            generate_secret_key()
        elif len(sys.argv) == 3:
            generate_secret_key(algorithm=name)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
