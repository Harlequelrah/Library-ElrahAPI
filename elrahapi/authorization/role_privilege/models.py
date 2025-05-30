from sqlalchemy import Column,Integer,ForeignKey,Boolean



class RolePrivilegeModel:
    id=Column(Integer,primary_key=True)
    role_id = Column(Integer,ForeignKey('roles.id'),nullable=False)
    privilege_id = Column(Integer,ForeignKey('privileges.id'),nullable=False)
    is_active=Column(Boolean,default=True)

