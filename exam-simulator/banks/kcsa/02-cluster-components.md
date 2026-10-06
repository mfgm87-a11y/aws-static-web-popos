# KCSA · Dominio 2 · Kubernetes Cluster Component Security

### [2/API Server/2]
Which kube-apiserver setting represents a secure authorization configuration?
- [ ] `--authorization-mode=AlwaysAllow`
- [x] `--authorization-mode=Node,RBAC`
- [ ] `--authorization-mode=AlwaysAllow,RBAC`
- [ ] `--authorization-mode=ABAC,AlwaysAllow`
> `Node,RBAC` es la configuración estándar: el autorizador **Node** limita lo que pueden hacer los kubelets y **RBAC** gobierna al resto. Los autorizadores se consultan en orden y el primero que permite gana, así que poner `AlwaysAllow` en cualquier posición deja pasar todo.

### [2/API Server/2]
Anonymous authentication is enabled on the kube-apiserver, and an unauthenticated request arrives. How is it treated?
- [ ] It is rejected immediately with a 401 by the API server
- [x] As user `system:anonymous`, then checked by the authorizers
- [ ] As the `cluster-admin` user, because no identity was given
- [ ] As the `default` ServiceAccount of the `default` namespace
> Con autenticación anónima activa, la petición sin credenciales recibe el usuario `system:anonymous` y el grupo `system:unauthenticated`, y después pasa por la autorización. Con RBAC por defecto solo puede acceder a endpoints como `/healthz` o `/version`. Por eso hay que evitar enlazar permisos a esas identidades.

### [2/API Server/2]
Which admission plugin restricts kubelets so that each one can only modify its own Node object and the Pods bound to it?
- [ ] PodSecurity
- [x] NodeRestriction
- [ ] LimitRanger
- [ ] AlwaysPullImages
> **NodeRestriction** complementa al autorizador Node: impide que un kubelet modifique otros nodos o Pods de otros nodos, y que se ponga a sí mismo labels con el prefijo `node-restriction.kubernetes.io/`. Si roban las credenciales de un kubelet, el daño queda acotado a ese nodo.

### [2/API Server/2]
Which kube-apiserver flag points to the configuration used to encrypt Secrets at rest in etcd?
- [ ] `--etcd-cafile`
- [x] `--encryption-provider-config`
- [ ] `--tls-cert-file`
- [ ] `--secrets-encryption=true`
> El cifrado en reposo se configura en el **API server** con un archivo `EncryptionConfiguration` indicado en `--encryption-provider-config`. etcd solo guarda el resultado cifrado. `--etcd-cafile` sirve para verificar a etcd y `--tls-cert-file` es el certificado del propio API server.

### [2/API Server/2]
Which pair of kube-apiserver flags enables audit logging to a file?
- [ ] `--audit-enabled` and `--audit-level`
- [x] `--audit-policy-file` and `--audit-log-path`
- [ ] `--log-level=audit` and `--v=10`
- [ ] `--enable-audit` and `--audit-namespace`
> La política (qué registrar y a qué nivel) se pasa con `--audit-policy-file` y el destino en archivo con `--audit-log-path` (también existe un backend webhook). Si no se indica una política, el API server no registra ningún evento de auditoría.

### [2/API Server/3]
How does the API server make sure it is talking to the real kubelet when it connects for `exec` or `logs`?
- [ ] It always verifies the kubelet certificate, with no configuration needed
- [x] It checks the kubelet cert with `--kubelet-certificate-authority`
- [ ] It sends the request over SSH using the node's private key
- [ ] It trusts any endpoint that answers on the kubelet port 10250
> Por defecto el API server **no verifica** el certificado de servicio del kubelet, lo que expone la conexión a ataques *man-in-the-middle*. Con `--kubelet-certificate-authority` le indicas la CA con la que comprobarlo (y conviene que los kubelets obtengan certificados firmados por el clúster). El API server se autentica ante el kubelet con `--kubelet-client-certificate`.

### [2/API Server/2]
Why does the CIS Kubernetes Benchmark recommend setting `--profiling=false` on control plane components?
- [ ] Profiling stores Secrets in plain text on the node disk
- [x] It exposes debugging data that production does not need
- [ ] Profiling disables TLS between the components automatically
- [ ] It makes etcd reject writes until profiling stops
> El endpoint de *profiling* revela detalles internos de rendimiento y del sistema que no se necesitan en producción y que podrían ayudar a un atacante (o facilitar una denegación de servicio). Desactivarlo reduce la superficie de ataque.

### [2/API Server/2]
Which kube-apiserver flag configures the CA used to validate X.509 client certificates presented by users and components?
- [ ] `--tls-private-key-file`
- [x] `--client-ca-file`
- [ ] `--service-account-key-file`
- [ ] `--kubelet-client-certificate`
> Con `--client-ca-file`, el API server acepta certificados de cliente firmados por esa CA; el CN del certificado se usa como nombre de usuario y los campos O como grupos. Por eso quien controle la clave de esa CA puede emitir identidades arbitrarias.

