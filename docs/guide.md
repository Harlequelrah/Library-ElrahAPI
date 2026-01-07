# I - **`Lancez vous ! `**

Voici un petit guide d'utilisation pour explorer et découvrir les fonctionnalités majeurs.

## **1.** `Quelques recommandations` :

- Il est recommandé de créer un environnement virtuel pour chaque projet ;

- Après la création du projet configurer l'environnement .

**NB** : Pour la suite **myproject** designe le nom de votre projet et **myapp** designe le nom d'une application .

## **2.** `créer un projet`

```bash
   elrahapi startproject myproject
```

## **3.** `configurer l'environnement`

- Ouvrez le fichier .env et configurez le !

- Configurer alembic au besoin :

  - Configurer le alembic.ini par son paramètre `sqlalchemy.url` :

    - exemple pour sqlite : `sqlite:///database.db`

  - Configurer le alembic/env.py :

    - Ajouter l'import :
      ```python
      from app.settings.database.base import Base
      ```
    - Passer les metadata à target_metadata :
      ```python
      database.target_metadata=Base.metadata
      ```

## **4.** `Demarrer le projet `

- Accéder au repertoire du projet :

```bash
  cd myproject
```

- Créer les tables :

```bash
  elrahapi create_tables
```

- Démarrer le serveur :

```bash
  elrahapi run
```

## **5.** `Créer une application`

- Assurer vous d'être dans le dossier du projet

- Génerer l'application

```bash
  elrahapi startapp myapp
```

## **6.** `Configurer une application`

- Ouvrer le dossier myproject/myapp

### **6.1.** `Définir les models de l'application`

`Entity` représente le nom d'une entité de base de donnée .

- Créer les models SQLAlchemy dans `models.py`

- Créer les schémas Pydantic dans `schemas.py`

- Créer les meta models dans `meta_models.py` si nécessaire ;

- Ajouter le model dans models_metadata.py comme suite :
  ```python
  from app.myapp.models import Model
  ```

**`Note:`** :

Avec `SQLAlchemy` en asynchrone , si dans vos schémas vous retourner des relations d'un model , il faudra ajouter `lazy=joined` aux relationship des models SQLAlchemy lorsque vous utilisez le `CrudForgery` ou le `CustomRouterProvider`.

**`exemple : `**

```python
  class User( UserModel,Base):
    user_privileges = relationship("UserPrivilege", back_populates="user",lazy="joined")
    user_roles=relationship("UserRole",back_populates="user",lazy="joined")
```

Pour les schémas pydantic l'on pourra d'abord créer ou non un `EntityBaseModel` dans `meta_models.py` pour le réutiliser au besoin dans les autres schémas et `EntityInEntity2Model` peut servir à définir un modèle partiel de `Entity` dans le retour d'un schéma de `Entity2`

Dans `schemas.py` il peut y avoir généralement :

- EntityCreateModel : pour la création d' une entité ;

- EntityUpdateModel : pour la mise à jour totale d'une entité ;

- EntityPatchModel : pour la mise à jour partielle d'une 'entité ;

- EntityReadModel : pour la lecture partielle d'une entité ;

- EntityFullReadModel : pour la lecture totale d'une entité avec ses relations ;

**`exemple : `**

```python
  class UserFullReadModel(UserReadModel) :
    user_roles:list["UserRoleInUser"] = []
    user_privileges: list["UserInUserPrivilege"]=[]
```

### **6.2.** `Créer les cruds`

Dans `cruds.py`

- Créer un CrudModels

- Créer un CrudForgery dans cruds.py

**`exemple : `**

```python
myapp_crud_models = CrudModels(
    entity_name="myapp",
    primary_key_name="id",  #remplacer au besoin par le nom de la clé primaire
    SQLAlchemyModel=Entity, #remplacer par l'entité SQLAlchemy
    ReadModel=EntityReadModel,
    CreateModel=EntityCreateModel, #Optionel
    UpdateModel=EntityUpdateModel, #Optionel
    PatchModel=EntityPatchModel, #Optionel
    FullReadModel=EntityFullReadModel #Optionel
)
myapp_crud = CrudForgery(
    crud_models=myapp_crud_models,
    session_manager=session_manager
)
```

