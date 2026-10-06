# KCSA · Dominio 1 · Overview of Cloud Native Security

### [1/4Cs/1]
In the 4Cs model of cloud native security, which layer is the outermost and forms the trusted base for all the others?
- [ ] Code
- [ ] Container
- [ ] Cluster
- [x] Cloud
> El modelo de las 4C va de fuera hacia dentro: **Cloud** (o datacenter/infraestructura), **Cluster**, **Container** y **Code**. La nube es la base de confianza: si está comprometida, los controles de las capas internas pueden saltarse.

### [1/4Cs/2]
A team scans its application dependencies for known CVEs and enforces TLS between its services. Which layer of the 4Cs do these controls mainly address?
- [ ] Cloud
- [ ] Cluster
- [ ] Container
- [x] Code
> La capa **Code** cubre la seguridad de la propia aplicación: dependencias sin vulnerabilidades conocidas, cifrado en tránsito (TLS), análisis estático, mínima exposición de puertos y validación de entradas. Es la capa sobre la que el desarrollador tiene más control.

### [1/4Cs/2]
Restricting access to the Kubernetes API, enabling RBAC and applying NetworkPolicies are controls of which 4C layer?
- [ ] Cloud
- [x] Cluster
- [ ] Container
- [ ] Code
> Estos controles protegen el **clúster**: quién puede hablar con el API server (autenticación, autorización/RBAC, admisión), cómo se comunican los Pods (NetworkPolicy) y cómo se protegen los Secrets. La capa Cloud cubriría, por ejemplo, IAM y firewalls de la cuenta del proveedor.

### [1/4Cs/2]
Which control belongs to the Container layer of the 4Cs?
- [ ] Configuring IAM policies on the cloud provider account
- [ ] Enforcing RBAC rules on the Kubernetes API server
- [x] Scanning images and running containers as non-root users
- [ ] Using parameterized queries in the application's code
> La capa **Container** trata de la imagen y de cómo se ejecuta: escaneo de vulnerabilidades, imágenes mínimas y firmadas, usuario no root, sin privilegios innecesarios. IAM pertenece a Cloud, RBAC a Cluster y las consultas parametrizadas (contra inyección SQL) a Code.

### [1/4Cs/3]
Why can strong application-level (Code) security not compensate for a compromised cloud layer?
- [ ] Because application code cannot use TLS when it runs in the cloud
- [x] Because inner layers rely on outer ones, which can bypass their controls
- [ ] Because cloud providers forbid application-level security controls
- [ ] Because the 4Cs model says Code security is optional in production
> Cada capa interna se apoya en la seguridad de la externa: quien controla la infraestructura (hipervisor, discos, red, credenciales de la cuenta) puede leer memoria o discos, manipular nodos o el control plane y saltarse los controles de las capas de dentro. Por eso se aplica defensa en profundidad en las cuatro capas.

### [1/4Cs/2]
The current Kubernetes documentation, aligned with the CNCF Cloud Native Security Whitepaper, frames security around lifecycle phases. Which are they?
- [ ] Plan, Build, Test and Release
- [x] Develop, Distribute, Deploy and Runtime
- [ ] Identify, Protect, Detect and Respond
- [ ] Code, Container, Cluster and Cloud
> La documentación de Kubernetes y el whitepaper de seguridad de la CNCF organizan los controles por fases del ciclo de vida: **Develop** (código seguro, pruebas), **Distribute** (imágenes, registros, firmas, SBOM), **Deploy** (políticas de admisión, configuración) y **Runtime** (acceso, cómputo, almacenamiento, red, detección). "Identify, Protect…" son funciones del NIST CSF y las 4C son otro modelo de capas.

### [1/4Cs/2]
Signing container images and verifying their signatures before they reach the cluster belongs to which lifecycle phase?
- [ ] Develop
- [x] Distribute
- [ ] Deploy
- [ ] Runtime
> La fase **Distribute** cubre cómo viajan los artefactos desde el build hasta el clúster: registros, escaneo de imágenes, firma, SBOM y procedencia. La verificación de la firma suele aplicarse además en **Deploy** mediante una política de admisión.

### [1/4Cs/2]
An admission policy that rejects privileged Pods and Pods without resource limits is part of which lifecycle phase?
- [ ] Develop
- [ ] Distribute
- [x] Deploy
- [ ] Runtime
> Los controles de **Deploy** verifican que lo que se va a ejecutar cumple las políticas antes de que llegue a correr: admisión (Pod Security Admission, Kyverno, Gatekeeper, ValidatingAdmissionPolicy) y verificación de imágenes. Runtime cubre lo que pasa mientras la carga ya está en ejecución.

