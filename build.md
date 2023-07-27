# Building

`docker build --tag leapfrogai/mpt-7b-chat:0.3.2 --build-arg="IMAGE_TAG=0.3.2" .`

`docker build --tag chat-ui-local -f Dockerfile-local .`
 
## ChatGPT Ingress Notes

how do I write a kubernetes ingress for a web application that has multiple routes?  My current setup will show the first page of the application but all of the links that should invoke calls to the backend on the page (like clicking buttons) don't work and I'm not seeing any traffic in the backend logs 
ChatGPT

Writing a Kubernetes Ingress for a web application with multiple routes involves defining the rules and paths to forward incoming requests to the appropriate backend services. If you're facing issues with some links not working and no traffic reaching the backend, there could be a few reasons for it. Let's go through the steps to create an Ingress resource and address some common troubleshooting points:

    Verify your backend services: First, ensure that your backend services are running and reachable. You can check their status using kubectl get services.

    Check your backend service routes: Verify that the backend service routes are correctly configured and accessible within the cluster.

    Validate the frontend application: Ensure that the frontend application is properly configured to send requests to the backend services. You can check the developer console in your browser for any errors related to failed API calls.

    Debug your Ingress configuration: Here's a general outline of how to create an Ingress resource for a web application with multiple routes:

    a. Create or ensure you have services running for both your frontend and backend applications.

    b. Define the Ingress resource, specifying the rules and paths for routing:

yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  rules:
    - host: your.domain.com   # Replace with your actual domain or IP
      http:
        paths:
          - path: /            # This is the root path
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80     # Replace with the correct frontend service port
          - path: /api/         # This is the path for backend API calls
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 80     # Replace with the correct backend service port

    Apply the Ingress resource:

bash

kubectl apply -f your-ingress-file.yaml

    Verify the Ingress:

bash

kubectl get ingress my-app-ingress

    Check for any errors:

bash

kubectl describe ingress my-app-ingress

    Check backend service logs: If everything looks fine with your Ingress resource, check your backend service logs to see if they are receiving any traffic when you access your application.

Keep in mind that this is a general outline, and your setup might require some additional configurations or modifications depending on your specific application and environment.

Remember to replace your.domain.com, frontend-service, and backend-service with the appropriate values from your setup. Additionally, make sure your frontend application is properly configured to make API calls to the backend using the correct URLs and ports.

If you are still facing issues, it's helpful to check the logs of your frontend application and your Ingress controller for any errors or misconfigurations. If you can provide more specific details about your application, Ingress configuration, and any error messages you encounter, I can assist you further in troubleshooting the problem.

## Leapfrog logs

Model name: leapfrogai/mpt-7b-chat

http://localhost:8080/openai/v1/models

Model list json

## Dockerfiles and logs

### No Mongo

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npm run dev`

```shell
> chat-ui@0.3.0 dev
> vite dev