### **6.3.** `Descriptif des routes génériques `

On dispose d'une multitude de routes génériques parmis lesquelles les `DefaultRoutesName` et `RelationRoutesName` .

#### **6.3.1.** `DefaultRoutesName `

- `DefaultRoutesName.COUNT` : Cette route retourne des statistiques de compte dont le nombre total de l'entité , le total pour aujourdhui , les sept derniers jours ou le mois passé.

- `DefaultRoutesName.READ_ALL` : Cette route retourne une liste d'instances de l'entité .

- `DefaultRoutesName.READ_ONE` : Cette route retourne une instance de l'entité à partir d'une valeur de clé primaire.

- `DefaultRoutesName.READ_ONE_USER` : Cette route retourne une instance de l'entité utilisateur à partir d'une valeur de clé primaire , de l'email ou du nom d'utilisateur .

- `DefaultRoutesName.READ_CURRENT_USER` : Cette route retourne une instance de l'entité utilisateur actuellement connecté .

- `DefaultRoutesName.CREATE` : Cette route sert à la création d'une instance de l'entité .

- `DefaultRoutesName.DELETE` : Cette route sert à la suppression définitive d'une instance de l'entité.

- `DefaultRoutesName.SOFT_DELETE` : Cette route sert à la suppression logique d'une instance de l'entité.

- `DefaultRoutesName.UPDATE` : Cette route sert à la mise à jour totale d'une instance de l'entité.

- `DefaultRoutesName.PATCH` : Cette route sert à la mise à jour partielle d'une instance de l'entité.

- `DefaultRoutesName.BULK_CREATE` : Cette route sert à la création multiple d'instances de l'entité .

- `DefaultRoutesName.BULK_DELETE` : Cette route sert à la suppression définitive multiple d'instances de l'entité .

- `DefaultRoutesName.BULK_SOFT_DELETE` : Cette route sert à la suppression logique multiple d'instances de l'entité .

- `DefaultRoutesName.TOKEN_URL` : Cette route sert à l'authentification sur le swagger .

- `DefaultRoutesName.LOGIN` : Cette route sert à l'authentification et permet d'obtenir un token d'accès et de rafraichissement .

- `DefaultRoutesName.REFRESH_TOKEN` : Cette route sert à obtenir un nouveau token d'accès .

- `DefaultRoutesName.CHANGE_PASSWORD` : Cette route permet à un utilisateur de modifier son mot de passe .

- `DefaultRoutesName.CHANGE_PASSWORD` : Cette route permet d'activer ou de désactiver un utilisateur .

#### **6.3.1.** `RelationRoutesName `

- `RelationRoutesName.CREATE_RELATION` : cette route sert à la création d'une relation entre deux instances d'entités .

**exemple** : On peut créer une `relation` entre une instance de l'entité `Utilisateur` et une instance de l'entité `Profile` .

- `RelationRoutesName.DELETE_RELATION` : cette route sert à la suppression d'une une relation entre deux instances d'entités .

- `RelationRoutesName.READ_ONE_BY_RELATION` : cette route retourne une instance d'une autre entité à partir de sa relation avec l'entité .

- `RelationRoutesName.READ_ALL_BY_RELATION` : cette route retourne une instance d'une autre entité à partir de sa relation avec l'entité .

**exemple** : retourne tous les posts d'un utilisateur .

- `RelationRoutesName.CREATE_BY_RELATION` : cette route permet la création d'une instance d'une autre entité à partir de sa relation avec l'entité .

- `RelationRoutesName.DELETE_BY_RELATION` : cette route permet la suppression définitive d'une instance d'une autre entité à partir de sa relation avec l'entité .

- `RelationRoutesName.SOFT_DELETE_BY_RELATION` : cette route permet la suppression logique d'une instance d'une autre entité à partir de sa relation avec l'entité .

- `RelationRoutesName.UPDATE` : cette route permet la mise à jour totale d'une instance d'une autre entité à partir de sa relation avec l'entité .

- `RelationRoutesName.PATCH` : cette route permet la mise à jour partielle d'une instance d'une autre entité à partir de sa relation avec l'entité .

