make ruff:
	ruff check . --fix

make git:
	git add *
	git commit -m Updated
	git push