### [2/API Server/2]
Which statement about the kube-apiserver's old insecure port (8080) is correct?
- [ ] It is still enabled by default for local health checks
- [x] It was removed; all API access now goes through the TLS port
- [ ] It is required for kubelets to register their nodes
- [ ] It is used to serve the Metrics API without authentication
> El puerto inseguro (HTTP sin autenticación ni autorización) se eliminó hace años. Todo el acceso pasa por el puerto seguro con TLS (6443 por defecto en kubeadm), con autenticación, autorización y admisión.

### [2/API Server/3]
A user's client certificate puts them in the group `system:masters`. Why is this especially dangerous?
- [ ] Members of that group can only read objects, which breaks RBAC
- [x] The group bypasses RBAC and cannot be restricted with bindings
- [ ] The group is automatically mapped to an anonymous identity
- [ ] Members must re-authenticate on every single API request
> `system:masters` es un grupo de superusuario codificado en el API server: sus miembros tienen acceso total sin pasar por RBAC, así que no se les puede quitar permisos borrando RoleBindings. Una credencial filtrada con ese grupo solo se neutraliza cuando expira o rotando la CA. Por eso no se debe usar para el día a día.

### [2/API Server/2]
What happens if an attacker steals the private key that the API server uses to sign ServiceAccount tokens?
- [ ] Nothing, because tokens are also validated against etcd records
- [x] They can forge valid tokens for any ServiceAccount
- [ ] Only the tokens of the `default` ServiceAccount are affected
- [ ] The API server immediately rotates the key on its own
> El API server firma los tokens con la clave de `--service-account-signing-key-file` y los valida con la pública. Quien tenga la privada puede fabricar tokens para cualquier ServiceAccount (incluidos los muy privilegiados de kube-system). Debe protegerse como un secreto crítico del control plane.

### [2/Controller Manager/2]
What does `--use-service-account-credentials=true` on kube-controller-manager do?
- [ ] It mounts a token into every Pod created by the controllers
- [x] Each controller uses its own ServiceAccount with minimal RBAC
- [ ] It disables ServiceAccount tokens across the whole cluster
- [ ] It lets controllers authenticate with the cluster-admin user
> Con esta opción, cada controlador (replicaset-controller, job-controller…) actúa con su propio ServiceAccount en `kube-system` y sus propios permisos RBAC, en lugar de compartir las credenciales amplias del controller-manager. Es mínimo privilegio aplicado al control plane.

### [2/Controller Manager/2]
Why is kube-controller-manager a high-value target for attackers?
- [ ] It stores the container images that run on every node
- [x] It holds broad credentials and signing keys for the cluster
- [ ] It terminates TLS for all Ingress traffic of the cluster
- [ ] It runs inside every Pod as an injected sidecar container
> El controller-manager tiene permisos amplios sobre casi todos los recursos y acceso a claves sensibles: la CA del clúster, con la que firma las CSRs aprobadas, y la clave privada de ServiceAccount (`--service-account-private-key-file`), con la que firma los tokens antiguos guardados en Secrets. Comprometerlo puede llevar al control total del clúster.
>
> No guarda imágenes (eso es el registro), no termina TLS de Ingress (eso es el Ingress controller) y no corre dentro de los Pods.

### [2/Controller Manager/2]
The CIS Benchmark recommends binding kube-controller-manager and kube-scheduler to `127.0.0.1`. Why?
- [ ] So that they can only be reached through the cluster's Ingress controller
- [x] Their health and metrics endpoints should not be exposed on the network
- [ ] Because both components refuse to start on any other interface
- [ ] So that kubelets can reach them directly without TLS
> Estos componentes solo necesitan hablar con el API server (saliente). Sus endpoints de salud y métricas no deberían estar expuestos a la red del clúster; ligarlos a localhost reduce la superficie de ataque.

### [2/Controller Manager/2]
Which key material does kube-controller-manager use to sign approved CertificateSigningRequests, such as kubelet client certificates?
- [ ] The etcd peer certificate and key
- [x] The cluster CA certificate and private key
- [ ] The Ingress controller's TLS certificate
- [ ] The ServiceAccount token signing key
> El controlador de firma de certificados usa `--cluster-signing-cert-file` y `--cluster-signing-key-file` (normalmente la CA del clúster) para firmar CSRs aprobadas de los firmantes integrados. Por eso la clave de la CA es uno de los secretos más críticos.