### [1/4Cs/1]
What does "defense in depth" mean?
- [ ] Relying on one very strong perimeter firewall for the whole cluster
- [x] Layering independent controls so a single failure is not a full breach
- [ ] Encrypting every disk twice with different encryption algorithms
- [ ] Hiring a dedicated red team to attack the platform every month
> Defensa en profundidad es apilar controles independientes (red, identidad, admisión, runtime, detección…) para que, si uno falla, otros sigan limitando el daño. El modelo de 4C y las fases del ciclo de vida son formas de organizar esas capas.

### [1/Cloud & Infrastructure/2]
In a managed Kubernetes service, who is typically responsible for securing control plane components such as etcd and the API server?
- [ ] The customer, who must patch and back up etcd manually
- [x] The cloud provider, under the shared responsibility model
- [ ] Nobody, because managed control planes are not attackable
- [ ] The CNCF, which certifies every managed Kubernetes offering
> En el **modelo de responsabilidad compartida**, el proveedor opera y protege el control plane (parches, disponibilidad, etcd, cifrado de su almacenamiento). El cliente sigue siendo responsable de sus cargas, RBAC, NetworkPolicies, imágenes, Secrets y de la configuración de los nodos que gestione.

### [1/Cloud & Infrastructure/2]
A compromised Pod sends requests to `http://169.254.169.254/` and obtains cloud credentials. What is this endpoint?
- [ ] The Kubernetes API server's internal health endpoint
- [x] The cloud instance metadata service of the node
- [ ] The CoreDNS service of the cluster
- [ ] The kubelet's read-only port
> 169.254.169.254 es el **servicio de metadatos de instancia** (IMDS) de los proveedores de nube. Puede entregar las credenciales del rol IAM del nodo, así que un Pod comprometido podría usarlas para atacar la cuenta de nube. Es un vector clásico de escalada de clúster a nube.

### [1/Cloud & Infrastructure/3]
Which measure best reduces the risk of Pods stealing node credentials from the cloud metadata service?
- [ ] Run the sensitive Pods with `hostNetwork: true` to bypass it
- [x] Block Pod access to the metadata endpoint and use workload identity
- [ ] Mount the node's cloud credentials into each Pod as a Secret
- [ ] Disable RBAC in the kube-system namespace to reduce exposure
> Se bloquea el acceso de los Pods al endpoint de metadatos (NetworkPolicy de egress, IMDSv2 con *hop limit* 1, reglas del proveedor) y se usa **workload identity** (IRSA/Pod Identity en EKS, Workload Identity en GKE, AKS Workload Identity) para dar a cada Pod sus propias credenciales mínimas. `hostNetwork` empeora el problema.

### [1/Cloud & Infrastructure/2]
What is the advantage of workload identity (e.g. IRSA on EKS or Workload Identity on GKE) over using the node's IAM role?
- [ ] It lets every Pod on the node share one single, powerful cloud role
- [x] Each ServiceAccount gets its own narrowly scoped cloud credentials
- [ ] It removes the need for any authentication to cloud APIs
- [ ] It stores long-lived cloud access keys inside etcd for each Pod
> Con workload identity, un ServiceAccount de Kubernetes se asocia a una identidad de nube concreta y recibe credenciales temporales solo con los permisos que necesita. Así no todos los Pods del nodo heredan el rol del nodo, y se aplica mínimo privilegio también en la nube.

### [1/Cloud & Infrastructure/2]
Which practice best protects the API server endpoint of a managed cluster?
- [ ] Exposing it publicly on a non-standard port so that it stays hidden
- [x] Restricting network access, e.g. a private endpoint or allowed IPs
- [ ] Disabling TLS so that every client can connect more easily
- [ ] Allowing anonymous access so that monitoring tools work
> Además de autenticación y autorización, conviene limitar **quién puede llegar** al endpoint: endpoint privado, rangos de IP autorizados o acceso solo desde una VPN/bastión. Cambiar el puerto no es seguridad, y desactivar TLS o permitir acceso anónimo aumenta el riesgo.

