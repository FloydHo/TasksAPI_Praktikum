from sqlalchemy import Column, Integer, Boolean, String
from app.database.session import  Base

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)      #Darf nicht null sein => Erforderliches Feld
    description = Column(String)                #Standarstmäßig Nullable => Optional
    completed = Column(Boolean, default=False)   #Default Wert ist immer falsch

    def __str__(self):
        return f"ID: {self.id} - Title: {self.title} - Description: {self.description}"