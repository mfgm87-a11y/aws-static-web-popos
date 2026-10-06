# KCSA · Dominio 4 · Kubernetes Threat Model

### [4/Trust Boundaries/2]
An attacker who escapes from a container lands on the underlying node. Which trust boundary have they crossed?
- [ ] The boundary between two namespaces of the same cluster
- [x] The boundary between a container and its host node
- [ ] The boundary between the CI system and the image registry
- [ ] The boundary between two replicas of the same Deployment
> Un escape de contenedor cruza la frontera **contenedor → nodo**: el atacante pasa de un proceso aislado a operar sobre el host, donde puede ver otros contenedores, las credenciales del kubelet y, a veces, las de la nube. Otras fronteras clave son usuario → API server, nodo → control plane, namespace → namespace y clúster → nube.

### [4/Trust Boundaries/2]
In threat modeling, what does a data flow diagram (DFD) help you identify?
- [ ] The exact CVEs present in each container image of the system
- [x] Components, data flows and the trust boundaries they cross
- [ ] The cost of each cloud resource used by the cluster
- [ ] The order in which the kubelet starts the containers of a Pod
> Un DFD representa procesos, almacenes de datos, entidades externas y los flujos entre ellos, marcando las fronteras de confianza. Sobre ese mapa se analizan amenazas, por ejemplo aplicando STRIDE a cada elemento y a cada flujo que cruza una frontera.

### [4/Trust Boundaries/2]
Which communication crosses the trust boundary between the control plane and the worker nodes?
- [ ] Traffic between two containers that run in the same Pod on one node
- [x] Kubelets calling the API server, and the API server calling kubelets
- [ ] Reads that a container makes from its own emptyDir volume on disk
- [ ] DNS lookups from a Pod to a Service name inside its own namespace
> La frontera control plane ↔ nodos la cruzan los kubelets cuando reportan al API server y el API server cuando llama al kubelet (logs, exec, port-forward). Por eso ambos sentidos deben autenticarse y cifrarse, y el kubelet debe limitarse con el autorizador Node y NodeRestriction.

### [4/Trust Boundaries/2]
Why is the namespace boundary considered weak from a threat modeling perspective?
- [ ] Because namespaces cannot have RBAC rules applied to them
- [x] Workloads still share nodes, the kernel and the network
- [ ] Because namespaces are deleted whenever a node restarts
- [ ] Because every namespace shares the same ServiceAccount token
> Los namespaces separan nombres y permiten aplicar políticas, pero las cargas comparten nodos, kernel, red plana por defecto y recursos de ámbito de clúster. Un escape de contenedor o un error de RBAC puede cruzar esa frontera, así que no hay que tratarla como un aislamiento fuerte.

### [4/Trust Boundaries/2]
Why is the boundary between a cluster and its cloud provider account important in the threat model?
- [ ] Because the cloud account can never be reached from inside Pods
- [x] Node or Pod credentials may let a compromised workload reach cloud APIs
- [ ] Because Kubernetes stores the cloud root password in a ConfigMap
- [ ] Because cloud providers forbid any network access from the cluster
> Los nodos suelen tener un rol de IAM y los Pods pueden alcanzar el servicio de metadatos. Si un atacante compromete un Pod o un nodo, puede saltar a la cuenta de nube (buckets, bases de datos, otros clústeres). Por eso se usa workload identity con permisos mínimos y se bloquea el acceso a los metadatos.

### [4/Trust Boundaries/2]
External traffic from the internet reaches an application in the cluster. Where does it first cross into the cluster?
- [ ] Directly at the etcd client port of the control plane
- [x] At the edge: the load balancer and Ingress/Gateway
- [ ] At the kubelet port 10250 of a randomly chosen node
- [ ] At the CoreDNS Service in the kube-system namespace
> El tráfico externo entra por el borde del clúster: un balanceador y el Ingress/Gateway controller, que termina TLS, aplica límites y enruta hacia los Services. Es un punto clave para controles como WAF, rate limiting y autenticación, y debe exponerse lo mínimo posible.