HTTP 7650: call onSocket 0 0
HTTP 7650: createConnection registry.npmjs.org:443::::::::true::::::::::::: [Object: null prototype] {
  auth: '',
  host: 'registry.npmjs.org',
  hostname: 'registry.npmjs.org',
  path: null,
  port: 443,
  protocol: 'https:',
  method: 'GET',
  headers: [Object: null prototype] {
    accept: [
      'application/vnd.npm.install-v1+json; q=1.0, application/json; q=0.8, */*'
    ],
    'npm-auth-type': [ 'web' ],
    'npm-command': [ 'run-script' ],
    'pacote-pkg-id': [ 'registry:npm' ],
    'pacote-req-type': [ 'packument' ],
    'pacote-version': [ '15.2.0' ],
    'user-agent': [ 'npm/9.8.0 node/v20.5.0 linux x64 workspaces/false' ],
    'if-none-match': [ '"702951134d8aada94625c90f117321bd"' ],
    'if-modified-since': [ 'Wed, 05 Jul 2023 20:29:17 GMT' ],
    connection: [ 'keep-alive' ],
    'Accept-Encoding': [ 'gzip,deflate' ]
  },
  agent: HttpsAgent {
    _events: [Object: null prototype] {
      free: [Array],
      newListener: [Function: maybeEnableKeylog]
    },
    _eventsCount: 2,
    _maxListeners: undefined,
    defaultPort: 443,
    protocol: 'https:',
    options: [Object: null prototype] {
      maxSockets: 15,
      ca: null,
      cert: null,
      key: null,
      localAddress: null,
      rejectUnauthorized: true,
      timeout: 300001,
      freeSocketTimeout: 15000,
      lookup: [Function (anonymous)],
      keepAlive: true,
      socketActiveTTL: 0,
      noDelay: true,
      path: null
    },
    requests: [Object: null prototype] {},
    sockets: [Object: null prototype] {
      'registry.npmjs.org:443::::::::true:::::::::::::': []
    },
    freeSockets: [Object: null prototype] {},
    keepAliveMsecs: 1000,
    keepAlive: true,
    maxSockets: 15,
    maxFreeSockets: 256,
    scheduling: 'lifo',
    maxTotalSockets: Infinity,
    totalSocketCount: 0,
    createSocketCount: 0,
    createSocketCountLastCheck: 0,
    createSocketErrorCount: 0,
    createSocketErrorCountLastCheck: 0,
    closeSocketCount: 0,
    closeSocketCountLastCheck: 0,
    errorSocketCount: 0,
    errorSocketCountLastCheck: 0,
    requestCount: 0,
    requestCountLastCheck: 0,
    timeoutSocketCount: 0,
    timeoutSocketCountLastCheck: 0,
    maxCachedSessions: 100,
    _sessionCache: { map: {}, list: [] },
    [Symbol(kCapture)]: false,
    [Symbol(agentkeepalive#currentId)]: 0
  },
  ca: null,
  cert: null,
  ciphers: undefined,
  clientCertEngine: undefined,
  crl: undefined,
  dhparam: undefined,
  ecdhCurve: undefined,
  family: undefined,
  honorCipherOrder: undefined,
  key: null,
  passphrase: undefined,
  pfx: undefined,
  rejectUnauthorized: true,
  secureOptions: undefined,
  secureProtocol: undefined,
  servername: 'registry.npmjs.org',
  sessionIdContext: undefined,
  timeout: 300001,
  _defaultAgent: Agent {
    _events: [Object: null prototype] {
      free: [Function (anonymous)],
      newListener: [Function: maybeEnableKeylog]
    },
    _eventsCount: 2,
    _maxListeners: undefined,
    defaultPort: 443,
    protocol: 'https:',
    options: [Object: null prototype] {
      keepAlive: true,
      scheduling: 'lifo',
      timeout: 5000,
      noDelay: true,
      path: null
    },
    requests: [Object: null prototype] {},
    sockets: [Object: null prototype] {},
    freeSockets: [Object: null prototype] {},
    keepAliveMsecs: 1000,
    keepAlive: true,
    maxSockets: Infinity,
    maxFreeSockets: 256,
    scheduling: 'lifo',
    maxTotalSockets: Infinity,
    totalSocketCount: 0,
    maxCachedSessions: 100,
    _sessionCache: { map: {}, list: [] },
    [Symbol(kCapture)]: false
  },
  maxSockets: 15,
  localAddress: null,
  freeSocketTimeout: 15000,
  lookup: [Function (anonymous)],
  keepAlive: true,
  socketActiveTTL: 0,
  noDelay: true,
  _agentKey: 'registry.npmjs.org:443::::::::true:::::::::::::'
}
TLS 7650: client _init handle? true
NET 7650: pipe false null
NET 7650: connect: find host registry.npmjs.org
NET 7650: connect: dns options { family: undefined, hints: 32 }
NET 7650: connect: autodetecting
HTTP 7650: sockets registry.npmjs.org:443::::::::true::::::::::::: 1 1
HTTP 7650: outgoing message end.
(node:7650) Warning: Setting the NODE_DEBUG environment variable to 'http' can expose sensitive data (such as passwords, tokens and authentication headers) in the resulting log.
(Use `node --trace-warnings ...` to show where the warning was created)
TLS 7650: client initRead handle? true buffered? false
NET 7650: _read - n 16384 isConnecting? true hasHandle? true
NET 7650: _read wait for connection
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: Socket._handle.readStart
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: connect/multiple: will try the following addresses [
  { address: '2606:4700::6810:1a22', family: 6 },
  { address: '104.16.28.34', family: 4 },
  { address: '2606:4700::6810:1922', family: 6 },
  { address: '104.16.31.34', family: 4 },
  { address: '2606:4700::6810:1c22', family: 6 },
  { address: '104.16.30.34', family: 4 },
  { address: '2606:4700::6810:123', family: 6 },
  { address: '104.16.3.35', family: 4 },
  { address: '2606:4700::6810:323', family: 6 },
  { address: '104.16.24.34', family: 4 },
  { address: '2606:4700::6810:223', family: 6 },
  { address: '104.16.26.34', family: 4 },
  { address: '2606:4700::6810:1e22', family: 6 },
  { address: '104.16.27.34', family: 4 },
  { address: '2606:4700::6810:1822', family: 6 },
  { address: '104.16.29.34', family: 4 },
  { address: '2606:4700::6810:23', family: 6 },
  { address: '104.16.2.35', family: 4 },
  { address: '2606:4700::6810:1b22', family: 6 },
  { address: '104.16.25.34', family: 4 },
  { address: '2606:4700::6810:1d22', family: 6 },
  { address: '104.16.0.35', family: 4 },
  { address: '2606:4700::6810:1f22', family: 6 },
  { address: '104.16.1.35', family: 4 }
]
NET 7650: connect/multiple: attempting to connect to 2606:4700::6810:1a22:443 (addressType: 6)
NET 7650: connect/multiple: setting the attempt timeout to 250 ms
NET 7650: connect/multiple: connection attempt to 2606:4700::6810:1a22:443 completed with status 0
NET 7650: afterConnect
TLS 7650: client _start handle? true connecting? false requestOCSP? false
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: Socket._handle.readStart
TLS 7650: client emit session
TLS 7650: client onhandshakedone
TLS 7650: client _finishInit handle? true alpn false servername registry.npmjs.org
TLS 7650: client emit secureConnect. authorized: true
HTTP 7650: AGENT incoming response!
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
HTTP 7650: AGENT socket keep-alive
NET 7650: _read - n 16384 isConnecting? false hasHandle? true
HTTP 7650: CLIENT socket onFree
HTTP 7650: agent.on(free) registry.npmjs.org:443::::::::true:::::::::::::
HTTP 7650: removeSocket registry.npmjs.org:443::::::::true::::::::::::: writable: true

NET 7667: setupListenHandle 127.0.0.1 5173 4 false undefined
NET 7667: setupListenHandle: create a handle
NET 7667: bind to 127.0.0.1
NET 7667: _read - n 16384 isConnecting? false hasHandle? true

  VITE v4.3.5  ready in 784 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
NET 7667: _read - n 0 isConnecting? false hasHandle? true
NET 7667: Socket._handle.readStart
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7650: _onTimeout
NET 7650: destroy
NET 7650: close
NET 7650: close handle
HTTP 7650: removeSocket registry.npmjs.org:443::::::::true::::::::::::: writable: false
HTTP 7650: CLIENT socket onTimeout
NET 7650: emit close
HTTP 7650: CLIENT socket onClose
HTTP 7650: removeSocket registry.npmjs.org:443::::::::true::::::::::::: writable: false
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: _read - n 16384 isConnecting? false hasHandle? true
NET 7667: SERVER _emitCloseIfDrained
NET 7667: SERVER: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npm run preview`

```shell
> chat-ui@0.3.0 preview
> vite preview

NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: Socket._handle.readStart
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: _read - n 16384 isConnecting? false hasHandle? true

NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: setupListenHandle 127.0.0.1 4173 4 false undefined
NET 8174: setupListenHandle: create a handle
NET 8174: bind to 127.0.0.1
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
  ➜  Local:   http://localhost:4173/
  ➜  Network: use --host to expose
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
NET 8174: _read - n 16384 isConnecting? false hasHandle? true
NET 8174: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8174: pipe false undefined
NET 8174: connect: find host localhost
NET 8174: connect: dns options { family: undefined, hints: 32 }
NET 8174: connect: autodetecting
NET 8174: connect/multiple: only one address found, switching back to single connection
NET 8174: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8174: afterConnect
NET 8174: destroy
NET 8174: close
NET 8174: close handle
NET 8174: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers node build`

```shell
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: setupListenHandle 0.0.0.0 3000 4 0 undefined
NET 8250: setupListenHandle: create a handle
NET 8250: bind to 0.0.0.0
Listening on 0.0.0.0:3000
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
NET 8250: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8250: pipe false undefined
NET 8250: connect: find host localhost
NET 8250: connect: dns options { family: undefined, hints: 32 }
NET 8250: connect: autodetecting
NET 8250: connect/multiple: only one address found, switching back to single connection
NET 8250: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8250: afterConnect
NET 8250: destroy
NET 8250: close
NET 8250: close handle
NET 8250: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers node build --host 0.0.0.0 --port 3000`

```shell
NET 8282: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8282: pipe false undefined
NET 8282: connect: find host localhost
NET 8282: connect: dns options { family: undefined, hints: 32 }
NET 8282: connect: autodetecting
NET 8282: setupListenHandle 0.0.0.0 3000 4 0 undefined
NET 8282: setupListenHandle: create a handle
NET 8282: bind to 0.0.0.0
Listening on 0.0.0.0:3000
NET 8282: connect/multiple: only one address found, switching back to single connection
NET 8282: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8282: afterConnect
NET 8282: destroy
NET 8282: close
NET 8282: close handle
NET 8282: emit close
NET 8282: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8282: pipe false undefined
NET 8282: connect: find host localhost
NET 8282: connect: dns options { family: undefined, hints: 32 }
NET 8282: connect: autodetecting
NET 8282: connect/multiple: only one address found, switching back to single connection
NET 8282: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8282: afterConnect
NET 8282: destroy
NET 8282: close
NET 8282: close handle
NET 8282: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite --host 0.0.0.0 --port 3000`

```shell
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: Socket._handle.readStart
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true

NET 8496: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 8496: setupListenHandle: create a handle
NET 8496: bind to 0.0.0.0

  VITE v4.3.5  ready in 478 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.22.0.1:3000/
  ➜  press h to show help
NET 8496: _read - n 0 isConnecting? false hasHandle? true
NET 8496: Socket._handle.readStart
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: _read - n 16384 isConnecting? false hasHandle? true
NET 8496: SERVER _emitCloseIfDrained
NET 8496: SERVER: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite preview --host 0.0.0.0 --port 3000`

```shell
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: Socket._handle.readStart
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: _read - n 16384 isConnecting? false hasHandle? true

NET 8624: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8624: pipe false undefined
NET 8624: connect: find host localhost
NET 8624: connect: dns options { family: undefined, hints: 32 }
NET 8624: connect: autodetecting
NET 8624: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 8624: setupListenHandle: create a handle
NET 8624: bind to 0.0.0.0
  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.22.0.1:3000/
NET 8624: connect/multiple: only one address found, switching back to single connection
NET 8624: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8624: afterConnect
NET 8624: destroy
NET 8624: close
NET 8624: close handle
NET 8624: emit close
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
NET 8624: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8624: pipe false undefined
NET 8624: connect: find host localhost
NET 8624: connect: dns options { family: undefined, hints: 32 }
NET 8624: connect: autodetecting
NET 8624: connect/multiple: only one address found, switching back to single connection
NET 8624: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8624: afterConnect
NET 8624: destroy
NET 8624: close
NET 8624: close handle
NET 8624: emit close
NET 8624: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 8624: pipe false undefined
NET 8624: connect: find host localhost
NET 8624: connect: dns options { family: undefined, hints: 32 }
NET 8624: connect: autodetecting
NET 8624: connect/multiple: only one address found, switching back to single connection
NET 8624: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 8624: afterConnect
NET 8624: destroy
NET 8624: close
NET 8624: close handle
NET 8624: emit close
NET 8624: _read - n 16384 isConnecting? false hasHandle? true
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite dev --host 0.0.0.0 --port 3000`

```shell
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: Socket._handle.readStart
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true

NET 8692: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 8692: setupListenHandle: create a handle
NET 8692: bind to 0.0.0.0

  VITE v4.3.5  ready in 472 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.22.0.1:3000/
  ➜  press h to show help
NET 8692: _read - n 0 isConnecting? false hasHandle? true
NET 8692: Socket._handle.readStart
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: _read - n 16384 isConnecting? false hasHandle? true
NET 8692: SERVER _emitCloseIfDrained
NET 8692: SERVER: emit close
```

### With mongo running on localhost:27017

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npm run dev`

```shell
> chat-ui@0.3.0 dev
> vite dev

NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: Socket._handle.readStart
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true

NET 33069: setupListenHandle 127.0.0.1 5173 4 false undefined
NET 33069: setupListenHandle: create a handle
NET 33069: bind to 127.0.0.1

  VITE v4.3.5  ready in 488 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
NET 33069: _read - n 0 isConnecting? false hasHandle? true
NET 33069: Socket._handle.readStart
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: _read - n 16384 isConnecting? false hasHandle? true
NET 33069: SERVER _emitCloseIfDrained
NET 33069: SERVER: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npm run preview`

```shell
> chat-ui@0.3.0 preview
> vite preview

NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true

NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: setupListenHandle 127.0.0.1 4173 4 false undefined
NET 33167: setupListenHandle: create a handle
NET 33167: bind to 127.0.0.1
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
  ➜  Local:   http://localhost:4173/
  ➜  Network: use --host to expose
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33167: pipe false undefined
NET 33167: connect: find host localhost
NET 33167: connect: dns options { family: undefined, hints: 32 }
NET 33167: connect: autodetecting
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: connect/multiple: only one address found, switching back to single connection
NET 33167: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: afterConnect
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: Socket._handle.readStart
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
NET 33167: _read - n 16384 isConnecting? false hasHandle? true
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers node build`

```shell
NODE_DEBUG=cluster,net,http,fs,tls,timers node build                      ─╯
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: setupListenHandle 0.0.0.0 3000 4 0 undefined
NET 33226: setupListenHandle: create a handle
NET 33226: bind to 0.0.0.0
Listening on 0.0.0.0:3000
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33226: pipe false undefined
NET 33226: connect: find host localhost
NET 33226: connect: dns options { family: undefined, hints: 32 }
NET 33226: connect: autodetecting
NET 33226: connect/multiple: only one address found, switching back to single connection
NET 33226: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33226: afterConnect
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: Socket._handle.readStart
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
NET 33226: _read - n 16384 isConnecting? false hasHandle? true
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers node build --host 0.0.0.0 --port 3000`

These logs include a single request to the web page in the browser to demonstrate what that looks like

```shell
NODE_DEBUG=cluster,net,http,fs,tls,timers node build --host 0.0.0.0 --port 3000                            ─╯
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: setupListenHandle 0.0.0.0 3000 4 0 undefined
NET 33875: setupListenHandle: create a handle
NET 33875: bind to 0.0.0.0
Listening on 0.0.0.0:3000
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: onconnection
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
HTTP 33875: SERVER new http connection
(node:33875) Warning: Setting the NODE_DEBUG environment variable to 'http' can expose sensitive data (such as passwords, tokens and authentication headers) in the resulting log.
(Use `node --trace-warnings ...` to show where the warning was created)
HTTP 33875: SERVER socketOnParserExecute 523
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33875: write ret = false
HTTP 33875: outgoing message end.
NET 33875: onconnection
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
HTTP 33875: SERVER new http connection
HTTP 33875: SERVER socketOnParserExecute NaN
HTTP 33875: parse error [Error: Parse Error: Invalid method encountered] {
  bytesParsed: 0,
  code: 'HPE_INVALID_METHOD',
  reason: 'Invalid method encountered',
  rawPacket: <Buffer 16 03 01 02 00 01 00 01 fc 03 03 ed 54 8b 1d a4 f4 1d 92 2b 0b c0 69 52 b7 b9 74 3e ec f3 c4 6c 69 bb 43 1c 88 5a 45 4f 74 8f e2 20 47 9b 26 43 e7 db ... 467 more bytes>
}
NET 33875: destroy
NET 33875: close
NET 33875: close handle
NET 33875: has server
NET 33875: SERVER _emitCloseIfDrained
NET 33875: SERVER handle? true   connections? 1
NET 33875: emit close
HTTP 33875: server socket close
NET 33875: onconnection
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
HTTP 33875: SERVER new http connection
HTTP 33875: SERVER socketOnParserExecute NaN
HTTP 33875: parse error [Error: Parse Error: Invalid method encountered] {
  bytesParsed: 0,
  code: 'HPE_INVALID_METHOD',
  reason: 'Invalid method encountered',
  rawPacket: <Buffer 16 03 01 02 00 01 00 01 fc 03 03 eb 0f 4a ef bc b9 fa 4d f6 fb 5c 1d 4c 40 07 d9 21 eb c1 db 37 f5 e6 b1 0f 50 5a cb ab 78 10 35 20 45 54 9e 8d 49 02 ... 467 more bytes>
}
NET 33875: destroy
NET 33875: close
NET 33875: close handle
NET 33875: has server
NET 33875: SERVER _emitCloseIfDrained
NET 33875: SERVER handle? true   connections? 1
NET 33875: emit close
HTTP 33875: server socket close
NET 33875: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33875: pipe false undefined
NET 33875: connect: find host localhost
NET 33875: connect: dns options { family: undefined, hints: 32 }
NET 33875: connect: autodetecting
NET 33875: connect/multiple: only one address found, switching back to single connection
NET 33875: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33875: afterConnect
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: Socket._handle.readStart
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
NET 33875: _read - n 16384 isConnecting? false hasHandle? true
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite --host 0.0.0.0 --port 3000`

This example includes a single page refresh and two clicks of the model selection dropdown

```shell
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true

NET 33988: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 33988: setupListenHandle: create a handle
NET 33988: bind to 0.0.0.0

  VITE v4.3.5  ready in 484 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.17.0.1:3000/
  ➜  Network: http://172.22.0.1:3000/
  ➜  press h to show help
NET 33988: _read - n 0 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
(node:33988) Warning: Setting the NODE_DEBUG environment variable to 'http' can expose sensitive data (such as passwords, tokens and authentication headers) in the resulting log.
(Use `node --trace-warnings ...` to show where the warning was created)
HTTP 33988: SERVER socketOnParserExecute 523
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 454
HTTP 33988: SERVER socketOnParserExecute 479
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 499
HTTP 33988: SERVER socketOnParserExecute 520
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
HTTP 33988: SERVER socketOnParserExecute 524
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
HTTP 33988: SERVER socketOnParserExecute 519
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 512
HTTP 33988: SERVER socketOnParserExecute 520
HTTP 33988: SERVER socketOnParserExecute 535
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: SERVER socketOnParserExecute 510
HTTP 33988: SERVER socketOnParserExecute 520
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
HTTP 33988: SERVER socketOnParserExecute 533
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 541
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 531
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 494
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 525
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 526
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 511
HTTP 33988: SERVER socketOnParserExecute 535
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 524
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 522
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 525
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 499
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: SERVER socketOnParserExecute 501
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 490
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 496
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 524
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 523
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 449
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 508
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 516
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 504
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 504
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 509
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 497
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 496
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 502
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
HTTP 33988: SERVER socketOnParserExecute 630
HTTP 33988: SERVER upgrade or connect GET
HTTP 33988: SERVER have listener for upgrade
HTTP 33988: SERVER socketOnParserExecute 518
HTTP 33988: SERVER socketOnParserExecute 518
HTTP 33988: SERVER socketOnParserExecute 518
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 464
HTTP 33988: SERVER socketOnParserExecute 463
HTTP 33988: SERVER socketOnParserExecute 462
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 487
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 490
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 485
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 464
HTTP 33988: SERVER socketOnParserExecute 447
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 455
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 446
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 444
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 454
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 453
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 455
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 460
HTTP 33988: SERVER socketOnParserExecute 458
HTTP 33988: SERVER socketOnParserExecute 456
HTTP 33988: SERVER socketOnParserExecute 464
HTTP 33988: SERVER socketOnParserExecute 461
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 450
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 474
HTTP 33988: SERVER socketOnParserExecute 465
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 463
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 481
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 472
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 481
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 476
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 484
HTTP 33988: SERVER socketOnParserExecute 481
HTTP 33988: SERVER socketOnParserExecute 484
HTTP 33988: SERVER socketOnParserExecute 482
HTTP 33988: SERVER socketOnParserExecute 469
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 455
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 493
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 467
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 471
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 501
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 507
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 477
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 507
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 480
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 470
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 490
HTTP 33988: SERVER socketOnParserExecute 485
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 479
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 479
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 463
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 474
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 482
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 484
HTTP 33988: SERVER socketOnParserExecute 490
HTTP 33988: SERVER socketOnParserExecute 486
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 471
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 491
HTTP 33988: SERVER socketOnParserExecute 477
HTTP 33988: SERVER socketOnParserExecute 485
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 477
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 475
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 476
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 477
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 488
HTTP 33988: write ret = false
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: SERVER socketOnParserExecute 479
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 473
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 478
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 482
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 483
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 519
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 484
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 477
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 6
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 5
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 4
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 3
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 2
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: _onTimeout
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 1
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 33988: pipe false undefined
NET 33988: connect: find host localhost
NET 33988: connect: dns options { family: undefined, hints: 32 }
NET 33988: connect: autodetecting
NET 33988: connect/multiple: only one address found, switching back to single connection
NET 33988: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 33988: afterConnect
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: onconnection
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: Socket._handle.readStart
HTTP 33988: SERVER new http connection
HTTP 33988: SERVER socketOnParserExecute 1242
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
HTTP 33988: SERVER socketOnParserExecute 437
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
HTTP 33988: write ret = true
HTTP 33988: outgoing message end.
NET 33988: _read - n 16384 isConnecting? false hasHandle? true
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 1
NET 33988: destroy
NET 33988: close
NET 33988: close handle
NET 33988: has server
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER handle? true   connections? 0
NET 33988: SERVER _emitCloseIfDrained
NET 33988: SERVER: emit close
NET 33988: emit close
HTTP 33988: server socket close
NET 33988: emit close
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite preview --host 0.0.0.0 --port 3000`

1 refresh of the homepage

```shell
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true

NET 34132: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34132: pipe false undefined
NET 34132: connect: find host localhost
NET 34132: connect: dns options { family: undefined, hints: 32 }
NET 34132: connect: autodetecting
NET 34132: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 34132: setupListenHandle: create a handle
NET 34132: bind to 0.0.0.0
  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.17.0.1:3000/
  ➜  Network: http://172.22.0.1:3000/
NET 34132: connect/multiple: only one address found, switching back to single connection
NET 34132: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34132: afterConnect
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34132: pipe false undefined
NET 34132: connect: find host localhost
NET 34132: connect: dns options { family: undefined, hints: 32 }
NET 34132: connect: autodetecting
NET 34132: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34132: pipe false undefined
NET 34132: connect: find host localhost
NET 34132: connect: dns options { family: undefined, hints: 32 }
NET 34132: connect: autodetecting
NET 34132: connect/multiple: only one address found, switching back to single connection
NET 34132: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34132: connect/multiple: only one address found, switching back to single connection
NET 34132: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34132: afterConnect
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: afterConnect
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34132: pipe false undefined
NET 34132: connect: find host localhost
NET 34132: connect: dns options { family: undefined, hints: 32 }
NET 34132: connect: autodetecting
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34132: pipe false undefined
NET 34132: connect: find host localhost
NET 34132: connect: dns options { family: undefined, hints: 32 }
NET 34132: connect: autodetecting
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: connect/multiple: only one address found, switching back to single connection
NET 34132: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34132: connect/multiple: only one address found, switching back to single connection
NET 34132: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: afterConnect
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: afterConnect
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: onconnection
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: Socket._handle.readStart
HTTP 34132: SERVER new http connection
(node:34132) Warning: Setting the NODE_DEBUG environment variable to 'http' can expose sensitive data (such as passwords, tokens and authentication headers) in the resulting log.
(Use `node --trace-warnings ...` to show where the warning was created)
HTTP 34132: SERVER socketOnParserExecute 428
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34132: write ret = true
HTTP 34132: write ret = true
HTTP 34132: outgoing message end.
HTTP 34132: SERVER socketOnParserExecute 509
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34132: outgoing message end.
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34132: SERVER socketOnParserExecute 523
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34132: outgoing message end.
NET 34132: _read - n 16384 isConnecting? false hasHandle? true
^C
```

#### `NODE_DEBUG=cluster,net,http,fs,tls,timers npx vite dev --host 0.0.0.0 --port 3000`

Includes single page refresh

```shell
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true

NET 34203: setupListenHandle 0.0.0.0 3000 4 false undefined
NET 34203: setupListenHandle: create a handle
NET 34203: bind to 0.0.0.0

  VITE v4.3.5  ready in 477 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.156:3000/
  ➜  Network: http://172.17.0.1:3000/
  ➜  Network: http://172.22.0.1:3000/
  ➜  press h to show help
NET 34203: _read - n 0 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
(node:34203) Warning: Setting the NODE_DEBUG environment variable to 'http' can expose sensitive data (such as passwords, tokens and authentication headers) in the resulting log.
(Use `node --trace-warnings ...` to show where the warning was created)
HTTP 34203: SERVER socketOnParserExecute 476
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34203: pipe false undefined
NET 34203: connect: find host localhost
NET 34203: connect: dns options { family: undefined, hints: 32 }
NET 34203: connect: autodetecting
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: connect/multiple: only one address found, switching back to single connection
NET 34203: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34203: afterConnect
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34203: pipe false undefined
NET 34203: connect: find host localhost
NET 34203: connect: dns options { family: undefined, hints: 32 }
NET 34203: connect: autodetecting
NET 34203: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34203: pipe false undefined
NET 34203: connect: find host localhost
NET 34203: connect: dns options { family: undefined, hints: 32 }
NET 34203: connect: autodetecting
NET 34203: connect/multiple: only one address found, switching back to single connection
NET 34203: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34203: connect/multiple: only one address found, switching back to single connection
NET 34203: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: afterConnect
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: afterConnect
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34203: pipe false undefined
NET 34203: connect: find host localhost
NET 34203: connect: dns options { family: undefined, hints: 32 }
NET 34203: connect: autodetecting
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: createConnection [
  { host: 'localhost', port: 27017 },
  null,
  [Symbol(normalizedArgs)]: true
]
NET 34203: pipe false undefined
NET 34203: connect: find host localhost
NET 34203: connect: dns options { family: undefined, hints: 32 }
NET 34203: connect: autodetecting
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: connect/multiple: only one address found, switching back to single connection
NET 34203: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34203: connect/multiple: only one address found, switching back to single connection
NET 34203: connect: attempting to connect to 127.0.0.1:27017 (addressType: 4)
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: afterConnect
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: afterConnect
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 523
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 506
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 499
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 520
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
HTTP 34203: SERVER socketOnParserExecute 524
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
HTTP 34203: SERVER socketOnParserExecute 497
HTTP 34203: SERVER socketOnParserExecute 570
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 565
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 520
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 535
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: SERVER socketOnParserExecute 510
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
HTTP 34203: SERVER socketOnParserExecute 533
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 545
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 541
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 520
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 526
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 525
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 511
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 535
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 522
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 524
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 525
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 502
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 502
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 486
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 501
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 490
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 496
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 550
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 524
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 523
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 508
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 516
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 501
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 504
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
NET 34203: onconnection
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: Socket._handle.readStart
HTTP 34203: SERVER new http connection
HTTP 34203: SERVER socketOnParserExecute 630
HTTP 34203: SERVER upgrade or connect GET
HTTP 34203: SERVER have listener for upgrade
HTTP 34203: SERVER socketOnParserExecute 504
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 509
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 569
HTTP 34203: SERVER socketOnParserExecute 569
HTTP 34203: SERVER socketOnParserExecute 569
HTTP 34203: outgoing message end.
HTTP 34203: outgoing message end.
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 517
HTTP 34203: SERVER socketOnParserExecute 516
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 515
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 490
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 485
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 517
HTTP 34203: SERVER socketOnParserExecute 499
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 506
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 497
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 487
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 498
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 506
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 505
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 506
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 513
HTTP 34203: SERVER socketOnParserExecute 511
HTTP 34203: SERVER socketOnParserExecute 509
HTTP 34203: SERVER socketOnParserExecute 517
HTTP 34203: SERVER socketOnParserExecute 514
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 501
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 533
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 486
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 527
HTTP 34203: SERVER socketOnParserExecute 517
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 515
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 530
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 524
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 533
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 528
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 537
HTTP 34203: SERVER socketOnParserExecute 537
HTTP 34203: SERVER socketOnParserExecute 535
HTTP 34203: SERVER socketOnParserExecute 522
HTTP 34203: SERVER socketOnParserExecute 534
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 507
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 546
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 520
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 524
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 507
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 501
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 559
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 522
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 529
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 529
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 532
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 539
HTTP 34203: SERVER socketOnParserExecute 543
HTTP 34203: SERVER socketOnParserExecute 538
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 531
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 526
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 482
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 516
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
HTTP 34203: write ret = false
HTTP 34203: outgoing message end.
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
NET 34203: _read - n 16384 isConnecting? false hasHandle? true
HTTP 34203: SERVER socketOnParserExecute 539
HTTP 34203: SERVER socketOnParserExecute 538
HTTP 34203: write ret = true
HTTP 34203: outgoing message end.
HTTP 34203: SERVER socketOnParserExecute 544
HTTP 34203: SERVER socketOnParserExecute 537
HTTP 34203: SERVER socketOnParserExecute 543
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 6
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 5
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 4
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 3
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 2
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 1
NET 34203: destroy
NET 34203: close
NET 34203: close handle
NET 34203: has server
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER handle? true   connections? 0
NET 34203: SERVER _emitCloseIfDrained
NET 34203: SERVER: emit close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
HTTP 34203: server socket close
NET 34203: emit close
```