### [1/Cloud & Infrastructure/2]
Which kind of operating system is recommended for Kubernetes nodes to reduce the attack surface?
- [ ] A full desktop distribution with many preinstalled tools
- [x] A minimal, container-optimized OS with only required packages
- [ ] Any OS, as long as SSH password login stays enabled
- [ ] An OS whose automatic security updates are disabled
> Los sistemas operativos mínimos y orientados a contenedores (Bottlerocket, Flatcar, Talos, Container-Optimized OS…) incluyen solo lo necesario para correr contenedores, suelen tener sistema de archivos de solo lectura y actualizaciones atómicas. Menos paquetes significa menos vulnerabilidades y menos herramientas para un atacante.

### [1/Cloud & Infrastructure/2]
In a self-managed cluster, which ports should be reachable only from the control plane network and never exposed to the internet?
- [ ] 443 on the public load balancer of the Ingress controller
- [x] 2379–2380 for etcd and 10250 for the kubelet API
- [ ] 80 on a public marketing website served by the cluster
- [ ] 53 on the company's public authoritative DNS servers
> etcd (2379 clientes, 2380 pares) guarda todo el estado del clúster y la API del kubelet (10250) permite ejecutar comandos en contenedores. Deben quedar restringidos con firewalls o security groups. El API server (6443) también debería limitarse a las redes que lo necesitan.

### [1/Cloud & Infrastructure/2]
Your team provisions clusters with Terraform. Which practice improves the security of the infrastructure layer?
- [ ] Committing the Terraform state file to a public repository for transparency
- [x] Scanning IaC for misconfigurations and protecting the state file
- [ ] Applying changes manually in the cloud console to avoid configuration drift
- [ ] Giving the CI pipeline permanent administrator keys on the cloud account
> La infraestructura como código debe tratarse como código de producción: revisión, escaneo de configuraciones inseguras (Checkov, Trivy, KICS) antes de aplicar, y protección del archivo de estado, que puede contener datos sensibles (guárdalo en un backend remoto cifrado y con acceso restringido, no en Git). Las credenciales de CI deben ser temporales y mínimas.

### [1/Controls & Frameworks/1]
Which of the following is an example of a preventive control?
- [ ] A Falco alert raised when a shell starts in a container
- [x] An admission policy that rejects privileged Pods
- [ ] Restoring etcd from a backup after an incident
- [ ] Reviewing audit logs once a week for anomalies
> Un control **preventivo** impide que algo malo ocurra (por ejemplo, rechazar Pods privilegiados en la admisión). Una alerta de Falco o la revisión de logs son controles **detectivos**, y restaurar un backup es un control **correctivo**.

### [1/Controls & Frameworks/2]
Falco raising an alert when a shell starts inside a production container is an example of which type of control?
- [ ] Preventive
- [x] Detective
- [ ] Corrective
- [ ] Deterrent
> Falco **detecta** comportamientos sospechosos en tiempo de ejecución, pero por sí mismo no los bloquea: es un control detectivo. Los controles preventivos (admisión, RBAC) evitan el problema y los correctivos (aislar el Pod, restaurar) responden después.

### [1/Controls & Frameworks/2]
What does the zero trust principle "never trust, always verify" imply for service-to-service traffic inside a cluster?
- [ ] All traffic inside the cluster network can be trusted by default
- [x] Each request is authenticated and authorized, even inside the cluster
- [ ] Only traffic that comes from the internet needs to be verified
- [ ] All services should share one token so that verification is simple
> En *zero trust* la ubicación en la red no otorga confianza: cada llamada se autentica (por ejemplo con mTLS e identidades SPIFFE) y se autoriza con políticas explícitas, y se limita la red con NetworkPolicies. Así, un Pod comprometido no puede moverse libremente por el clúster.

### [1/Controls & Frameworks/2]
What does separation of duties mean on a Kubernetes platform?
- [ ] Each namespace must be stored in a separate etcd cluster
- [x] No single identity can perform every critical step on its own
- [ ] Developers and operators must use different container runtimes
- [ ] Every Pod must be split into separate sidecar containers
> La separación de funciones reparte las acciones críticas entre distintos roles: por ejemplo, quien escribe las políticas de seguridad no es quien despliega las aplicaciones, y los cambios a producción requieren revisión de otra persona. Reduce el riesgo de abuso y de errores no detectados.

### [1/Controls & Frameworks/2]
Which document provides prescriptive configuration checks for hardening Kubernetes components and is commonly automated with kube-bench?
- [ ] The OWASP Top 10
- [x] The CIS Kubernetes Benchmark
- [ ] The Twelve-Factor App
- [ ] The OpenGitOps principles
> El **CIS Kubernetes Benchmark** (Center for Internet Security) contiene recomendaciones concretas para el API server, etcd, kubelet, scheduler, controller-manager y políticas. **kube-bench** automatiza esas comprobaciones en los nodos.

