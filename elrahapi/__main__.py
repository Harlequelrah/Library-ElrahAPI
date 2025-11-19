import os
import shutil
import subprocess
import sys

from colorama import Fore, Style, init
from elrahapi.security.secret import define_algorithm_and_key

init(autoreset=True)


def replace_line(file, line, line_content):
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
        replace_line(env_file, secret_key_line, f"SECRET_KEY = {key}\n")
    if algorithm_line:
        replace_line(env_file, algorithm_line, f"ALGORITHM = {algo}\n")


def generate_secret_key(
    env_src_path: str | None = None, algorithm: str = "HS256"
) -> str:
    if env_src_path is None:
        project_folder = os.getcwd()
        env_src_path = os.path.join(project_folder, ".env")
    update_env_with_secret_and_algorithm(env_src_path, algorithm)
    print(
        Fore.GREEN
        + "SECRET_KEY and ALGORITHM have been generated and added to the .env file"
    )


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
    print(Fore.GREEN + f"Alembic has been initialized in {project_path}")

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
    shutil.copyfile(env_src_path, env_dest_path)
    print(f"The '.env' file has been copied to {env_dest_path}")

    example_env_src_path = os.path.join(main_path_dir, ".env.example")
    example_env_dest_path = os.path.join(project_path, ".env.example")
    shutil.copyfile(example_env_src_path, example_env_dest_path)
    print(f"The file '.env.example' has been copied to {example_env_dest_path}")

    main_project_files_path = os.path.join(main_path_dir, "main_project_files")
    if os.path.exists(main_project_files_path):
        shutil.copytree(main_project_files_path, project_path, dirs_exist_ok=True)
        print(
            "The files .gitignore, __main__.py, and README.md have been copied successfully."
        )
    else:
        print("The source folder 'main_project_files' was not found.")

    source_tests_path = os.path.join(script_dir, "tests")
    if os.path.exists(source_tests_path):
        shutil.copytree(source_tests_path, os.path.join(project_path, "tests"), dirs_exist_ok=True)
        print("The 'tests' folder has been copied successfully.")
    if os.path.exists(source_settings_path):
        shutil.copytree(source_settings_path, settings_path, dirs_exist_ok=True)
        print("The 'settings' folder has been copied successfully.")
    else:
        print("The source folder 'settings' was not found.")
    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        subprocess.run(["pip", "freeze"], stdout=f)
    with open(env_dest_path, "r") as f:
        lines = f.readlines()
    with open(env_dest_path, "w") as f:
        for line in lines:
            if line.strip().startswith("PROJECT_NAME"):
                f.write(f"PROJECT_NAME = {project_name}\n")
            elif line.strip().startswith("ISSUER"):
                f.write(f"ISSUER = {project_name}\n")
            else:
                f.write(line)
    print(Fore.CYAN + f"The project {project_name} has been created successfully.")
    generate_secret_key(env_src_path=env_dest_path)