### [2/Scheduler/2]
What could an attacker achieve by compromising the kube-scheduler?
- [ ] Read every Secret directly from the etcd database files
- [x] Place Pods on chosen nodes, or stop scheduling altogether
- [ ] Bypass the TLS between every component of the control plane
- [ ] Change the RBAC roles bound to every user
> El scheduler decide dónde corre cada Pod. Un atacante que lo controle podría colocar cargas maliciosas junto a objetivos sensibles o en nodos concretos, o dejar Pods sin programar (denegación de servicio). Por eso su identidad (`system:kube-scheduler`) tiene solo los permisos que necesita.

### [2/Scheduler/2]
Which file on a kubeadm control plane node contains the kube-scheduler's credentials and must have restrictive permissions?
- [ ] `/etc/kubernetes/pki/ca.crt`
- [x] `/etc/kubernetes/scheduler.conf`
- [ ] `/var/lib/kubelet/config.yaml`
- [ ] `/etc/cni/net.d/10-flannel.conflist`
> Cada componente del control plane tiene su kubeconfig con credenciales (`scheduler.conf`, `controller-manager.conf`, `admin.conf`…). El CIS Benchmark pide que sean propiedad de root y con permisos restrictivos (600), porque quien los lea obtiene esa identidad.

### [2/Scheduler/3]
Why is the Pod field `spec.nodeName` relevant to workload isolation?
- [ ] It forces the Pod to run inside a sandboxed runtime class
- [x] It bypasses the scheduler, so taints and affinity are skipped
- [ ] It encrypts the Pod's traffic to its node with mutual TLS
- [ ] It prevents the Pod from ever being evicted by the kubelet
> Si un Pod ya trae `nodeName`, el scheduler no interviene: no se evalúan taints `NoSchedule`, afinidades ni topologías, y el kubelet de ese nodo intenta ejecutarlo. Si confías en taints para aislar nodos sensibles, conviene restringir `nodeName` (y las tolerations) con políticas de admisión.

### [2/Scheduler/2]
Which identity does the kube-scheduler normally use to talk to the API server?
- [ ] The `kubernetes-admin` user from the `admin.conf` kubeconfig
- [x] The `system:kube-scheduler` user with a dedicated ClusterRole
- [ ] An anonymous identity that is limited by NetworkPolicies
- [ ] The kubelet identity of the control plane node where it runs
> kubeadm crea para el scheduler la identidad `system:kube-scheduler`, enlazada a un ClusterRole del mismo nombre con los permisos justos (leer Pods y nodos, crear bindings, eventos, leases…). Es mínimo privilegio para un componente del control plane.

### [2/Kubelet/2]
With the kubelet binary's built-in defaults, what is the authorization mode of the kubelet API?
- [ ] Webhook
- [x] AlwaysAllow
- [ ] RBAC
- [ ] Node
> El valor por defecto del binario del kubelet es `AlwaysAllow` (y la autenticación anónima está habilitada). Por eso hay que configurarlo con `--authorization-mode=Webhook` (o `authorization.mode: Webhook` en su archivo de configuración), que delega la decisión al API server. kubeadm ya lo configura así.

### [2/Kubelet/2]
Which kubelet setting makes unauthenticated requests to the kubelet API receive `401 Unauthorized`?
- [ ] `--read-only-port=10255`
- [x] `--anonymous-auth=false`
- [ ] `--authorization-mode=AlwaysAllow`
- [ ] `--rotate-certificates=false`
> Con `--anonymous-auth=false` (o `authentication.anonymous.enabled: false`), las peticiones sin credenciales válidas se rechazan con 401 en lugar de tratarse como `system:anonymous`. Se combina con certificados de cliente o *token webhook* para autenticación y con `Webhook` para autorización.

### [2/Kubelet/2]
What should be done with the kubelet's read-only port (10255)?
- [ ] Expose it to the internet so that monitoring works
- [x] Disable it by setting the read-only port to 0
- [ ] Protect it with a Kubernetes NetworkPolicy only
- [ ] Use it for kubectl exec instead of port 10250
> El puerto de solo lectura 10255 sirve información del nodo y de sus Pods **sin autenticación ni autorización**. La recomendación (CIS) es desactivarlo (`--read-only-port=0` o `readOnlyPort: 0`) y obtener métricas por el puerto seguro 10250 con autenticación.

### [2/Kubelet/2]
What can an attacker do through an unprotected kubelet API on port 10250?
- [ ] Only read the node's CPU temperature and uptime
- [x] Run commands in containers and read their logs
- [ ] Change the cluster's RBAC roles and bindings
- [ ] Rotate the cluster CA and lock out administrators
> La API del kubelet permite listar Pods, leer logs y ejecutar comandos dentro de contenedores (`exec`/`run`). Si acepta peticiones anónimas o no autoriza, cualquiera con acceso de red al nodo puede comprometer sus cargas. Por eso: autenticación obligatoria, autorización Webhook y firewall.