### [1/Controls & Frameworks/2]
A legacy application must run as root and cannot be changed yet. The team adds strict NetworkPolicies, dedicated nodes and extra runtime monitoring. What kind of control is this?
- [ ] A detective-only control
- [x] A compensating control
- [ ] A deterrent control
- [ ] A directive control
> Un control **compensatorio** se usa cuando el control principal (aquí, no ejecutar como root) no se puede aplicar: se reduce el riesgo con medidas alternativas, como aislamiento de red y de nodos y más monitoreo. Debe documentarse y revisarse hasta poder aplicar el control original.

### [1/Isolation/2]
Are Kubernetes namespaces a strong security boundary on their own?
- [ ] Yes, each namespace runs on its own isolated kernel
- [x] No, workloads still share nodes, the kernel and the control plane
- [ ] Yes, Pods in different namespaces can never talk to each other
- [ ] No, because namespaces cannot be targeted by RBAC rules
> Un namespace delimita nombres y es la unidad para aplicar RBAC, NetworkPolicies, Pod Security Admission y cuotas, pero no aísla por sí mismo: los Pods comparten nodos, kernel, red (plana por defecto) y control plane. El aislamiento real se construye combinando esos controles.

### [1/Isolation/2]
Which technology runs each Pod inside a lightweight virtual machine to provide hardware-level isolation?
- [ ] gVisor
- [x] Kata Containers
- [ ] runc
- [ ] seccomp
> **Kata Containers** ejecuta cada Pod en una micro-VM con su propio kernel, aprovechando la virtualización por hardware. **gVisor** usa otro enfoque: un kernel en espacio de usuario que intercepta las llamadas al sistema. runc es el runtime OCI estándar sin aislamiento extra y seccomp filtra syscalls.

### [1/Isolation/2]
What does gVisor provide?
- [ ] A hardware virtual machine for every single container
- [x] A user-space kernel that intercepts container system calls
- [ ] A network plugin that encrypts traffic between Pods
- [ ] A scanner that finds vulnerabilities in container images
> gVisor implementa en espacio de usuario gran parte de la interfaz del kernel de Linux (su componente *Sentry*), de modo que las syscalls del contenedor no llegan directamente al kernel del host. Reduce la superficie de ataque frente a exploits del kernel. Se usa con un RuntimeClass (handler `runsc`).

### [1/Isolation/3]
You must run untrusted customer code in a shared cluster. Which combination gives the strongest isolation?
- [ ] A separate namespace labeled with the Privileged Pod Security level
- [x] Dedicated tainted nodes, a sandboxed RuntimeClass and default-deny rules
- [ ] The default runtime with `hostPID: true` so the team can monitor it
- [ ] A shared node pool where tenants are only told apart by their Pod labels
> Para código no confiable se combinan capas: nodos dedicados (taints/tolerations y afinidad) para no compartir kernel con otras cargas, un runtime con sandbox (gVisor o Kata vía RuntimeClass), Pod Security *restricted* y NetworkPolicies de denegación por defecto. Un namespace con nivel *privileged* o `hostPID` hacen lo contrario.

### [1/Isolation/2]
What does setting `hostUsers: false` in a Pod spec do?
- [ ] It prevents the Pod from using the host network namespace
- [x] It maps container root to an unprivileged user on the host
- [ ] It removes every user account from the container image
- [ ] It forbids any user from running `kubectl exec` into the Pod
> Con `hostUsers: false` el Pod usa **user namespaces** (estable desde Kubernetes 1.36): el UID 0 dentro del contenedor corresponde a un UID sin privilegios en el host. Si el proceso escapa del contenedor, no es root en el nodo, lo que reduce mucho el impacto.

### [1/Isolation/2]
Which Linux mechanism restricts the system calls a container process can make?
- [ ] cgroups
- [x] seccomp
- [ ] chroot
- [ ] iptables
> **seccomp** filtra las llamadas al sistema que puede hacer un proceso. En Kubernetes se configura con `securityContext.seccompProfile` (`RuntimeDefault` o `Localhost`). Los cgroups limitan recursos, chroot cambia el directorio raíz e iptables filtra tráfico de red.

