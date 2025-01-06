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
├── __main__.py
├── nomduprojet/
│   ├── __init__.py
│   ├── main.py
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
├── router.py
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
├── log_router.py
├── log_schema.py
```

### `Modules`

#### Module `exception`

Ce module contient des exceptions personnalisées utilisés dans cette bibliothèque

##### 1. Sous module auth_exception

ce sous module dispose de quelques variables d'exceptions prédéfinies liés à l'authentification

- `INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de paramètres d'authentification invalides .

- `INACTIVE_USER_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de compte utilisateur inactive .
##### 2. Sous module exceptions_utils
ce sous module contient des fonction utilitaires pour les exceptions
(status_code:int,detail:str)
- `raise_custom_http_exception` : lève une erreur CustomHttpException
  - **paramètre** :
    - `status_code` : **int**
    - `detail` : **str**
##### 3. Sous module custom_http_exception

- `CustomHttpException` : génère une exception personnalisé qui definit une exception de type HTTPExeption.



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
- `UserLoginRequestModel` : le modèle pydantic la connexion d'utilisateur
- `SECRET_KEY` : une clé secrète générer par défaut **str**
- `ALGORITHM` : un algorithm par défaut **[`HS256`]**
- `REFRESH_TOKEN_EXPIRE_DAYS` : **int**
- `ACCESS_TOKEN_EXPIRE_MINUTES` : **int**
- `session_factory` : **sessionmaker[Session]**


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
  - `sortie`:
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
  - `sortie`:
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

##### Sous module `models`

Ce sous module définit les modèles de Log : `LoggerMiddlewareModel` et `LoggerMiddlewarePydanticModel` pour la validation Pydantic

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

Ce sous module définit les middelwares de loggins

- Class **`LoggerMiddleware`**
  - `paramètres` :
    - LoggerMiddlewareModel : définit le modèle de Log a utilisé
    - session_factory : **sessionmaker[Session]**
    - manager : **ConnectionManager**

##### Sous module `error_middleware`

Ce sous module définit les middelwares d'erreurs

- Class **`ErrorMiddleware`**
  - `paramètres optionels` :
    - LoggerMiddlewareModel : définit le modèle de Log a utilisé
    - session_factory : **sessionmaker[Session]**
    - manager : **ConnectionManager**

##### Sous module crud_middelware

ce sous module définit les methodes pour sauvegarder les logs .

- **`save_log`** : enregistre les logs
  - `paramètres`:
    - *request*: Request
    - *LoggerMiddelewareModel*
    - *db* : Session
    - *call_next_*: Optional
    - *error* : Optional[str]
    - *response* : Optional[Response]
    - *manager*: Optional[ConnectionManager]
- `sortie`: **response : Response**

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

- `UserLoginRequestModel` :
  - username : **Optional[str]**
  - password : **str**
  - email : **Optional[str]**

##### Sous module userCrud

class **`UserCrud`**

paramètres de **init** :

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

#### Module `websocket`

Ce module comporte certaines classes et methodes pour interagir avec des websockets

##### Sous module `connectionManager`

Contient la classe ConnectionManager pour gérer une connextion avec un websocket .

- **methodes**:
  - **init**
  - **connect** (self,websocket)
  - **disconnect** (self,websocket)
  - **send_message** (self,str):

#### Module `crud`

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des cruds.

##### Sous module `crud_model`

Ce sous module comporte la classe CrudForgery pour générer des cruds de base .

**`CrudForgery`**:

- **`__init__`** :

  - **paramètres** :
    - `entity_name`: **str**
    - `session_factory`: **sessionmaker**
    - `SQLAlchemyModel` : Le model SQLAlchemy
    - `CreatePydanticModel` : Le model Pydantic pour la création .
    - `UpdatePydanticModel` : Le model Pydantic pour la mise à jour .

- **`create`** :

  - **paramètres** :
    - `create_ob`: **CreatePydanticModel**
  - **sortie** : **SQLAlchemyModel**

- **`count`** :

  - **sortie** : **int**

- **`read_all`** :

  - **paramètres** :
    - `skip`: **Optional[int]**
    - `limit`: **Optional[int]**
  - **sortie** : **List[SQLAlchemyModel]**

- **`read_all_by_filter`** :

  - **paramètres** :
    - `filter`: **str**
    - `value`: **str**
    - `skip`: **Optional[int]**
    - `limit`: **Optional[int]**
  - **sortie** : **List[SQLAlchemyModel]**

- **`read_one`** :

  - **paramètres** :
    - `id`: **int**
    - `db`: **Optional[Session]** : pour utiliser la même session lors de update et delete .
  - **sortie** : **SQLAlchemyModel**

- **`update`** :

  - **paramètres** :
    - `id`: **int**
    - `update_obj`: **UpdatePydanticModel**
  - **sortie** : **SQLAlchemyModel**

- **`delete`** :
  - **paramètres** :
    - `id`: **int**
  - **sortie** : **JsonResponse**

#### Module `router`

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des router.

##### Sous module `route_config`

Ce sous module comporte la classe RouteConfig pour configurer un CustomRouterProvider .

`RouteConfig`

- `__init__` :
  - `paramètres`:
    - `route_name`: **str**
    - `is_activated`: **bool** , default : `False`
    - `is_protected`: **bool** , default : `False`

##### Sous module `route_provider`

Ce sous module comporte la classe CustomRouterProvider pour configurer un CustomRouterProvider .
`CustomRouterProvider`

**`Attributs de classe`**

```python
ROUTES_NAME : List[str]=[
    "count",
    "read-one",
    "read-all",
    "read-all-by-filter",
    "create",
    "update",
    "delete",
  ]
DEFAULT_CONFIG : List[RouteConfig]=[RouteConfig(route_name,is_activated=True,is_protected=False) for route_name in ROUTES_NAME]
AUTH_CONFIG : List[RouteConfig]=[RouteConfig(route_name,is_activated=True,is_protected=True) for route_name in ROUTES_NAME]
```

- `__init__` :

  - `paramètres`:

    - `prefix`: **str**
    - `tags`: **List[str]**
    - `PydanticModel`: **Model de reponse Pydantic**
    - `crud` : **CrudForgery**
    - `get_access_token` : **Option[callable]**
    - `get_session` : **callable**

  - `utilisation` :

```python
router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    PydanticModel=model.PydanticModel,
    crud=myapp_crud,
    get_session=authentication.get_session,
    get_access_token=authentication.get_access_token,
)
```

- **`get_default_router`** : renvoie un router avec la configuration de `DEFAULT_CONFIG`

  - `sortie`: **APIRouter**

- **`get_protected_router`** : renvoie un router avec la configuration de `AUTH_CONFIG`

  - `sortie`: **APIRouter**

- **`initialize_router`** : renvoie un router avec une configuration personnalisée .
  - `paramètres`:
    - `init_data`: **List[RouteConfig]**
  - `sortie`: **APIRouter**
  - `utilisation` :

```python
init_data: List[RouteConfig] = [
    RouteConfig(route_name="create", is_activated=True),
    RouteConfig(route_name="read-one", is_activated=True),
    RouteConfig(route_name="update", is_activated=True, is_protected=True),
    RouteConfig(route_name="delete", is_activated=True, is_protected=True),
]
app_myapp = router_provider.initialize_router(init_data=init_data)
```

# Contact ou Support

Pour des questions ou du support, contactez-moi à maximeatsoudegbovi@gmail.com ou au (+228) 91 36 10 29.
