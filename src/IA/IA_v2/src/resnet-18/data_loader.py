"""
Data loader para ResNet-18 que usa o módulo compartilhado.
"""

import sys
from pathlib import Path

# Adicionar o diretório modules ao path
current_dir = Path(__file__).parent
modules_dir = current_dir.parent / "modules"
sys.path.insert(0, str(modules_dir))

from data_loader import DataOrganizer
from config import Config


def get_data_splits(config: Config = None):
    """
    Obtém as divisões do dataset usando o organizador compartilhado.
    
    Args:
        config: Configuração do modelo
        
    Returns:
        Dict com as divisões train/val/test
    """
    if config is None:
        config = Config()
    
    organizer = DataOrganizer(config)
    return organizer.get_splits()


# Para compatibilidade com código existente
class DataOrganizer(DataOrganizer):
    """Wrapper para manter compatibilidade."""
    pass