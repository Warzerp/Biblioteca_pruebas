"""Crea la base PostgreSQL del proyecto si todavía no existe."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
import psycopg2  # noqa: E402
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # noqa: E402


def _txt(exc: BaseException) -> str:
    raw = getattr(exc, 'args', [None])[0]
    if isinstance(raw, bytes):
        return raw.decode('latin-1', errors='replace')
    return str(exc)


def main() -> int:
    cfg = settings.DATABASES['default']
    db_name = cfg['NAME']
    conn = psycopg2.connect(
        dbname='postgres',
        user=cfg['USER'],
        password=cfg['PASSWORD'],
        host=cfg.get('HOST') or 'localhost',
        port=cfg.get('PORT') or '5432',
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (db_name,))
    if cur.fetchone():
        print(f'La base "{db_name}" ya existe.')
    else:
        cur.execute(f'CREATE DATABASE "{db_name}"')
        print(f'Base "{db_name}" creada.')
    cur.close()
    conn.close()
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print('Error al crear la base:', _txt(exc), file=sys.stderr)
        print(
            'Revisa USER/PASSWORD/HOST/PORT en config/settings.py '
            '(deben coincidir con PostgreSQL local).',
            file=sys.stderr,
        )
        raise SystemExit(1)
