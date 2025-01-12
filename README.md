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

- `raise_custom_http_exception` : lève une erreur CustomHttpException

  - **paramètres** :

    - `status_code` : **int**

    - `detail` : **str**


##### 3. Sous module custom_http_exception

- `CustomHttpException` : génère une exception personnalisé qui definit une exception de type HTTPExeption.

#### Module `utility`

Ce module contient des utilitaires utilisés dans cette bibliothèque.

- `update_entity` : mets à jour les champs d'une entité objet .

  - **paramètres** :

    - existing_entity : l'entité existante à mettre à jour.

    - update_entity : l'entité pour mettre  : l'entité pour la mise à jour .

  - **sortie** : **existing_entity**


#### Module `authentication`

Ce module contient des classes et des fonctions utilisées pour l'authentification.

##### 1. Sous module `token`

Ce sous module définit des classes pydantics pour la gestions des tokens :

- AccessToken :

  - access_token : **str**

  -  token_type : **str**

- RefreshToken :

  - refresh_token : **str**

  - token_type : **str**

- Token :

  - access_token : **str**

  - refresh_token : **str**

  - token_type : **str**


##### 2. Sous module `authenticate`

ce sous module définit les classes et fonctions utilisées pour l'authentification

**`Classe Authentication`**: classe principale pour gérer l'authentification

**Attributs**

- `__oauth2_scheme` : définit le schéma d'authentication

- `User` : le modèle d'utilisateur SQLAlchemy

- `UserCreateModel` : le modèle pydantic pour la création d'utilisateur

- `UserUpdateModel` : le modèle pydantic pour la mise à jour d'utilisateur

- `UserPydanticModel` : le modèle pydantic pour lire un utilisateur

- `UserLoginRequestModel` : le modèle pydantic la connexion d'utilisateur

- `__secret_key` : **str** [une clé secrète générer par défaut]

- `__algorithms` : **List[str]**un tableau d'algorithm [par défaut **[`HS256`]**]

- `REFRESH_TOKEN_EXPIRE_DAYS` : **int**

- `ACCESS_TOKEN_EXPIRE_MINUTES` : **int**

- `__session_factory` : **sessionmaker[Session]**

**methodes**

- `__init__` :

  - **paramètres** :

    - database_username : **str**

    - database_password : **str**

    - connector : **str**

    - database_name : **str**

    - server : **str**


- `get_session` : retourne une session

  - **sortie** : `Session`

- `is_authorized` : verifie si un utilisateur a un privilège

  - **paramètres** :

    - user_id : **int**

    - privilege_id : **int**

  - **sortie** : **bool**

-  `authenticate_user`

  - **paramètres** :

    - password : **str**

    - username_or_email : **str**

   - session : **Optional[Session]**

  - **sortie** : **User**

-  `create_access_token`

  - **paramètres** :

    - data : **dict**

    - expires_delta : **timedelta**

  - **sortie** : **AccessToken**

-  `create_refresh_token`

  - **paramètres** :

    - data : **dict**

    - expires_delta : **timedelta**

  - **sortie** : **RefreshToken**

-  `get_access_token` : retourne le token d'accès de l'utilisateur actuellement authentifié .

  - **sortie** : **str**

-  `get_current_user` : retourne  l'utilisateur actuellement authentifié .

  - **sortie** : **User**

-  `validate_token` : valide le token et retourne un payload

  - **paramètres** :

    - token : **str**

  - **sortie** : **dict[str,any]**

- `refresh_token`

  - **paramètres** :

    - refresh_token_datat : **RefreshToken**

  - **sortie** : **AccessToken**

#### Module `authorization`

Ce module contient des classes et des fonctions utilisées pour l'autorisation.

##### Sous module `role_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Role .

`Role`:

- id : **Column(Integer)**

- name : **Column(String)**

- normalized_name : **Column(String)** automatique à l'ajout de name

- is_active : **Column(Boolean)**

`RoleCreateModel` :

- name : **str**

`RoleUpdateModel`

- name : **Optional[str]**

- is_active : **Optional[bool]**

`RolePydanticModel` :

- id : **int**

- name : **str**

- normalizedName : **str**

- is_active : **bool**

- privileges : **List[MetaPrivilege]**

##### Sous module `privilege_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Privilege .

- sous module `privilege_model`

- id : **Column(Integer)**

- name : **Column(String)**

- normalized_name : **Column(String)** automatique à l'ajout de name

- is_active : **Column(Boolean)**

- description : **Column(String)**

`PrivilegeCreateModel`:

- name : **str**

- description : **str**

- role_id : **int**

`PrivilegeUpdateModel` :

- name : **Optional[str]**

- description : **Optional[str]**

- role_id : **Optional[int]**

`PrivilegePydanticModel` :

- id : **int**

- name : **str**

- normalizedName : **str**

- description : **str**

- is_active : **str**

- role_id : **int**

`MetaPrivilege` :

- id : **int**

- normalizedName : **str**

- description : **str**

- is_active : **str**

#### Module `middleware`

Ce module regroupe toute la gestion des middelwares

##### Sous module `models`

Ce sous module définit les modèles de Log : `LoggerMiddlewareModel` et `LoggerMiddlewarePydanticModel` pour la validation Pydantic
`LoggerMiddlewareModel`:
**Attributs prédéfinis**:

- id : **Column(Integer)**

- status_code :**Column(Integer)**

- method : **Column(String)**

- url : **Column(String)**

- error_message : **Column(Text)**

- date_created : **Column(DateTime)**

- process_time : **Column(Numeric)**

- remote_adress: **Column(String)**


