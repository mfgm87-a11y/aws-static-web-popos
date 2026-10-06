# KCSA · Dominio 5 · Platform Security

### [5/Supply Chain/1]
What is an SBOM?
- [ ] A signed record of every deployment made to a cluster
- [x] An inventory of the components inside a piece of software
- [ ] A benchmark that scores the security of a Kubernetes node
- [ ] A Kubernetes object that stores image pull credentials
> Un **SBOM** (Software Bill of Materials) es la "lista de ingredientes" de un software o imagen: paquetes, librerías, versiones, licencias y dependencias. Permite saber rápidamente si estás afectado cuando se publica una vulnerabilidad nueva.

### [5/Supply Chain/2]
Which two formats are the most widely used SBOM standards?
- [ ] YAML and TOML
- [x] SPDX and CycloneDX
- [ ] SARIF and JUnit
- [ ] OCI and CRI
> **SPDX** (Linux Foundation, estándar ISO/IEC 5962) y **CycloneDX** (OWASP) son los formatos de SBOM más usados. Herramientas como Syft o Trivy los generan. SARIF es un formato de resultados de análisis estático y OCI/CRI son estándares de contenedores.

### [5/Supply Chain/2]
What is Sigstore's cosign mainly used for?
- [ ] Scanning container images for known vulnerabilities
- [x] Signing and verifying container images and attestations
- [ ] Encrypting Kubernetes Secrets at rest in etcd
- [ ] Building container images without a Dockerfile
> **cosign** firma imágenes OCI (y otros artefactos y atestaciones, como SBOMs o procedencia) y verifica esas firmas. Las firmas se guardan junto a la imagen en el registro. Puede usar claves propias o firma *keyless* con identidades OIDC.

### [5/Supply Chain/2]
In Sigstore keyless signing, what role does Fulcio play?
- [ ] It stores the container images that have been signed by CI
- [x] It issues short-lived certificates bound to an OIDC identity
- [ ] It scans the signed images for malware before every release
- [ ] It replaces the cluster CA for Kubernetes components
> **Fulcio** es la autoridad de certificación de Sigstore: tras autenticar al firmante con OIDC (por ejemplo, la identidad de un workflow de CI), emite un certificado de muy corta duración ligado a esa identidad. Así no hay que gestionar claves privadas de larga vida.

### [5/Supply Chain/2]
What is Rekor in the Sigstore project?
- [ ] A container registry for storing signed images
- [x] A transparency log that records signing events
- [ ] A policy engine that blocks unsigned images
- [ ] A build system that produces reproducible images
> **Rekor** es un registro de transparencia inmutable y auditable donde se anotan las firmas. Permite verificar que una firma existió en un momento dado y detectar firmas sospechosas hechas con una identidad.

### [5/Supply Chain/2]
What does the SLSA framework focus on?
- [ ] Encrypting network traffic between microservices
- [x] Build integrity and provenance levels for software artifacts
- [ ] Rating the severity of known vulnerabilities from 0 to 10
- [ ] Defining Kubernetes Pod Security profiles
> **SLSA** (Supply-chain Levels for Software Artifacts, de la OpenSSF) define niveles crecientes de garantías sobre cómo se construyó un artefacto: desde tener procedencia documentada hasta builds en plataformas endurecidas con procedencia firmada y difícil de falsificar.

### [5/Supply Chain/2]
What is provenance in the context of the software supply chain?
- [ ] The geographic location of the registry that stores and serves an image
- [x] Verifiable metadata about how and from what an artifact was built
- [ ] The list of users who pulled an image during the last month
- [ ] The license of each open source dependency in the image
> La **procedencia** describe de forma verificable cómo se produjo un artefacto: qué código fuente (repo y commit), qué sistema de build, qué pasos y parámetros. Firmada (por ejemplo como atestación in-toto), permite comprobar en la admisión que la imagen salió del pipeline esperado.

### [5/Supply Chain/2]
What does in-toto provide?
- [ ] A runtime sandbox that isolates containers from the host's kernel
- [x] Verification that each supply chain step was authorized
- [ ] A public vulnerability database maintained by the CNCF TAG Security
- [ ] An admission controller that enforces the Pod Security Standards
> **in-toto** (graduado en la CNCF) define un *layout* con los pasos de la cadena de suministro y quién puede realizarlos; cada paso produce metadatos firmados (atestaciones). Al final se verifica que el artefacto pasó por todos los pasos, en orden y sin manipulación. SLSA usa el formato de atestaciones de in-toto.

