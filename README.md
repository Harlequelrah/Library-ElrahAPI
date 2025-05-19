# I - **`Présentation`**

![Logo](https://raw.githubusercontent.com/Harlequelrah/Library-ElrahAPI/main/Elrah.png)

# **1.** `Description`

Passioné par la programmation et le développement avec python je me lance dans la création progressive d'une bibliothèque personnalisée ou framework basé sur pour `FASTAPI` m'ameliorer , devenir plus productif et partager mon expertise .

# **2.** `Objectifs`

ElrahAPI permet notament dans le cadre d'un développement avec FASTAPI de :

- Démarrer rapidement un projet en fournissant une architecture de projet ;

- Minimiser les configurations pour un projet ;

- Fournir un système d'authentification configurable ;

- Générer les principaux cruds d'un model ;

- Configurer facilement les routes avec des configurations personnalisées ;

- Fournir et configurer facilement les principales routes d'un model ;

- Permet d'effectuer un enregistrement des logs dans la base de donnée grâce à un middleware de log ;

- Fournir un middleware de gestion d'erreur et des utilitaires pour lancer des exceptions personnalisées ;

- Permet de gérer efficement l'authentification et les routes protégées ;

- Une gestion simple et efficace de l'autorisation par l'utilisation de rôles et privileges ;

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

- Il est recommandé de créer un environnement virtuel pour chaque projet

- **myproject** designe le nom de votre projet .

- **myapp** designe le nom d'une application .

- Après la creation du projet configurer l'environnement .

## **2.** `créer un projet`

```bash
   elrahapi startproject myproject
```

## **3.** `configurer l'environnement`

- Ouvrer le fichier .env et configurer le

- Configurer alembic au besoin :

  - Configurer le alembic.ini par son paramètre `sqlalchemy.url`

    - pour sqlite : `sqlite:///database.db`

  - Configurer le alembic/env.py :

    - Ajouter l'import : from myproject.settings.models_metadata import target_metadata

    - Passer les metadata à target_metadata : target_metadata=target_metadata

- Configurer le main.py en decommentant les lignes commentées au besoin

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

- Créer les models SQLAlchemy dans `models.py`

- Créer les models Pydantic dans `schemas.py`

- Créer les meta models dans` meta_models.py` si nécessaire

- Importer la variable metadata depuis `myapp/models.py` de l'application dans le settings/models_metadata.py

### **6.2.** `Créer les cruds`

- Configurer un objet de type CrudModels

- Configurer le CrudForgery dans cruds.py

### **6.3.** `Configurer le fournisseur de routage de l'application`

Configurer le CustomRouterProvider dans router.py

- **`Configuration de base`**

Importer le crud depuis `myapp/cruds`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,

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

- **`Configuration avec relations entre model`** :

La configuration des relations se fait par le paramètre `read_with_relations` par défaut à False qui détermine si les models de réponses doivent inclure ou non les relations c'est à dire si `EntityReadModel` sera utilisé ou `EntityFullReadModel`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    read_with_relations = True
)
```

Cette configuration se fait aussi par le paramètre `relations` qui définit une liste d'instance de `Relationship`

```python
   router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    relations=[
        Relationship(
            relationship_name="item_categories",
            relationship_crud_models=item_categories.crud_models,
            joined_entity_crud_models=category_crud.crud_models,
            relationship_key1_name="item_id",
            relationship_key2_name="category_id",
            joined_model_key_name="id",
        )
    ],
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

- **`Création des configurations d'authorizations de routes`**

```python
  custom_authorizations : List[AuthorizationConfig] = [
  AuthorizationConfig(route_name=DefaultRoutesName.DELETE,roles=["ADMIN","MANAGER"]),
  AuthorizationConfig(route_name=DefaultRoutesName.UPDATE,privileges=["CAN_UPDATE_ENTITY"]
  ]
```

- **`Création des configurations de model de reponse pour les routes`**

```python
  custom_response_models : List[ResponseModelConfig] = [
  ResponseModelConfig(route_name=DefaultRoutesName.DELETE,response_model=MyModel),
  ResponseModelConfig(route_name=DefaultRoutesName.UPDATE,read_with_relations=True
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

- Configurer au besoin `settings/logger`

- Dans le fichier `myproject/main.py` du projet , ajouter et configurer le middleware de logs et ou celui d'erreur :

```python
from elrahapi.middleware.log_middleware import LoggerMiddleware
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from .settings.logger.router import app_logger
from .settings.logger.model import Log
from .settings.database import engine,session_manager

app = FastAPI()
app.include_router(app_logger)
app.add_middleware(
    ErrorHandlingMiddleware,
    LogModel=Logger,
    session_manager=session_manager
)
app.add_middleware(
    LoggerMiddleware,
    LogModel=Logger,
    session_manager=session_manager
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

- `raise_custom_http_exception` :

```python
  from elrahapi.exception.exception_utils import raise_custom_http_exception
  from fastapi import status
  raise_custom_http_exception(
  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
  detail="Cette requête est intratable par le serveur")
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

Pour consulter la documentation technique :

├── docs/
│ ├── README.md
