# IV - **`Documentation`**

Ce package contient plusieurs modules utiles pour accélérer et modulariser le dévéloppement avec FASTAPI. Voici un aperçu de leurs fonctionnalités.

# **1. `Commandes`**

## **1.1. `Commande de création du projet`**

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
├── .env.example
├── alembic.ini
├── requirements.txt
├── __main__.py
├── nomduprojet/
│   ├── __init__.py
│   ├── main.py
│   ├── settings/
│       ├── __init__.py
│       ├── database.py
│       ├── secret.py
│       ├── models_metadata.py
│       ├── auth/
│           ├── __init__.py
│           ├── configs.py
│           ├── models.py
│           ├── cruds.py
│           ├── meta_models.py
│           ├── routers.py
│           ├── schemas.py
│       ├── logger/
│           ├── __init__.py
│           ├── crud.py
│           ├── model.py
│           ├── router.py
│           ├── schema.py
```

## **1.2. `Commande de lancement de l'application`**

```bash
  elrahapi run
```

## **1.3. `Commande de génération d'une application`**

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

# **2. `Modules`**

## **2.1. Module `exception`**

Ce module contient des exceptions personnalisées utilisés dans cette bibliothèque

### **2.1.1. Sous module `auth_exception`**

ce sous module dispose de quelques variables d'exceptions prédéfinies liés à l'authentification