### [5/Supply Chain/2]
What is a dependency confusion attack?
- [ ] Two microservices using different versions of the same shared library
- [x] A public package impersonating an internal one gets pulled into builds
- [ ] Mounting a ConfigMap in place of a Secret by mistake in a Deployment
- [ ] Running two container runtimes on the same node at once
> El atacante publica en un repositorio público (npm, PyPI…) un paquete con el mismo nombre que uno interno y una versión más alta. Si el gestor de paquetes está mal configurado, el build descarga el malicioso. Se mitiga con registros privados, *scopes*, versiones fijadas y verificación de hashes.

### [5/Supply Chain/3]
How can a cluster ensure that only images signed by the company's CI pipeline are deployed?
- [ ] By scanning the nodes nightly and deleting unsigned images
- [x] With an admission policy that verifies image signatures
- [ ] By setting `imagePullPolicy: Always` on every container
- [ ] By storing the signing key as a Secret in each namespace
> Una política de admisión verifica la firma (y opcionalmente atestaciones como la procedencia) antes de admitir el Pod: Kyverno `verifyImages`, el *policy-controller* de Sigstore o Ratify con Gatekeeper. Así una imagen sin firma válida ni siquiera llega a ejecutarse.

### [5/Image Repository/2]
Which CNCF graduated project is a container registry that offers RBAC, vulnerability scanning, signature support and replication?
- [ ] Notary
- [x] Harbor
- [ ] Dragonfly
- [ ] Buildpacks
> **Harbor** es un registro de contenedores graduado en la CNCF con proyectos y RBAC, escaneo integrado (por ejemplo con Trivy), soporte de firmas, replicación entre registros, retención e inmutabilidad de tags. Notary es un proyecto de firma, Dragonfly distribuye imágenes P2P y Buildpacks construye imágenes.

### [5/Image Repository/2]
What does tag immutability in a container registry prevent?
- [ ] Pulling the same image more than once per day per node
- [x] Overwriting an existing tag with different content
- [ ] Deleting old images to free storage space
- [ ] Scanning images that were pushed long ago
> Con tags inmutables, una vez publicado `app:1.4.2` no se puede volver a subir otra imagen con ese tag. Así nadie (ni un atacante con permisos de escritura ni un error de CI) puede cambiar silenciosamente lo que se despliega con ese tag.

### [5/Image Repository/2]
Why do organizations use a pull-through cache or mirror for public images?
- [ ] Because Kubernetes cannot pull from public registries directly
- [x] To control, scan and cache external images in one place
- [ ] Because mirrored images no longer need to be signed
- [ ] To give public images access to the cluster's Secrets
> Un registro intermedio permite aprobar y escanear las imágenes externas antes de usarlas, aplicar políticas en un único punto, evitar límites de descarga y no depender de la disponibilidad del registro público. Las políticas de admisión pueden exigir que todas las imágenes vengan de ese registro.

### [5/Image Repository/2]
How should Pods authenticate to a private registry following least privilege?
- [ ] With the registry's administrator account, shared by all teams
- [x] With read-only pull credentials scoped to the needed repositories
- [ ] With credentials baked into the container image itself
- [ ] Without authentication, by making the registry public
> Las credenciales de pull deben ser de solo lectura y limitarse a los repositorios necesarios (en `imagePullSecrets`, en el ServiceAccount o con identidad del nodo o de la carga). Si se filtran, el atacante solo puede descargar, no publicar imágenes maliciosas.

### [5/Image Repository/2]
Which kind of control prevents Pods from using images from untrusted registries?
- [ ] A NetworkPolicy that blocks egress from the kube-system namespace
- [x] An admission policy that restricts allowed image registries
- [ ] A PodDisruptionBudget on every workload
- [ ] A PriorityClass for trusted applications
> Las políticas de admisión (Kyverno, Gatekeeper, ValidatingAdmissionPolicy o el plugin ImagePolicyWebhook) pueden rechazar Pods cuyas imágenes no provienen de registros aprobados, o que no usan digests.

