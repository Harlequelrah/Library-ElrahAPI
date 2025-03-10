# I - **`Description`**

![Logo](Elrah.png)

Passioné par la programmation et le développement avec python je me lance dans la création progressive d'une bibliothèque personnalisée ou framework basé sur pour `FASTAPI` m'ameliorer , devenir plus productif et partager mon expertise .

# II - **`Installation`**

- **Avec Github :**
  ```bash
  git clone https://github.com/Harlequelrah/Library-ElrahAPI

  cd Library-ElrahAPI

  pip install -e ./elrahapi
  ```
- **Avec pip :**

  ```bash
  pip install elrahapi
  ```

# III - **`Lancez vous ! `**

## 1. `Quelques recommandations` :

- **myproject** designe le nom de votre projet .

- **myapp** designe le nom d'une application .

- Après la creation du projet configurer l'environnement .

- Après chaque creation d'application faire les changements appropriés dans chaque fichier de l'application .


## 2. `créer un projet`

```bash
   elrahapi startproject myproject
```

## 3. `configurer l'environnement`

- Ouvrer le fichier .env et configurer le

- Configurer alembic au besoin :

  - Configurer le alembic.ini  par son paramètre `sqlalchemy.url`

  - Configurer le alembic/env.py  :

    - Ajouter l'import : from myproject.settings.models_metadata import target_metadata

    - Passer les metadata à target_metadata : target_metadata=target_metadata

- Configurer le main.py en decommentant les lignes commentées au besoin

## 4. `Demarrer le projet `

- Accéder au repertoire du projet :
```bash
  cd myproject
```

- Démarrer le serveur  :

```bash
  elrahapi run
```

## 5. `Créer une application`

- Génerer l'application
```bash
  elrahapi startapp myapp
```

- Modifier les lignes commentées au besoin

## 6. `Configurer une application`

- Ouvrer le dossier myproject/myapp

### 6.1.  `Définir les models de l'application`

- Créer les models SQLAlchemy dans models.py

- Créer les models Pydantic dans schemas.py

- Créer les meta models dans meta_models.py

- Importer la variable metadata de l'application dans le settings/models_metadata.py


### 6.2 `Créer les cruds`

- Configurer le CrudForgery dans cruds.py

### 6.3 `Configurer le fournisseur de routage de l'application`