### [2/Kubelet/2]
Which authorizer limits each kubelet to reading only the Secrets, ConfigMaps and volumes referenced by Pods scheduled to its own node?
- [ ] The RBAC authorizer
- [x] The Node authorizer
- [ ] The ABAC authorizer
- [ ] The Webhook authorizer
> El **autorizador Node** es un autorizador especial para kubelets (usuarios `system:node:<nombre>` del grupo `system:nodes`): solo les deja leer los Secrets, ConfigMaps, PVCs y PVs vinculados a Pods de su propio nodo. Junto con NodeRestriction, limita el daño si roban las credenciales de un nodo.

### [2/Kubelet/2]
What is the benefit of enabling kubelet client certificate rotation?
- [ ] It lets the kubelet skip authentication against the API server
- [x] The kubelet renews its certificate before it expires
- [ ] It encrypts the container images stored on the node's disk
- [ ] It rotates the cluster CA every time a node reboots
> Con la rotación de certificados, el kubelet solicita uno nuevo (mediante una CSR) cuando el actual se acerca a su vencimiento. Así las credenciales del nodo duran poco y no hay que renovarlas a mano.

### [2/Kubelet/3]
Why is RBAC `get` permission on the `nodes/proxy` subresource considered dangerous?
- [ ] It only exposes node metrics, which are verbose but harmless
- [x] It reaches the kubelet API, allowing exec into any Pod on the node
- [ ] It lets the user reboot nodes through the cloud provider's API
- [ ] It grants permission to edit the node's labels, taints and annotations
> `nodes/proxy` da acceso a la API del kubelet. Algunos de sus endpoints funcionan con WebSockets mediante peticiones HTTP `GET`, así que el verbo **get** basta para ejecutar comandos en cualquier contenedor del nodo, y además esas acciones **no pasan por la auditoría ni por la admisión** del API server. No es un permiso de solo lectura.

### [2/Kubelet/2]
Why must write access to the kubelet's static Pod manifest directory be tightly restricted?
- [ ] Because the directory also stores the etcd encryption keys
- [x] Anyone who writes there can run Pods on the node, skipping admission
- [ ] Because the kubelet deletes the Node object if a file changes there
- [ ] Because static Pods always share the same IP as the API server
> El kubelet ejecuta todo lo que encuentre en ese directorio (en kubeadm, `/etc/kubernetes/manifests`) sin pasar por el scheduler ni por la admisión del API server. Un atacante con acceso de escritura al nodo podría lanzar Pods privilegiados y persistentes.

### [2/Kubelet/2]
How does a new node securely obtain its kubelet client certificate when it joins a kubeadm cluster?
- [ ] It copies `admin.conf` from the control plane over SSH
- [x] TLS bootstrapping: a bootstrap token is used to submit a CSR that gets signed
- [ ] The scheduler emails a certificate to the node administrator
- [ ] The kubelet generates a self-signed certificate that the API server trusts
> Con *TLS bootstrapping*, el kubelet usa un token de arranque de corta vida para autenticarse, envía una CertificateSigningRequest y, una vez aprobada, el controller-manager la firma con la CA del clúster. Así cada nodo obtiene su propia identidad `system:node:<nombre>` sin compartir credenciales de administrador.

### [2/Kubelet/2]
With `--authorization-mode=Webhook`, how does the kubelet decide whether a request is allowed?
- [ ] It checks a local file that lists the allowed users
- [x] It asks the API server through a SubjectAccessReview
- [ ] It allows every request that arrives over TLS
- [ ] It forwards the request to the cluster's Ingress controller
> En modo Webhook, el kubelet envía una **SubjectAccessReview** al API server, que evalúa la petición con sus autorizadores (por ejemplo RBAC sobre los subrecursos `nodes/proxy`, `nodes/log` o `nodes/stats`). Así los permisos sobre el kubelet se gestionan de forma centralizada.

### [2/Container Runtime/3]
Why is mounting the container runtime socket (e.g. `containerd.sock` or `docker.sock`) into a Pod dangerous?
- [ ] It only slows down image pulls for the other Pods on the node
- [x] It gives full control of the node's container runtime
- [ ] It exposes the Pod's environment variables to the API server
- [ ] It disables the readiness probes of every container on the node
> Quien habla con el socket del runtime puede crear contenedores privilegiados, montar el sistema de archivos del host o leer cualquier contenedor del nodo: en la práctica es **root en el nodo**, saltándose el API server, la auditoría y la admisión. Es uno de los vectores de escape más conocidos.

### [2/Container Runtime/2]
Vulnerabilities such as CVE-2019-5736 and CVE-2024-21626 ("Leaky Vessels") in runc allowed what?
- [ ] Reading Secrets from etcd without any authentication
- [x] Escaping from a container to gain access to the host
- [ ] Bypassing RBAC on the Kubernetes API server
- [ ] Spoofing DNS answers for every Service in the cluster
> Ambas vulnerabilidades del runtime de bajo nivel permitían a un contenedor malicioso escapar al host (sobrescribiendo el binario de runc o abusando de descriptores de archivo filtrados). Mantener el runtime actualizado y añadir capas como seccomp, AppArmor/SELinux o runtimes con sandbox reduce el riesgo.