### [5/Image Repository/2]
What does continuous scanning of images already stored in a registry catch that build-time scanning alone misses?
- [ ] Syntax errors in the image's Dockerfile
- [x] New CVEs disclosed after the image was built
- [ ] Images that were built for another CPU architecture
- [ ] Tags that were pushed by the CI pipeline
> Una imagen limpia el día del build puede volverse vulnerable cuando se publican CVEs nuevos de sus componentes. Re-escanear periódicamente lo almacenado (y lo que corre en el clúster) detecta esos casos para reconstruir y redesplegar.

### [5/Observability/2]
Which data source does Falco primarily use to detect threats at runtime?
- [ ] Container image layers stored in the registry and their SBOMs
- [x] System calls, enriched with container and Kubernetes context
- [ ] The cluster's Prometheus metrics and alerts
- [ ] The Git history of the application repository
> **Falco** captura llamadas al sistema (con eBPF o un módulo del kernel), las enriquece con metadatos de contenedor y Kubernetes y las evalúa con reglas. También puede procesar otras fuentes (como el audit log de Kubernetes) mediante plugins.

### [5/Observability/2]
Which Cilium sub-project provides eBPF-based security observability and runtime enforcement?
- [ ] Hubble
- [x] Tetragon
- [ ] Envoy
- [ ] Clair
> **Tetragon** usa eBPF para observar ejecución de procesos, accesos a archivos y actividad de red con contexto de Kubernetes, y puede incluso bloquear acciones en el kernel. **Hubble** es la herramienta de observabilidad de red de Cilium; Envoy es un proxy y Clair un escáner de imágenes.

### [5/Observability/2]
Why should audit logs and security alerts be shipped off the cluster, for example to a SIEM?
- [ ] Because Kubernetes deletes audit logs every five minutes
- [x] Attackers in the cluster could tamper with local logs
- [ ] Because the API server cannot write logs to local disk
- [ ] Because alerts only fire when they leave the cluster
> Si los logs solo viven en el clúster, un atacante con suficientes privilegios puede borrarlos o alterarlos. Enviarlos a un sistema externo (SIEM) protege su integridad, permite correlacionar eventos de distintas fuentes y conservarlos el tiempo que exige el cumplimiento normativo.

### [5/Observability/2]
Why are Kubernetes Events not a substitute for audit logs in security investigations?
- [ ] Events are encrypted and cannot be read by cluster administrators
- [x] Events are short-lived operational notes, not a full audit trail
- [ ] Events are only generated for Pods in kube-system
- [ ] Events record every request body, which makes them too big
> Los Events describen lo que ocurre con los objetos (programación, fallos, pulls) y se borran pronto (una hora por defecto). No registran sistemáticamente quién hizo cada petición. El audit log sí está pensado como registro de seguridad.

### [5/Observability/2]
How can you detect that a container is making unexpected outbound connections?
- [ ] By checking the container's resource requests
- [x] With network flow observability and runtime security rules
- [ ] By listing the ConfigMaps in the container's namespace
- [ ] By reading the container image's labels
> Herramientas como Hubble (Cilium) muestran los flujos de red con identidad de Pod, y Falco o Tetragon pueden alertar sobre conexiones salientes inesperadas. Combinadas con políticas de egress que permiten solo destinos conocidos, el tráfico anómalo se detecta y se bloquea.

### [5/Service Mesh/2]
In Istio, which PeerAuthentication mode requires mutual TLS for all traffic to the selected workloads?
- [ ] PERMISSIVE
- [x] STRICT
- [ ] DISABLE
- [ ] OPTIONAL
> En modo **STRICT** los workloads solo aceptan tráfico mTLS. **PERMISSIVE** acepta mTLS y texto plano (útil durante la migración) y **DISABLE** desactiva mTLS. "OPTIONAL" no es un modo de PeerAuthentication.

### [5/Service Mesh/2]
What does Istio's PERMISSIVE mTLS mode do?
- [ ] It rejects every connection that does not use mTLS
- [x] It accepts both plaintext and mTLS connections
- [ ] It encrypts traffic only for external clients
- [ ] It disables certificate rotation for all workloads
> En PERMISSIVE los proxies aceptan tanto mTLS como texto plano, para poder migrar servicios gradualmente al mesh. Es útil de forma temporal, pero el objetivo es pasar a STRICT para que nadie pueda hablar en claro con los servicios.

