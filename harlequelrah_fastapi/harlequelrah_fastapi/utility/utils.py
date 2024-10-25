def update_entity(existing_entity, update_entity):
    for key, value in update_entity.dict().items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