### [2/Container Runtime/2]
What does running the container runtime and containers in rootless mode achieve?
- [ ] Containers can bind to any privileged port on the host
- [x] An escape lands as an unprivileged user instead of root
- [ ] The runtime no longer needs any Linux namespaces
- [ ] Images no longer need to be pulled from a registry
> En modo *rootless*, el runtime y los contenedores se ejecutan con un usuario sin privilegios del host (apoyándose en user namespaces). Si un proceso escapa, no obtiene root en el nodo, lo que reduce mucho el impacto.

### [2/Container Runtime/2]
Which seccomp profile type applies the container runtime's default system call filter?
- [ ] Unconfined
- [x] RuntimeDefault
- [ ] Privileged
- [ ] HostDefault
> `seccompProfile.type: RuntimeDefault` aplica el filtro por defecto del runtime, que bloquea syscalls peligrosas o poco usadas. `Localhost` usa un perfil propio del nodo y `Unconfined` no filtra nada (prohibido por el perfil *baseline*).

### [2/Container Runtime/2]
Why is it recommended to enable the kubelet's `seccompDefault` setting?
- [ ] It forces every container on the node to run in privileged mode
- [x] Pods get `RuntimeDefault` seccomp unless they specify otherwise
- [ ] It removes all Linux capabilities from system Pods only
- [ ] It replaces AppArmor profiles with SELinux labels
> Sin esta opción, los contenedores que no indican un perfil se ejecutan como `Unconfined`. Con `seccompDefault: true` (estable desde 1.27) el kubelet aplica `RuntimeDefault` por defecto, elevando la base de seguridad de todo el nodo.

### [2/KubeProxy/2]
What is the security impact of a compromised kube-proxy?
- [ ] It could read every Secret stored in etcd directly
- [x] It could rewrite the node's Service rules to redirect traffic
- [ ] It could approve CertificateSigningRequests for any user
- [ ] It could change the Pod Security level of namespaces
> kube-proxy programa las reglas (iptables, nftables…) que implementan los Services en el nodo. Si un atacante lo controla, podría redirigir o interceptar el tráfico hacia los Services. Por eso su configuración y su DaemonSet deben protegerse.

### [2/KubeProxy/2]
Does kube-proxy encrypt Service traffic that travels between nodes?
- [ ] Yes, it always wraps Service traffic in TLS by default
- [x] No, it only programs forwarding rules on each node
- [ ] Yes, but only for NodePort and LoadBalancer Services
- [ ] Only when the IPVS proxy mode is selected
> kube-proxy solo traduce la IP virtual del Service a IPs de Pods; no cifra nada. Para cifrar el tráfico entre nodos se usa cifrado del CNI (WireGuard o IPsec en Cilium o Calico) o un service mesh con mTLS.

### [2/KubeProxy/2]
Why can NodePort Services increase a cluster's attack surface?
- [ ] They disable the NetworkPolicies of the namespace
- [x] They open a port on every node, even where no backend runs
- [ ] They give the Pods direct access to the host filesystem
- [ ] They expose the API server on the same port number
> Un Service NodePort abre su puerto en todos los nodos, y el tráfico se reenvía a los Pods aunque estén en otro nodo. Si los nodos son accesibles desde redes no confiables, ese puerto también lo es. Conviene restringirlo con firewalls o security groups y preferir balanceadores internos o Ingress/Gateway.

### [2/KubeProxy/2]
kube-proxy usually runs as a privileged DaemonSet with host networking. What follows from that?
- [ ] Its DaemonSet can safely be edited by every developer in the team
- [x] Whoever can change its DaemonSet runs privileged code on every node
- [ ] It cannot be affected by any vulnerability in the node's kernel
- [ ] Its Pods are exempt from being scheduled on new nodes
> Como necesita modificar las reglas de red del host, kube-proxy corre con privilegios y en la red del nodo. Quien pueda modificar su DaemonSet (o su imagen) podría ejecutar código privilegiado en todos los nodos, así que esos permisos RBAC deben estar muy restringidos.

### [2/Pod/2]
Which Pod setting gives a container nearly the same access to the host as a root process running on the node?
- [ ] `runAsNonRoot: true`
- [x] `privileged: true`
- [ ] `readOnlyRootFilesystem: true`
- [ ] `automountServiceAccountToken: false`
> Un contenedor **privilegiado** tiene todas las capabilities, acceso a los dispositivos del host y desactiva la mayoría de mecanismos de aislamiento (seccomp, AppArmor…). Escapar al nodo es trivial. Los perfiles *baseline* y *restricted* lo prohíben.