### [4/Trust Boundaries/3]
A validating admission webhook running in the cluster receives every Pod creation request. Why is this relevant to the threat model?
- [ ] It is not relevant, because webhooks only ever see object names
- [x] It sees sensitive objects, and its failure policy affects security
- [ ] Webhooks run inside etcd and can corrupt the whole database
- [ ] Webhooks replace RBAC, so authorization is skipped for all Pods
> Un webhook recibe los objetos completos que admite (y uno mutante puede modificarlos), así que su compromiso es grave. Además, su `failurePolicy` decide qué pasa si cae: con `Fail` puede bloquear despliegues (disponibilidad) y con `Ignore` deja pasar todo sin validar (seguridad). Es un componente de alta confianza.

### [4/Persistence/2]
After gaining API access, an attacker creates a CronJob that starts a reverse shell every hour. Which attacker tactic does this represent?
- [ ] Initial access
- [x] Persistence
- [ ] Discovery
- [ ] Exfiltration
> Crear un CronJob que vuelve a abrir acceso periódicamente es una técnica de **persistencia**: mantener el acceso aunque se cierre la sesión inicial o se reinicie el Pod comprometido. Aparece en las matrices de amenazas de Kubernetes junto con DaemonSets maliciosos, Pods estáticos o webhooks.

### [4/Persistence/2]
An attacker has root on a node. Which technique keeps a malicious container running even if its API objects are deleted?
- [ ] Creating a Deployment with a very high replica count
- [x] Writing a static Pod manifest on the node
- [ ] Adding a label to the node with the attacker's name
- [ ] Changing the default StorageClass of the cluster
> El kubelet ejecuta cualquier manifiesto que encuentre en su directorio de Pods estáticos, sin pasar por la admisión, y lo recrea si se borra el *mirror pod* del API server. Es una persistencia efectiva a nivel de nodo; hay que vigilar la integridad de ese directorio.

### [4/Persistence/2]
Why might an attacker create a legacy ServiceAccount token Secret (type `kubernetes.io/service-account-token`)?
- [ ] To encrypt the namespace's Secrets with the attacker's own key
- [x] To obtain a non-expiring API credential that survives Pod restarts
- [ ] To make the API server restart and drop all current sessions
- [ ] To hide the ServiceAccount from `kubectl get serviceaccounts`
> Los tokens guardados en Secrets de ese tipo no caducan. Si el atacante tiene acceso a un ServiceAccount privilegiado, crear uno de estos Secrets le da una credencial persistente. Conviene auditar su creación y usar solo tokens de corta duración (TokenRequest).

### [4/Persistence/2]
How can a malicious mutating admission webhook provide persistence?
- [ ] By deleting the audit policy every time the API server restarts
- [x] By injecting a malicious container into every new Pod
- [ ] By encrypting etcd with a key that only the attacker knows
- [ ] By renaming the namespaces in which it was installed
> Un webhook mutante puede modificar cada Pod que se crea, por ejemplo añadiendo un contenedor o un init container malicioso. Así el atacante reaparece en cada nuevo despliegue. Por eso el permiso sobre `mutatingwebhookconfigurations` es crítico y debe auditarse.

### [4/Persistence/2]
Which data source is most useful to detect persistence through new RoleBindings, CronJobs or webhook configurations?
- [ ] The container runtime's image cache
- [x] The Kubernetes API server audit log
- [ ] The CoreDNS query cache
- [ ] The node's kernel message buffer (dmesg)
> Todas esas técnicas se hacen a través del API server, así que quedan registradas en el **audit log** (quién creó qué recurso, cuándo y desde dónde). Enviar esos logs a un SIEM con alertas para recursos sensibles es clave para detectar persistencia.

### [4/Persistence/2]
Why is a backdoored image referenced by a DaemonSet an especially effective persistence mechanism?
- [ ] Because DaemonSets are exempt from every admission controller
- [x] It runs automatically on every node, including newly added ones
- [ ] Because DaemonSet Pods cannot be deleted by administrators
- [ ] Because DaemonSet images are never scanned by registries
> Un DaemonSet garantiza un Pod en cada nodo y lo despliega también en los nodos nuevos. Si su imagen tiene una puerta trasera, el atacante obtiene presencia en todo el clúster de forma automática. La firma y verificación de imágenes y el control de quién modifica DaemonSets lo mitigan.

### [4/Persistence/2]
Which combination best reduces an attacker's ability to persist through privileged Pods?
- [ ] Larger nodes and a higher replica count for every Deployment
- [x] Pod Security enforcement plus least-privilege RBAC
- [ ] Disabling audit logging to reduce the noise from alerts
- [ ] Moving all workloads into the kube-system namespace
> Si los usuarios y ServiceAccounts no pueden crear cargas privilegiadas (Pod Security *baseline* o *restricted*, RBAC mínimo y políticas de admisión adicionales), el atacante pierde la mayoría de vías para instalarse en los nodos. Desactivar la auditoría solo ayudaría al atacante.

