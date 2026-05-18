import shutil
import os
from datetime import datetime


def crear_backup():

    db_path = "atspro.db"

    if not os.path.exists(db_path):

        return None

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_name = (
        f"backup_{fecha}.db"
    )

    backup_path = os.path.join(
        "backups",
        backup_name
    )

    shutil.copy(
        db_path,
        backup_path
    )

    return backup_path