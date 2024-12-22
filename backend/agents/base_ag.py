
# # backend/agents/base_agent.py
# from abc import ABC, abstractmethod
# from typing import Dict, Any

# class BaseAgent(ABC):
#     """Base class for all agents in the system."""
    
#     @abstractmethod
#     async def process(self, input_data: Dict[Any, Any]) -> Dict[Any, Any]:
#         """Process the input data and return results."""
#         pass
# backend/agents/base_ag.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        pass