- `INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de paramètres d'authentification invalides .

- `INACTIVE_USER_CUSTOM_HTTP_EXCEPTION` : exception personnalisée de compte utilisateur inactive .

- `INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION` : exception personnalisée lorsqu'un utilisateur n'a pas les permissions suffisantes pour acceder à une ressource .

### **2.1.2. Sous module `exceptions_utils`**

ce sous module contient des fonction utilitaires pour les exceptions

- `raise_custom_http_exception` : lève une erreur CustomHttpException

  - **paramètres** :

    - `status_code` : **int**

    - `detail` : **str**

### **2.1.3. Sous module `custom_http_exception`**

- `CustomHttpException` : génère une exception personnalisé qui definit une exception de type HTTPExeption.

## **2.2. Module `utility`**

Ce module contient des utilitaires comme des fonctions , des variables , des classes ou des types.

### **2.2.1. Sous module `utils`**

Ce sous module contient des quelques fonctions utiles .

- `update_entity` : mets à jour les champs d'une entité objet .

  - **paramètres** :

    - existing_entity : l'entité existante à mettre à jour.

    - update_entity : **Type[BaseModel]** l'entité pour mettre : l'entité pour la mise à jour .

  - **sortie** : **existing_entity**

- `validate_value` : permet valider une valeur pour s'assurer qu'il est conforme à son type.

  - **paramètres** :

    - value : la valeur à vérifier.

  - **sortie** : **value**

  - **utilisation** :

  ```python
  myvalue= validate_value("True") # retourne True
  ```

- **create_database_if_not_exists** : créer la base de donnée si elle n'existe pas .

  - **paramètres** :

    - database_url : **str** , l'url de la base de donnée dans le nom de la base de donnée .

    - database_name : **str** , le nom de la base de donnée

- **map_list_to** : map une liste d'objet d'une classe pydantic en une liste d'objet d'une classe sqlalchemy .

  - **paramètres** :

    - obj_list : **List[BaseModel]** , la liste d'objet à mapper

    - obj_sqlalchemy_class : **type** , la classe sqlalchemy

    - obj_pydantic_class : **Type[BaseModel]** , la classe pydantic

### **2.2.2. Sous module `patterns`**

Ce sous module comporte quelques regex utilisables comme pattern dans les schemas de validations pydantic

- `*TELEPHONE_PATTERN*`

- `*URL_PATTERN*`

## **2.3. Module `authentication`**

Ce module contient des classes et des fonctions utilisées pour l'authentification.

### **2.3.1. Sous module `token`**

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

### **2.3.2 Sous module `authentication_namespace`**

Ce sous module comporte des variables , constantes et éléments réutilisable dans l'authentifiation

- `TOKEN_URL` : L'url d'authentification

- `OAUTH2_SCHEME` : Le schéma d'authentification définit sur `TOKEN_URL`

- `REFRESH_TOKEN_EXPIRATION`

- `ACCESS_TOKEN_EXPIRATION`

### **2.3.3 Sous module `authentication_manager`**

ce sous module définit les classes et fonctions utilisées pour l'authentification

**`Classe AuthenticationManager`**: classe principale pour gérer l'authentification

**Attributs**

- `authentication_models` : **CrudModels** , definit les classes et attributs pour l'authentification

- `refresh_token_expiration` : **int** , l'expiration du token de rafraichissement en millsecondes .

- `access_token_expiration` : **int** , l'expiration du token d'accès en millsecondes .

- `algorithm` : **str** , l'algorithm utilisé pour le cryptage des tokens

- `secret_key` : **str** , la clé secrète

- `session_manager` : **SessionManager** , le gestionnaire de session

- `database_username` : **str** , le nom d'utilisateur de base de donnée

- `database_password` : **str** , le mot de passe lié à `database_username`

- `connector` : **str** , le connecteur de base de donnée

- `server` : **str** , le serveur de base de donnée

- `database_name` : **str** , le nom de la base de donnée

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

- `get_session` : retourne une session

  - **sortie** : `Session`

- `authenticate_user` : authentifie un utilisateur

  - **paramètres** :

    - password : **str**

    - username_or_email : **str**

    - session : **Optional[Session]**

  - **sortie** : **authentication_models.sqlalchemy_model**

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

- `check_authorizations` : vérifie des authorizations suivant des roles ou privilèges en retournant un objet **callable** qui sera utilisé comme dépendence

  - **paramètres** :

    - privileges_name: **Optional[List[str]]**

    - roles_name : **Optional[List[str]]**

  - **sortie** : **callable**

- `check_authorization` : vérifie une autorisation suivant un role ou un privilège en retournant un objet **callable** qui sera utilisé comme dépendence

  - **paramètres** :

    - privilege_name: **str**

    - role_name : **str**

  - **sortie** : **callable**

- `get_user_by_sub` : retourne un utilisateur à partir de son username ou email

  - **paramètres** :

    - username_or_email : **str**

    - db : **Session**

  - **sortie** : **authentication_models.sqlalchemy_model**

- `is_unique` : méthode pour vérifier si l'email ou le username est unique .

  - **paramètres** :

    - sub : **str**

  - **sortie** : **bool**

- `read_one_user` : méthode lire un utilisateur à partir de son id , son email ou de son username .

  - **paramètres** :

    - credential : **str|int**
    - db : Optional[Session] = None

  - **sortie** : **authentication_models.sqlalchemy_model**

- `change_password` : méthode pour changer le mot de passe d'un utilisateur

  - **paramètres** :

    - username_or_email : **str**

    - current_password : **str**

    - new_passowrd : **str**

  - **sortie** : **Reponse avec status code 204**

- `change_user_state` : méthode pour changer le statut d'activité d'un utilisateur

  - **paramètres** :

    - pk : la clé primaire

  - **sortie** : **Reponse avec status code 204**

### **2.3.4 Sous module `authentication_router_provider`**

Ce sous module définit la classe AuthenticationRouterProvider pour gérer le routage de l'authentification

- **`Attributs`** :

  - authentication : **AuthenticationManager**

  - read_with_relations : **Optional[bool]**

  - roles : **Optional[List[str]]**

  - privileges : **Optional[List[str]]**

  - router : **APIRouter**

- **`Methodes`**

  - `__init__`

    - **parametres** :

      - authentication : **AuthenticationManager**

      - read_with_relations : **Optional[bool]**

      - roles : **Optional[List[str]]**

      - privileges : **Optional[List[str]]**

  - `get_auth_router ` : renvoie un router configurable pour l'authentification

    - **paramètres** :

      - init_data : **List[RouteConfig]** = `USER_AUTH_CONFIG_ROUTES`

      - authorizations : **Optional[List[AuthorizationConfig]]**

      - exclude_routes_name: **Optional[List[DefaultRoutesName]]**

      - response_model_configs : **Optional[List[ResponseModelConfig]]**

    - **sortie** : APIRouter

## **2.4. Module `authorization`**

Ce module contient des classes et des fonctions utilisées pour l'autorisation.

### 2.4.1. Sous module `base_meta_model`

Ce sous module contient des models Meta pour définir les models liés à l'authorization et pour lire partiellement des données .

- `MetaAuthorization` : classe pour définir les models SQLAlchemy Role et Privilege

  - id : **Column(Integer)**

  - name : **Column(String)**

  - normalizedName : **Column(String)** , dépend de name

  - description : **Column(String)**

  - is_active : **Column(Boolean)**

- `MetaAuthorizationBaseModel(BaseModel)` : classe pour définir les Models Meta pour Role et Privilege .

  - normalizedName : **str**

  - is_active : **bool**

- `MetaAuthorizationReadModel(MetaAuthorizationModel)` , classe pour définir les Models Pydantic complet pour Role et Privilege.

- name : **str**

- id : **int**

### **2.4.2. Sous module `role`**

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Role .

#### **2.4.2.1. Sous module `models`**

- `RoleModel(MetaAuthorization)`

#### **2.4.2.2. Sous module `schemas`**

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

- `RoleReadModel(MetaAuthorizationReadModel)`

- `RoleFullReadModel(MetaAuthorizationReadModel)`

  - role_privileges : **List[MetaAuthorizationBaseModel]**

  - role_users : **List[MetaRoleUsers]**

#### **2.4.2.3. Sous module `meta_models`**

- `MetaRoleUsers(BaseModel)`

  - user_id : int

  - is_active : int

### **2.4.3. Sous module `privilege`**

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité Privilege .

#### **2.4.3.1 Sous module `models`**

- `PrivilegeModel(MetaAuthorization)`

#### **2.4.3.2 Sous module `schemas`**

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

- `PrivilegeReadModel(MetaAuthorizationReadModel)`

- `PrivilegeFullReadModel(PrivilegeReadModel)` :

  - privilege_roles : **Optional[List[MetaAuthorizationBaseModel]]**

  - privilege_users : **Optional[List[MetaPrivilegeUsers]]**

#### **2.4.3.3 Sous module `meta_models`**

- `MetaPrivilegeUsers` :

  - `user_id`:int

  - `is_active` : **bool**

### **2.4.4. Sous module `role_privilege`**

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité RolePrivilege .

#### **2.4.4.1. Sous module `models`**

- `RolePrivilegeModel`

  - id : **Column(Integer)**

  - role_id : **Column(Integer)**

  - privilege_id : **Column(Integer)**

#### **2.4.4.2. Sous module `schemas`**

- `RolePrivilegeCreateModel(BaseModel)`

  - role_id : **int**

  - privilege_id : **int**

- `RolePrivilegeUpdateModel(BaseModel)`

  - role_id : **int**

  - privilege_id : **int**

- `RolePrivilegePatchModel(BaseModel)`

  - role_id : **Optional[int]**

  - privilege_id : **Optional[int]**

- `RolePrivilegeReadModel(RolePrivilegeCreateModel)`

  - id : **int**

- `RolePrivilegeFullReadModel(BaseModel)`

  - id : **int**

  - role : **MetaAuthorizationBaseModel**

  - privilege : **MetaAuthorizationBaseModel**

### **2.4.5. Sous module `user_privilege`**

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité UserPrivilege .

#### **2.4.5.1 Sous module `models`**

- `UserPrivilegeModel`

  - id : **Column(Integer)**

  - user_id : **Column(Integer)**

  - privilege_id : **Column(Integer)**

  - is_active : **Column(Boolean)**

#### **2.4.5.2 Sous module `schemas`**

- `UserPrivilegeCreateModel(BaseModel)`

  - user_id : **int**

  - privilege_id : **int**

  - is_active : **Optional[bool]** , default : True

- `UserPrivilegeUpdateModel(BaseModel)`

  - user_id : **int**

  - privilege_id : **int**

  - is_active : **bool**

- `UserPrivilegePatchModel(BaseModel)`

  - user_id : **Optional[int]**

  - privilege_id : **Optional[int]**

  - is_active : **Optional[bool]**

- `UserPrivilegeReadModel(UserPrivilegeCreateModel)`

  - id : **int**

- `UserPrivilegeFullReadModel(BaseModel)`

  - id : **int**

  - user : **UserBaseModel**

  - privilege : **MetaAuthorizationBaseModel**

#### **2.4.5.3. Sous module `meta_models`**

- `MetaUserPrivilegeModel(BaseModel)` :

  - privilege : **MetaAuthorizationBaseModel**

  - is_active : **bool**

### **2.4.6. Sous module `user_role`**

Ce sous module contient les models SQLAlchemy et classes pydantic pour l'entité UserRole .

#### **2.4.6.1 Sous module `models`**

- `UserRoleModel`

  - id : **Column(Integer)**

  - user_id : **Column(Integer)**

  - role_id : **Column(Integer)**

  - is_active : **Column(Boolean)**

#### **2.4.6.2 Sous module `schemas`**

- `UserRoleCreateModel(BaseModel)`

  - user_id : **int**

  - role_id : **int**

  - is_active : **Optional[bool]** , default : True

- `UserRoleUpdateModel(BaseModel)`

  - user_id : **int**

  - role_id : **int**

  - is_active : **bool**

- `UserRolePatchModel(BaseModel)`

  - user_id : **Optional[int]**

  - role_id : **Optional[int]**

  - is_active : **Optional[bool]**

- `UserRoleReadModel(UserRoleCreateModel)`

  - id : **int**

- `UserRoleReadModel(BaseModel)`

  - id : **int**

  - user : **UserBaseModel**

  - role : **MetaAuthorizationBaseModel**

  - is_active : **bool**

#### **2.4.6.3. Sous module `meta_models`**

- `MetaUserRoleModel(BaseModel)` :

  - role : **MetaAuthorizationBaseModel**

  - is_active : **bool**

## **2.5. Module `middleware`**

Ce module regroupe toute la gestion des middelwares .

### **2.5.1. Sous module `models`**

Ce sous module définit les modèles de Log : `LogModel` et `LogReadModel` pour la validation Pydantic

`LogModel`:

**Attributs prédéfinis**:

- id : **Column(Integer)**

- status_code :**Column(Integer)**

- method : **Column(String)**

- url : **Column(String)**

- error_message : **Column(Text)**

- date_created : **Column(DateTime)**

- process_time : **Column(Numeric)**

- remote_adress: **Column(String)**

`LogReadModel`:

**Attributs prédéfinis**:

- id : **int**

- status_code : **int**

- method : **str**

- url : **str**

- error_message : **str**

- date_created : **datetime**

- process_time : **float**

- remote_adress: **str**

### **2.5.2 Sous module `log_middleware`**

Ce sous module définit la classe **`LoggerMiddleware`** comme middleware de logs .

- `__init__`

  - **paramètres** :

    - LogModel

    - session_manager : **SessionManager**

    - websocket_manager : **ConnectionManager**

### **2.5.3. Sous module `error_middleware`**

Ce sous module définit la classe **`ErrorMiddleware`** comme middleware de gestion d'erreur .

- `__init__`

  - **paramètres** :

    - LogModel

    - session_manager : **SessionManager**

    - websocket_manager : **ConnectionManager**

### **2.5.4. Sous module `crud_middelware`**

ce sous module définit les methodes pour sauvegarder les logs .

- **`save_log`** : enregistre les logs

  - **paramètres**:

    - **request** : Request

    - **LogModel**

    - **db** : Session

    - **call_next**: Optional

    - **error** : Optional[str]

    - **response** : Optional[Response]

    - **websocket_manager**: Optional[ConnectionManager]

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

## 2.6. **Module `user`**

Ce module comporte toute la gestion des utilisateurs

### **2.6.1. Sous module `model`**

Ce sous module comporte le model `User` utilisé dans le système d'authentification.

**`UserModel`**

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

- MAX_ATTEMPT_LOGIN = None ou definit dans le fichier .env

- PasswordHasher

**`Methodes`** :

- `try_login` :
  tente de connecter un utilisateur et mets à jour attempt_login en fonction .

  - **paramètres** :

    - is_success : **bool**

  - **sortie** : **bool**

- `check_password` : permet de vérifier le mot de passe.

  - **paramètres** :

    - password : **str**

  - **sortie** : **bool**

- `change_user_state` : permet de changer le statut d'activité .

- `has_role` : permet de vérifier si l'utilisateur a un role

  - **paramètres** :

    - roles_name : **List[str]**

  - **sortie** : **bool**

- `has_permission`: permet de vérifier si l'utilisateur a un privilege dans ses privileges personnels

  - **paramètres** :

    - privilege_name : **str**

  - **sortie** : **bool**

- `has_privilege` : permet de vérifier si l'utilisateur a un privilege que ce soit par son role ou ses privileges personnels

  - **paramètres** :

    - privilege_name : **str**

  - **sortie** : **bool**

### **2.6.2. Sous module `schemas`**

Ce sous module rassemble les classes pydantics liées à `User` pour la validation

**`Models pydantics pour la validations`** :

- `UserBaseModel(BaseModel)`

  - email : **EmailStr**

  - username : **str**

  - lastname : **str**

  - firstname : **str**

- `UserCreateModel`

  - password : **str**

- `UserUpdateModel`

  - password : **str**

- `UserPatchModel`

  - email: **Optional[str]**

  - username: **Optional[str]**

  - lastname: **Optional[str]**

  - firstname: **Optional[str]**

- **`UserReadModel`**

  - id : **int**

  - date_created : **datetime**

  - date_updated : **Optional[datetime]**

  - is_active : **bool**

  - attempt_login : **int**

- **`UserFullReadModel(UserReadModel)`**

  - user_roles : **Optional[List[MetaUserRoleModel]]**

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

## **2.7. Module `websocket`**

Ce module comporte certaines classes et methodes pour interagir avec des websockets

### **2.7.1. Sous module `connectionManager`**

Contient la classe ConnectionManager pour gérer une connextion avec un websocket .

**methodes**:

- **connect** : permet de connecter un websocket au manager

  - **paramètres:**

    - websocket : WebSocket

- **disconnect** : permet de déconnecter un websocket

  - **paramètres:**

    - websocket : WebSocket

- **broadcast** : permet de diffuser un message

  - **paramètres:**

    - message : **str**

- **send_message** : permet d'envoyer un message

  - **paramètres:**

    - sender_websocket : WebSocket

    - message : **str**

### 2.8. **Module `crud`**

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des cruds.

### 2.8.1. **Sous module `crud_forgery`**

Ce sous module comporte la classe CrudForgery pour générer des cruds de base .

**`CrudForgery`**:

- **`__init__`** :

  - **paramètres** :

  - session_manager : **SessionManager**

  - crud_models : **CrudModels**

- **`create`** :

  - **paramètres** :

    - `create_ob`: **Type[BaseModel]** mais potentiellement **CreatePydanticModel**

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

    - `value`: **Optiona[Any]**

    - `second_model_filter`: **Optional[str]**

    - `second_model_filter_value`: **Optional[Any]**

    - `skip`: **Optional[int]**

    - `limit`: **Optional[int]**

    - `relation`: **Optional[Relationship]**

  - **sortie** : **List[SQLAlchemyModel]**

- **`read_one`** :

  - **paramètres** :

    - `pk` : **Any**

    - `db`: **Optional[Session]** : pour utiliser la même session lors de update , patch et delete .

  - **sortie** : **SQLAlchemyModel**

- **`update`** :

  - **paramètres** :

    - `pk`: **Any**

    - `update_obj`: : **Type[BaseModel]** mais potentiellement **UpdatePydanticModel** ou **PatchPydanticModel**

    - `is_full_update`: **bool** , True pour une mise à jour totale et False pour une mise à jour partielle

  - **sortie** : **SQLAlchemyModel**

- **`delete`** :

  - **paramètres** :

    - `pk` : **Any**

  - **sortie** : **Reponse avec status code 204**

- **`bulk_delete`** : permet de faire plusieurs suppression d'entités

  - **paramètres** :

    - `pk_list`: **BulkDeleteModel**

  - **sortie** : **Reponse avec status code 204**

### **2.8.2 Sous module `crud_models`**

Ce sous module definit CrudModels qui définit l'ensemble des classes et informations sur une entité

- `__init__`:

  - `entity_name`: **str**

  - `primary_key_name`: **str**

  - `SQLAlchemyModel` : **Type** , Le model SQLAlchemy de l'entité.

  - `CreateModel` : Optional[Type[BaseModel]] , Le model Pydantic pour la création .

  - `UpdateModel` : Optional[Type[BaseModel]] , Le model Pydantic pour la mise à jour totale.

  - `PatchModel` : Optional[Type[BaseModel]], Le model Pydantic pour la mise à jour partielle.

  - `ReadModel` : Optional[Type[BaseModel]], Le model Pydantic pour la lecture partielle.

  - `FullReadModel` : Optional[Type[BaseModel]], Le model Pydantic pour la lecture complète.

- **`get_pk`** : retourne la colonne de clé primaire .

- **`get_attr`** :

- **paramètre** : attr_name : **str**

- **sortie** : **Column**

### **2.8.3. `Sous module bulk_models`**

Ce sous module définit des classes pour les opérations en masse .

- **`BulkDeleteModel`** : pour la suppression multiple

  - delete_liste : **list**

## **2.9. Module `router`**

Ce module comporte des classes methodes et autres utilitaires pour automatiser la création des routeurs.

### **2.9.1. Sous module `route_config`**

Ce sous module comporte la classe `RouteConfig` pour configurer un CustomRouterProvider et des classes utilitaires `DEFAULT_ROUTE_CONFIG` , `ResponseModelConfig` et `AuthorizationConfig` les configurations du routeur et des routes.

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

    - `roles` : **Optional[List[str]]**

    - `privileges` : **Optional[List[str]]**

    - `dependencies` : **Optional[List[Callable[...,Any]]]**

    - `read_with_relations` : Optional[bool]

    - `response_model` : Optional[Any]

- `get_authorizations` : retourne une liste de callable utilisable comme dépendance pour l'authorization

  - **paramètres** :

    - authentication : **Authentication**

  - **sortie** : **List[callable]**

- `validate_route_path` : permet de gérer les valeurs de route_path en fonction de route_name

  - **paramètres** :

    - route_name : **DefaultRoutesName**

    - route_path : **Optional[str]**

  - **sortie** : **str**

- **`AuthorizationConfig`**

  - `__init__` :

    - **paramètres** :

    - route_name : **DefaultRoutesName**

    - roles : **List[str]**

    - privileges : **List[str]**

- **`ResponseModelConfig`**

  - `__init__` :

    - **paramètres** :

    - route_name : **DefaultRoutesName**

    - read_with_relations : **bool**

    - response_model : **Optional[Any]**

### **2.9.2 Sous module `route_namespace`**

Ce sous module comporte des Constantes et classes réutilisables dans le contexte du routage .

- **`class TypeRoute `** : **(str,Enum)** , définit les types de routes : **PUBLIC** et **PROTECTED**

- **`DEFAULT_ROUTES_CONFIGS`** : **dict[DefaultRoutesName,DEFAULT,ROUTE_CONFIG]** , contient une configuration de base pour définir les routes par défaut .

- **`ROUTES_PUBLIC_CONFIG`** : **List[RouteConfig]** ,contient une liste de RouteConfig pour les routes par défaut publics ou non protégés .

- **`ROUTES_PROTECTED_CONFIG`**: **List[RouteConfig]** , contient une liste de RouteConfig pour les routes par défaut protégés .

- **`USER_AUTH_CONFIG`** : **dict[DefaultRoutesName,RouteConfig]** , contient un dictionnaire de nom de route et de RouteConfig pour les routes par défaut liés à l'authentification d'un utilisateur .

- **`USER_AUTH_CONFIG_ROUTES`** : **List[RouteConfig]** , contient toutes les RouteConfig définit par `USER_AUTH_CONFIG_ROUTES`

### **2.9.3. Sous module `router_default_routes_name`**

Ce sous module définit notament des classes contenant les définitions des noms des routes

- `DefaultRoutesName` : **(str,Enum)** , contient les définitions des noms des routes définies par le routage .

- `DEFAULT_DETAIL_ROUTES_NAME` : **list** , définit les routes de detail

- `DEFAULT_DETAIL_ROUTES_NAME` : **list** , définit les routes qui ne sont pas des routes de detail

### **2.9.4. Sous module `router_provider`**

Ce sous module comporte la classe CustomRouterProvider pour configurer un routeur .
`CustomRouterProvider`

- `__init__` :

  - **paramètres**:

    - `prefix`: **str**

    - `tags`: **List[str]**

    - `authentication` : **Optional[AuthenticationManager]**

    - `crud` : **CrudForgery**

    - `roles` : **Optional[List[str]]**

    - `privileges `: **Optional[List[str]]**

    - `read_with_relations` : **bool**

    - `relations` : **Optional[List[Relationship]]**

- **`get_public_router`** : renvoie un router avec la configuration de `ROUTES_PUBLIC_CONFIG`

  - **paramètres**:

  - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

  - response_model_configs: Optional[List[ResponseModelConfig]]

- **`get_protected_router`** : renvoie un routeur avec la configuration de `ROUTES_PROTECTED_AUTH_CONFIG`

  - **paramètres**:

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - authorizations: **Optional[List[AuthorizationConfig]]**

    - response_model_configs: Optional[List[ResponseModelConfig]]

- **`get_custom_router_init_data`** : renvoie une liste de configurations de routes personnalisés

  - **paramètres** :

    - init_data : **Optional[List[RouteConfig]]**

    - route_names : **Optional[List[DefaultRoutesName]]**

    - `is_protected`: **TypeRoute** , default : `TypeRoute.PUBLIC`

  - **sortie** : List[RouteConfig]

- **`get_custom_public_router`** : retourne un routeur personnalisé

  - **paramètres** :

    - init_data : **Optional[List[RouteConfig]]**

    - routes_name : **Optional[List[DefaultRoutesName]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - authorizations: **Optional[List[AuthorizationConfig]]**

    - response_model_configs: Optional[List[ResponseModelConfig]]

    - type_route : **TypeRoute**

  - **sortie** : **APIRouter**

- **`get_mixed_router`** : renvoie un routeur avec une configuration personnalisée entre routes publiques et protégées .

  - **paramètres**:

    - init_data: **Optional[List[RouteConfig]]**

    - public_routes_name : **Optional[List[DefaultRoutesName]]**

    - protected_routes_name : **Optional[List[DefaultRoutesName]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - response_model_configs: Optional[List[ResponseModelConfig]]

- **`initialize_router`** : initialise un routeur avec une configuration .

  - **paramètres**:

    - init_data : **List[RouteConfig]**

    - authorizations: **Optional[List[AuthorizationConfig]]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - response_model_configs: Optional[List[ResponseModelConfig]]

### **2.9.5. Sous module `router_crud`**

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

    - read_with_relations: **bool**

    - authorizations : **List[AuthorizationConfig]**

    - exclude_routes_name : **Optional[List[DefaultRoutesName]]**

    - authentication: **Optional[AuthenticationManager]**

    - response_model_configs: **Optional[List[ResponseModelConfig]]**

    - roles: **Optional[List[str]]**

    - privileges: **Optional[List[str]] = None**

    - ReadPydanticModel: **Optional[Type[BaseModel]]**

    - FullReadPydanticModel: **Optional[Type[BaseModel]]**

  - **sortie** : **List[RouteConfig]**

- `set_response_model_config` : permet de préparer les configurations de routage en ajoutant les models de reponses specifiques.

  - **paramètres:**

    - routes_config : **List[RouteConfig]**

    - response_model_configs : **List[ResponseModelConfig]**

  - **sortie** : **List[RouteConfig]**

- `set_response_model` : permet d'ajouter un model de reponse à une route .

  - **paramètres:**

    - ReadPydanticModel: **Type[BaseModel]**

    - FullReadPydanticModel:**Type[BaseModel]**

    - route_config: **RouteConfig**

    - read_with_relations:**bool**

  - **sortie** : **Type[BaseModel]**

### **2.9.6. Sous module `relationship`**

Ce sous module définit `Relationship` une classe pour permettre de retourner des données en effectuant des jointures .

- `__init__`

  - **paramètres**

    - relationship_name : **str**

    - relationship_crud_models : **CrudModels**

    - joined_entity_crud_models : **CrudModels**

    - relationship_key1_name : **str**

    - relationship_key2_name : **str**

    - joined_model_key_name : **str**

- `get_relationship_key1`

- `get_relationship_key2`

- `get_second_model_key`

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

#### 2.10. Module `session`

Ce module définit des classes utilitaires pour la gestion des sessions

##### 2.10.1 Sous module `session_manager`

Ce sous module définit la classe SessionManager pour gérer les sessions

- `attributs` :

  - `session_manager` : **sessionmaker[Session]** , le générateur de session

- `méthodes` :

  - `yield_session` : renvoie une session

    - sortie : `Session`
