# Description

Passioné par la programmation et le développement avec python je me lance dans la création progressive d'une bibliothèque personnalisée pour m'ameliorer , devenir plus productif et partager mon expertise avec `FASTAPI`

# Logo
![Logo](harlequelrah.png)

## Installation

- **Avec Github :**
   ```bash
   git clone https://github.com/Harlequelrah/Library-harlequelrah_fastapi
   ```
- **Avec pip :**
   ```bash
   pip install harlequelrah_fastapi
   ```

## Utilisation
Ce package contient plusieurs modules utiles pour accélérer et modulariser le dévéloppement avec FASTAPI. Voici un aperçu de leurs fonctionnalités.

### `Commandes`

#### 1. Commande de création du projet
Cette commande permet de générer un projet FASTAPI avec une archictecture définie

 ```bash

   harlequelrah_fastapi startproject nomduprojet
 ```
 **`architecture`:**
```
nomduprojet/
├── __init__.py
├── .gitignore
├── alembic/
├── alembic.ini
├── requirements.txt
├── env/
├── nomduprojet/
│   ├── __init__.py
│   ├── __main__.py
│   ├── settings/
│       ├── .gitignore
│       ├── __init__.py
│       ├── database.py
│       ├── secret.py
│       └── models_metadata.py
```

#### 2. Commande de génération d'une application
Cette commande permet de créer une application dans le projet
```bash
  harlequelrah_fastapi startapp nomappli
```
**`architecture`:**
```
sqlapp/
├── __init__.py
├── crud.py
├── model.py
├── route.py
├── schema.py
├── util.py
```
#### 3. Commande génération d'une application utilisateur
Cette commande permet de créer une application utilisateur

**`architecture`:**
```
userapp/
├── __init__.py
├── app_user.py
├── user_model.py
├── user_crud.py
```

#### 4. Commande de génération d'une application de log
Cette commande permet de créer une application de log

**`architecture`:**
```
loggerapp/
├── __init__.py
├── log_user.py
├── log_model.py
├── log_crud.py
├── log_schema.py
```
### `Modules`
####  Module `exception`
Ce module contient des exceptions personnalisées utilisés dans cette bibliothèque
##### 1. Sous module auth_exception
ce sous module dispose de quelques variables d'exceptions prédéfinies liés à l'authentification

- `AUTHENTICATION_EXCEPTION` : exception personnalisée à léver lorsqu'une erreur d'authentification se produit

##### 2. Sous module custom_http_exception
- `CustomHttpException` : génère une exception personnalisé qui definit une exception de type HTTPExeption.
```python
  from fastapi import HTTPException , status
  from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException
  http_exception= HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="La requête a provoquée une exception non gérée")
  raise CustomHttpException(http_exception)
```
#### Module `utility`
Ce module contient des utilitaires utilisés dans cette bibliothèque.
- `update_entity` : mets à jour les champs d'une entité objet
  - paramètres : `existing_entity` , `update_entity`
  - retourne : `existing_entity`
  - utilisation :
  ```python
  from harlequelrah_fastapi.utility.utils import update_entity
  existing_entity = {"id": 1, "name": "John"}
  update_entity = {"id":1 , "name" : "Johnson"}
  existing_entity=update_entity(existing_entity,update_entity)
  ```

#### Module `authentication`
Ce module contient des classes et des fonctions utilisées pour l'authentification.

##### 1. Sous module `token`
Ce sous module définit des classes pydantics pour la gestions des tokens :
- AccessToken : access_token : **str** , token_type : **str**
- RefreshToken : refresh_token : **str** , token_type : **str**
- Token : access_token : **str** ,refresh_token : **str** , token_type : **str**

##### 2. Sous module `authenticate`
ce sous module définit les classes et fonctions utilisées pour l'authentification

- **`Classe Authentication`**:classe principale pour gérer l'authentification
- `oauth2_scheme` : définit le schéma d'authentication
- `User` : le modèle d'utilisateur SQLAlchemy
- `UserCreateModel` : le modèle pydantic pour la création d'utilisateur
- `UserUpdateModel` : le modèle pydantic pour la mise à jour d'utilisateur
- `UserPydanticModel` : le modèle pydantic pour lire un utilisateur
- `UserLoginModel` : le modèle pydantic la connexion d'utilisateur
- `SECRET_KEY` : une clé secrète générer par défaut
- `ALGORITHM` : un algorithm par défaut `HS256`
- `REFRESH_TOKEN_EXPIRE_DAYS` : **int**
- `ACCESS_TOKEN_EXPIRE_MINUTES` : **int**
- `session_factory` : un générateur de session
- `CREDENTIALS_EXCEPTION` : une exception de type `CustomHttpException` à lever lorsque l'authentification échoue

#### Module `authorization`
Ce module contient des classes et des fonctions utilisées pour l'autorisation.

##### Sous module `role`
Ce sous module contient les models SQLAlchemy et classes pydantic et crud pour l'entité Role .
- sous module `role_model`