### [4/Denial of Service/2]
Which controls prevent a single namespace from consuming all the resources of the cluster?
- [ ] NetworkPolicies and Ingress rules
- [x] ResourceQuotas and LimitRanges
- [ ] PodDisruptionBudgets and PriorityClasses
- [ ] RoleBindings and ServiceAccounts
> **ResourceQuota** limita el consumo total de un namespace (CPU, memoria, almacenamiento, número de objetos) y **LimitRange** fija valores por defecto y máximos por contenedor. Juntos evitan que un inquilino agote el clúster.

### [4/Denial of Service/2]
A container runs a fork bomb. Which setting limits its impact on the node?
- [ ] `readOnlyRootFilesystem: true` on the container
- [x] A PID limit, such as the kubelet's `podPidsLimit`
- [ ] `imagePullPolicy: Always` on every container
- [ ] `automountServiceAccountToken: false` on the Pod
> Una *fork bomb* crea procesos sin parar hasta agotar los PIDs del nodo, afectando a todos los Pods. Limitar el número de procesos por Pod (`podPidsLimit` en la configuración del kubelet) contiene el ataque. Los límites de CPU y memoria no limitan el número de procesos.

### [4/Denial of Service/2]
An attacker floods the API server with expensive LIST requests. Which built-in feature helps protect the other clients?
- [ ] NodeRestriction
- [x] API Priority and Fairness
- [ ] Pod Security Admission
- [ ] The Node authorizer
> **API Priority and Fairness** reparte la capacidad del API server entre niveles de prioridad y colas, de modo que un cliente abusivo no deja sin servicio al resto. Las peticiones de componentes críticos (por ejemplo, del control plane) tienen niveles reservados.

### [4/Denial of Service/2]
A user with create rights floods a namespace with hundreds of thousands of ConfigMaps. Which control limits this?
- [ ] A NetworkPolicy that denies all ingress traffic in the namespace
- [x] A ResourceQuota with object counts such as `count/configmaps`
- [ ] A PodDisruptionBudget with `minAvailable: 1`
- [ ] A LimitRange with default memory requests
> ResourceQuota también limita **número de objetos** (`count/configmaps`, `count/secrets`, `pods`…). Sin ese límite, crear objetos masivamente puede agotar el almacenamiento de etcd y degradar el API server para todo el clúster.

### [4/Denial of Service/2]
Why should containers set `ephemeral-storage` requests and limits?
- [ ] To encrypt the container's writable layer on the disk
- [x] To keep logs and writable layers from filling the node's disk
- [ ] To give the container access to the host's root filesystem
- [ ] To make the container image download faster
> Los logs, la capa escribible y los `emptyDir` consumen el disco del nodo. Sin límites, un contenedor puede llenarlo, provocando presión de disco y desalojos de otros Pods. Con límites de `ephemeral-storage` el kubelet desaloja solo al contenedor que se excede.

### [4/Denial of Service/3]
A validating admission webhook with `failurePolicy: Fail` becomes unavailable. What is the impact, and what is the trade-off of using `Ignore` instead?
- [ ] No impact; the API server caches the last answer of the webhook
- [x] Matching requests are rejected; with `Ignore` they bypass the policy
- [ ] All nodes are drained until the webhook comes back online
- [ ] etcd becomes read-only, and `Ignore` would delete the webhook
> Con `Fail`, si el webhook no responde, las peticiones que coinciden se rechazan: se protegen las políticas pero se arriesga la disponibilidad (por ejemplo, no se pueden crear Pods). Con `Ignore`, se admiten sin validar: se mantiene la disponibilidad, pero un atacante que tumbe el webhook se salta la política. Conviene que el webhook sea altamente disponible y excluir los namespaces del sistema.

### [4/Denial of Service/2]
Why should the size of the etcd database be monitored?
- [ ] Because etcd deletes the oldest Secrets when it gets full
- [x] Exceeding its storage quota raises an alarm that stops writes
- [ ] Because a large database disables the cluster's TLS
- [ ] Because etcd restarts every node when it grows too large
> etcd tiene una cuota de almacenamiento (`--quota-backend-bytes`). Si se supera, activa una alarma `NOSPACE` y deja de aceptar escrituras, con lo que el clúster queda prácticamente inmovilizado. Las cuotas de objetos, la compactación y la desfragmentación ayudan a evitarlo.

