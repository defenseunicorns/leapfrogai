
clean-all: clean-artifacts clean-cache clean-env clean-logs clean-models


clean-artifacts: # Zarf packages, UDS bundles, Python build artifacts, etc.
	-rm zarf-package-*.tar.zst
	-rm packages/**/zarf-package-*.tar.zst
	-rm -rf build/*
	-rm -rf src/**/build/*
	-rm -rf packages/**/build/*
	find . -name 'uds-bundle-*-*.tar.zst' -delete
	find . -type d -name 'zarf-sbom' -exec rm -rf {} +
	find . -name '*.whl' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +

clean-cache:
	-rm -rf ./**/__pycache__/
	-rm -rf ./**/.ruff_cache ./.ruff_cache
	-rm -rf ./**/.pytest_cache ./.pytest_cache

clean-env:
	rm -f .env
	rm -f .env.email
	rm -f .env.password

clean-logs:
	-rm -rf ./.logs/

clean-models:
	-rm -rf ./packages/**/.model/
