from typing import List


class LinkClass :
    def __init__(self,key:str,Model:type):
        self.key=key
        self.Model=Model

async def manage_linked_classes(Linked_Classes:List[LinkClass],dict_obj:dict):
    for relation in Linked_Classes:
                    if dict_obj.get(relation.key):
                        entities_obj=[]
                        for entity in dict_obj[relation.key]:
                            entity_obj= relation.Model(**entity)
                            entities_obj.append(entity_obj)
                        dict_obj[relation.key]=entities_obj
    return dict_obj