### [4/Malicious Code/2]
An attacker gets remote code execution in a web application container. Which settings most limit what they can do next?
- [ ] A high CPU limit and a large memory request for the container
- [x] Non-root user, read-only root FS, dropped capabilities and seccomp
- [ ] A LoadBalancer Service and a public DNS name for the app
- [ ] `hostPID: true` and an automatically mounted admin token
> Si el proceso no es root, no puede escribir en el sistema de archivos, no tiene capabilities extra, está filtrado por seccomp y no tiene un token de ServiceAccount útil, el atacante tiene muy poco margen para escalar o moverse. `hostPID` y un token privilegiado harían justo lo contrario.

### [4/Malicious Code/2]
Which runtime behavior is a strong indicator that a container has been compromised?
- [ ] The container writes its normal logs to stdout
- [x] An interactive shell or package manager starts unexpectedly
- [ ] The container's readiness probe succeeds after startup
- [ ] The container restarts once during a rolling update
> En producción, la mayoría de contenedores no deberían lanzar shells, instalar paquetes ni descargar herramientas. Reglas de Falco como *Terminal shell in container* o la ejecución de `apt`/`curl` inesperados son indicadores típicos de compromiso.

### [4/Malicious Code/2]
What is cryptojacking in a Kubernetes context?
- [ ] Encrypting the cluster's Secrets with a ransom key
- [x] Abusing cluster resources to mine cryptocurrency
- [ ] Stealing TLS certificates from the Ingress controller
- [ ] Signing container images with a stolen private key
> Es uno de los ataques más comunes contra clústeres expuestos: el atacante despliega mineros que consumen CPU a costa de la víctima. Se detecta por picos de consumo, conexiones a *mining pools* y reglas de runtime (Falco); se previene con buenas credenciales, admisión estricta y límites de recursos.

### [4/Malicious Code/2]
Which combination of Pod settings makes a container escape to the node trivial?
- [ ] `runAsNonRoot: true` and `readOnlyRootFilesystem: true`
- [x] `privileged: true` and `hostPID: true`
- [ ] `allowPrivilegeEscalation: false` and `drop: [ALL]`
- [ ] `seccompProfile: RuntimeDefault` and a memory limit
> Con un contenedor privilegiado que comparte el espacio de procesos del host, basta con entrar en los namespaces del proceso 1 del nodo (por ejemplo, `nsenter -t 1 -m -u -i -n -p -- bash`) para obtener una shell root en el host. Las otras combinaciones son configuraciones de endurecimiento.

### [4/Malicious Code/2]
Why does mounting the host's root filesystem (`hostPath: /`) into a container enable a full node compromise?
- [ ] Because it silently disables the container runtime's seccomp profile
- [x] The attacker can rewrite host files such as cron jobs or SSH keys
- [ ] Because it gives the container the node's IP address
- [ ] Because it automatically adds the container to `system:masters`
> Con escritura sobre `/` del host, el atacante puede añadir tareas cron, claves SSH, modificar binarios o la configuración del kubelet, o leer credenciales del nodo. Por eso los Pod Security Standards *baseline* y *restricted* prohíben `hostPath`.

### [4/Malicious Code/2]
How do sandboxed runtimes such as gVisor or Kata Containers help against kernel exploits launched by malicious code?
- [ ] They patch the host kernel automatically before each container starts
- [x] Syscalls hit a user-space or VM kernel, not the host kernel directly
- [ ] They block every outbound network connection from the container
- [ ] They scan the container image for malware before it runs
> El código malicioso necesita explotar el kernel para escapar. Con gVisor, sus syscalls las atiende un kernel en espacio de usuario; con Kata, el kernel de una micro-VM. Un exploit tendría que romper además esa capa para llegar al host.

### [4/Malicious Code/2]
A container image from a public registry contains a hidden cryptocurrency miner. Which control would have prevented its deployment?
- [ ] A PodDisruptionBudget for the affected Deployment
- [x] Admission that only allows signed, trusted images
- [ ] A HorizontalPodAutoscaler with a low CPU target
- [ ] A NodePort Service instead of a LoadBalancer
> Si solo se admiten imágenes de registros aprobados, escaneadas y firmadas por el pipeline propio (verificadas en la admisión con Kyverno, Gatekeeper o el *policy-controller* de Sigstore), una imagen pública manipulada no llega a ejecutarse.

