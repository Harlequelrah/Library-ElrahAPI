from myproject.myapp.cruds import myapp_crud


from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
)
app_myapp=router_provider.initialize_router()
app_myapp = router_provider.get_public_router()