### **6.4.** `Configurer le fournisseur de routage de l'application`

Configurer le CustomRouterProvider dans router.py

#### **6.4.1** `Configuration de base`

Il faut au préalable s'assurer importer le crud depuis `myapp/cruds`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud
)
```

#### **6.4.2** `Configuration avec authentification et autorisation`

Pour utiliser les méthodes qui peuvent prendre en compte des routes protégées faut s'assurer d'ajouter l'attribut authentication . Avec ce paramètre on peut aussi gérer les autorisation en ajoutant des roles et ou privileges directement qui seront utilisés par toutes les routes .

**exemple**:

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    authentication = authentication,
    roles = ["ADMIN"]
)
```

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    authentication = authentication,
    privileges = [
    "CAN_CREATE_BOOK",
    "CAN_DELETE_CATEGORY"
    ]
)
```

#### **6.4.3** `Configuration des models de réponse`

La configuration des relations se fait par le paramètre `read_with_relations` par défaut à False qui détermine si les models de réponses doivent inclure ou non les relations c'est à dire si `EntityReadModel` sera utilisé ou `EntityFullReadModel`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    read_with_relations = True
)
```

#### **6.4.4** `Configuration des relations`

Cette configuration se fait par le paramètre `relations` qui définit une liste d'instance de `Relationship`.

**`exemple`** :

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    relations=[
    user_role_relation,
    post_relation
    ],
)
```

**Note** : RELATION_RULES est un attribut de liste correspondant aux routes possibles une relation .

##### **6.4.4.1** `ManyToManyClassRelationship`: Relation plusieurs à plusieurs avec une classe `SQLAlchemy` intermédiaire

- **RELATION_RULES** :

```python
    RELATION_RULES = [
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.READ_ONE_RELATION,
    ]
```

- **exemple** :

```python
from elrahapi.relationship.many_to_many_class import ManyToManyClassRelationship
user_role_relation = ManyToManyClassRelationship(
    relationship_name="user_roles",
    second_entity_crud=role_crud,
    relationship_crud=user_role_crud,
    relationship_key1_name="user_id",
    relationship_key2_name="role_id",
    default_public_relation_routes_name=ManyToManyClassRelationship.RELATION_RULES,
)
```

##### **6.4.4.2** `ManyToManyTableRelationship`: Relation plusieurs à plusieurs avec table `Table` intermédiaire

- **RELATION_RULES** :

```python
    RELATION_RULES = [
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.CREATE_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.CREATE_BY_RELATION,
    ]
```

- **exemple** :

```python
from elrahapi.relationship.many_to_many_table import ManyToManyTableRelationship
task_assign_user_relation =       ManyToManyTableRelationship(
    relationship_name="assigned_users",
    second_entity_crud=user_crud,
    relation_table=task_assign_user_association,
    relationship_key1_name="task_id",
    relationship_key2_name="user_id",
    default_protected_relation_routes_name=[
      RelationRoutesName.CREATE_RELATION,
      RelationRoutesName.DELETE_RELATION,
    ],
)
```

##### **6.4.4.3** `OneToOneRelationship`: Relation un à un

- **RELATION_RULES** :

```python
    RELATION_RULES = [
        RelationRoutesName.READ_ONE_BY_RELATION,
        RelationRoutesName.CREATE_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.CREATE_BY_RELATION,
        RelationRoutesName.UPDATE_BY_RELATION,
        RelationRoutesName.PATCH_BY_RELATION,
        RelationRoutesName.SOFT_DELETE_BY_RELATION,
        RelationRoutesName.DELETE_BY_RELATION,
    ]
```

**exemple** :

```python
from elrahapi.relationship.one_to_one import OneToOneRelationship
profile_relation = OneToOneRelationship(
    relationship_name="profile",
    second_entity_crud=profile_crud,
    default_public_relation_routes_name=OneToOneRelationship.RELATION_RULES,
)
```

##### **6.4.4.4** `OneToManyRelationship`: Relation un à plusieurs

- **RELATION_RULES** :

```python
    RELATION_RULES = [
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.CREATE_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.CREATE_BY_RELATION,
    ]