### [1/Isolation/2]
How do AppArmor and SELinux differ as mandatory access control systems for containers?
- [ ] AppArmor encrypts files, while SELinux only filters network traffic
- [x] AppArmor uses path-based profiles; SELinux uses security labels
- [ ] SELinux only works on Windows nodes, while AppArmor works on Linux
- [ ] They are the same project published under two different names
> Ambos son módulos de seguridad de Linux (LSM) que aplican control de acceso obligatorio. AppArmor define perfiles basados en rutas (Kubernetes los configura con `securityContext.appArmorProfile`); SELinux usa etiquetas (contextos) en procesos y archivos (`seLinuxOptions`). La distribución del nodo suele determinar cuál está disponible.

### [1/Artifact & Image Security/2]
Why should production manifests reference images by digest instead of by tag?
- [ ] Digests make the images download faster from the registry
- [x] A digest pins exact, immutable content; a tag can be repointed
- [ ] Tags are not supported by the container runtimes anymore
- [ ] Digests automatically include the results of image scanning
> El digest (`@sha256:...`) identifica el contenido exacto de la imagen; un tag es un puntero que alguien con permisos de escritura en el registro puede mover a otra imagen (posiblemente maliciosa). Fijar digests garantiza que se despliega exactamente lo que se probó y escaneó.

### [1/Artifact & Image Security/2]
What is the main security benefit of a private registry such as Harbor with access control and vulnerability scanning?
- [ ] It guarantees that no image will ever contain a vulnerability
- [x] It controls who can push or pull and blocks vulnerable images
- [ ] It replaces the need for runtime security tools on the nodes
- [ ] It encrypts the memory of containers while they are running
> Un registro privado permite controlar quién publica y quién descarga imágenes, escanearlas, exigir firmas y bloquear la descarga de imágenes con vulnerabilidades graves. No hace las imágenes perfectas ni sustituye a los controles de runtime: es una capa más.

### [1/Artifact & Image Security/2]
In a multi-tenant cluster, which admission plugin ensures that a private image already cached on a node cannot be used by a Pod that lacks the pull credentials?
- [ ] NodeRestriction
- [x] AlwaysPullImages
- [ ] LimitRanger
- [ ] DefaultStorageClass
> Con `IfNotPresent`, un Pod de otro inquilino podría usar una imagen privada que ya estaba en la caché del nodo sin tener credenciales. El plugin de admisión **AlwaysPullImages** fuerza `imagePullPolicy: Always`, así el registro verifica las credenciales en cada arranque (a cambio de más descargas).
>
> Desde v1.35 el kubelet también puede verificar las credenciales de imágenes ya presentes en el nodo (*KubeletEnsureSecretPulledImages*, beta y activo por defecto), pero eso es configuración del kubelet, no un plugin de admisión.

### [1/Artifact & Image Security/2]
A developer added an API key in one Dockerfile layer and deleted the file in a later layer. Is the key still exposed?
- [ ] No, deleting the file removes it from every layer of the image
- [x] Yes, the earlier layer still contains it and can be extracted
- [ ] No, because image layers are encrypted by the registry
- [ ] Only if the image runs with `privileged: true` in the cluster
> Las capas de una imagen son acumulativas: borrar un archivo en una capa posterior solo lo oculta en el sistema de archivos final, pero la capa anterior sigue teniéndolo y cualquiera que pueda descargar la imagen puede extraerlo. Hay que rotar la clave y reconstruir la imagen sin ella (usando *build secrets*).

### [1/Artifact & Image Security/2]
What is the main purpose of scanning container images with tools such as Trivy or Grype?
- [ ] To compress the image layers before pushing them to a registry
- [x] To find known vulnerabilities in packages and app dependencies
- [ ] To sign the image so that the cluster trusts where it came from
- [ ] To convert Dockerfiles into Kubernetes manifests automatically
> Los escáneres comparan los paquetes del sistema operativo y las dependencias de la aplicación con bases de datos de vulnerabilidades (CVEs); muchos también detectan configuraciones inseguras y secretos. La firma de imágenes (cosign) es otro control distinto.

### [1/Artifact & Image Security/2]
Which base image choice usually reduces the number of potential vulnerabilities the most?
- [ ] A full Ubuntu image with build tools included
- [x] A distroless or scratch-based minimal image
- [ ] Whatever image has the most stars on Docker Hub
- [ ] An image tagged `latest` so it is always current
> Las imágenes **distroless** o basadas en `scratch` solo incluyen la aplicación y sus dependencias de runtime: sin shell, gestor de paquetes ni utilidades. Menos componentes significa menos CVEs y menos herramientas para un atacante. `latest` no garantiza nada y además es mutable.