def create_seed(seed_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    main_path_dir = os.path.join(script_dir, "main")
    seed_src_src = os.path.join(main_path_dir, "seed.py")
    seeders_dir = get_seeders_dir()
    if not seeders_dir:
        print(Fore.RED + Style.BRIGHT + "Seeders directory not found")
        return
    seed_file_dest = os.path.join(seeders_dir, f"{seed_name}_seed.py")
    if os.path.exists(seed_file_dest):
        print(Fore.RED + Style.BRIGHT + f"Seeder {seed_name} already exists.")
        return
    shutil.copyfile(seed_src_src, seed_file_dest)
    print(
        Fore.GREEN
        + Style.BRIGHT
        + f"The seeder '{seed_name}_seed.py' file has been create to {seed_file_dest}"
    )


def startapp(app_name):
    apps_dir_folder = get_apps_dir()
    app_path = os.path.join(apps_dir_folder, app_name)
    os.makedirs(app_path, exist_ok=True)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    sqlapp_path = os.path.join(script_dir, "sqlapp")

    if os.path.exists(sqlapp_path):
        shutil.copytree(sqlapp_path, app_path, dirs_exist_ok=True)
        print(Fore.CYAN + f"The application {app_name} has been created successfully.")
    else:
        print("The 'sqlapp' folder was not found.")


def get_project_name():
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
    return project_name


def get_apps_dir():
    parent_dir = os.getcwd()
    # env_path = os.path.join(parent_dir, ".env")
    project_name = os.getenv("PROJECT_NAME")
    if project_name is None:
        project_name = get_project_name()
    apps_dir_folder = os.path.join(parent_dir, project_name)
    # print(apps_dir_folder)
    if not os.path.isdir(apps_dir_folder):
        print(f"Apps dirs '{apps_dir_folder}' not found.")
        return
    # print(apps_dir_folder)

    return apps_dir_folder


def get_settings_dir():
    apps_dir = get_apps_dir()
    if not apps_dir:
        print(Fore.RED + Style.BRIGHT + "Apps directory not found")
        return None
    settings_dir = os.path.join(apps_dir, "settings")
    if not os.path.exists(settings_dir):
        print(Fore.RED + Style.BRIGHT + "Settings directory not found")
        return None
    return settings_dir


def get_seeders_dir():
    settings_dir = get_settings_dir()
    if not settings_dir:
        print(Fore.RED + Style.BRIGHT + "Settings directory not found")
        return None
    seeders_dir = os.path.join(settings_dir, "seeders")
    if not os.path.exists(seeders_dir):
        print(Fore.RED + Style.BRIGHT + "Seeders directory not found")
        return None
    return seeders_dir


def get_seeders_log_file():
    seeders_dir = get_seeders_dir()
    if not seeders_dir:
        print(Fore.RED + Style.BRIGHT + "Seeders directory not found")
        return None
    log_file = os.path.join(seeders_dir, "seeders.log")
    return log_file


def run_seed(seed_name, action: bool):
    seeders_dir = get_seeders_dir()
    seeder_path = os.path.join(seeders_dir, f"{seed_name}_seed.py")
    if not os.path.exists(seeder_path):
        print(Fore.RED + Style.BRIGHT + f"seeder {seed_name} file not found")
        return
    env = set_python_path()
    subprocess.run(
        [
            sys.executable,
            seeder_path,
            "up" if action else "down",
        ],
        env=env,
    )


def run_seed_manager(action: str):
    try:
        seeders_dir = get_seeders_dir()
        seeder_path = os.path.join(seeders_dir, "seed_manager_seed.py")
        if not os.path.exists(seeder_path):
            print(Fore.RED + Style.BRIGHT + f"seeder seed_manager_seed file not found")
            return
        env = set_python_path()
        subprocess.run(
            [
                sys.executable,
                seeder_path,
                "up" if action else "down",
            ],
            env=env,
        )
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error running seed manager: {e}")


def set_python_path():
    env = os.environ.copy()
    path = os.pathsep.join([os.getcwd(), get_apps_dir(), get_settings_dir()])
    env["PYTHONPATH"] = path
    return env


def create_tables():
    try:
        apps_dir = get_apps_dir()
        models_metadata_path = os.path.join(apps_dir, "settings/models_metadata.py")
        env = set_python_path()
        subprocess.run([sys.executable, models_metadata_path], env=env)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error creating tables: {e}")


def run():
    project_folder = os.getcwd()
    main_entry = os.path.join(project_folder, "__main__.py")
    env = set_python_path()
    subprocess.run([sys.executable, main_entry], env=env)


def main():
    if len(sys.argv) < 2:
        print("Usage: elrahapi <commande> <name> [<action>]")
        sys.exit(1)
    command = sys.argv[1]
    name: str | None = None
    action: str | None = None
    if len(sys.argv) > 2:
        name = sys.argv[2]
    if len(sys.argv) > 3:
        action = sys.argv[3]
    if command == "run":
        run()
    elif command == "startapp" and name:
        startapp(name)
    elif command == "startproject" and name:
        startproject(name)
    elif command == "create_seed" and name:
        create_seed(name)
    elif command == "run_seed" and name:
        action_name = action or "up"
        action = True if action_name == "up" else False
        run_seed(seed_name=name, action=action)
    elif command == "run_seed_manager":
        action_name = name or "up"
        action = True if action_name == "up" else False
        run_seed_manager(action=action)
    elif command == "create_tables":
        create_tables()
    elif command == "generate_secret_key":
        if name:
            generate_secret_key(algorithm=name)
        else:
            generate_secret_key()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