```

**exemple** :

```python
from elrahapi.relationship.one_to_many import OneToManyRelationship
user_task_relation = OneToManyRelationship(
    relationship_name="user_tasks",
    second_entity_crud=task_crud,
    default_public_relation_routes_name=OneToManyRelationship.RELATION_RULES,
)
)
```

##### **6.4.4.5** `ManyToOneRelationship`: Relation plusieurs à un

- **RELATION_RULES** :

```python
    RELATION_RULES = [RelationRoutesName.READ_ONE_BY_RELATION]
```

**exemple** :

```python
from elrahapi.relationship.many_to_one import ManyToOneRelationship
user_relation = ManyToOneRelationship(
    relationship_name="user",
    second_entity_crud=user_crud,
    default_public_relation_routes_name=ManyToOneRelationship.RELATION_RULES,
)
```

**Note** : Les paramètres `relations_routes_configs` , `relations_authorizations_configs` et `relations_responses_model_configs` peuvent eventuellement être utilisés .

### **6.5.** `Configurer un router`

Les possibilités de configuration d'un routeur :

- **`Créér des configurations de routes`**

```python
  custom_init_data: list[RouteConfig] = [
    RouteConfig(
      route_name=DefaultRoutesName.CREATE,
      is_activated=True,
      read_with_relations = False
     ),
    RouteConfig(
      route_name=DefaultRoutesName.READ_ONE,
      is_activated=True,
      roles= ["SECRETARY"],
      is_protected=True
     ),
    RouteConfig(
      route_name=DefaultRoutesName.READ_ALL,
      is_activated=True,
      privileges=["CAN_CREATE_MEET"],
      is_protected=True
     ),
    RouteConfig(route_name=DefaultRoutesName.UPDATE, is_activated=True),
    RouteConfig(route_name=DefaultRoutesName.DELETE, is_activated=True),
]
```

- **`Création des configurations de routes de relation`**

```python
user_relation: Relationship = Relationship(
    relationship_name="user",
    second_entity_crud=user_crud,
    type_relation=TypeRelation.MANY_TO_ONE,
    default_public_relation_routes_name=[
    RouteConfig(route_name=RelationRoutesName.UPDATE_BY_RELATION, is_activated=True)
    ],
)
```

- **`Création des configurations d'authorizations de routes`**

```python
  custom_authorizations : list[AuthorizationConfig] = [
  AuthorizationConfig(route_name=DefaultRoutesName.DELETE,roles=["ADMIN","MANAGER"]),
  AuthorizationConfig(route_name=DefaultRoutesName.UPDATE,privileges=["CAN_UPDATE_ENTITY"]
  ]
```

- **`Création des configurations de model de réponse pour les routes`**

```python
  custom_response_models : list[ResponseModelConfig] = [
  ResponseModelConfig(route_name=DefaultRoutesName.READ_ONE,response_model=MyModel),
  ResponseModelConfig(route_name=DefaultRoutesName.READ_ALL,read_with_relations=True
  ]
```

- **`Créer un router en initialisant totalement une configuration`**

```python
app_myapp = router_provider.initialize_router(
init_data=custom_init_data,
)
```

le paramètre `exclude_routes_name` pourra éventuellement être utilisé pour exclure certaines routes.

le paramètre `authorizations` pourra éventuellement utilisés pour configurer les permissions .

le paramètre `response_model_configs` pourra éventuellement utilisés pour configurer les models de reponses .

- **`Créér un router préconfiguré sans authentification`**

```python
  app_myapp = router_provider.get_public_router()
```

- **`Créér un router préconfiguré avec authentification`**

```python
  app_myapp = router_provider.get_protected_router(
  authorizations=custom_authorizations
  )
```

- **`Créer un router avec configuration et des routes publiques`**

```python
  app_myapp = router_provider.get_custom_router(
    init_data= custom_init_data ,
    routes_name=[DefaultRoutesName.PATCH],
    exclude_routes_name=[DefaultRoutesName.READ_ONE],
    type_route=TypeRoute.PUBLIC
  )

```

- **`Créer un router avec éventuellement une configuration et avec des routes publics et protégées`**

