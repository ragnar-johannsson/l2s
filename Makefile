
version=0.1

.PHONY: package
package: l2s_$(version)_amd64.deb

l2s_$(version)_amd64.deb: .buildcontainer
l2s_$(version)_amd64.deb:
	docker run --interactive --workdir /src --name l2s-build l2s-build /src/build_deb_pkg.sh
	docker cp l2s-build:/src/l2s_$(version)_amd64.deb .
	docker rm --force l2s-build

.buildcontainer: SHELL := /bin/bash
.buildcontainer: Dockerfile
	docker build --tag l2s-build ${CURDIR}
	touch $@

.PHONY: install
install: package
	gdebi -n l2s*.deb

.PHONY: clean
clean: SHELL := /bin/bash
clean:
	rm -rf .buildcontainer
	rm -rf l2s*.deb
	docker rmi --force l2s-build
	docker rm --force l2s-build