`Role`:
- id : int
- name : str
- normalized_name : str (automatique à l'ajout de name)

Les classes pydantic sont : `RolePydanticModel`,`RoleCreateModel`,`RoleUpdateModel`

- Sous module `role_crud`
ce sous module définit les cruds :
- **`get_count_roles`**
  - `paramètres` :
    - db : **Session**
  - `sortie` : **int**
- **`create_role`**
  - `paramètres` :
    - db : **Session**
    - role_create : **RoleCreateModel**
  -  `sortie`:
    - role : **Role**
- **`get_role`**
  - `paramètres` :
    - db : **Session**
    - role_id : **int**
  - `sortie` : **Role**
- **`get_roles`**
  - `paramètres` :
    - db : **Session**
    - skip : **int**
    - limit : **int**
  - `sortie` : **List[Role]**
- **`update_role`**
  - `paramètres` :
    - db : **Session**
    - role_id : **int**
    - role_update : **RoleUpdateModel**
  - `sortie`: **Role**
- **`delete_role`**
  - `paramètres` :
    - db : **Session**
    - role_id : **int**
  - `sortie`: **JSONResponse**
- **`add_role_to_user`**
  - `paramètres` :
    - db : **Session**
    - user : **User**
    - role_id : **int**
  - `sortie`: **JsonResponse**

##### Sous module `privilege`
Ce sous module contient les models SQLAlchemy et classes pydantic et crud pour l'entité Privilege .
- sous module `privilege_model`

`Privilege`:
- id : int
- name : str
- normalized_name : str (automatique à l'ajout de name)

Les classes pydantic sont : `PrivilegePydanticModel`,`PrivilegeCreateModel`,`PrivilegeUpdateModel`

- Sous module `privilege_crud`
ce sous module définit les cruds :
- **`get_count_privileges`**
  - `paramètres` :
    - db : **Session**
  - `sortie` : **int**
- **`create_privilege`**
  - `paramètres` :
    - db : **Session**
    - privilege_create : **PrivilegeCreateModel**
  -  `sortie`:
    - privilege : **Privilege**
- **`get_privilege`**
  - `paramètres` :
    - db : **Session**
    - privilege_id : **int**
  - `sortie` : **Privilege**
- **`get_privileges`**
  - `paramètres` :
    - db : **Session**
    - skip : **int**
    - limit : **int**
  - `sortie` : **List[Privilege]**
- **`update_privilege`**
  - `paramètres` :
    - db : **Session**
    - privilege_id : **int**
    - privilege_update : **PrivilegeUpdateModel**
  - `sortie`: **Privilege**
- **`delete_privilege`**
  - `paramètres` :
    - db : **Session**
    - privilege_id : **int**
  - `sortie`: **JSONResponse**

#### Module `middleware`
Ce module regroupe toute la gestion des middelwares

##### Sous module `model`
Ce sous module définit les  modèles de Log : `LoggerMiddlewareModel` et `LoggerMiddlewarePydanticModel` pour la validation Pydantic

**Attributs prédéfinis**:
- id : **int**
- status_code : **int**
- method : **str**
- url : **str**
- error_message : **str**
- date_created : **datetime**
- process_time : **float**
- remote_adress: **str**

##### Sous module `log_middleware`
Ce sous module définit les  middelwares de loggins

- Class **`LoggerMiddleware`**
  - `paramètres` :
    - LoggerMiddlewareModel : définit le modèle de Log a utilisé
    - session_factory : le générateur de session

##### Sous module `error_middleware`
Ce sous module définit les  middelwares d'erreurs

- Class **`ErrorMiddleware`**
  - `paramètres optionels` :
    - LoggerMiddlewareModel : définit le modèle de Log a utilisé
    - session_factory : le générateur de session

##### Sous module logCrud
ce sous module définit une classe pour le crud des logs

Class **`LogCrud`**

- `paramètres` :
  - LoggerModel : définit le modèle de Log à utiliser
  - session_factory : le générateur de session

- `methodes` :
  - `get_count_logs` : retourne le nombre total de log
  - `get_log` :
    - `paramètres` :
      - id : **int**
    - `sortie` : **LoggerModel**

  - `get_logs` :
    - `paramètres` :
      - skip : **int**
      - limit : **int**
    - `sortie` : **List[LoggerModel]**

#### Module `user`
Ce module comporte toute la gestion des utilisateurs

##### Sous module `models`
Ce sous module comporte tous les models pour l'entité utilisateur

class **`User`**
`Attributs`:
- id : **int**
- email : **str**
- username : **str**
- password : **str**
- lastname : **str**
- date_created : **datetime**
- is_active : **bool**
- attempt_login : **int**


`Methodes` :
- try_login :
tente de connecter un utilisateur et mets à jour attempt_login en fonction
  - paramètres :
     - is_success : **bool**
  - sortie : **bool**

- set_password
  - paramètres :
   - password : **str**
  - sortie : **None**

- check_password
  - paramètres :
   - password : **str**
  - sortie : **bool**

Models pydantics pour la validations :
- `UserBaseModel`
- `UserCreateModel`
- `UserUpdateModel`
- `UserPydanticModel`
- `AdditionalUserPydanticModelField`

- `UserLoginModel` :
  - username : **Optional[str]**
  - password : **str**
  - email : **Optional[str]**

##### Sous module userCrud

class **`UserCrud`**

paramètres de __init__ :
- authentication : **Authentication**

Methodes :
- get_count_users
  - sortie : **int**

- is_unique
  - paramètres :
    - sub : **str** (id or username)
  - sortie : **bool**

- create_user
  - paramètres :
    - user : **authentication.UserCreateModel**
  - sortie : **authentication.User**

- get_user
  - paramètres :
    id : **Optional[int]**
    sub : **Optional[str]** (username)
  - sortie : **authentication.User**

- get_users
  - paramètres :
    - skip : **Optional[int]**
    - limit : **Optional[int]**
   - sortie : **List[authentication.User]**

- update_user
  - paramètres :
    - user_id : **int**
    - userUpdated : **authentication.UserUpdateModel**
  - sortie : **List[authentication.User]**
- delete_user
  - paramètres :
    - user_id : **int**
  - sortie : **JsonResponse**
# Contact ou Support
Pour des questions ou du support, contactez-moi à maximeatsoudegbovi@gmail.com ou au (+228) 91 36 10 29.
