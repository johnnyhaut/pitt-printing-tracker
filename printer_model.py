from sqlalchemy import Column, String, Integer 
from sqlalchemy.orm import declarative_base
import os


Base = declarative_base()

# Used to create a database for all the printers on campus 
class Printer(Base): 
    __tablename__ = "printers"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    location = Column("location", String, nullable=False)
    type = Column("type", String, nullable=False) 
    status = Column("status",String, nullable=False)
    
    # Returns an easily readable JSON containing all of the important printer infomration 
    def toJSON(self): 
        return {
            "id":self.id, 
            "location":self.location, 
            "type":self.type,
            "status":self.status}