```python
  app_myapp = router_provider.get_mixed_router(
    protected_routes_name=[DefaultRoutesName.COUNT],
    public_routes_name=[DefaultRoutesName.READ_ALL]
  )
```

**Note** : `Ajouter le router au main.py`

```python
app.include_router(app_myapp)
```

## **7.** `Configurer les logs`

- Configurer au besoin `settings/logger` et ajouter son routeur au `myproject/main.py`

- Dans le fichier `myproject/main.py` du projet , ajouter et configurer le middleware de logs et ou celui d'erreur :

```python
from elrahapi.middleware.log_middleware import LoggerMiddleware
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from elrahapi.middleware.middleware_helper import MiddlewareHelper
from app.settings.logger.router import app_logger
from app.settings.logger.model import LogModel
from app.settings.config.database_config import session_manager

app = FastAPI()
app.include_router(app_logger)
middleware_helper = MiddlewareHelper(LogModel=LogModel,
session_manager= session_manager,
authentication=authentication)
app.add_middleware(ErrorHandlingMiddleware, middleware_helper=middleware_helper)
app.add_middleware(LoggerMiddleware, middleware_helper=middleware_helper)
```

**Note**: Si vous utilisez `ErrorHandlingMiddleware` et `LoggerMiddleware` vous pouvez définir le `middleware_helper` dans le `settings.logger.router` . Il est recommandé d'utiliser l'ordre des middlewares comme dans l'exemple et de configurer aussi le middleware d'erreur pour avoir les logs des erreurs aussi.

## **8.** `Configurer l'authentification`:

- Configurer au besoin `app/settings/auth`

- Ajouter au besoin les routers du `app/settings/auth/routers` au `myproject/main.py`

## **9.** `Utilisation des seeders`

Deux classes principales servent au seeders .
`Seed` pour un seed simple et `SeedManager` pour gérer les opérations de plusieurs Seed simultanément.

Dans le repertoire `app/settings/database/seeders` du projet vous trouverez les seeders par défaut.

Vous pouvez voir des fichers seeders `Seed` comme `user_seed.py` et ``SeedManager` comme `seed_manager_seed.py`.

Dans le repertoire `app/settings/config` il y a le ficher `seeders_logger_config.py` qui contient un logger pour enregistrer les logs des seeders dans le fichier `seeders.log`.

### **9.1.** `Creer un seeder`

```cmd
elrahapi create_seed nomduseeder
```

ex : nomduseeder peut être user , book ou item etc...

**Note** : Ensuite mettez à jour les imports et le ficher

### **9.2.** `Lancer un seeder`

Seed ou SeedManager se lance en mode up ou down.
Le mode up pour seeder et down pour rollback.
Sans précision c'est le mode up qui sera actif.

### **9.2.1** `Seed`

**`exemple`** :

```cmd
elrahapi run_seed nomduseeder
```

ou

```cmd
elrahapi run_seed nomduseeder down
```

### **9.2.1** `SeedManager`

**`exemple`** :

```cmd
elrahapi run_seed_manager up
```

la variable `seeds_dict` est un dictionnaire qui contient les seeders et leurs noms.

On peut toutes fois remplir `seeds_name` avec des noms de seeders pour en exécuter que ceux là .

En mode up les seeders sont exécutés dans l'ordre de leur nom dans le dictionnaire `seeds_dict` et dans l'ordre inverse en mode down .

### **9.3.** `Seeder des privlièges`

Il est possible de seeder des privilèges pour des entités précises et obtenir des privileges génériques facilement comme `CAN CREATE BOOK` ou `CAN READ ITEM` etc...

Cela se passe dans `seeders/privilege_seed.py`.

**`exemple`** :

```python
from elrahapi.utility.utils import get_entities_all_privilege_data

data: list[PrivilegeCreateModel] = []
entities_name:list[str]=[
    "user",
    "role",
    "role_privilege",
    "user_privilege",
    "user_role",
    "privilege",
    ] # lister les entités pour lesquelles on veut créer des privilèges génériques
