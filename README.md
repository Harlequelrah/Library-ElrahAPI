# I - **`Présentation`**

![Logo](https://raw.githubusercontent.com/Harlequelrah/Library-ElrahAPI/main/Elrah.png)

# **1.** `Description`

Passioné par la programmation et le développement avec python je me lance dans la création progressive d'une bibliothèque/package/framework personnalisée basé sur pour `FASTAPI` m'ameliorer , devenir plus productif et partager mon expertise .

# **2.** `Objectifs`

ElrahAPI permet notament dans le cadre d'un développement avec FASTAPI de :

- Démarrer rapidement un projet en fournissant une architecture de dossier ;

- Minimiser les configurations de base de données et de gestion des sessions pour un projet ;

- Fournir et gérer un système d'authentification simple et configurable ;

- Générer les principaux cruds d'un model ;

- Fournir Configurer facilement les routes avec des configurations personnalisées ;

- Pemettre d'utiliser les sessions asynchrones ;

- Permet d'effectuer un enregistrement des logs dans la base de donnée grâce à un middleware de log ;

- Fournir un middleware de gestion d'erreur  ;

- Une gestion simple et efficace de l'autorisation par l'utilisation de rôles et privileges ;

- Fournir une pile d'utilitaires ;

- L'utilisation de gestionnaire de websocket pour particulièrement envoyer les erreurs des requêtes .

# II - **`Installation`**

**Il serait judicieux de créer un environnement virtuel dans un repertoire avant de poursuivre l'installation**

- **Créer un environnement virtuel :**

```bash
    python -m venv env
```

ou si virtualenv est dejà installé au préalable

```bash
    virtualenv env
```

- **`Avec Github :`**

  ```bash
  git clone https://github.com/Harlequelrah/Library-ElrahAPI

  cd Library-ElrahAPI

  pip install -e ./elrahapi
  ```

- **`Avec pip :`**

  ```bash
  pip install elrahapi
  ```

# III - **`Lancez vous ! `**

## **1.** `Quelques recommandations` :

- Il est recommandé de créer un environnement virtuel pour chaque projet ;

- **myproject** designe le nom de votre projet ;

- **myapp** designe le nom d'une application ;

- Après la creation du projet configurer l'environnement .

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

    - Ajouter l'import : from myproject.settings.database import database ;

    - Passer les metadata à target_metadata : database.target_metadata=target_metadata ;


## **4.** `Demarrer le projet `

- Accéder au repertoire du projet :

```bash
  cd myproject
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

- Créer les meta models dans `meta_models.py`  si nécessaire ;

**`Note:`** :

Avec `SQLAlchemy` en asynchrone , si dans vos schémas vous retourner des relations d'un model , il faudra ajouter `lazy=joined` aux relationship des models SQLAlchemy .

Pour les schémas pydantic l'on pourra d'abord créer ou non un EntityBaseModel dans `meta_models.py` pour le réutiliser au besoin dans les autres schémas .

Dans `schemas.py` il peut y avoir généralement :

- EntityCreateModel : pour la création d' une entité ;

- EntityUpdateModel : pour la mise à jour totale d'une entité ;

- EntityPatchModel : pour la mise à jour partielle d'une 'entité ;

- EntityReadModel : pour la lecture partielle d'une entité ;

- EntityFullReadModel : pour la lecture totale d'une entité avec ses relations ;


**`exemple : `**

```python
  class User( UserModel,database.base):
    user_privileges = relationship("UserPrivilege", back_populates="user",lazy="joined")
    user_roles=relationship("UserRole",back_populates="user",lazy="joined")

  class UserFullReadModel(UserReadModel) :
    user_roles:List["MetaUserRoleModel"] = []
    user_privileges: List["MetaUserPrivilegeModel"]=[]
```

### **6.2.** `Créer les cruds`

Dans `cruds.py`

- Créer un  CrudModels

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
    session_manager=database.session_manager
)
```

### **6.3.** `Configurer le fournisseur de routage de l'application`

Configurer le CustomRouterProvider dans router.py

- **`Configuration de base`**

Il faut au préalable s'assurer importer  le crud depuis `myapp/cruds`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud
)
```

- **`Configuration avec authentification et autorisation`**

Pour utiliser les méthodes qui peuvent prendre en compte des routes protégées faut s'assurer d'ajouter l'attribut authentication . Avec ce paramètre on peut aussi gérer les autorisation en ajoutant des roles et privileges directement qui seront utilisés par toutes les routes .

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    authentication = authentication,
    roles = ["ADMIN"],
    privileges = [
    "CAN_CREATE_BOOK",
    "CAN_DELETE_CATEGORY"
    ]
)
```

- **`Configuration des models de réponse`** :

