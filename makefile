make ruff:
	ruff check miscellaneous --fix
	ruff format miscellaneous

make git:
	git add *
	git commit -m Updated
	git push