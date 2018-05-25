import click
import os
from rqalpha import cli

__config__ = {
    "source": "quantos",
    "mongo_url": os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017"),
    "redis_url": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"),
    "bundle_path": None,
    # quantos
    "quantos_url": "tcp://data.quantos.org:8910",
    "quantos_user": "15010492066",
    "quantos_token": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTMwNTA0ODY3MTQiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTUwMTA0OTIwNjYifQ.s_530n20Aelg7-8-1IorTgoa_yp6goImz20hhGIzMGU",
    # cache
    "enable_cache": True,
    "cache_length": None,
    "max_cache_space": None,
    # other
    "fps": 60,
    "persist_path": ".persist",
    "priority": 200,
}


def load_mod():
    from .mod import FxdayuSourceMod
    return FxdayuSourceMod()


"""
--force-init
"""

cli.commands['run'].params.append(
    click.Option(
        ('--force-init/--no-force-init', 'extra__force_run_init_when_pt_resume'),
        is_flag=True, default=False, show_default=True,
        help="[fxdayu_source]force run init when paper trading resume or not"
    )
)