### [2/Pod/2]
What does `hostPID: true` allow a container to do?
- [ ] Use a private PID namespace separate from the host
- [x] See and interact with every process running on the host
- [ ] Choose its own process ID when the Pod starts
- [ ] Limit the number of processes it is allowed to create
> Con `hostPID` el contenedor comparte el espacio de procesos del nodo: ve todos los procesos, puede leer sus variables de entorno o memoria si tiene permisos y, con privilegios, entrar en sus namespaces (por ejemplo con `nsenter -t 1`). *Baseline* lo prohíbe.

### [2/Pod/2]
What is the main security benefit of `readOnlyRootFilesystem: true`?
- [ ] It encrypts the container's filesystem at rest
- [x] Attackers cannot modify binaries or drop tools into the image
- [ ] It makes Secrets mounted in the Pod read-only for the kubelet
- [ ] It prevents the container from reading its own configuration
> Con el sistema de archivos raíz en solo lectura, un atacante no puede reemplazar binarios ni descargar y guardar herramientas en el contenedor. Si la app necesita escribir, se le dan volúmenes concretos (por ejemplo un `emptyDir` para `/tmp`).

### [2/Pod/2]
From a security perspective, why should containers set CPU and memory limits?
- [ ] Limits encrypt the memory pages used by the container
- [x] They contain resource exhaustion and denial-of-service attacks
- [ ] Limits stop the container from making any network calls
- [ ] They are required for the container to use TLS certificates
> Sin límites, un contenedor comprometido (o con un bug) puede consumir toda la CPU o la memoria del nodo y afectar a los demás Pods. Los limits, junto con ResourceQuotas y LimitRanges, acotan ese impacto.

### [2/Pod/2]
Which Linux capability is especially dangerous to add to a container because it allows a very wide range of administrative operations?
- [ ] `CAP_NET_BIND_SERVICE`
- [x] `CAP_SYS_ADMIN`
- [ ] `CAP_CHOWN`
- [ ] `CAP_KILL`
> `CAP_SYS_ADMIN` es una "super-capability": permite montar sistemas de archivos, manipular namespaces y mucho más, y aparece en muchas técnicas de escape. *Baseline* no permite añadirla. `NET_BIND_SERVICE` solo permite usar puertos por debajo de 1024.

### [2/Pod/2]
What changes when a Pod uses `hostNetwork: true`?
- [ ] It gets a dedicated virtual NIC that is isolated from the node
- [x] It shares the node's network namespace, interfaces and ports
- [ ] Its traffic is encrypted automatically by the CNI plugin
- [ ] It can only reach the cluster's DNS service and nothing else
> Con `hostNetwork` el Pod usa directamente la red del nodo: puede escuchar en sus puertos, ver su tráfico y alcanzar servicios que el nodo solo expone en localhost, y la mayoría de plugins no le aplica NetworkPolicies. *Baseline* lo prohíbe salvo para agentes del sistema.

### [2/etcd/2]
Why is direct write access to etcd equivalent to full cluster compromise?
- [ ] etcd stores the container images that the nodes pull and run
- [x] Writes to etcd bypass authentication, authorization and admission
- [ ] etcd can reboot every node of the cluster when its data changes
- [ ] etcd holds the private keys of every linked cloud account
> El API server aplica autenticación, autorización y admisión, pero si alguien escribe directamente en etcd se salta todo eso: puede crear un ClusterRoleBinding a cluster-admin, modificar Pods o leer todos los Secrets. Por eso solo el API server debe poder hablar con etcd.

### [2/etcd/2]
Which etcd setting requires clients to present a certificate signed by a trusted CA?
- [ ] `--auto-tls=true` with `--peer-auto-tls=true`
- [x] `--client-cert-auth=true` with `--trusted-ca-file`
- [ ] `--listen-client-urls=http://0.0.0.0:2379`
- [ ] `--enable-v2=true`
> Con `--client-cert-auth=true` y `--trusted-ca-file`, etcd exige certificados de cliente válidos (el API server usa `--etcd-certfile` y `--etcd-keyfile`). `--auto-tls` genera certificados autofirmados que no deberían usarse en producción, y escuchar en `http://` dejaría el tráfico sin cifrar.

### [2/etcd/2]
Which components should be allowed to reach etcd's client port (2379)?
- [ ] Every Pod in the kube-system namespace
- [x] Only the kube-apiserver
- [ ] All kubelets, so they can read their Pods
- [ ] Any client inside the cluster network
> Solo el kube-apiserver necesita hablar con etcd por el puerto de clientes 2379 (los miembros de etcd se comunican entre sí por el 2380). Restringirlo con firewall y certificados de cliente evita que un Pod o nodo comprometido lea o modifique el estado del clúster.