### [4/Network Attacker/2]
An attacker inside a Pod tries ARP spoofing to intercept traffic from other Pods on the same node. Which capability do they need?
- [ ] `CAP_CHOWN`
- [x] `CAP_NET_RAW`
- [ ] `CAP_SETGID`
- [ ] `CAP_KILL`
> Para fabricar paquetes ARP falsos hace falta `NET_RAW` (sockets raw). Muchos runtimes la dan por defecto; eliminarla (`drop: [ALL]`, como exige *restricted*) impide este tipo de ataque desde el contenedor.

### [4/Network Attacker/2]
Which control prevents an attacker on the network from reading service-to-service traffic?
- [ ] A ResourceQuota on the namespace
- [x] Encryption in transit, such as mTLS
- [ ] A readiness probe on every Pod
- [ ] A PriorityClass for the backend
> Cifrar el tráfico (mTLS con un service mesh, o cifrado del CNI con WireGuard/IPsec) hace que quien espíe la red solo vea datos cifrados. Con mTLS, además, cada extremo verifica la identidad del otro, lo que también protege contra suplantaciones.

### [4/Network Attacker/2]
After compromising a frontend Pod, an attacker scans the cluster network for other services. Which control limits this lateral movement?
- [ ] A higher replica count for the frontend Deployment
- [x] Default-deny NetworkPolicies with explicit allow rules
- [ ] A larger CPU limit for the compromised container
- [ ] A ClusterIP Service in front of the frontend Pods
> Con una red plana, el atacante puede alcanzar cualquier Pod. Las NetworkPolicies de denegación por defecto, con permisos explícitos solo para los flujos necesarios, limitan el movimiento lateral a lo estrictamente permitido.

### [4/Network Attacker/2]
Why should application Pods generally not be able to reach port 10250 on the nodes?
- [ ] Because that port serves the public website of the cluster
- [x] It exposes the kubelet API, which can run commands in containers
- [ ] Because that port is used by the etcd peers to replicate their data
- [ ] Because the Ingress controller uses it for TLS termination
> El puerto 10250 es la API del kubelet. Aunque debería exigir autenticación y autorización, limitar a nivel de red quién puede alcanzarlo (firewalls, políticas) añade una capa más ante errores de configuración o vulnerabilidades del kubelet.

### [4/Network Attacker/2]
An attacker spoofs DNS answers inside the cluster to redirect a client to a malicious endpoint. Which control prevents the client from trusting that endpoint?
- [ ] A ResourceQuota on the client's namespace and its Pods
- [x] mTLS with certificate verification of the server's identity
- [ ] A larger memory limit and more replicas for the CoreDNS Pods
- [ ] A PodDisruptionBudget for the client Deployment
> Si el cliente verifica el certificado y la identidad del servidor (TLS o mTLS con identidades SPIFFE), un endpoint falso no podrá presentar un certificado válido para ese servicio, aunque el DNS haya sido manipulado. Por eso el cifrado con verificación de identidad mitiga la suplantación.

### [4/Network Attacker/2]
Which network control prevents Pods from reaching the cloud instance metadata endpoint?
- [ ] An ingress NetworkPolicy that allows only port 443
- [x] An egress policy that blocks `169.254.169.254/32`
- [ ] A Service of type ExternalName pointing to it
- [ ] A readiness probe that checks the metadata API
> El acceso a los metadatos es tráfico **saliente** del Pod, así que se bloquea con una política de egress (NetworkPolicy con `ipBlock` y `except`, o políticas del CNI) que excluya 169.254.169.254. Combinado con IMDSv2 y workload identity, evita el robo de credenciales del nodo.

### [4/Sensitive Data/2]
Where is a Pod's ServiceAccount token mounted by default?
- [ ] `/var/lib/kubelet/serviceaccounts/default/token`
- [x] `/var/run/secrets/kubernetes.io/serviceaccount/token`
- [ ] `/run/kubernetes/serviceaccount/default-token`
- [ ] `/etc/kubernetes/pki/serviceaccount/token`
> Salvo que se desactive con `automountServiceAccountToken: false`, Kubernetes monta en esa ruta el token del ServiceAccount, el certificado de la CA y el namespace. Un atacante que logra ejecutar código en el contenedor lo buscará ahí para hablar con el API server.

