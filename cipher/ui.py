from . import __author__, __copyright__, __description__, __type__
from click import secho

def initialise_cipher(time, priv_key_generated : bool = False):
	rounded = round((time*1000/60)/10)
	string = f'{rounded} seconds were taken for generating private key' if priv_key_generated else ''
	secho(f"""
  ____ _       _
 / ___(_)_ __ | |__   ___ _ __
| |   | | '_ \| '_ \ / _ \ '__|		{__description__}
| |___| | |_) | | | |  __/ |		Type: {__type__.capitalize()}
 \____|_| .__/|_| |_|\___|_|		{__copyright__}
        |_|

{string}
		""",
		fg="bright_red"
	)
	print(f"""\nThe keys are stored as follows.
	
Public key: public.pem
Private key: private.pem
	
DO NOT MODIFY THE KEYS OR SHARE THE PRIVATE KEY WITH ANYONE.\n""")