- Configurer le CustomRouterProvider dans router.py
comme suite :

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    PydanticModel=EntityPydanticModel,
    crud=myapp_crud
)
```
**Note** : `Des roles et des privileges peuvent lui etre ajoutés directement .`

### 6.4 `Configurer un router`

**Notes** :

- `le paramètre exclude_routes_name pourra éventuellement être passé aux méthodes suivantes pour exclure certaines routes.`

- `le paramètre authorizations pourra éventuellement être passé aux méthodes de routes protégées.`

- Créér des configurations de routes

```python
  custom_init_data: List[RouteConfig] = [
    RouteConfig(route_name=DefaultRoutesName.CREATE, is_activated=True),
    RouteConfig(route_name=DefaultRoutesName.READ_ONE, is_activated=True),
    RouteConfig(route_name=DefaultRoutesName.READ_ALL, is_activated=True),
    RouteConfig(route_name=DefaultRoutesName.UPDATE, is_activated=True, is_protected=True),
    RouteConfig(route_name=DefaultRoutesName.DELETE, is_activated=True, is_protected=True),
]
```


- Création des configurations d'authorizations de routes

```python
  custom_authorizations : List[AuthorizationConfig] = [
  AuthorizationConfig(route_name=DefaultRoutesName.DELETE,roles=["ADMIN","MANAGER"]),
  AuthorizationConfig(route_name=DefaultRoutesName.UPDATE,privileges=["CAN_UPDATE_ENTITY"]
  ]
```
- Créér un router préconfiguré sans authentification

```python
  app_myapp = router_provider.get_public_router()
```

- Créér un router préconfiguré avec authentification

```python
  app_myapp = router_provider.get_protected_router(
  authorizations=custom_authorizations
  )
```

- Créer un router avec configuration et des routes publiques
```python
  app_myapp = router_provider.get_custom_public_router(
    init_data= custom_init_data ,
    public_routes_name=[DefaultRoutesName.PATCH],
    exclude_routes_name=[DefaultRoutesName.READ_ONE]
  )
```

- Créer un router avec configuration et des routes protégées
```python
  app_myapp = router_provider.get_custom_protected_router(
    init_data= custom_init_data ,
    protected_routes_name=[DefaultRoutesName.COUNT],
  )
```

- Créer un router avec éventuellement une configuration et  avec des routes publics et protégés

```python
  app_myapp = router_provider.get_mixed_router(
    protected_routes_name=[DefaultRoutesName.COUNT],
    public_routes_name=[DefaultRoutesName.READ_ALL]
  )
```

**Note** : `Ajouter le router au main.py`

## 6. `Configurer générale d'une application utilisateur ou de logs`

- Générer l'application  :

  - Utilisateur :
```bash
  elrahapi generate appuser
```

  - Log :
```bash
  elrahapi generate loggerapp
```

- Modifier correctement les imports dans l'application

- Personnalisés au besoin les configurations de routes , cruds , models et schemas  les models

- Ajouter les metadata depuis user_models ou log_model  à settings/models_metadata

- Ajouter le router à myproject/main.py

## 7. `Configurer des logs`

Dans le fichier myproject/main.py du projet :

- Ajouter et configurer le middleware de logs :

```python
from elrahapi.middleware.log_middleware import LoggerMiddleware
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from myproject.loggerapp.log_model import Logger
from myproject.settings.database import  authentication
app = FastAPI()
app.include_router(app_logger)
app.add_middleware(
    ErrorHandlingMiddleware,
    LoggerMiddlewareModel=Logger,
    session_factory=authentication.session_factory
)
app.add_middleware(
    LoggerMiddleware,
    LoggerMiddlewareModel=Logger,
    session_factory=authentication.session_factory
)
```
**Note**: `Il est recommandé d'utiliser l'ordre des middlewares comme dans l'exemple et de configurer aussi le middleware d'erreur pour avoir les logs des erreurs aussi.`

## 8. `Utilisation de  ConnectionManager`

```python
from elrahapi.websocket.connectionManager import ConnectionManager
from fastapi import (
    FastAPI,
    WebSocketDisconnect,
    WebSocket,
)
app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/notifications")
async def websocket_notification(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
```

**Note**: `Il est aussi possible d'ajouter un objet de type ConnectionManager aux middlewares pour notifier les erreurs dans le projet`

# IV - **`Documentation`**

Ce package contient plusieurs modules utiles pour accélérer et modulariser le dévéloppement avec FASTAPI. Voici un aperçu de leurs fonctionnalités.

## 1. `Commandes`

### 1.1. **Commande de création du projet**

Cette commande permet de générer un projet FASTAPI avec une archictecture définie

```bash
elrahapi startproject nomduprojet
```

**`architecture`:**

```
nomduprojet/
├── __init__.py
├── .gitignore
├── alembic/
├── README.md
├── .env
├── alembic.ini
├── requirements.txt
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
### 1.2. **Commande de lancement de l'application**
```bash
  elrahapi run
```

### 1.3. **Commande de génération d'une application**

Cette commande permet de créer une application dans le projet

```bash
  elrahapi startapp sqlapp
```

**`architecture`:**

```
sqlapp/
├── __init__.py
├── cruds.py
├── models.py
├── router.py
├── schemas.py
├── utils.py
├── meta_models.py
```

### 1.4. **Commande génération d'une application utilisateur**

Cette commande permet de créer une application utilisateur

```bash
elrahapi generate  userapp
```

**`architecture`:**

```
userapp/
├── __init__.py
├── user_cruds.py
├── user_models.py
├── user_router_providers.py
├── user_routers.py
├── user_schemas.py
```

### 1.5. **Commande de génération d'une application de log**

Cette commande permet de créer une application de log

```bash
elrahapi generate loggerapp
```

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

## 2. `Modules`

### 2.1. **Module `exception`**

Ce module contient des exceptions personnalisées utilisés dans cette bibliothèque

#### 2.1.1. Sous module `auth_exception`

ce sous module dispose de quelques variables d'exceptions prédéfinies liés à l'authentification

- `INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de paramètres d'authentification invalides .

- `INACTIVE_USER_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de compte utilisateur inactive .

- `INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION` : exception personnalisée lorsqu'un utilisateur n'a pas les permissions suffisantes pour acceder à une ressource .

#### 2.1.2. Sous module `exceptions_utils`

ce sous module contient des fonction utilitaires pour les exceptions

- `raise_custom_http_exception` : lève une erreur CustomHttpException

  - **paramètres** :

    - `status_code` : **int**

    - `detail` : **str**

#### 2.1.3. Sous module custom_http_exception

- `CustomHttpException` : génère une exception personnalisé qui definit une exception de type HTTPExeption.

### 2.2. **Module `utility`**

Ce module contient des utilitaires .

#### 2.2.1. Sous module `utils`

Ce sous module contient des quelques fonctions utiles .

- `update_entity` : mets à jour les champs d'une entité objet .

  - **paramètres** :

    - existing_entity : l'entité existante à mettre à jour.

    - update_entity : l'entité pour mettre : l'entité pour la mise à jour .

  - **sortie** : **existing_entity**

- `validate_value_type` : permet valider une valeur pour s'assurer qu'il est conforme à son type.

  - **paramètres** :

    - value : la valeur à vérifier.

  - **sortie** : **value**

  - **utilisation** :

  ```python
  myvalue= validate_value_type("True") # retourne True
  ```

- **create_database_if_not_exists** : créer la base de donnée si elle n'existe pas .

  - **paramètres** :

    - database_url : **str** , l'url de la base de donnée dans le nom de la base de donnée .

    - database_name : **str** , le nom de la base de donnée

- **map_list_to** : map une liste d'objet d'une classe pydantic en une liste d'objet d'une classe  sqlalchemy .

  - **paramètres** :

    - obj_list : **list** , la liste d'objet à mapper

    - obj_sqlalchemy_class : **type** , la classe sqlalchemy

    - obj_pydantic_class : **type** , la classe pydantic

### 2.3. **Module `authentication`**

Ce module contient des classes et des fonctions utilisées pour l'authentification.

#### 2.3.1. Sous module `token`

Ce sous module définit des classes pydantics pour la gestions des tokens :

- AccessToken :

  - access_token : **str**

  - token_type : **str**

- RefreshToken :

  - refresh_token : **str**

  - token_type : **str**

- Token :

  - access_token : **str**

  - refresh_token : **str**

  - token_type : **str**

#### 2.3.2 Sous module `authenticate`

ce sous module définit les classes et fonctions utilisées pour l'authentification

**`Classe Authentication`**: classe principale pour gérer l'authentification

**Attributs**

- `TOKEN_URL` : définit l'url du schéma d'authentication

- `OAUTH2_SCHEME` : définit le schéma d'authentication

- `User` : le modèle d'utilisateur SQLAlchemy

- `UserCreateModel` : le modèle pydantic pour la création d'utilisateur

- `UserUpdateModel` : le modèle pydantic pour la mise à jour  totale d'utilisateur

- `UserPatchModel` : le modèle pydantic pour la mise à jour partielle un utilisateur

- `UserPydanticModel` : le modèle pydantic pour lire un utilisateur




- `REFRESH_TOKEN_EXPIRATION` : **int** , l'expiration du token de rafraichissement en millsecondes .

- `ACCESS_TOKEN_EXPIRATION` : **int** , l'expiration du token d'accès en millsecondes .


**methodes**

- `__init__` :

  - **paramètres** :

    - database_username : **str**

    - database_password : **str**

    - connector : **str**

    - server : **str**

    - database_name : **str**

    - secret_key : **Optional[str]**

    - algorithm : **Optional[str]**

    - access_token_expiration : **Optional[int]**

    - refresh_token_expiration : **Optional[int]**

    - session_factory : sessionmaker[Session]

- `get_session` : retourne une session

  - **sortie** : `Session`



- `authenticate_user` : authentifie un utilisateur

  - **paramètres** :

    - password : **str**

    - username_or_email : **str**

    - session : **Optional[Session]**

  - **sortie** : **User**

- `create_access_token` : créer un token d'acces

  - **paramètres** :

    - data : **dict**

    - expires_delta : **timedelta**

  - **sortie** : **AccessToken**

- `create_refresh_token` : créer un token de rafraichissement

  - **paramètres** :

    - data : **dict**

    - expires_delta : **timedelta**

  - **sortie** : **RefreshToken**

- `get_access_token` : retourne le token d'accès de l'utilisateur actuellement authentifié .

  - **sortie** : **str**

- `get_current_user` : retourne l'utilisateur actuellement authentifié .

  - **sortie** : **User**

- `validate_token` : valide le token et retourne un payload

  - **paramètres** :

    - token : **str**

  - **sortie** : **dict[str,any]**

- `refresh_token` : rafraichi un token d'acces par un token de rafraichissement

  - **paramètres** :

    - refresh_token_datat : **RefreshToken**

  - **sortie** : **AccessToken**

- `check_authorization` : vérifie des authorizations suivant des roles ou privilèges en retournant un objet **callable** qui sera utilisé comme dépendence

  - **paramètres** :

    - privilege_name: **Optional[List[str]]**

    - roles_name : **Optional[List[str]]**

  - **sortie** : **callable**

- `get_user_by_sub` : retourne un utilisateur à partir de son username ou email

  - **paramètres** :

    - username_or_email : **str**

    - db : **Session**

  - **sortie** : **User**

### 2.4. **Module `authorization`**

Ce module contient des classes et des fonctions utilisées pour l'autorisation.

#### 2.4.1. Sous module `meta_model`

Ce sous module contient des models Meta pour définir les models liés à l'authorization et pour lire partiellement des données .

- `MetaAuthorization` : classe pour définir les models SQLAlchemy Role et Privilege

  - id : **Column(Integer)**

  - name : **Column(String)**

  - normalizedName : **Column(String)** [automatique à l'ajout de name]

  - description : **Column(String)**

- `MetaAuthorizationBaseModel(BaseModel)` : classe pour définir les Models Meta pour Role et Privilege .

  - id : **int**

  - normalizedName : **str**

  - is_active : **bool**

- `MetaAuthorizationPydanticModel(MetaAuthorizationModel)` ; classe pour définir les Models Pydantic complet pour Role et Privilege.

- name : **str**

- `MetaUserPrivilegeModel(BaseModel)` :

  - privilege_id : **int**

  - is_active : **bool**


#### 2.4.2 Sous module `role_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Role .

- `RoleModel(MetaAuthorization)`

- `RoleBaseModel(BaseModel)` :

  - name : **str**

  - description : **str**

- `RoleCreateModel(RoleBaseModel)` :

  - is_active : **Optional[bool]** , default: True


- `RoleUpdateModel(RoleBaseModel)` :

  - is_active : **bool**

- `RolePatchModel(BaseModel)`

  - name : **Optional[str]**

  - description : **Optional[str]**

  - is_active : **Optional[bool]**


- `RolePydanticModel(MetaAuthorizationPydanticModel)` :

  - role_privileges : **List[MetaAuthorizationBaseModel]**

#### 2.4.3. Sous module `privilege_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Privilege .

- `PrivilegeModel(MetaAuthorization)`

- `PrivilegeBaseModel(BaseModel)`

  - name : **str**

  - description : **str**


- `PrivilegeCreateModel(PrivilegeBaseModel)`:

  - is_active : Optional[bool] , default : True

- `PrivilegeUpdateModel(RoleBaseModel)` :

  - is_active : **bool**

- `PrivilegePatchModel(BaseModel)` :

  - name : **Optional[str]**

  - description : **Optional[str]**

  - is_active : **Optional[bool]**

- `PrivilegePydanticModel(MetaAuthorizationPydanticModel)` :

  - privilege_roles : **Optional[List[MetaAuthorizationBaseModel]]**

  - privilege_users : **Optional[List[MetaPrivilegeUsers]]**

#### 2.4.4. Sous module `role_privilege_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité RolePrivilege .

- `RolePrivilegeModel`

  - id : **Column(Integer)**

  - role_id : **Column(Integer)**

  - privilege_id : **Column(Integer)**

- `RolePrivilegeCreateModel(BaseModel)`

  - role_id : **int**

  - privilege_id : **int**

- `RolePrivilegeUpdateModel(BaseModel)`

  - role_id : **int**

  - privilege_id : **int**


- `RolePrivilegePatchModel(BaseModel)`

  - role_id : **Optional[int]**

  - privilege_id : **Optional[int]**

- `RolePrivilegePydanticModel(RolePrivilegeCreateModel)`
  - id : **int**

#### 2.4.5. Sous module `user_privilege_model`

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité UserPrivilege .

- `UserPrivilegeModel`

  - id : **Column(Integer)**

  - role_id : **Column(Integer)**

  - privilege_id : **Column(Integer)**

- `UserPrivilegeCreateModel(BaseModel)`

  - user_id : **int**

  - privilege_id : **int**

  - is_active : **Optional[bool]** , default : True

- `UserPrivilegeUpdateModel(BaseModel)`

  - role_id : **int**

  - privilege_id : **int**

  - is_active : **bool**

- `UserPrivilegePatchModel(BaseModel)`

  - role_id : **Optional[int]**

  - privilege_id : **Optional[int]**

  - is_active : **Optional[bool]**

- `UserPrivilegePydanticModel(UserPrivilegeCreateModel)`
  - id : **int**



### 2.5. **Module `middleware`**

Ce module regroupe toute la gestion des middelwares

##### 2.5.1. Sous module `models`

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

##### 2.5.2 Sous module `log_middleware`

Ce sous module définit les middelwares de loggins

- Class **`LoggerMiddleware`**

  - **paramètres** :

    - LoggerMiddlewareModel : définit le modèle de Log

    - session_factory : **sessionmaker[Session]**

    - manager : **ConnectionManager**

##### 2.5.3. Sous module `error_middleware`

Ce sous module définit les middelwares d'erreurs

- Class **`ErrorMiddleware`**

  - **paramètres** :

    - LoggerMiddlewareModel : définit le modèle de Log

    - session_factory : **sessionmaker[Session]**

    - manager : **ConnectionManager**

##### 2.5.4. Sous module crud_middelware

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

- **`read_response_body`** : **renvoie une chaine de caractère contenant la partie du detail du body si elle existe du corps de la requête**

  - **paramètres**:

    - **response** : Response

- **paramètres**: **str**

- **`recreate_async_iterator`** : **recree un nouvel itérateur pour la requete**

  - `paramètres`:

    - **body** : bytes

### 2.6. **Module `user`**

Ce module comporte toute la gestion des utilisateurs

##### 2.6.1. Sous module `models`

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

- role_id : **Column(Integer)**

- MAX_ATTEMPT_LOGIN = 3

- PasswordHasher

**`Methodes`** :

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

- `has_role` : permet de vérifier si l'utilisateur a un role

  - **paramètres** :

    - roles_name : **List[str]**

  - **sortie** : **bool**

- `has_privilege` : permet de vérifier si l'utilisateur a un privilege

  - **paramètres** :

    - privilege_name : **str**

  - **sortie** : **bool**

- `UserPrivilegeModel`

  - id : **Column(Integer)**

  - user_id : **Column(Integer)**

  - privilege_id : **Column(Integer)**

  - is_active : **Column(Integer)**

**`Models pydantics pour la validations`** :

- `UserBaseModel`

  - email : **str**

  - username : **str**

  - lastname : **str**

  - firstname : **str**

- `UserCreateModel(UserBaseModel)`

  - password : **str**

  - role_id : **Optional[int]**

- `UserUpdateModel`

  - email: **Optional[str]**

  - username: **Optional[str]**

  - lastname: **Optional[str]**

  - firstname: **Optional[str]**

  - is_active: **Optional[bool]**

  - password: **Optional[str]**

  - role_id : **Optional[int]**

- **`UserPydanticModel(UserBaseModel)`**

  - id : **int**

  - date_created : **datetime**

  - date_updated : **Optional[datetime]**

  - is_active : **bool**

  - attempt_login : **int**

  - role : **Optional[MetaAuthorizationBaseModel]**

  - user_privileges : **Optional[List[MetaUserPrivilegeModel]]**




- `UserRequestModel` :

  - username : **Optional[str]**

  - email : **Optional[str]**

  - username_or_email : @property **str|None**

- `UserLoginRequestModel(UserRequestModel)` :

  - password : **str**

- `UserChangePasswordRequestModel(UserRequestModel)` :

  - current_password : **str**

  - new_password : **str**

### 2.7. **Module `websocket`**

Ce module comporte certaines classes et methodes pour interagir avec des websockets

##### 2.7.1. Sous module `connectionManager`

Contient la classe ConnectionManager pour gérer une connextion avec un websocket .

**methodes**:

- **connect** : permet de connecter un websocket au manager

  - **paramètres:**

    - websocket : WebSocket

- **disconnect** : permet de déconnecter un websocket

  - **paramètres:**

    - websocket : WebSocket

- **send_message** : permet d'envoyer un message

  - **paramètres:**

    - message : **str**

### 2.8. **Module `crud`**

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des cruds.

##### 2.8.1. Sous module `crud_forgery`

Ce sous module comporte la classe CrudForgery pour générer des cruds de base .

**`CrudForgery`**:

- **`__init__`** :

  - **paramètres** :

    - `entity_name`: **str**

    - `primary_key_name`: **str**

    - `authentication`: **Authentication**

    - `SQLAlchemyModel` : Le model SQLAlchemy

    - `CreatePydanticModel` : Le model Pydantic pour la création . **Optional**

    - `UpdatePydanticModel` : Le model Pydantic pour la mise à jour totale. **Optional**

    - `PatchPydanticModel` : Le model Pydantic pour la mise à jour partiel. **Optional**

- **``get_pk``** : retourne la colonne de clé primaire .


- **`create`** :

  - **paramètres** :

    - `create_ob`: **CreatePydanticModel**

  - **sortie** : **SQLAlchemyModel**

- **`bulk_create`** : permet de créer plusieurs entités

  - **paramètres** :

    - `create_ob_list`: **List[CreatePydanticModel]**

  - **sortie** : **List[SQLAlchemyModel]**


- **`count`** :

  - **sortie** : **int**


- **`read_all`** :

  - **paramètres** :

    - `filter`: **Optional[str]**

    - `value`: **Optional**

    - `skip`: **Optional[int]**

    - `limit`: **Optional[int]**

  - **sortie** : **List[SQLAlchemyModel]**


- **`read_one`** :

  - **paramètres** :

    - `pk`

    - `db`: **Optional[Session]** : pour utiliser la même session lors de update , patch et delete .

  - **sortie** : **SQLAlchemyModel**

- **`update`** :

  - **paramètres** :

    - `pk`

    - `update_obj`: **UpdatePydanticModel** | **PatchPydanticModel**

    - `is_full_updated`: **bool** , True pour une mise à jour totale et False pour une mise à jour partielle

  - **sortie** : **SQLAlchemyModel**

- **`delete`** :

  - **paramètres** :

    - `pk`

  - **sortie** : **Reponse avec status code 204**

- **`bulk_delete`** : permet de faire plusieurs suppression d'entités

  - **paramètres** :

    - `pk_list`: **BulkDeleteModel**

  - **sortie** : **Reponse avec status code 204**


##### 2.8.2 Sous module `user_crud_forgery`

Ce sous module définit une classe UserCrudForgery hérité de CrudForgery pour offire un crud personnalisé pour l'utilisateur .

**Méthodes** :

- `__init__`

  - **paramètres** :

    - authentication : Authentication

- `change_password` : méthode pour changer le mot de passe d'un utilisateur

  - **paramètres** :

    - username_or_email : **str**

    - current_password : **str**

    - new_passowrd : **str**

  - **sortie** : **Reponse avec status code 204**

- `is_unique` : méthode pour vérifier si l'email ou le username est unique .

  - **paramètres** :

    - sub : **str**

  - **sortie** : **bool**

- `read_one_user` : méthode lire un utilisateur à partir de son id , son email ou de son username .

  - **paramètres** :

    - credential : **str|int**
    - db : Optional[Session] = None

  - **sortie** : **bool**

##### 2.8.3. `Sous module bulk_models`

Ce sous module définit des classes pour les opérations en masse .

- **`BulkDeleteModel`** : pour la suppression multiple

    - delete_liste : **list**


### 2.9. **Module `router`**

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des routeurs.

##### 2.9.1. Sous module `route_config`

Ce sous module comporte la classe `RouteConfig` pour configurer un CustomRouterProvider et des classes utilitaires `DEFAULT_ROUTE_CONFIG` et `AuthorizationConfig` les configurations du routeur et des routes.

- **`DEFAULT_ROUTE_CONFIG`**

  - `__init__` :

    - **paramètres**

      - summary : **str**

      - description : **str**

- **`RouteConfig`**

- `__init__` :

  - **paramètres**:

    - `route_name`: **str**

    - `route_path`: **Optional[str]**

    - `summary`: **Optional[str]**

    - `description`: **Optional[str]**

    - `is_activated`: **bool** , default : `False`

    - `is_protected`: **bool** , default : `False`

    - `is_unlocked`: **Optional[bool]** , default : `False`

    - roles : **Optional[List[str]]**

    - privileges : **Optional[List[str]]**

- `get_authorizations` : retourne une liste de callable utilisable comme dépendance pour l'authorization

  - **paramètres** :

    - authentication : **Authentication**

  - **sortie** : **List[callable]**

- `validate_route_path` : permet de gérer les valeurs de route_path en fonction de route_name

  - **paramètres** :

    - route_name : **str**

    - route_path : **Optional[str]**

  - **sortie** : **str**

- **`AuthorizationConfig`**

  - `__init__` :

    - **paramètres** :

    - route_name : **DefaultRoutesName**

    - roles : **List[str]**

    - privileges : **List[str]**

##### 2.9.2 Sous module `route_namespace`

Ce sous module comporte des Constantes et classes réutilisables dans le contexte du routage .

- **`class TypeRoute `** : **(str,Enum)** , définit les types de routes : **PUBLIC** et **PROTECTED**

- **`DEFAULT_ROUTES_CONFIGS`** : **dict[DefaultRoutesName,DEFAULT,ROUTE_CONFIG]** , contient une configuration de base pour définir les routes par défaut .

- **`ROUTES_PUBLIC_CONFIG`** : **List[RouteConfig]** ,contient une liste de RouteConfig pour les routes par défaut publics ou non protégés .

- **`ROUTES_PROTECTED_CONFIG`**: **List[RouteConfig]** , contient une liste de RouteConfig pour les routes par défaut protégés .

- **`USER_AUTH_CONFIG`** : dict[DefaultRoutesName,RouteConfig]** , contient un dictionnaire de nom de route et de RouteConfig pour les routes par défaut liés à l'authentification d'un utilisateur .

- **`USER_AUTH_CONFIG_ROUTES`** : List[RouteConfig]** , contient toutes les RouteConfig définit par `USER_AUTH_CONFIG_ROUTES`

##### 2.9.3. Sous module `router_default_routes_name`

Ce sous module définit notament des classes contenant les définitions des noms des routes

- `DefaultRoutesName` : **(str,Enum)** , contient les définitions des noms des routes définies par le routage .

- `DEFAULT_DETAIL_ROUTES_NAME` : **list** , définit les routes de detail

- `DEFAULT_DETAIL_ROUTES_NAME` : **list** , définit les routes qui ne sont pas des routes de detail

##### 2.9.4. Sous module `route_provider`

Ce sous module comporte la classe CustomRouterProvider pour configurer un routeur .
`CustomRouterProvider`


- `__init__` :

  - **paramètres**:

    - `prefix`: **str**

    - `tags`: **List[str]**

    - `PydanticModel`: **type** , Model de reponse Pydantic

    - `crud` : **CrudForgery**

    - `roles` : **Optional[List[str]]**

    - `privileges `: **Optional[List[str]]**



- **`get_public_router`** : renvoie un router avec la configuration de `ROUTES_PUBLIC_CONFIG`

  - **paramètres**:

  - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

- **`get_protected_router`** : renvoie un routeur avec la configuration de `ROUTES_PROTECTED_AUTH_CONFIG`

  - **paramètres**:

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - authorizations: **Optional[List[AuthorizationConfig]]**


- **`get_custom_router_init_data`** :  renvoie une liste de configurations de routes personnalisés

  - **paramètres** :

    - init_data : **Optional[List[RouteConfig]]**

    - route_names : **Optional[List[DefaultRoutesName]]**

    - is_protected : **bool** , default: False

  - **sortie** :  List[RouteConfig]

- **`get_custom_public_router`** : retourne un routeur public personnalisée

  - **paramètres** :

    - init_data : **Optional[List[RouteConfig]]**

    - public_routes_name : **Optional[List[DefaultRoutesName]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - **sortie** :  **APIRouter**


- **`get_custom_protected_router`** : retourne un routeur protégé personnalisée

  - **paramètres** :

    - init_data : **Optional[List[RouteConfig]]**

    - protected_routes_name : **Optional[List[DefaultRoutesName]]**

    - authorizations: **Optional[List[AuthorizationConfig]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - **sortie** :  **APIRouter**


- **`get_mixed_router`** : renvoie un routeur avec une configuration personnalisée entre routes publiques et protégées .

  - **paramètres**:

    - init_data: **Optional[List[RouteConfig]]**

    - public_routes_name : **Optional[List[DefaultRoutesName]]**

    - protected_routes_name : **Optional[List[DefaultRoutesName]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

- **`initialize_router`** : initialise un routeur avec une configuration .

  - **paramètres**:

    - init_data : **List[RouteConfig]**

    - authorizations: **Optional[List[AuthorizationConfig]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**


##### 2.9.5. Sous module `router_crud`

Ce sous module comporte certaines fonctions utilisées dans le cadre du routage .

- `exclude_route` : permet d'exclure des routes d'une liste de routes

  - **paramètres:**

    - routes : **List[RouteConfig]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - **sortie** : **List[RouteConfig]**

- `get_single_route` : permet d'avoir une configuration par défaut d'une route particulière .

  - **paramètres:**

    - route_name : **DefaultRoutesName**

    - type_route : **Optional[TypeRoute]= TypeRoute.PROTECTED**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - **sortie** : **RouteConfig**

- `initialize_dependencies` : permet d'initialiser les dépendances à passer à une route .

  - **paramètres:**

    - config : **RouteConfig**

    - authentication : **Authentication**

    - roles : **Optional[List[str]]**

    - privileges : **Optional[List[str]]**

  - **sortie** : **List[Depends]**


- `add_authorizations` : permet d'ajouter des authorizations à des configurations de routes.

  - **paramètres:**

    - route_config : **List[RouteConfig]**

    - authorizations : **List[AuthorizationConfig]**

  - **sortie** : **List[RouteConfig]**

- `format_init_data` : permet de preparer les configurations de routage en excluant des routes et en ajoutant les authorizations.

  - **paramètres:**

    - init_data : **List[RouteConfig]**

    - authorizations : **List[AuthorizationConfig]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - **sortie** : **List[RouteConfig]**


##### 2.9.6. Sous module `user_router_provider`

ce sous module continent UserRouterProvider qui hérite de CustomRouterProvider , personnalisé pour l'utilisateur .

- `__init__` :

  - **paramètres** :

    - crud: **UserCrudForgery**

    - prefix : **str**

    - tags : **List[str]**

    - roles : **Optional[List[str]]**

    - privileges : **Optional[List[str]]**

#### 2.10. Module `security`
Ce module définit la gestion de la sécurité .

##### 2.10.1 Sous module `secret`
Ce sous module définit des utilitaires pour la sécurité

- `ALGORITHMS_KEY_SIZES` : **dict[str,int]** , un dictionnaire d'algorithmes et de longueur de clé pour définir aléatoirement ces paramètres si ils ne sont pas fournis

- `ALGORITHMS` : **List[str]** , une liste des algorithms de **ALGORITHMS_KEY_SIZES**

- **define_algorithm_and_key** : permet de définir l'algorithme et la clé utilisée pour signé les tokens

  - **parametres** :

    - secret_key : **Optional[str]**

    - algorithm : **Optional[str]**

# V - **`Contact ou Support`**

Pour des questions ou du support, contactez-moi à maximeatsoudegbovi@gmail.com ou au (+228) 91 36 10 29.