`LoggerMiddlewarePydanticModel`:
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

  - **paramètres** :

    - LoggerMiddlewareModel : définit le modèle de Log

    - session_factory : **sessionmaker[Session]**

    - manager : **ConnectionManager**


##### Sous module `error_middleware`

Ce sous module définit les middelwares d'erreurs

- Class **`ErrorMiddleware`**

  - **paramètres** :

    - LoggerMiddlewareModel : définit le modèle de Log

    - session_factory : **sessionmaker[Session]**

    - manager : **ConnectionManager**

##### Sous module crud_middelware

ce sous module définit les methodes pour sauvegarder les logs .

- **`save_log`** : enregistre les logs

  - **paramètres**:

    - **request** : Request

    - **LoggerMiddelewareModel**

    - **db** : Session

    - **call_next**: Optional

    - **error** : Optional[str]

    - **response** : Optional[Response]

    - **manager**: Optional[ConnectionManager]

- **paramètres**: **Response**


- **`get_response_and_process_time`** : renvoie le temps de la requete et la reponse .

  - **paramètres**:

    - **request**: Request

    - **call_next**:callable

    - **response** : Response

    - **call_next**: Optional

- **paramètres**: [ **response** , **process_time** ]


- **`read_response_body`** : **renvoie  une chaine de caractère contenant la partie du detail du body si elle existe du corps de la requête**

  - **paramètres**:

    - **response** : Response

- **paramètres**: **str**


- **`recreate_async_iterator`** : **recree un nouvel itérateur pour la requete**

  - `paramètres`:

    - **body** : bytes


#### Module `user`

Ce module comporte toute la gestion des utilisateurs

##### Sous module `models`

Ce sous module comporte tous les models pour l'entité utilisateur .

class **`User`**

`Attributs`:

- id : **Column(Integer)**

- email : **Column(String)**

- username : **Column(String)**

- password : **Column(String)**

- lastname : **Column(String)**

- date_created : **Column(DateTime)**

- date_updated : **Column(DateTime)**

- is_active : **Column(Boolean)**

- attempt_login : **Column(Integer)**


`Methodes` :

- `try_login` :
  tente de connecter un utilisateur et mets à jour attempt_login en fonction .

  - **paramètres** :

    - is_success : **bool**

  - **sortie** : **bool**

- `set_password` : permet de modifier le mot de passe .

  - **paramètres** :

    - password : **str**

  - **sortie** : **None**


- `check_password` : permet de vérifier le mot de passe.

  - **paramètres** :

    - password : **str**

  - **sortie** : **bool**



Models pydantics pour la validations :


- `UserCreateModel`
  - email  : **str**

  - username : **str**

  - lastname : **str**

  - firstname : **str**

  - password : **str**



- `UserUpdateModel`
  -  email: **Optional[str]**

  -  username: **Optional[str]**

  -  lastname: **Optional[str]**

  -  firstname: **Optional[str]**

  -  is_active: **Optional[bool]**

  -  password: **Optional[str]**


class **`UserPydanticModel`**

`Attributs`:

- id : **int**

- email : **str**

- username : **str**

- password : **str**

- lastname : **str**

- date_created : **datetime**

- is_active : **bool**

- attempt_login : **int**


- `UserLoginRequestModel` :

  - username : **Optional[str]**

  - password : **str**

  - email : **Optional[str]**

 - **property** : username_or_email

- `UserChangePasswordRequestMode` :

  - current_password : **str**

  - new_password : **str**

  - username : **Optional[str]**

  - password : **str**

  - email : **Optional[str]**


#### Module `websocket`

Ce module comporte certaines classes et methodes pour interagir avec des websockets

##### Sous module `connectionManager`

Contient la classe ConnectionManager pour gérer une connextion avec un websocket .

**methodes**:

- **connect** : permet de  connecter un websocket au manager

  - **paramètres:**

    - websocket : WebSocket

- **disconnect** : permet de déconnecter un websocket

  - **paramètres:**

    - websocket : WebSocket

- **send_message**  : permet d'envoyer un message

  - **paramètres:**

    - message : **str**


#### Module `crud`

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des cruds.

##### Sous module `crud_forgery`

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

  - **sortie** : **Reponse avec status code 204**

##### Sous module user_crud_forgery
Ce sous module définit une classe UserCrudForgery hérité de CrudForgery pour offire un crud personnalisé pour l'utilisateur .

**Méthodes** :

- `__init__`

  - **paramètres** :

    - authentication : Authentication

- `change_password`  : méthode pour changer le mot de passe d'un utilisateur

  - **paramètres** :

    -  username_or_email : **str**

    -  current_password : **str**

    -  new_passowrd : **str**

  - **sortie** : **Reponse avec status code 204**

- `is_unique`  : méthode pour vérifier si l'email ou le username est unique .

  - **paramètres** :

    -  sub : **str**

  - **sortie** : **bool**

- `read_one`  : méthode lire un utilisateur à partir de son id , son email ou de son username .

  - **paramètres** :

    -  credential : **str|int**
    -  db : Optional[Session] = None

  - **sortie** : **bool**




#### Module `router`

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des router.

##### Sous module `route_config`

Ce sous module comporte la classe RouteConfig pour configurer un CustomRouterProvider .

`RouteConfig`

- `__init__` :
  - **paramètres**:
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

  - **paramètres**:

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

  - **paramètres**: **APIRouter**

- **`get_protected_router`** : renvoie un router avec la configuration de `AUTH_CONFIG`

  - **paramètres**: **APIRouter**

- **`initialize_router`** : renvoie un router avec une configuration personnalisée .
  - **paramètres**:
    - `init_data`: **List[RouteConfig]**
  - **paramètres**: **APIRouter**
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