### [1/Artifact & Image Security/1]
What does a CVSS score represent?
- [ ] The number of containers affected by a vulnerability
- [x] A standard severity rating for a vulnerability (0–10)
- [ ] The time a vendor needs to publish a security patch
- [ ] The probability that a given image contains malware
> El **CVSS** (Common Vulnerability Scoring System) asigna una puntuación de severidad de 0 a 10 a una vulnerabilidad según factores como el vector de ataque, la complejidad y el impacto. Ayuda a priorizar, pero el riesgo real depende también del contexto (si el componente se usa o es alcanzable).

### [1/Workload & Code Security/2]
What is the difference between SAST and DAST?
- [ ] SAST tests the running app from outside; DAST reads the source code
- [x] SAST analyzes source code without running it; DAST tests the running app
- [ ] Both are names for the same container image scanning technique
- [ ] SAST is only for Kubernetes manifests; DAST is only for Dockerfiles
> **SAST** (Static Application Security Testing) analiza el código fuente o binario sin ejecutarlo, buscando patrones inseguros. **DAST** (Dynamic) ataca la aplicación en ejecución desde fuera, como lo haría un atacante. Son complementarios y encajan en distintas etapas del pipeline.

### [1/Workload & Code Security/2]
What does Software Composition Analysis (SCA) focus on?
- [ ] The performance of the application under heavy load
- [x] Third-party dependencies, their CVEs and their licenses
- [ ] The network topology between microservices in the cluster
- [ ] The CPU architecture the application is compiled for
> El SCA identifica las librerías de terceros y open source que usa la aplicación, sus vulnerabilidades conocidas y sus licencias. Es clave porque la mayor parte del código de una aplicación moderna proviene de dependencias, y su resultado suele expresarse en un SBOM.

### [1/Workload & Code Security/2]
A developer accidentally committed a cloud access key to a Git repository. What is the correct first response?
- [ ] Delete the commit with a force push and assume the key is now safe
- [x] Revoke or rotate the key immediately, then clean up the history
- [ ] Make the repository private and keep using the same key
- [ ] Encode the key in base64 in a new commit to hide it
> Una vez publicada, hay que asumir que la clave está comprometida (los bots escanean repositorios en minutos): primero se revoca o rota, luego se revisa si se usó, se limpia el historial y se añade escaneo de secretos (pre-commit, CI) para evitar que se repita. Borrar el commit o hacer privado el repo no basta.

### [1/Workload & Code Security/1]
Which resource lists the most critical web application security risks and is widely used as an awareness standard for application code?
- [ ] The CIS Kubernetes Benchmark
- [x] The OWASP Top 10
- [ ] The NIST SP 800-190 guide
- [ ] The MITRE ATT&CK matrix
> El **OWASP Top 10** recoge los riesgos más críticos de las aplicaciones web (control de acceso roto, fallos criptográficos, inyección, etc.). El CIS Benchmark trata de configuración de Kubernetes, NIST SP 800-190 de contenedores y MITRE ATT&CK de técnicas de atacantes.

### [1/Workload & Code Security/2]
Why should applications avoid logging full request payloads and environment variables?
- [ ] Because verbose logging slows down the Kubernetes scheduler
- [x] Because they may carry secrets or personal data into the logs
- [ ] Because Kubernetes rejects containers that write to stdout
- [ ] Because log collectors are unable to parse JSON payloads
> Los logs suelen centralizarse en sistemas con controles de acceso más amplios y retenciones largas. Si contienen tokens, contraseñas o datos personales, se convierten en una vía de filtración y en un problema de cumplimiento (por ejemplo, GDPR). Se deben enmascarar o excluir los datos sensibles.

### [1/Workload & Code Security/2]
Pinning dependency versions with lock files and verifying their checksums mainly helps mitigate which risk?
- [ ] Container escapes that exploit vulnerabilities in the host kernel
- [x] Unexpected or malicious dependency updates entering the build
- [ ] Denial of service against the Kubernetes API server
- [ ] Theft of ServiceAccount tokens from running Pods
> Fijar versiones y verificar hashes hace los builds reproducibles e impide que una nueva versión (comprometida o con *typosquatting*) entre sin revisión. Es una práctica básica de seguridad de la cadena de suministro de software.