### [4/Sensitive Data/2]
Which of these is a common way in which secrets accidentally leak in Kubernetes environments?
- [ ] Through the readiness probe results shown by kubectl
- [x] Through image layers and application logs
- [ ] Through the resource requests of the containers
- [ ] Through the labels of the PersistentVolumes
> Secretos copiados en capas de la imagen o impresos en los logs de la aplicación son filtraciones muy frecuentes: las imágenes se distribuyen ampliamente y los logs se centralizan con accesos amplios. Hay que inyectar secretos en tiempo de ejecución y enmascararlos en los logs.

### [4/Sensitive Data/2]
Who can read every Secret in the cluster even without any RBAC permission on Secrets?
- [ ] Any user who can list the Nodes and their status in the cluster
- [x] Anyone with access to etcd or to its unencrypted backups
- [ ] Any ServiceAccount in the `default` namespace
- [ ] Any user who can read Kubernetes Events
> etcd y sus copias de seguridad contienen todos los Secrets; sin cifrado en reposo, en claro. Quien acceda a ellos se salta por completo RBAC. Por eso se cifra en reposo (idealmente con KMS), se restringe el acceso a etcd y se protegen los backups.

### [4/Sensitive Data/2]
A Deployment passes a database password with `env.value: "S3cr3t"` instead of `secretKeyRef`. What is the risk?
- [ ] None, because environment variables are always encrypted at rest
- [x] Anyone who can read the Deployment or Pod spec sees the password
- [ ] The password is rotated automatically by the kubelet every day
- [ ] The Pod is rejected by the API server for containing a password
> Un valor literal queda dentro del manifiesto, en etcd como parte del objeto, en Git y en la salida de `kubectl get -o yaml`, visible para cualquiera que pueda leer Deployments o Pods (permiso mucho más común que leer Secrets). Hay que referenciar un Secret o un gestor externo.

### [4/Sensitive Data/2]
Why should audit policies avoid logging the request and response bodies of Secrets and TokenReviews?
- [ ] Because those requests are never sent to the API server
- [x] To keep secret values and tokens out of the audit logs
- [ ] Because logging them makes the API server read-only
- [ ] Because audit logs cannot store JSON objects
> Los cuerpos de esas peticiones contienen valores secretos y tokens. Si se registran con nivel `Request` o `RequestResponse`, el sistema de logs pasa a ser un almacén de secretos con controles más débiles. Se registran a nivel `Metadata`.

### [4/Sensitive Data/2]
Which Kubernetes feature reduces the impact of a stolen ServiceAccount token?
- [ ] Long-lived tokens stored as Secrets in every namespace
- [x] Short-lived tokens bound to an audience and a Pod
- [ ] Sharing a single token among all the workloads
- [ ] Mounting the token into every container of the node
> Los tokens emitidos por TokenRequest caducan, están limitados a una audiencia y ligados al Pod: si el Pod se elimina, el token deja de ser válido. Un token robado sirve poco tiempo y solo para lo que fue emitido.

### [4/Sensitive Data/2]
How can a workload use a database password without it ever being stored in etcd?
- [ ] By writing it into a ConfigMap instead of a Secret object
- [x] By fetching it at runtime from an external secrets manager
- [ ] By base64-encoding it twice inside the Pod spec's env section
- [ ] By adding it as an annotation on the Deployment
> Con un gestor externo (Vault, AWS Secrets Manager…) la aplicación, un agente sidecar o el Secrets Store CSI Driver obtienen el secreto en tiempo de ejecución, sin crear un Secret de Kubernetes. Un ConfigMap o una anotación también acaban en etcd, y en claro.

### [4/Privilege Escalation/2]
What does `allowPrivilegeEscalation: false` prevent?
- [ ] The container from listening on privileged ports below 1024
- [x] Gaining privileges via setuid binaries such as `sudo`
- [ ] The container from writing to its own root filesystem layer
- [ ] Any network traffic that leaves the container's namespace
> Esta opción activa el flag `no_new_privs` del kernel: un proceso no puede obtener más privilegios que su padre, así que los binarios setuid o setgid (como `sudo`) no sirven para escalar. Es obligatoria en el perfil *restricted*.