### [5/Service Mesh/2]
Which identity standard do Istio and other service meshes use for workload identities in their certificates?
- [ ] Kerberos principals
- [x] SPIFFE IDs
- [ ] LDAP distinguished names
- [ ] Docker image digests
> Los meshes identifican cargas con **SPIFFE IDs** como `spiffe://cluster.local/ns/<ns>/sa/<serviceaccount>`, incluidos en el certificado X.509 (SVID). Así las políticas de autorización se basan en identidades criptográficas y no en IPs.

### [5/Service Mesh/2]
Which Istio resource enforces layer 7 rules such as "only service A may call GET /api on service B"?
- [ ] PeerAuthentication
- [x] AuthorizationPolicy
- [ ] DestinationRule
- [ ] ServiceEntry
> **AuthorizationPolicy** permite o deniega peticiones según la identidad de origen, el método, la ruta, cabeceras, etc. **PeerAuthentication** define si se exige mTLS, **DestinationRule** configura el tráfico hacia un destino (balanceo, TLS) y **ServiceEntry** registra servicios externos.

### [5/Service Mesh/2]
Do service mesh authorization policies replace Kubernetes NetworkPolicies?
- [ ] Yes, NetworkPolicies are ignored once a mesh is installed
- [x] No, they complement each other at different layers
- [ ] Yes, but only in clusters that use the IPVS proxy mode
- [ ] No, because a mesh cannot be used together with a CNI
> Las NetworkPolicies filtran en L3/L4 y las aplica el CNI, incluso para tráfico que no pasa por el mesh. Las políticas del mesh actúan en L7 con identidades criptográficas, pero dependen de que el tráfico pase por los proxies. Usar ambas es defensa en profundidad.

### [5/Service Mesh/2]
Which Istio component issues and rotates workload certificates by default?
- [ ] The kube-controller-manager
- [x] istiod, using its built-in CA
- [ ] cert-manager, installed automatically
- [ ] The kubelet of each node
> **istiod** incluye una CA que firma los certificados de los workloads (entregados a los proxies o a ztunnel) y los rota automáticamente con vidas cortas. Puede integrarse con una CA externa (por ejemplo, con cert-manager o una PKI corporativa) si se configura.

### [5/Service Mesh/2]
What is SPIRE?
- [ ] An Istio plugin that compresses HTTP traffic between proxies
- [x] The SPIFFE runtime that attests workloads and issues SVIDs
- [ ] A Kubernetes scheduler for security-sensitive Pods
- [ ] A vulnerability scanner for service mesh proxies
> **SPIRE** (graduado en la CNCF junto con SPIFFE) es la implementación de referencia de SPIFFE: verifica (atestigua) la identidad de las cargas según propiedades del nodo y del proceso y les emite identidades (SVIDs) de corta duración. Puede integrarse con meshes y aplicaciones.

### [5/PKI/2]
In a kubeadm cluster, where are the cluster CA and the component certificates stored?
- [ ] `/var/lib/etcd/certs`
- [x] `/etc/kubernetes/pki`
- [ ] `/root/.kube/certs`
- [ ] `/opt/cni/bin`
> kubeadm guarda la PKI en `/etc/kubernetes/pki`: la CA del clúster, la del front-proxy, la de etcd (en `pki/etcd`) y los certificados del API server y de sus clientes. Esas claves privadas son de los secretos más críticos del clúster.

### [5/PKI/2]
What is the risk if the private key of the cluster CA is stolen?
- [ ] Only the Ingress certificates of the cluster are affected
- [x] The attacker can mint client certificates for any identity
- [ ] The nodes stop being able to pull container images
- [ ] Nothing, because Kubernetes rotates the CA every hour
> Con la clave de la CA, el atacante puede firmar certificados de cliente para cualquier usuario o grupo (incluido `system:masters`) que el API server aceptará. La única solución real es rotar la CA y reemitir todos los certificados.

### [5/PKI/2]
Why does Kubernetes use a separate front-proxy CA?
- [ ] To sign the certificates that Ingress controllers serve
- [x] To authenticate the API server to aggregated API servers
- [ ] To encrypt the traffic between etcd members
- [ ] To sign the container images built in the cluster
> La capa de agregación reenvía peticiones a API servers de extensión (como metrics-server). El front-proxy se autentica ante ellos con un certificado de una CA separada, para que esos certificados no sirvan como credenciales de cliente normales ante el API server.