### [2/etcd/2]
What is the purpose of `--peer-client-cert-auth` and the peer TLS settings in etcd?
- [ ] To let kubelets authenticate to etcd with their node certificates
- [x] To authenticate and encrypt traffic between etcd members
- [ ] To encrypt Secrets at rest inside the etcd data directory
- [ ] To expose etcd metrics to Prometheus without authentication
> Los miembros de etcd replican datos entre sí por el puerto de pares (2380). Las opciones `--peer-cert-file`, `--peer-key-file`, `--peer-trusted-ca-file` y `--peer-client-cert-auth` cifran y autentican ese tráfico para que nadie pueda unirse al clúster de etcd ni espiar la replicación.

### [2/etcd/2]
Why must etcd snapshot backups be protected as carefully as etcd itself?
- [ ] Because snapshots can only be restored once
- [x] They contain all cluster data, including Secrets
- [ ] Because snapshots also include the node OS images
- [ ] Because restoring one deletes the RBAC configuration
> Una snapshot contiene todo el estado del clúster, incluidos los Secrets (en claro si no hay cifrado en reposo). Los backups deben cifrarse, guardarse con acceso restringido y, en lo posible, fuera del clúster.

### [2/etcd/2]
Where is encryption at rest for Kubernetes Secrets configured?
- [ ] In etcd, with a flag that encrypts every key automatically
- [x] In the API server, through an EncryptionConfiguration file
- [ ] In each kubelet, which encrypts Secrets before sending them
- [ ] In the CNI plugin, which encrypts traffic towards etcd
> El API server cifra los recursos indicados (normalmente Secrets) antes de escribirlos en etcd según la `EncryptionConfiguration`. Así, aunque alguien obtenga los datos de etcd o un backup, ve texto cifrado (y con KMS, la clave maestra ni siquiera está en el clúster).

### [2/etcd/2]
Why do kubeadm clusters use a separate certificate authority for etcd?
- [ ] Because etcd cannot parse certificates from the cluster CA
- [x] So certificates from the cluster CA cannot authenticate to etcd
- [ ] So that etcd can use plain HTTP inside the cluster
- [ ] Because the API server refuses to talk to an etcd sharing its CA
> Si etcd confiara en la misma CA que el resto del clúster, cualquier certificado de cliente válido del clúster (por ejemplo, de un kubelet) podría usarse contra etcd. Una CA dedicada limita quién puede conectarse: en la práctica, solo el API server y los propios miembros de etcd.

### [2/etcd/2]
Why should the etcd data directory be owned by the etcd user with restrictive permissions?
- [ ] Because etcd refuses to start if anyone else can read it
- [x] It stores raw cluster data that could expose Secrets
- [ ] Because the directory also holds the kubelet binaries
- [ ] Because Kubernetes deletes it when permissions are open
> El directorio de datos de etcd contiene todo el estado del clúster. El CIS Benchmark recomienda permisos 700 y propietario `etcd:etcd`, para que ningún otro usuario del nodo pueda copiarlo o modificarlo.

### [2/Container Networking/2]
By default, can a compromised Pod in namespace A connect to a database Pod in namespace B?
- [ ] No, namespaces block traffic between them by default
- [x] Yes, unless NetworkPolicies restrict that traffic
- [ ] Only if both Pods use the same ServiceAccount
- [ ] Only through the API server's proxy subresource
> La red de Pods es plana por defecto: cualquier Pod puede conectarse a cualquier otro, sin importar el namespace. Para segmentar hay que aplicar NetworkPolicies (con un CNI que las soporte), idealmente con una política de denegación por defecto.

### [2/Container Networking/2]
How can Pod-to-Pod traffic between nodes be encrypted without changing the applications?
- [ ] By enabling the kube-proxy IPVS mode with strict ARP on every node
- [x] With CNI encryption (WireGuard/IPsec) or a service mesh with mTLS
- [ ] By labeling the namespaces with `encryption=true`
- [ ] By switching all Services to the ExternalName type
> Hay dos enfoques comunes: cifrado en la capa de red del CNI (WireGuard o IPsec en Cilium o Calico), que cifra todo el tráfico entre nodos, o un service mesh con mTLS, que además autentica identidades de servicio. kube-proxy y las labels no cifran nada.

### [2/Container Networking/3]
Why may NetworkPolicies fail to protect traffic from Pods that use `hostNetwork: true`?
- [ ] Because hostNetwork Pods always run inside a sandboxed runtime
- [x] Their traffic looks like node traffic, which most plugins cannot police
- [ ] Because NetworkPolicies only apply inside the `default` namespace
- [ ] Because hostNetwork Pods can only use the UDP protocol
> El comportamiento de las NetworkPolicies con Pods `hostNetwork` no está definido: en la mayoría de plugins su tráfico es indistinguible del tráfico del propio nodo, así que no se les aplican las reglas de Pod. Es otra razón para restringir `hostNetwork` con Pod Security.

