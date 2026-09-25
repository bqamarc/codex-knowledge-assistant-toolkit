.PHONY: test public-check verify

test:
	python3 -m unittest discover -s tests -v

public-check:
	python3 scripts/verify_public_release.py . --require-license

verify: test public-check
