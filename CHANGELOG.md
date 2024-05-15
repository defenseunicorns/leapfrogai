# Changelog

## [0.7.1](https://github.com/defenseunicorns/leapfrogai/compare/v0.7.0...v0.7.1) (2024-05-15)


### Bug Fixes

* allow release-please to update pyrpoject.toml files ([#509](https://github.com/defenseunicorns/leapfrogai/issues/509)) ([3e1f0a6](https://github.com/defenseunicorns/leapfrogai/commit/3e1f0a6c3a749e868caabf31035ddbbe6831bb1c))
* update 'latest' bundles to reference ui and supabase via reposistory instead of path ([#508](https://github.com/defenseunicorns/leapfrogai/issues/508)) ([818f55a](https://github.com/defenseunicorns/leapfrogai/commit/818f55ab8c0d173355345f58f46e36dca7f9e51b))


### Miscellaneous

* Turn supabase domain into a templated value ([#512](https://github.com/defenseunicorns/leapfrogai/issues/512)) ([312d587](https://github.com/defenseunicorns/leapfrogai/commit/312d5874e7c8fd28f2c50b1b91082e5f25356c08))

## [0.7.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.6.1...v0.7.0) (2024-05-14)


### Features

* Add supabase deployment package ([#380](https://github.com/defenseunicorns/leapfrogai/issues/380)) ([8982bc0](https://github.com/defenseunicorns/leapfrogai/commit/8982bc08e7e2dac496409a38e3f53f7757c3bdbf))
* files endpoints ([#467](https://github.com/defenseunicorns/leapfrogai/issues/467)) ([c269eee](https://github.com/defenseunicorns/leapfrogai/commit/c269eee174124949b103240110bd1eae5177d301))
* sidenav redesign with import and export ([#398](https://github.com/defenseunicorns/leapfrogai/issues/398)) ([368e4e9](https://github.com/defenseunicorns/leapfrogai/commit/368e4e9b152a126a02473dbff46875da94c58d3a))
* textarea instead of text input ([#435](https://github.com/defenseunicorns/leapfrogai/issues/435)) ([47a0fba](https://github.com/defenseunicorns/leapfrogai/commit/47a0fba2196fd3ea67d0190401a9247f1bad5803))
* ui assistants management ([#469](https://github.com/defenseunicorns/leapfrogai/issues/469)) ([28ba7ed](https://github.com/defenseunicorns/leapfrogai/commit/28ba7edd1cdd22eda99b50a3fe08f987cc53e020))
* **ui:** Assistant Avatars ([#494](https://github.com/defenseunicorns/leapfrogai/issues/494)) ([b4d9cfc](https://github.com/defenseunicorns/leapfrogai/commit/b4d9cfc0b2d7b6d89f0efc0d6d76438fd2f9d92e))
* **ui:** dates ([#404](https://github.com/defenseunicorns/leapfrogai/issues/404)) ([7efcebf](https://github.com/defenseunicorns/leapfrogai/commit/7efcebfceac3a3f9670005ebb9ba6ba6e977d94d))


### Bug Fixes

* input resize bug ([#472](https://github.com/defenseunicorns/leapfrogai/issues/472)) ([da7e377](https://github.com/defenseunicorns/leapfrogai/commit/da7e37700b8a19a34e92109f1a8479c0b681146f))
* make sure pytest catches files ([#438](https://github.com/defenseunicorns/leapfrogai/issues/438)) ([fe3bd9b](https://github.com/defenseunicorns/leapfrogai/commit/fe3bd9b05bd9df6e82e6db976acadfbab855297d))
* Quality of Life issues ([#429](https://github.com/defenseunicorns/leapfrogai/issues/429)) ([5f5444b](https://github.com/defenseunicorns/leapfrogai/commit/5f5444baf238c09af65f977c1c8e187121da3809))
* send and cancel btn tooltips ([#436](https://github.com/defenseunicorns/leapfrogai/issues/436)) ([bbb6ea9](https://github.com/defenseunicorns/leapfrogai/commit/bbb6ea9f7a8a45a67af4c7989c569b66aa388b6b))


### Miscellaneous

* add zarf variable to api package for exposing the OpenAPI specification ([#503](https://github.com/defenseunicorns/leapfrogai/issues/503)) ([054444c](https://github.com/defenseunicorns/leapfrogai/commit/054444c8dd6770c5cf4cacfcb3495db09533b82d))
* adding huggingface_hub has optional dev dependency ([#440](https://github.com/defenseunicorns/leapfrogai/issues/440)) ([857f583](https://github.com/defenseunicorns/leapfrogai/commit/857f5838ab7ef5cc4b1545bff4406a616babf211))
* bring ui into monorepo ([#349](https://github.com/defenseunicorns/leapfrogai/issues/349)) ([0463af9](https://github.com/defenseunicorns/leapfrogai/commit/0463af916558bb46c965a7a37b2ef169d1c3a4dc))
* **ci:** add unit test and linting workflow for leapfrogai_ui ([#439](https://github.com/defenseunicorns/leapfrogai/issues/439)) ([b5aa668](https://github.com/defenseunicorns/leapfrogai/commit/b5aa668df38b6149d009ae663e39deefa01455ce))
* **ci:** setup release-please to assist with manage version refs internally ([#465](https://github.com/defenseunicorns/leapfrogai/issues/465)) ([8c300b0](https://github.com/defenseunicorns/leapfrogai/commit/8c300b0b8d25c9a96a9915d41922066509292957))
* **ci:** update publish workflow w leapfrogai UI artifacts ([#464](https://github.com/defenseunicorns/leapfrogai/issues/464)) ([32c4ab5](https://github.com/defenseunicorns/leapfrogai/commit/32c4ab5e2a37fb086b9925397c510965af1b0b47))
* **deps-dev:** bump @sveltejs/kit in /src/leapfrogai_ui ([#452](https://github.com/defenseunicorns/leapfrogai/issues/452)) ([d2553fe](https://github.com/defenseunicorns/leapfrogai/commit/d2553fe249e1d3de54be982ae8b680bab9d6dc98))
* **deps-dev:** bump @testing-library/svelte in /src/leapfrogai_ui ([#449](https://github.com/defenseunicorns/leapfrogai/issues/449)) ([e3d6a45](https://github.com/defenseunicorns/leapfrogai/commit/e3d6a45696ca39e08a5db154277446d4a05fb39b))
* **deps-dev:** bump @typescript-eslint/parser in /src/leapfrogai_ui ([#427](https://github.com/defenseunicorns/leapfrogai/issues/427)) ([a8be49b](https://github.com/defenseunicorns/leapfrogai/commit/a8be49bb0cbca30d7429e444bbdb94bdfa1837e0))
* **deps-dev:** bump eslint-plugin-svelte in /src/leapfrogai_ui ([#477](https://github.com/defenseunicorns/leapfrogai/issues/477)) ([9666a79](https://github.com/defenseunicorns/leapfrogai/commit/9666a79d82feedbec0fb7bdc15a85e4cc3a3ab58))
* **deps-dev:** bump svelte from 4.2.12 to 4.2.15 in /src/leapfrogai_ui ([#451](https://github.com/defenseunicorns/leapfrogai/issues/451)) ([62cb193](https://github.com/defenseunicorns/leapfrogai/commit/62cb19318e5d60ffb2fd3f1e5352dd2409bf09ba))
* **deps-dev:** bump svelte-check in /src/leapfrogai_ui ([#475](https://github.com/defenseunicorns/leapfrogai/issues/475)) ([21be2a1](https://github.com/defenseunicorns/leapfrogai/commit/21be2a19e43af2aacf23c48d62080777c8ac38a7))
* **deps-dev:** bump typescript in /src/leapfrogai_ui ([#478](https://github.com/defenseunicorns/leapfrogai/issues/478)) ([5393e34](https://github.com/defenseunicorns/leapfrogai/commit/5393e34b42a727d5b53b4d5dcc678cecc900976d))
* **deps-dev:** bump vite from 5.1.5 to 5.2.10 in /src/leapfrogai_ui ([#426](https://github.com/defenseunicorns/leapfrogai/issues/426)) ([392c821](https://github.com/defenseunicorns/leapfrogai/commit/392c82121faf4a0213524c4b4581c92c875cd26f))
* **deps:** bump @supabase/ssr in /src/leapfrogai_ui ([#476](https://github.com/defenseunicorns/leapfrogai/issues/476)) ([49efaec](https://github.com/defenseunicorns/leapfrogai/commit/49efaec9aea05e8e5fad3ff94cc0c2ab95efe2bc))
* **deps:** bump @sveltejs/vite-plugin-svelte in /src/leapfrogai_ui ([#453](https://github.com/defenseunicorns/leapfrogai/issues/453)) ([06062c8](https://github.com/defenseunicorns/leapfrogai/commit/06062c8c8c7bfdd929bcd3e65d80ab864d4290f7))
* **deps:** bump msw from 2.2.3 to 2.2.14 in /src/leapfrogai_ui ([#425](https://github.com/defenseunicorns/leapfrogai/issues/425)) ([8cfe8b5](https://github.com/defenseunicorns/leapfrogai/commit/8cfe8b5fe13abf09da9f9fa2f3916e96fbd97c3f))
* **deps:** bump openai from 4.29.0 to 4.38.5 in /src/leapfrogai_ui ([#450](https://github.com/defenseunicorns/leapfrogai/issues/450)) ([7567bc7](https://github.com/defenseunicorns/leapfrogai/commit/7567bc7321de5550b228968af5a58a7458d78b86))
* **deps:** bump openai from 4.38.5 to 4.41.1 in /src/leapfrogai_ui ([#474](https://github.com/defenseunicorns/leapfrogai/issues/474)) ([86837e9](https://github.com/defenseunicorns/leapfrogai/commit/86837e96c107dcce917d26b1b03268108098c40c))
* documenting proposal for solution to database ADR ([#416](https://github.com/defenseunicorns/leapfrogai/issues/416)) ([7a3a0ad](https://github.com/defenseunicorns/leapfrogai/commit/7a3a0add9d67fb229ed1f20a8df27bc3ea8f1d84))
* Misc UI package configuration updates ([#495](https://github.com/defenseunicorns/leapfrogai/issues/495)) ([ebe4fde](https://github.com/defenseunicorns/leapfrogai/commit/ebe4fde51217708c0a7535eb7382628ced740abb))
* refactoring API and adding stubs for new OpenAI endpoints ([#437](https://github.com/defenseunicorns/leapfrogai/issues/437)) ([cba9676](https://github.com/defenseunicorns/leapfrogai/commit/cba967646b3f0e4cabd833b53c51fefaa30cda78))
* reformat with new prettier settings ([#466](https://github.com/defenseunicorns/leapfrogai/issues/466)) ([2bfad2d](https://github.com/defenseunicorns/leapfrogai/commit/2bfad2dff6d844b7563251fd8dffb447caae5561))
* restrict e2e tests from running on lfai-ui changes ([#401](https://github.com/defenseunicorns/leapfrogai/issues/401)) ([037d157](https://github.com/defenseunicorns/leapfrogai/commit/037d157895df4592a9f57319b45025fed30a1bb1))
* show copy/edit btns for non last message during regen ([#444](https://github.com/defenseunicorns/leapfrogai/issues/444)) ([7c67a4f](https://github.com/defenseunicorns/leapfrogai/commit/7c67a4fbf521ec388f7a36512c9aa10e064c380f))
* Supabase migrations ([#496](https://github.com/defenseunicorns/leapfrogai/issues/496)) ([86ed880](https://github.com/defenseunicorns/leapfrogai/commit/86ed88072b0664619b763eff38e85ec2b040a507))

## [0.6.1](https://github.com/defenseunicorns/leapfrogai/compare/v0.6.0...v0.6.1) (2024-04-12)

### Features

### Bug Fixes
* fix: remove hardcoded gpu request value by @YrrepNoj in https://github.com/defenseunicorns/leapfrogai/pull/386

### Miscellaneous
* chore: update version refs to 0.6.1 by @YrrepNoj in https://github.com/defenseunicorns/leapfrogai/pull/389


## [0.6.0](https://github.com/defenseunicorns/leapfrogai/releases/tag/v0.6.0) (2024-04-12)

### Features

### Bug Fixes

### Miscellaneous