entities_data =  get_entities_all_privilege_data(entities_names=entities_name)
data.extend(entities_data)
```

## **10.** `Utilisation de  ConnectionManager et de ChatManager`

La classe ConnectionManager permet de gérer les websockets de façon basique .
Exemple :

Il est aussi possible d'ajouter un objet de type ConnectionManager aux middlewares pour notifier les erreurs dans le projet

```python
from elrahapi.websocket.connectionManager import ConnectionManager
from fastapi import (
    FastAPI,
    WebSocketDisconnect,
    WebSocket,
)
app = FastAPI()
websocket_manager = ConnectionManager()

@app.websocket("/ws/notifications")
async def websocket_notification(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast(data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
```

La classe ChatManager permet une gestion plus poussé des websockets avec utilisations des rooms et des sub.

**`exemple`** :

```python

chat_manager = ChatConnectionManager()
@app.websocket("/ws/room/{room_name}")
async def chat_websocket(websocket:WebSocket,room_name:str,sub:str=Query(...)):
    chat_manager.create_room(room_name=room_name)
    await chat_manager.connect(websocket=websocket,room_name=room_name,sub=sub)
    try:
        while True:
            data= await websocket.receive_text()
            await chat_manager.broadcast(room_name=room_name,message=f"{sub} a dit : {data}")
    except WebSocketDisconnect:
        sub = await chat_manager.disconnect(websocket=websocket,room_name=room_name)
```

**`Note:`** : Pour en savoir plus , vous pouvez consulter : `https://github.com/Harlequelrah/learning_websocket`

## **11.** `Utilisation du module otp_setup` :

Module pour gérer l'authentification par otp.
Dans `otp_setup/schemas` vous disposez d'un schéma `OTPVerification` pour retourner l'OTP et le token temporaire .
Dans le sous module `otp_setup/otp_auth` vous disposez de `OTPAuthManager` qui hérite de `AuthenticationManager` et `OTPAuthRouterProvider` qui hérite de `AuthenticationRouterProvider`.

`SMTP_EMAIL` correspond à l'email à utiliser pour expédier les emails , `SMTP_PASSWORD` un mot de passe d'application et `OTP_EXPIRE_TIME` à la durée de validité de l'OTP en milliseconde.

**exemple**

```python
from elrahapi.otp_setup import OTPAuthManager,OTPAuthRouterProvider
from redis import Redis
from app.settings.config.database_config import session_manager
from app.settings.config.env_config import settings
r= Redis.from_url(settings.redis_url, decode_responses=True)
authentication = OTPAuthManager(
    settings=settings
    session_manager=session_manager,
    redis=r,
)
authentication_router_provider = AuthenticationRouterProvider(
    authentication=authentication,
)
```

## **12.** `Utilisation de certaines fonctions utiles` :

- `raise_custom_http_exception` : permet de lever un CustomHttpException

```python
  from elrahapi.exception.exception_utils import raise_custom_http_exception
  from fastapi import status
  raise_custom_http_exception(
  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
  detail="Cette requête est intraitable par le serveur")
```

- `validate_value` : permet de valider une valeur

```python
  from elrahapi.utility.utils import validate_value
  a = validate_value("True") # a contient True
  b = validate_value("false") # b continent False
  c = validate_value("1")  # c contient 1
```

- `update_entity` : permet de mettre à jour un objet sqlalchemy

```python
  from elrahapi.utility.utils import update_entity
        existing_plant = update_entity(
            existing_entity=existing_plant,
            update_entity=plant_update_obj
        )
```

## **13.** `Patterns ` :

- TELEPHONE_PATTERN

- URL_PATTERN

**exemple :**

```python
from elrahapi.utility.patterns import TELEPHONE_PATTERN
class Test(BaseModel):
    telephone: str = Field(
        example="+22891361029",
        pattern=TELEPHONE_PATTERN,
        description="Telephone number must be in the format +<country_code><number>"
    )
```

## **14.** `Generation de clé` :

Vous pouve générer une clé pour coder vos tokens JWT comme suit :

```cmd
elrahapi generate_secret_key
```

**Note** : par défaut l'algorithme est HS256

```cmd
elrahapi generate_secret_key HS512
```

**Note** : vous pouvez choisir entre HS256 , HS384 et HS512 .