### [4/Privilege Escalation/3]
A user can create Pods in a namespace but has no permission to read Secrets there. How could they still read a Secret?
- [ ] They cannot; RBAC also checks Secrets when a Pod mounts them
- [x] By creating a Pod that mounts the Secret and prints its contents
- [ ] By asking the scheduler to copy the Secret into a ConfigMap
- [ ] By running `kubectl get secret` with the `--force` flag
> El kubelet monta en el Pod los Secrets que este referencia, sin comprobar los permisos RBAC del usuario que creó el Pod. Basta con un Pod que monte el Secret y lo imprima en sus logs. Por eso crear Pods equivale, en la práctica, a poder leer los Secrets del namespace.

### [4/Privilege Escalation/2]
A user can create CertificateSigningRequests and approve them for the `kubernetes.io/kube-apiserver-client` signer. Why is this dangerous?
- [ ] They can only issue certificates for the Ingress controller
- [x] They can issue client certificates for any identity, even admin groups
- [ ] Approved certificates are valid only on their own laptop
- [ ] The CSR API automatically revokes the certificates after one hour
> Con ese firmante se emiten certificados de cliente para el API server con el CN y la O que el solicitante elija, por ejemplo un usuario de sistema o el grupo `system:masters`. Quien puede crear y aprobar esas CSRs puede convertirse en administrador del clúster.

### [4/Privilege Escalation/2]
Which RBAC permission lets a user issue new tokens for existing ServiceAccounts?
- [ ] `get` and `list` on `serviceaccounts`
- [x] `create` on `serviceaccounts/token`
- [ ] `list` on `configmaps` in kube-system
- [ ] `watch` on `events`
> El subrecurso `serviceaccounts/token` (API TokenRequest) emite tokens para un ServiceAccount. Con `create` sobre él, un usuario puede obtener credenciales de cualquier ServiceAccount del namespace, incluso de los más privilegiados.

### [4/Privilege Escalation/2]
An attacker stole a kubelet's credentials and tries to modify Pods on other nodes. What limits the damage?
- [ ] The default `view` ClusterRole bound to all kubelets
- [x] The Node authorizer plus NodeRestriction admission
- [ ] The readiness probes configured on the target Pods
- [ ] The PodDisruptionBudgets of the target Deployments
> El autorizador **Node** solo permite a cada kubelet acceder a los objetos relacionados con su propio nodo, y **NodeRestriction** impide que modifique otros nodos o los Pods vinculados a ellos. El atacante queda limitado al nodo comprometido.

### [4/Privilege Escalation/2]
Why is granting the `impersonate` verb on users and groups risky?
- [ ] It lets the user restart the API server whenever they want
- [x] They can act as more privileged identities
- [ ] It only allows reading the user's own profile information
- [ ] It removes the user from every RoleBinding of the cluster
> Con `impersonate`, una petición puede ejecutarse como otro usuario o grupo (por ejemplo `kubectl --as=admin --as-group=system:masters`). Si se permite suplantar identidades privilegiadas, el usuario obtiene sus permisos. Debe limitarse con `resourceNames` concretos, si se concede.

### [4/Privilege Escalation/2]
A Pod runs with `hostPID: true` and `privileged: true`. Which command could an attacker use from inside it to get a root shell on the node?
- [ ] `kubectl exec -it node/<node-name> --as=root -- bash`
- [x] `nsenter --target 1 --mount --uts --ipc --net --pid -- bash`
- [ ] `unshare --mount --uts --ipc --net --pid --fork -- bash`
- [ ] `sudo -u kubelet --preserve-env /bin/bash -i`
> Con el espacio de PIDs del host y privilegios, `nsenter` puede entrar en todos los namespaces del proceso 1 del nodo (init/systemd) y abrir una shell como root en el host. Es la técnica de escape más conocida y la razón por la que *baseline* prohíbe ambas opciones. Ojo con la trampa: `unshare` hace lo contrario, crea namespaces **nuevos** en lugar de entrar en los del host.

### [4/Privilege Escalation/2]
Why should operators and controllers with broad RBAC permissions be treated as highly sensitive?
- [ ] Because they always run as non-root and cannot be compromised
- [x] Compromising them yields their wide, often cluster-wide, privileges
- [ ] Because their Pods are never scheduled on worker nodes
- [ ] Because they cannot be updated without deleting the cluster
> Muchos operadores pueden crear Pods o leer Secrets en todos los namespaces. Si un atacante compromete uno (una vulnerabilidad, una imagen manipulada), hereda esos permisos. Hay que limitar su RBAC, aislarlos y vigilar sus actualizaciones.