La configuration des relations se fait par le paramètre `read_with_relations` par défaut à False qui détermine si les models de réponses doivent inclure ou non les relations c'est à dire si `EntityReadModel` sera utilisé ou `EntityFullReadModel`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    read_with_relations = True
)
```

- **`Configuration des relations`** :

Cette configuration se fait  par le paramètre `relations` qui définit une liste d'instance de `Relationship`.

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

**`exemples de relations `** :

**Note** : RELATION_RULES est un dictionnaire où la clé est le type de relation et la valeur une liste des routes permises .

- Relation plusieurs à plusieurs avec une classe `SQLAlchemy` intermédiaire :

```python
user_role_relation: Relationship = Relationship(
    relationship_name="user_roles",
    second_entity_crud=role_crud,
    relationship_crud=user_role_crud,
    type_relation=TypeRelation.MANY_TO_MANY_CLASS,
    relationship_key1_name="user_id",
    relationship_key2_name="role_id",
    default_public_relation_routes_name=[
      RelationRoutesName.READ_ALL_BY_RELATION,
      RelationRoutesName.DELETE_RELATION,
    ],
)
```

- Relation plusieurs à plusieurs avec table `Table` intermédiaire :

```python
tag_relation: Relationship = Relationship(
    relation_table=post_tag_table,
    relationship_name="tags",
    second_entity_crud=tag_crud,
    relationship_key1_name="post_id",
    relationship_key2_name="tag_id",
    type_relation=TypeRelation.MANY_TO_MANY_TABLE,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.MANY_TO_MANY_TABLE],
)
```

- Relation un à un :

```python
profile_relation: Relationship = Relationship(
    relationship_name="profile",
    second_entity_crud=profile_crud,
    type_relation=TypeRelation.ONE_TO_ONE,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.ONE_TO_ONE],
)
```
- Relation un à plusieurs :

```python
post_relation: Relationship = Relationship(
    relationship_name="posts",
    second_entity_crud=post_crud,
    second_entity_fk_name="user_id",
    type_relation=TypeRelation.ONE_TO_MANY,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.ONE_TO_MANY],
)
```

**Note** : second_entity_fk_name est facultatif et permet d'attribuer cette valeur automatiquement dans la création , mise à jour partielle , mise à jour totale de l'entité secondaire . Il faut tout de même avoir ce champ dans les schémas correspondant ,et il pourra désormais etre optionel .

- Relation plusieurs à un :

```python
user_relation: Relationship = Relationship(
    relationship_name="user",
    second_entity_crud=user_crud,
    type_relation=TypeRelation.MANY_TO_ONE,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.MANY_TO_ONE],
)
```

### **6.4.** `Configurer un router`

Les possibilités de configuration d'un routeur :

- **`Créér des configurations de routes`**

```python
  custom_init_data: List[RouteConfig] = [
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
  custom_authorizations : List[AuthorizationConfig] = [
  AuthorizationConfig(route_name=DefaultRoutesName.DELETE,roles=["ADMIN","MANAGER"]),
  AuthorizationConfig(route_name=DefaultRoutesName.UPDATE,privileges=["CAN_UPDATE_ENTITY"]
  ]
```

- **`Création des configurations de model de réponse pour les routes`**

```python
  custom_response_models : List[ResponseModelConfig] = [
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
from .settings.logger.router import app_logger
from .settings.logger.model import LogModel
from .settings.database import database

app = FastAPI()
app.include_router(app_logger)
app.add_middleware(
    ErrorHandlingMiddleware,
    LogModel=LogModel,
    session_manager=database.session_manager
)
app.add_middleware(
    LoggerMiddleware,
    LogModel=LogModel,
    session_manager=database.session_manager
)
```

**Note**: `Il est recommandé d'utiliser l'ordre des middlewares comme dans l'exemple et de configurer aussi le middleware d'erreur pour avoir les logs des erreurs aussi.`

## **8.** `Configurer l'authentification`:

- Configurer au besoin `myproject/settings/auth`

- Ajouter au besoin les routers du `myproject/settings/auth/routers` au `myproject/main.py`

- Ajouter au besoin le router pour l'authentification du `myproject/settings/auth/configs` au `myproject/main.py`

## **9.** `Utilisation de  ConnectionManager`

La classe ConnectionManager permet de gérer les websockets .
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

## **9.** `Utilisation de certaines fonctions utiles` :

- `raise_custom_http_exception` :  permet de lever un CustomHttpException

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

## **10.** `Utilisation de patterns ` :

```python
from elrahapi.utility.patterns import TELEPHONE_PATTERN
class Test(BaseModel):
    telephone: str = Field(
        example="+22891361029",
        pattern=TELEPHONE_PATTERN,
        description="Telephone number must be in the format +<country_code><number>"
    )
```

# V - **`Contact ou Support`**

Pour des questions ou du support, contactez-moi à **`maximeatsoudegbovi@gmail.com`** ou au **`(+228) 91 36 10 29`**.

La version actuelle est le `1.1.6`

Vérifier la version  en executant `pip show elrahapi`

Pour un exemple concret , vous pouvez consulter le repository de test pour cette version : `https://github.com/Harlequelrah/elrahapi-testproject-v-1.1.6`

Vous pouvez  consulter la documentation technique pour découvrir toutes les fonctionnaliés :

├── docs/
│ ├── README.md
