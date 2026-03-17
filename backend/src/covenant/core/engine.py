import logging
from typing import Dict, Any, Optional
from covenant.core.constitutional_engine import AdvancedConstitutionalEngine

logger = logging.getLogger(__name__)

class EngineManager:
    _instance: Optional[AdvancedConstitutionalEngine] = None

    @classmethod
    def get_engine(cls, config: Optional[Dict[str, Any]] = None) -> AdvancedConstitutionalEngine:
        if cls._instance is None:
            logger.info("Initializing Global Constitutional Engine instance...")
            cls._instance = AdvancedConstitutionalEngine(config)
        return cls._instance

def create_engine(config: Dict[str, Any]) -> AdvancedConstitutionalEngine:
    """
    Factory function for engine creation.
    """
    return EngineManager.get_engine(config)
