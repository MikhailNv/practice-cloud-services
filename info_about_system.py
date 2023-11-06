import os
for item in os.environ:
	print(f'{item}{" : "}{os.environ[item]}')