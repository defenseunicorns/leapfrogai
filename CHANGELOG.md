# Changelog

## [0.12.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.11.0...v0.12.0) (2024-09-06)


### ⚠ BREAKING CHANGES

* standardize flavors, bundle dir and ghcr namespace ([#933](https://github.com/defenseunicorns/leapfrogai/issues/933))
* **api:** initial integration of registry1 api flavor ([#920](https://github.com/defenseunicorns/leapfrogai/issues/920))

### Features

* add RAG Evals Runner and Needle in a Haystack Evaluation ([#945](https://github.com/defenseunicorns/leapfrogai/issues/945)) ([c191b54](https://github.com/defenseunicorns/leapfrogai/commit/c191b54a361edf0694ec56722f149d866c27ac2e))
* **api:** adds migration for tracking vector store indexing status ([#830](https://github.com/defenseunicorns/leapfrogai/issues/830)) ([eee3ed7](https://github.com/defenseunicorns/leapfrogai/commit/eee3ed7b570d728cc10a2e4a9dec6bfdb38de2c4))
* **api:** initial integration of registry1 api flavor ([#920](https://github.com/defenseunicorns/leapfrogai/issues/920)) ([a8e93fb](https://github.com/defenseunicorns/leapfrogai/commit/a8e93fbab123b6cf90cbe102077a61ed76cfeb8e))
* **ui:** chat completion with files ([#951](https://github.com/defenseunicorns/leapfrogai/issues/951)) ([020dc07](https://github.com/defenseunicorns/leapfrogai/commit/020dc07c11105444dd33abf1195af8007f5eb876))
* **ui:** persist file upload status ([#967](https://github.com/defenseunicorns/leapfrogai/issues/967)) ([cb0650d](https://github.com/defenseunicorns/leapfrogai/commit/cb0650d40d5dcab80a86ed36f2fa2321e96864e7))
* **ui:** refresh token early ([#922](https://github.com/defenseunicorns/leapfrogai/issues/922)) ([4f0449d](https://github.com/defenseunicorns/leapfrogai/commit/4f0449dbe4609468a8a9d2b7a4775e6b3fadec89))


### Bug Fixes

* **api:** search vectorstore using only last message ([#939](https://github.com/defenseunicorns/leapfrogai/issues/939)) ([8a1d61e](https://github.com/defenseunicorns/leapfrogai/commit/8a1d61e1f91282689e4e0196524aba4dc8291939))
* correct fsGroup configuration in various deployments ([#974](https://github.com/defenseunicorns/leapfrogai/issues/974)) ([86766db](https://github.com/defenseunicorns/leapfrogai/commit/86766db8b2d423a3dfbf60483e720971f05a088a))
* run on thread containing an assistant without files ([#995](https://github.com/defenseunicorns/leapfrogai/issues/995)) ([1072654](https://github.com/defenseunicorns/leapfrogai/commit/10726542ae8aca2d0a83ea01fb3277b6c12e6cb2))
* **ui:** csp prevents iframe content from showing ([ff71c56](https://github.com/defenseunicorns/leapfrogai/commit/ff71c5629404e109be2d580801c67a8f889a372d))
* **ui:** file upload data shows 1970 ([#941](https://github.com/defenseunicorns/leapfrogai/issues/941)) ([1a80646](https://github.com/defenseunicorns/leapfrogai/commit/1a8064678a550471c843d9e2d2728bdf2122a38f))
* **ui:** playwright logout causes others to fail ([#923](https://github.com/defenseunicorns/leapfrogai/issues/923)) ([464ddbd](https://github.com/defenseunicorns/leapfrogai/commit/464ddbd104aaf6b7bb11da6cbd26c18ea811a5f9))
* **vllm:** initializes dictionary entry prior to usage ([#959](https://github.com/defenseunicorns/leapfrogai/issues/959)) ([d0e09cf](https://github.com/defenseunicorns/leapfrogai/commit/d0e09cf2ac989dc71386ef113c81d4fc31c21174))


### Miscellaneous

* add logger configuration to our various main entrypoints ([#918](https://github.com/defenseunicorns/leapfrogai/issues/918)) ([03bf0fd](https://github.com/defenseunicorns/leapfrogai/commit/03bf0fd7e42fe64b9c2dc234b9ee9433f62401bc))
* **api:** add background task for processing vectors ([#942](https://github.com/defenseunicorns/leapfrogai/issues/942)) ([5f259f1](https://github.com/defenseunicorns/leapfrogai/commit/5f259f1f406bff422102a0ba5708571798d0e9e0))
* commitlint and labelint workflows ([#931](https://github.com/defenseunicorns/leapfrogai/issues/931)) ([186a92c](https://github.com/defenseunicorns/leapfrogai/commit/186a92c76102dbe7617b3faf7750f87e9c7ae0de))
* **deps:** pin all python deps and standardize pyprojects ([#929](https://github.com/defenseunicorns/leapfrogai/issues/929)) ([af74924](https://github.com/defenseunicorns/leapfrogai/commit/af74924171ef55b08f30f33593f75d8f7b28781f))
* **docs:** markdown linting and improved documentation ([#902](https://github.com/defenseunicorns/leapfrogai/issues/902)) ([046a466](https://github.com/defenseunicorns/leapfrogai/commit/046a466fe60746eb90ca62031c3d3a139a022d6d))
* pin python dependencies in root pyproject ([#958](https://github.com/defenseunicorns/leapfrogai/issues/958)) ([cef1535](https://github.com/defenseunicorns/leapfrogai/commit/cef15357faf429b5df142f3a7dde12b46b3df408))
* release 0.12.0 ([#993](https://github.com/defenseunicorns/leapfrogai/issues/993)) ([547988f](https://github.com/defenseunicorns/leapfrogai/commit/547988f1ff9e1157643d35e22de47ee2519570e6))
* rename indexing_status migration version ([#996](https://github.com/defenseunicorns/leapfrogai/issues/996)) ([c39ff94](https://github.com/defenseunicorns/leapfrogai/commit/c39ff948fbf7d27457a880ed98c5d3bff29263ab))
* standardize flavors, bundle dir and ghcr namespace ([#933](https://github.com/defenseunicorns/leapfrogai/issues/933)) ([985642a](https://github.com/defenseunicorns/leapfrogai/commit/985642afccb25d347971e6e581a6e3bcb73bbe58))
* **supabase:** enable realtime for the file_objects table ([#985](https://github.com/defenseunicorns/leapfrogai/issues/985)) ([38e9705](https://github.com/defenseunicorns/leapfrogai/commit/38e9705645a99818b63b48da0023cefce41b3d96))
* **supabase:** fix supabase-realtime ([#855](https://github.com/defenseunicorns/leapfrogai/issues/855)) ([b1ee076](https://github.com/defenseunicorns/leapfrogai/commit/b1ee0769f51bd5ffbf5df6cec23520469db406a5))
* **tests:** Conformance testing templates ([#910](https://github.com/defenseunicorns/leapfrogai/issues/910)) ([b9f8d6a](https://github.com/defenseunicorns/leapfrogai/commit/b9f8d6a022757be917d90a7b56dacc9764c3f70c))
* **ui:** add test for assistant with no files ([#997](https://github.com/defenseunicorns/leapfrogai/issues/997)) ([d9b9361](https://github.com/defenseunicorns/leapfrogai/commit/d9b93612935a8bba13102b835735939c87787b48))
* **ui:** use keycloak for e2es in workflow ([#909](https://github.com/defenseunicorns/leapfrogai/issues/909)) ([cdd3e61](https://github.com/defenseunicorns/leapfrogai/commit/cdd3e615549b6bed2033223aee2372937a774095))
* Update CODEOWNERS ([#971](https://github.com/defenseunicorns/leapfrogai/issues/971)) ([ae203b6](https://github.com/defenseunicorns/leapfrogai/commit/ae203b600e55fbd514fbd7d4628eac9e65aeaf6f))
* update release workflow trigger type ([#988](https://github.com/defenseunicorns/leapfrogai/issues/988)) ([ce4952b](https://github.com/defenseunicorns/leapfrogai/commit/ce4952be3cf55220c5c888172562afd24afc9cba))

## [0.11.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.10.0...v0.11.0) (2024-08-16)


### Features

* **ui:** 663- skeleton text for assistant responses ([#898](https://github.com/defenseunicorns/leapfrogai/issues/898)) ([a4b0e1b](https://github.com/defenseunicorns/leapfrogai/commit/a4b0e1b51afecbbb7731b1d165e9419a4adf3c2f))
* **ui:** 669-annotations ([#908](https://github.com/defenseunicorns/leapfrogai/issues/908)) ([9d14dbf](https://github.com/defenseunicorns/leapfrogai/commit/9d14dbf8bc66758f918e1461a28303a6499a5290))
* **ui:** download files ([0ff7aa7](https://github.com/defenseunicorns/leapfrogai/commit/0ff7aa78e4f508d22fc315fe1018b6358364ea34))
* **ui:** settings/profile header btn re-design ([941da3a](https://github.com/defenseunicorns/leapfrogai/commit/941da3af38621c869b5724dc91439238b046febd))


### Bug Fixes

* **api:** Adds migration to prevent null metadata messages ([#895](https://github.com/defenseunicorns/leapfrogai/issues/895)) ([44aafca](https://github.com/defenseunicorns/leapfrogai/commit/44aafca529edfb64a4cd7f7cae86835c46a6ba24))
* **api:** Fix invalid nltk reference and bug ([#914](https://github.com/defenseunicorns/leapfrogai/issues/914)) ([6e3e5b8](https://github.com/defenseunicorns/leapfrogai/commit/6e3e5b8831f2fdebfab6f01326464c9b65beca14))
* **api:** Updates unstructured to fix punkt_tab issue ([#905](https://github.com/defenseunicorns/leapfrogai/issues/905)) ([67a05bb](https://github.com/defenseunicorns/leapfrogai/commit/67a05bb3ab012dac605939d85f6d8d243157ee5c))
* batch requests to the CreateEmbedding stub ([#887](https://github.com/defenseunicorns/leapfrogai/issues/887)) ([8ed4328](https://github.com/defenseunicorns/leapfrogai/commit/8ed4328a5cb2af51ad5ca1f7c0ead0d187336915))
* Remove explicit requests install ([#906](https://github.com/defenseunicorns/leapfrogai/issues/906)) ([863e9d6](https://github.com/defenseunicorns/leapfrogai/commit/863e9d64d588fa8d7f026b2c3818c68c70c8a70d))
* **ui:** CSP ([#913](https://github.com/defenseunicorns/leapfrogai/issues/913)) ([b83ef04](https://github.com/defenseunicorns/leapfrogai/commit/b83ef045e9ea6305d811a847a2fed76ad1c4baa9))


### Miscellaneous

* add default GH PR workflow triggers to test workflows ([#892](https://github.com/defenseunicorns/leapfrogai/issues/892)) ([c418a4c](https://github.com/defenseunicorns/leapfrogai/commit/c418a4cc46cd7a23f6605252c9474d31e2ee6601))
* Bumps all the uds core versions to 0.25.0 and updates deployment docs ([#874](https://github.com/defenseunicorns/leapfrogai/issues/874)) ([6ca39f1](https://github.com/defenseunicorns/leapfrogai/commit/6ca39f1b616c436107b9eaf6f36137988b3bade5))
* Remove "review_requested" as trigger to prevent unintentional test re-runs ([4c20d9e](https://github.com/defenseunicorns/leapfrogai/commit/4c20d9e16eb05ccf9a24a3c9114eb64ecbf8317c))
* **ui:** content security policy ([#903](https://github.com/defenseunicorns/leapfrogai/issues/903)) ([c2d2262](https://github.com/defenseunicorns/leapfrogai/commit/c2d22622163b21d277eeefedbde020dda6341051))
* **ui:** improve reliability of playwright test in workflow ([29703cb](https://github.com/defenseunicorns/leapfrogai/commit/29703cb64204879dacee286b158caad63c8c677a))
* **ui:** improve sveltekit store mocking ([90bef05](https://github.com/defenseunicorns/leapfrogai/commit/90bef057a66ce521d0a6d6276df970c0568121a0))
* **ui:** typescript updates and fix rag e2e tests ([#883](https://github.com/defenseunicorns/leapfrogai/issues/883)) ([8cd3011](https://github.com/defenseunicorns/leapfrogai/commit/8cd301153a9865e436f90170e971ce482da148bf))

## [0.10.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.9.2...v0.10.0) (2024-08-02)


### ⚠ BREAKING CHANGES

* **api:** updating api endpoints ([#817](https://github.com/defenseunicorns/leapfrogai/issues/817))

### Features

* **backend:** add k3d gpu image builder ([#797](https://github.com/defenseunicorns/leapfrogai/issues/797)) ([4504085](https://github.com/defenseunicorns/leapfrogai/commit/4504085dc10e9b6cb74115c974ea5e8f8c7fa98c))
* **backend:** nvidia runtimeclass ([#787](https://github.com/defenseunicorns/leapfrogai/issues/787)) ([106997d](https://github.com/defenseunicorns/leapfrogai/commit/106997d42e750014de94959c939442ac4e23378b))
* silent parallel make targets for build and deployment ([#824](https://github.com/defenseunicorns/leapfrogai/issues/824)) ([681aafd](https://github.com/defenseunicorns/leapfrogai/commit/681aafdec1b59f00fb8c8deb598a00327ef404b6))
* **ui:** remove carbon and replace with Flowbite ([#862](https://github.com/defenseunicorns/leapfrogai/issues/862)) ([921a864](https://github.com/defenseunicorns/leapfrogai/commit/921a8642c3e70c4d0dc3d92cd0d7745e45e21524))


### Bug Fixes

* **api:** fix indexing files with api key auth ([#852](https://github.com/defenseunicorns/leapfrogai/issues/852)) ([c4d9c3f](https://github.com/defenseunicorns/leapfrogai/commit/c4d9c3f289f8708cd08a82d290fe9ab51ba8cc09))
* helm template evluation for whisper GPU_REQUEST envvar ([#859](https://github.com/defenseunicorns/leapfrogai/issues/859)) ([5320890](https://github.com/defenseunicorns/leapfrogai/commit/532089087fd520121c64d331716945563509a062))
* make errors when supabase is unavailable ([#814](https://github.com/defenseunicorns/leapfrogai/issues/814)) ([976635c](https://github.com/defenseunicorns/leapfrogai/commit/976635cd5c5d615cc16adcbf6d6622845ab64eca))
* **ui:** logout ([#849](https://github.com/defenseunicorns/leapfrogai/issues/849)) ([f71af5d](https://github.com/defenseunicorns/leapfrogai/commit/f71af5d6c0d6432644144f0ad090100969c69c04))
* **ui:** playwright login without keycloak ([#833](https://github.com/defenseunicorns/leapfrogai/issues/833)) ([fd1e3dd](https://github.com/defenseunicorns/leapfrogai/commit/fd1e3dd3148581307d9ccf021c94d4208d839c56))
* **whisper:** Including missing cuda dependencies required for GPU runtimes ([2aba4af](https://github.com/defenseunicorns/leapfrogai/commit/2aba4af86b37d32fbb4a8cbe73b6151e2e1c3190))


### Miscellaneous

* **api:** Adds API load testing ([#801](https://github.com/defenseunicorns/leapfrogai/issues/801)) ([67b9755](https://github.com/defenseunicorns/leapfrogai/commit/67b9755f8ff8ed2c1197efe9f22d12ace685ef82))
* **api:** Indexing performance improvements ([#799](https://github.com/defenseunicorns/leapfrogai/issues/799)) ([e679ad2](https://github.com/defenseunicorns/leapfrogai/commit/e679ad22f52cb411e47fcc01f6e3eb3d7191ffcd))
* **api:** updating api endpoints ([#817](https://github.com/defenseunicorns/leapfrogai/issues/817)) ([6ff292f](https://github.com/defenseunicorns/leapfrogai/commit/6ff292f0d3462b0a12cb0bd032ed9bdaa4077d69))
* **deps:** bump torch from 2.1.2 to 2.2.0 in /packages/text-embeddings ([#831](https://github.com/defenseunicorns/leapfrogai/issues/831)) ([22c75cb](https://github.com/defenseunicorns/leapfrogai/commit/22c75cbfb662f8f1f53d91875d9bdf5126c31900))
* make python test dependencies optional ([#815](https://github.com/defenseunicorns/leapfrogai/issues/815)) ([89ff0a6](https://github.com/defenseunicorns/leapfrogai/commit/89ff0a6a34957bbcd788250c10e28312192f0af1))
* optimize vLLM Dockerfile to reduce layer sizes ([#805](https://github.com/defenseunicorns/leapfrogai/issues/805)) ([0fec864](https://github.com/defenseunicorns/leapfrogai/commit/0fec864f5f870dee560bd60dac74bca11b219442))
* release 0.10.0 ([#864](https://github.com/defenseunicorns/leapfrogai/issues/864)) ([7e6f574](https://github.com/defenseunicorns/leapfrogai/commit/7e6f57433c0b2ea49f814906d9625f7419baecf3))
* Remove model weights from container images ([#786](https://github.com/defenseunicorns/leapfrogai/issues/786)) ([33e4efb](https://github.com/defenseunicorns/leapfrogai/commit/33e4efb3031e7fd95333c4f98d47933a8123cb2d))
* restrict daemonset to cuda compute, utility ([#836](https://github.com/defenseunicorns/leapfrogai/issues/836)) ([4bf9124](https://github.com/defenseunicorns/leapfrogai/commit/4bf9124f2019cd9c20abfc3db717de5fd5c16d95))
* set kong service to default to cluster IP ([#857](https://github.com/defenseunicorns/leapfrogai/issues/857)) ([08f1d10](https://github.com/defenseunicorns/leapfrogai/commit/08f1d109f571e6c1649261cc99da115e23675b5d))
* split e2e tests into multiple workflows ([#808](https://github.com/defenseunicorns/leapfrogai/issues/808)) ([c993ad5](https://github.com/defenseunicorns/leapfrogai/commit/c993ad5526e0bf23148e5f9ceef215abadef30fe))
* Update defenseunicorns/zarf to zarf-dev/zarf ([#832](https://github.com/defenseunicorns/leapfrogai/issues/832)) ([cc18cea](https://github.com/defenseunicorns/leapfrogai/commit/cc18ceabfedf88bf355ec4eb53b436443b9a1f3c))
* update release workflow to install necessary python deps ([#867](https://github.com/defenseunicorns/leapfrogai/issues/867)) ([1e667a4](https://github.com/defenseunicorns/leapfrogai/commit/1e667a44504e2441549c60951d8f1a1757c81864))
* **whisper:** Pass through variables down to whisper ([#840](https://github.com/defenseunicorns/leapfrogai/issues/840)) ([4e8092a](https://github.com/defenseunicorns/leapfrogai/commit/4e8092ac4fe2ba9fb369506773074e929a1a1a25))

## [0.9.2](https://github.com/defenseunicorns/leapfrogai/compare/v0.9.1...v0.9.2) (2024-07-19)


### Bug Fixes

* address Docker warning about case mismatch between 'as' and 'from'. ([#780](https://github.com/defenseunicorns/leapfrogai/issues/780)) ([a72bc94](https://github.com/defenseunicorns/leapfrogai/commit/a72bc94d96a975ca40687cf76cd525d293076102))
* disable forceRun for supabase jwt generation ([#806](https://github.com/defenseunicorns/leapfrogai/issues/806)) ([eb9b1e0](https://github.com/defenseunicorns/leapfrogai/commit/eb9b1e034eeb65b78f32263e92a1e99c421a01e2))


### Miscellaneous

* **supabase:** Increases supabase-storage file size and makes it configurable ([#775](https://github.com/defenseunicorns/leapfrogai/issues/775)) ([0c01f36](https://github.com/defenseunicorns/leapfrogai/commit/0c01f3628aa770dcd29b2254138f92e7dee537d9))

## [0.9.1](https://github.com/defenseunicorns/leapfrogai/compare/v0.9.0...v0.9.1) (2024-07-15)


### Bug Fixes

* fix references to architectures across various Dockerfiles ([#779](https://github.com/defenseunicorns/leapfrogai/issues/779)) ([eb3b77d](https://github.com/defenseunicorns/leapfrogai/commit/eb3b77d46cde82734628a45f548748537ced555c))

## [0.9.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.8.0...v0.9.0) (2024-07-12)


### Features

* **api:** long lived api keys ([#658](https://github.com/defenseunicorns/leapfrogai/issues/658)) ([8de7de5](https://github.com/defenseunicorns/leapfrogai/commit/8de7de571d58b52683615860388fb848ebd0acb7))
* **api:** set api variable to expose by default ([#768](https://github.com/defenseunicorns/leapfrogai/issues/768)) ([310a735](https://github.com/defenseunicorns/leapfrogai/commit/310a7352bcf8f5933cc3b5dac775333bc31b78b7))
* **api:** Support Uploading PowerPoint Files for RAG ([#733](https://github.com/defenseunicorns/leapfrogai/issues/733)) ([612126d](https://github.com/defenseunicorns/leapfrogai/commit/612126d0541a6ad0cc2215bf57227a89663ab648))
* **api:** transcription/translation endpoints ([#726](https://github.com/defenseunicorns/leapfrogai/issues/726)) ([a62b07e](https://github.com/defenseunicorns/leapfrogai/commit/a62b07e7e053cce92302286722ba26373214d5cc))
* **ui:** API Keys ([#729](https://github.com/defenseunicorns/leapfrogai/issues/729)) ([1fa59ee](https://github.com/defenseunicorns/leapfrogai/commit/1fa59ee3465f0b6aaa4be7271965def9fba9820d))


### Bug Fixes

* **api:** bump max tokens to maximum for Synthia-7B to prevent chopping ([#699](https://github.com/defenseunicorns/leapfrogai/issues/699)) ([ef7e098](https://github.com/defenseunicorns/leapfrogai/commit/ef7e09802b00cc46b6fe350ed4d701ee710a9433))
* **api:** type-checking embedding list[str] ([#773](https://github.com/defenseunicorns/leapfrogai/issues/773)) ([a7030ad](https://github.com/defenseunicorns/leapfrogai/commit/a7030ad4f7abf6a2e902e4dca45f3e04f24c6fc7))


### Miscellaneous

* [#491](https://github.com/defenseunicorns/leapfrogai/issues/491) support arm64 (Apple Silicon) ([#659](https://github.com/defenseunicorns/leapfrogai/issues/659)) ([adf3334](https://github.com/defenseunicorns/leapfrogai/commit/adf3334e1fa0bc3f62895de25e60ebf2e8e3a27a))
* **api:** raise exception on CRUD base fails ([#748](https://github.com/defenseunicorns/leapfrogai/issues/748)) ([4d8ff03](https://github.com/defenseunicorns/leapfrogai/commit/4d8ff03a2efb7326e02a02bc915d95d684a39859))
* **deps-dev:** bump braces from 3.0.2 to 3.0.3 in /website ([#612](https://github.com/defenseunicorns/leapfrogai/issues/612)) ([ead5d49](https://github.com/defenseunicorns/leapfrogai/commit/ead5d49d9d1e88c9594fbfe852f815d909a69429))
* **deps:** bump llama-cpp-python in /packages/llama-cpp-python ([#574](https://github.com/defenseunicorns/leapfrogai/issues/574)) ([10b288e](https://github.com/defenseunicorns/leapfrogai/commit/10b288e3739cfc6ac8b993210de8931ed54067ea))
* **deps:** bump tqdm in /packages/text-embeddings ([#470](https://github.com/defenseunicorns/leapfrogai/issues/470)) ([d1e42d9](https://github.com/defenseunicorns/leapfrogai/commit/d1e42d9296f6e014ffbbcec2ba295443b1675567))
* **docs:** Add documentation to types ([#680](https://github.com/defenseunicorns/leapfrogai/issues/680)) ([9f7f68b](https://github.com/defenseunicorns/leapfrogai/commit/9f7f68b5e55579fefa4b5ee278b3401d564de19a))
* Fill in package READMEs and update docs ([#660](https://github.com/defenseunicorns/leapfrogai/issues/660)) ([7dab8bd](https://github.com/defenseunicorns/leapfrogai/commit/7dab8bd7934b573a77c6fed2be5d6b1d0417a246))
* Standardize package vars relating to domain names ([#770](https://github.com/defenseunicorns/leapfrogai/issues/770)) ([19ce48a](https://github.com/defenseunicorns/leapfrogai/commit/19ce48aa6ddabe39d95c25a58c85eafd2b4ee4ce))
* **test:** Create Testing Strategy ADR ([#586](https://github.com/defenseunicorns/leapfrogai/issues/586)) ([4e8fb18](https://github.com/defenseunicorns/leapfrogai/commit/4e8fb18d955d5bdcf0a03eeaefd27ebfed30a93b))

## [0.8.0](https://github.com/defenseunicorns/leapfrogai/compare/v0.7.2...v0.8.0) (2024-06-18)


### Features

* Add ability edit delete assistants within the UI ([#510](https://github.com/defenseunicorns/leapfrogai/issues/510)) ([e8408b7](https://github.com/defenseunicorns/leapfrogai/commit/e8408b75468902861a41c11060ae4d0b138f24ad))
* **API:** Add authentication ([#533](https://github.com/defenseunicorns/leapfrogai/issues/533)) ([a634a59](https://github.com/defenseunicorns/leapfrogai/commit/a634a59d011fbbd2a355458e3bad711af16cb5df))
* **api:** assistants endpoint ([#424](https://github.com/defenseunicorns/leapfrogai/issues/424)) ([0c483a1](https://github.com/defenseunicorns/leapfrogai/commit/0c483a1fd1848836bb1d964d0f1c831c26957ea6))
* **api:** Runs endpoints ([#583](https://github.com/defenseunicorns/leapfrogai/issues/583)) ([fecf0f8](https://github.com/defenseunicorns/leapfrogai/commit/fecf0f8e6d163cf8e28237639cf1bf250d552398))
* **api:** Threads and Message Endpoints ([#554](https://github.com/defenseunicorns/leapfrogai/issues/554)) ([4b69d3c](https://github.com/defenseunicorns/leapfrogai/commit/4b69d3c7713a6924d846afb60a72486135c4be30))
* **api:** vector store endpoints ([#468](https://github.com/defenseunicorns/leapfrogai/issues/468)) ([2cc0737](https://github.com/defenseunicorns/leapfrogai/commit/2cc07376fca20d491a15a5c1fddc317f3bacdfad))
* **ui:** 531 file management ([#558](https://github.com/defenseunicorns/leapfrogai/issues/558)) ([884761b](https://github.com/defenseunicorns/leapfrogai/commit/884761b06dde49bb701cc25678fefd03248cd102))
* **ui:** Utilize OpenAI for backend ([#553](https://github.com/defenseunicorns/leapfrogai/issues/553)) ([5371956](https://github.com/defenseunicorns/leapfrogai/commit/5371956867d6a98196e22ec24574f885c25bce80))


### Bug Fixes

* **api:** Migrations ([#606](https://github.com/defenseunicorns/leapfrogai/issues/606)) ([e91e525](https://github.com/defenseunicorns/leapfrogai/commit/e91e5254482e447c1ec876c762c217aae5178e25))
* **build:** supabase bundle deployment order ([#635](https://github.com/defenseunicorns/leapfrogai/issues/635)) ([c1a8294](https://github.com/defenseunicorns/leapfrogai/commit/c1a8294a2896795354c93fd442f24f1db6ed584a))
* handle database permissions errors and workflow exceptions ([#609](https://github.com/defenseunicorns/leapfrogai/issues/609)) ([e910f06](https://github.com/defenseunicorns/leapfrogai/commit/e910f06bcf8a568717a3e7deac74b2ec1ebd04d0))
* tool resources validation ([#654](https://github.com/defenseunicorns/leapfrogai/issues/654)) ([d2cbb09](https://github.com/defenseunicorns/leapfrogai/commit/d2cbb091129398ecab197ffae84adca6af22f638))
* update README table of contents and formatting ([#653](https://github.com/defenseunicorns/leapfrogai/issues/653)) ([cd7e2a6](https://github.com/defenseunicorns/leapfrogai/commit/cd7e2a6d2c0857bf14edf68fff86108ca7d85fd3))
* update the keycloak url that supabase redirects to ([#535](https://github.com/defenseunicorns/leapfrogai/issues/535)) ([541c7bd](https://github.com/defenseunicorns/leapfrogai/commit/541c7bdf82aa8dc94dbb1113ecfeb0f075f5b260))


### Miscellaneous

* Add RAG Evals Toolset ADR ([#529](https://github.com/defenseunicorns/leapfrogai/issues/529)) ([840f49a](https://github.com/defenseunicorns/leapfrogai/commit/840f49a1ecc7695fb96afd35c5a6c2097a77c581))
* Add Supabase Migrations Documentation ([#592](https://github.com/defenseunicorns/leapfrogai/issues/592)) ([c1105b9](https://github.com/defenseunicorns/leapfrogai/commit/c1105b936c13f8ca715d7d1c08b3cc3c909e2902))
* Backwards compatible migration support ([#618](https://github.com/defenseunicorns/leapfrogai/issues/618)) ([3b91e7f](https://github.com/defenseunicorns/leapfrogai/commit/3b91e7f378e2513b73765d0b874e345656224ddd))
* better database migrations - managed by supabase ([#570](https://github.com/defenseunicorns/leapfrogai/issues/570)) ([ce6512f](https://github.com/defenseunicorns/leapfrogai/commit/ce6512f3731c508ff5a771ba203c852ddbd59985))
* group 'minor' and 'patch' level npm dependency updates ([#547](https://github.com/defenseunicorns/leapfrogai/issues/547)) ([064cb84](https://github.com/defenseunicorns/leapfrogai/commit/064cb84de7e6711487ffd4b9513b09135cbbf1d4))
* Handle migrations with least permissions necessary ([#630](https://github.com/defenseunicorns/leapfrogai/issues/630)) ([37badae](https://github.com/defenseunicorns/leapfrogai/commit/37badaeeee7d41e8dace24b94c0e52ac96594e59))
* remove unused requirements.txt file ([#546](https://github.com/defenseunicorns/leapfrogai/issues/546)) ([e71e74f](https://github.com/defenseunicorns/leapfrogai/commit/e71e74fc23b68895ceaddc743db3d4386aa59d7a))

## [0.7.2](https://github.com/defenseunicorns/leapfrogai/compare/v0.7.1...v0.7.2) (2024-05-15)


### Bug Fixes

* use zarf vendored kubectl during supabase deployment ([#517](https://github.com/defenseunicorns/leapfrogai/issues/517)) ([c236d39](https://github.com/defenseunicorns/leapfrogai/commit/c236d39a62694d7750ebe562b2f55dcafc238d34))

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