### [2/Container Networking/2]
A cluster uses a CNI plugin that does not implement NetworkPolicy. What is the security consequence?
- [ ] The API server rejects any NetworkPolicy object you create
- [x] Policies are accepted by the API but never enforced
- [ ] All Pod traffic is blocked until a policy is created
- [ ] Only egress rules are enforced, ingress rules are ignored
> El API server acepta y guarda las NetworkPolicies, pero quien las aplica es el plugin CNI. Si no las soporta, no tienen efecto y dan una falsa sensación de seguridad. Conviene comprobarlo con una prueba de conectividad.

### [2/Client Security/2]
Why should `insecure-skip-tls-verify: true` be avoided in a kubeconfig?
- [ ] It makes kubectl commands noticeably slower
- [x] It stops checking the API server cert, enabling MITM attacks
- [ ] It sends the user's password to the API server in plain text
- [ ] It disables RBAC for that user on the API server
> Esta opción hace que kubectl no verifique el certificado del API server, así que un atacante en la red podría hacerse pasar por él y capturar credenciales o respuestas. Hay que usar `certificate-authority-data` con la CA real del clúster.

### [2/Client Security/2]
Why are long-lived client certificates risky as credentials for human users in Kubernetes?
- [ ] Kubernetes cannot verify certificates signed by its own CA
- [x] Kubernetes cannot revoke them; a leaked one works until it expires
- [ ] Certificates force every user into the `system:masters` group
- [ ] They can only be used from the control plane nodes
> Kubernetes no consulta listas de revocación para certificados de cliente: uno filtrado sigue funcionando hasta que vence (o hasta rotar la CA). Para personas es mejor usar OIDC con tokens de corta duración y grupos gestionados en el proveedor de identidad.

### [2/Client Security/2]
Which is a good practice for kubeconfig files on administrators' workstations?
- [ ] Share one admin kubeconfig between all team members
- [x] Use personal identities with short-lived credentials
- [ ] Store the kubeconfig in a public Git repository
- [ ] Disable TLS verification so that VPN changes do not break it
> Cada persona debe tener su propia identidad (auditable y revocable a nivel de RBAC), con credenciales de corta duración (OIDC o plugins de credenciales). El archivo debe tener permisos restrictivos y nunca compartirse ni subirse a un repositorio.

### [2/Client Security/2]
What does a client-go credential plugin (the `exec` section of a kubeconfig) enable?
- [ ] Running shell commands inside Pods without any RBAC checks
- [x] Fetching short-lived tokens from an external identity provider
- [ ] Executing kubectl commands on the control plane through SSH
- [ ] Storing user passwords encrypted inside the kubeconfig file
> Los plugins `exec` permiten que kubectl obtenga tokens de un proveedor externo (IAM de la nube, OIDC, Vault…) cuando los necesita, en lugar de guardar credenciales estáticas en el kubeconfig. Es lo que usan, por ejemplo, `aws eks get-token` o `kubelogin`.

### [2/Storage/2]
How can data stored on PersistentVolumes be protected at rest?
- [ ] By labeling the PersistentVolumeClaim with `security: sensitive`
- [x] With storage-level encryption, e.g. encrypted disks with KMS keys
- [ ] By mounting the volume with `readOnly: true` in every Pod
- [ ] By using an `emptyDir` volume in front of the real volume
> El cifrado en reposo de los volúmenes lo proporciona el backend de almacenamiento o el driver CSI (por ejemplo, discos de nube cifrados con claves gestionadas en KMS). Kubernetes no cifra los datos de los PV por sí mismo.

### [2/Storage/2]
Why is permission to create PersistentVolumes considered sensitive?
- [ ] PersistentVolumes can change the RBAC roles of a namespace
- [x] It allows creating `hostPath` PVs that expose node filesystems
- [ ] PersistentVolumes automatically run privileged init containers
- [ ] It lets the user read the etcd snapshot of the cluster
> Quien puede crear PVs arbitrarios puede crear uno de tipo `hostPath` y, con un PVC, dar a un Pod acceso al sistema de archivos del nodo, saltándose las restricciones de Pod Security sobre volúmenes `hostPath`. Los usuarios normales deberían usar PVCs con StorageClasses aprobadas.

### [2/Storage/3]
A PV with `persistentVolumeReclaimPolicy: Retain` is released after a tenant deletes their PVC. What is the security concern before the volume is reused?
- [ ] The PV's encryption key is deleted together with the PVC
- [x] The previous tenant's data is still on it and must be wiped
- [ ] The PV is automatically bound to a Pod in kube-system
- [ ] Retained volumes are mounted read-write on every node
> Con `Retain`, los datos sobreviven al PVC. Si un administrador reutiliza el volumen para otro inquilino sin borrarlo de forma segura, este podría leer los datos anteriores (remanencia de datos). Hay que limpiarlo o destruirlo antes de reasignarlo.