### [5/PKI/2]
What is the purpose of the CertificateSigningRequest (CSR) API in Kubernetes?
- [ ] To scan existing certificates for weak algorithms automatically
- [x] To request certificates that a signer issues after approval
- [ ] To store the TLS certificates of every Ingress object in etcd
- [ ] To revoke client certificates that were leaked
> Con la API `certificates.k8s.io`, un cliente envía una CSR, alguien (o un controlador) la **aprueba** y un firmante la firma. Se usa, por ejemplo, para los certificados de los kubelets. Aprobar CSRs es un permiso sensible y Kubernetes no ofrece revocación de certificados.

### [5/PKI/2]
Which tool is commonly used to automate the issuance and renewal of TLS certificates for workloads and Ingresses, for example from Let's Encrypt?
- [ ] kube-bench
- [x] cert-manager
- [ ] Trivy
- [ ] Velero
> **cert-manager** (CNCF) gestiona certificados como recursos de Kubernetes (`Certificate`, `Issuer`): los solicita a ACME/Let's Encrypt, Vault o una CA propia, los guarda en Secrets y los renueva antes de que caduquen.

### [5/PKI/2]
What does the kubelet's `serverTLSBootstrap` setting enable?
- [ ] It makes the kubelet skip TLS to get faster communication with Pods
- [x] Kubelet serving certificates signed by the cluster CA via CSR
- [ ] It stores the kubelet's private key inside etcd
- [ ] It shares one serving certificate across all the nodes
> Por defecto el kubelet puede usar un certificado de servicio autofirmado, que el API server no puede verificar. Con `serverTLSBootstrap: true` el kubelet solicita su certificado de servicio mediante una CSR firmada por el clúster, lo que permite verificarlo con `--kubelet-certificate-authority`.

### [5/PKI/3]
Kubernetes cannot revoke an individual client certificate. An admin certificate in the `system:masters` group has leaked. What is the most robust remediation?
- [ ] Delete the ClusterRoleBinding that grants it cluster-admin
- [x] Rotate the CA that signed it and re-issue the other certificates
- [ ] Add the certificate's serial number to a ConfigMap blocklist
- [ ] Restart the API server so that it forgets the certificate
> No hay listas de revocación para certificados de cliente y `system:masters` no depende de RBAC, así que borrar bindings no sirve. Hay que rotar la CA (y redistribuir certificados a los componentes y usuarios legítimos). Por eso se recomiendan certificados de vida corta y no usar `system:masters` en el día a día.

### [5/Connectivity/2]
What is the Konnectivity service used for?
- [ ] Encrypting traffic between Pods on the same node
- [x] Proxying control plane to node traffic over TCP
- [ ] Connecting several clusters into a single mesh
- [ ] Synchronizing Secrets from an external vault
> Konnectivity proporciona un proxy a nivel TCP para el tráfico del control plane hacia el clúster (por ejemplo, cuando el API server llama a los kubelets). Los agentes en los nodos abren la conexión hacia el servidor, así el control plane no necesita acceso de red directo a los nodos; es habitual en servicios gestionados.

### [5/Connectivity/2]
Are the API server's proxy connections to nodes, Pods and Services safe to run over untrusted networks by default?
- [ ] Yes, they always use mutual TLS with full verification
- [x] No, they default to plain HTTP without authentication
- [ ] Yes, because kube-proxy encrypts them transparently
- [ ] Only when the Pods use the Restricted profile
> Según la documentación oficial, las conexiones del API server hacia nodos, Pods o Services usan por defecto HTTP sin autenticar ni cifrar (con `https:` no se valida el certificado del destino), así que **no** son seguras en redes no confiables. La conexión API server → kubelet sí puede protegerse con `--kubelet-certificate-authority`.

### [5/Connectivity/2]
Which statement about node-to-control-plane communication is correct?
- [ ] Nodes talk directly to etcd to report their Pods' status
- [x] Nodes reach the API server over HTTPS with their own credentials
- [ ] Nodes use the scheduler's port to receive new Pods
- [ ] Nodes use unauthenticated HTTP, because the network is trusted
> Kubernetes sigue un modelo *hub-and-spoke*: todo lo que los nodos (kubelets) y los Pods hacen con la API termina en el API server, por HTTPS y con autenticación (certificados de cliente o tokens de ServiceAccount). Ningún otro componente del control plane expone servicios remotos a los nodos.

