from abc import ABC, abstractmethod

class graph_index_repo(ABC):
    
    @abstractmethod
    def get(self, id: str):
        pass

    @abstractmethod
    def index(self, id: str, value: dict):
        pass