### [5/Connectivity/2]
Where is TLS typically terminated for external HTTPS traffic going to an application in Kubernetes?
- [ ] At the kubelet of the node that runs the backend Pod
- [x] At the Ingress controller or Gateway, using a TLS Secret
- [ ] Inside etcd, just before the request body is stored
- [ ] At CoreDNS, when the Service name is resolved for the client
> Lo habitual es terminar TLS en el Ingress controller o Gateway con un certificado guardado en un Secret (a menudo gestionado por cert-manager). Si el tráfico interno también debe cifrarse, se re-cifra hacia los backends o se usa mTLS con un service mesh.

### [5/Connectivity/2]
Why do some platforms route outbound traffic from workloads through an egress gateway?
- [ ] Because Pods cannot open outbound connections by themselves
- [x] To control and monitor which external destinations are reached
- [ ] Because egress gateways make DNS resolution faster
- [ ] To give every Pod a public IP address on the internet
> Un *egress gateway* concentra el tráfico saliente en un punto controlado: se pueden permitir solo ciertos destinos, registrar las conexiones y salir con IPs fijas que los sistemas externos puedan autorizar. Ayuda a detectar y frenar la exfiltración de datos.

### [5/Admission Control/2]
In which order are the admission phases executed for a request to the API server?
- [ ] Validating admission → mutating admission → schema validation
- [x] Mutating admission → schema validation → validating admission
- [ ] Schema validation → validating admission → mutating admission
- [ ] Mutating and validating webhooks all run in parallel
> Primero se ejecutan los controladores y webhooks **mutantes** (pueden cambiar el objeto), luego se valida el esquema del objeto y al final los **validantes** (solo aceptan o rechazan). Así la validación ve el objeto final, tal como se guardará en etcd.

### [5/Admission Control/2]
What is ValidatingAdmissionPolicy?
- [ ] A webhook that must be deployed as a separate service
- [x] A built-in, in-process admission check written in CEL
- [ ] A command-line tool that validates YAML files locally
- [ ] A Pod Security level stricter than Restricted
> **ValidatingAdmissionPolicy** (estable desde Kubernetes 1.30) permite escribir reglas de validación con expresiones **CEL** que el propio API server evalúa, sin desplegar ni mantener un webhook externo. Se aplica con un `ValidatingAdmissionPolicyBinding`.

### [5/Admission Control/2]
Which policy engine expresses its policies in the Rego language?
- [ ] Kyverno
- [x] OPA Gatekeeper
- [ ] Falco
- [ ] Tetragon
> **OPA Gatekeeper** usa Rego en sus `ConstraintTemplates` y crea `Constraints` para aplicarlas. **Kyverno** escribe sus políticas como recursos YAML de Kubernetes. Falco y Tetragon son herramientas de seguridad en tiempo de ejecución, no de admisión.

### [5/Admission Control/2]
Which policy engine writes policies as Kubernetes YAML resources and can validate, mutate, generate resources and verify image signatures?
- [ ] OPA Gatekeeper
- [x] Kyverno
- [ ] kube-bench
- [ ] Trivy
> **Kyverno** (CNCF) define políticas como recursos de Kubernetes, sin un lenguaje aparte, y puede validar, mutar, generar recursos (por ejemplo, una NetworkPolicy por namespace) y verificar firmas e imágenes (`verifyImages`).

### [5/Admission Control/2]
What does the ImagePolicyWebhook admission plugin do?
- [ ] It pulls every image in advance onto all of the nodes
- [x] It asks an external backend whether each image may be used
- [ ] It converts image tags into digests automatically
- [ ] It signs images with the cluster CA before they run
> ImagePolicyWebhook envía a un servicio externo una revisión (`ImageReview`) con las imágenes del Pod, y ese servicio decide si se permiten. Hoy es más común hacerlo con Kyverno, Gatekeeper o políticas CEL, pero sigue siendo un plugin de admisión integrado.

### [5/Admission Control/2]
Which built-in admission plugin enforces the Pod Security Standards?
- [ ] NodeRestriction
- [x] PodSecurity
- [ ] SecurityContextDeny
- [ ] AlwaysPullImages
> El plugin **PodSecurity** implementa Pod Security Admission y aplica los niveles privileged, baseline o restricted según las labels del namespace. NodeRestriction limita a los kubelets y AlwaysPullImages fuerza la descarga de imágenes; SecurityContextDeny era un plugin antiguo que se eliminó.
