# KCNA · Dominio 2 · Container Orchestration · Networking y Security

### [2/Networking/1]
Which statement describes the Kubernetes networking model?
- [ ] Pods on different nodes must use NAT to talk to each other
- [x] Every Pod gets its own IP and can reach other Pods without NAT
- [ ] Each container inside a Pod gets its own unique IP address
- [ ] Pods can only communicate with each other through Services
> El modelo de red de Kubernetes exige que cada Pod tenga su propia IP y que todos los Pods puedan comunicarse entre sí, en cualquier nodo, sin NAT. Los contenedores de un Pod comparten esa IP. Los Services añaden IPs estables y balanceo, pero no son obligatorios para hablar de Pod a Pod.

### [2/Networking/2]
Which component assigns IP addresses to Pods and wires up their network interfaces?
- [ ] kube-proxy, when it programs the Service rules
- [x] The CNI plugin, such as Calico or Cilium
- [ ] CoreDNS, when it registers the Pod's name
- [ ] The kube-scheduler, when it binds the Pod
> Cuando el runtime crea el sandbox del Pod, invoca al plugin **CNI** (Container Network Interface), que crea la interfaz, asigna la IP (IPAM) y configura las rutas. kube-proxy solo implementa los Services y CoreDNS resuelve nombres.

### [2/Networking/1]
What is the default Service type when `type` is not specified?
- [x] ClusterIP
- [ ] NodePort
- [ ] LoadBalancer
- [ ] ExternalName
> Por defecto un Service es **ClusterIP**: una IP virtual accesible solo dentro del clúster. NodePort lo expone en un puerto de cada nodo, LoadBalancer pide un balanceador externo y ExternalName devuelve un CNAME.

### [2/Networking/2]
What is the default port range for NodePort Services?
- [ ] 1–1024
- [ ] 8000–9000
- [x] 30000–32767
- [ ] 49152–65535
> Por defecto los NodePorts se asignan en el rango 30000–32767 (configurable en el API server con `--service-node-port-range`). El Service queda accesible en `<IP-de-cualquier-nodo>:<nodePort>`.

### [2/Networking/2]
A Service is defined with `port: 80` and `targetPort: 8080`. What does each value mean?
- [x] Clients use port 80 on the Service; traffic goes to port 8080 on the Pods
- [ ] The Pods listen on port 80, while the Service itself listens on port 8080
- [ ] Port 80 carries the HTTP traffic and port 8080 carries the HTTPS traffic
- [ ] Port 8080 is the NodePort that is opened on every node of the cluster
> `port` es el puerto del Service (lo que usan los clientes, p. ej. `mi-svc:80`) y `targetPort` es el puerto del contenedor al que se reenvía el tráfico. En un Service NodePort existe además `nodePort` (30000–32767).

### [2/Networking/2]
What does a headless Service (`clusterIP: None`) return when a client resolves its DNS name?
- [ ] The ClusterIP that was assigned to the Service
- [x] The IP addresses of the ready Pods behind it
- [ ] The IP address of the node that runs CoreDNS
- [ ] An NXDOMAIN error, because it has no IP address
> Un Service headless no tiene IP virtual ni balanceo de kube-proxy: su nombre DNS devuelve registros con las IPs de los Pods listos. Es útil para StatefulSets o para clientes que eligen el backend ellos mismos, como bases de datos con réplicas.

### [2/Networking/1]
What is the fully qualified DNS name of a Service named `api` in the namespace `shop`, in a cluster with the default domain?
- [ ] `api.shop.cluster.local`
- [x] `api.shop.svc.cluster.local`
- [ ] `shop.api.svc.cluster.local`
- [ ] `api.svc.shop.local`
> El formato es `<servicio>.<namespace>.svc.<dominio-del-clúster>`, y el dominio por defecto es `cluster.local`. Desde el mismo namespace basta con `api`; desde otro, `api.shop` funciona gracias a los dominios de búsqueda del `resolv.conf` del Pod.

### [2/Networking/1]
Which component provides DNS-based service discovery in most Kubernetes clusters?
- [ ] etcd
- [ ] kube-proxy
- [x] CoreDNS
- [ ] Envoy
> **CoreDNS** (graduado en la CNCF) es el DNS del clúster por defecto. Observa Services y EndpointSlices a través del API server y responde consultas como `mi-svc.mi-ns.svc.cluster.local`.

### [2/Networking/2]
What does a Service of type `ExternalName` do?
- [ ] It asks the cloud provider for an external load balancer
- [x] It returns a CNAME record for an external hostname, without proxying
- [ ] It exposes the Service on a high port of every node's IP address
- [ ] It assigns a static public IP address from the cloud provider
> `ExternalName` asocia el Service a un nombre DNS externo (p. ej. `db.example.com`) mediante un registro CNAME. No hay ClusterIP, ni proxy, ni selector. Sirve para referirse a servicios externos con un nombre interno estable.

### [2/Networking/2]
What is required for Ingress resources to have any effect?
- [ ] A Service of type LoadBalancer in every namespace
- [x] An Ingress controller running in the cluster
- [ ] The Gateway API CRDs installed in the cluster
- [ ] A service mesh with sidecars in every Pod
> Un objeto Ingress solo describe reglas HTTP/HTTPS (hosts, rutas, TLS). Necesita un **Ingress controller** (Traefik, HAProxy, Contour, el del proveedor de nube…) que las implemente; sin él, el Ingress no hace nada.

### [2/Networking/2]
Which statement about the Gateway API is correct?
- [ ] It is a proprietary routing API maintained by a single cloud provider
- [x] It is an official, role-oriented API with GatewayClass, Gateway and HTTPRoute
- [ ] It replaces Services and now handles all Pod-to-Pod traffic in the cluster
- [ ] It works only at layer 4 and therefore cannot route HTTP requests
> Gateway API es un proyecto oficial de Kubernetes (SIG Network) y la evolución de Ingress. Separa roles: el proveedor de infraestructura define la GatewayClass, el operador del clúster el Gateway y los desarrolladores las rutas (HTTPRoute, GRPCRoute…). No reemplaza a los Services: las rutas apuntan a Services.

### [2/Networking/2]
Which of the following is a kube-proxy mode on Linux nodes?
- [ ] VXLAN
- [ ] BGP
- [x] nftables
- [ ] WireGuard
> kube-proxy implementa los Services programando reglas del kernel. En Linux soporta `iptables` (el modo clásico por defecto), `nftables` (estable desde 1.33) e `ipvs` (obsoleto desde 1.35). VXLAN y BGP son técnicas que usan los plugins CNI para la red entre nodos, y WireGuard se usa para cifrar ese tráfico.

### [2/Networking/2]
Without any NetworkPolicy in place, which traffic between Pods is allowed?
- [x] All Pod-to-Pod traffic, across all namespaces
- [ ] Only traffic between Pods in the same namespace
- [ ] No traffic at all; everything is denied by default
- [ ] Only traffic that passes through a Service IP
> Kubernetes es "allow-all" por defecto: cualquier Pod puede hablar con cualquier otro. En cuanto una NetworkPolicy selecciona un Pod (para ingress o egress), ese Pod pasa a denegar todo lo que no esté permitido explícitamente en esa dirección.

### [2/Networking/2]
You created NetworkPolicy objects, but traffic is not restricted at all. What is the most likely reason?
- [ ] NetworkPolicies only take effect in the `default` namespace
- [x] The cluster's CNI plugin does not enforce NetworkPolicies
- [ ] kube-proxy must be restarted after policies are created
- [ ] NetworkPolicies only work when a service mesh is installed
> El API server acepta NetworkPolicies, pero quien las aplica es el **plugin CNI**. Calico, Cilium o Antrea las soportan; Flannel por sí solo no. Si el CNI no las implementa, no tienen ningún efecto.

### [2/Networking/3]
What is the effect of this NetworkPolicy?
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np
  namespace: prod
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```
- [ ] It allows all ingress traffic to every Pod in `prod`
- [x] It denies all ingress traffic to every Pod in `prod`
- [ ] It denies all egress traffic from every Pod in `prod`
- [ ] It has no effect, because it does not contain rules
> `podSelector: {}` selecciona todos los Pods del namespace, y `policyTypes: [Ingress]` sin reglas `ingress` significa que no se permite ninguna entrada: es la política clásica *default deny ingress*. El egress no se ve afectado porque no aparece en `policyTypes`.

### [2/Networking/2]
How do Pods usually find the IP address of a Service?
- [ ] By reading `/etc/hosts`, which the scheduler keeps updated
- [x] By resolving the Service name through the cluster DNS
- [ ] By querying etcd directly with their ServiceAccount token
- [ ] By scanning every address in the Pod CIDR range
> El kubelet configura el `/etc/resolv.conf` de cada Pod para usar el DNS del clúster (CoreDNS), con dominios de búsqueda como `<ns>.svc.cluster.local`. También existen variables de entorno `<SVC>_SERVICE_HOST` para los Services que ya existían al crear el Pod, pero el mecanismo principal es el DNS.

### [2/Networking/2]
What is a service mesh primarily used for?
- [ ] Caching container images on nodes to speed up Pod startup
- [x] Managing service-to-service traffic: mTLS, retries, traffic splitting
- [ ] Replacing the CNI plugin so that it can assign IP addresses to Pods
- [ ] Scheduling Pods across several clusters based on their cost
> Un service mesh (Istio, Linkerd…) gestiona la comunicación entre servicios sin cambiar el código: cifrado e identidad con mTLS, reintentos, timeouts, *circuit breaking*, división de tráfico para canaries y métricas o trazas uniformes. No asigna IPs ni programa Pods.

### [2/Networking/2]
In a sidecar-based service mesh such as Istio, what forms the data plane?
- [x] The proxies, such as Envoy, that run next to each workload
- [ ] The control plane component that issues mesh certificates
- [ ] The etcd cluster that stores the mesh routing configuration
- [ ] The CNI plugin that assigns IP addresses to the proxies
> El **data plane** son los proxies (Envoy en Istio, linkerd2-proxy en Linkerd) que interceptan y gestionan el tráfico real. El **control plane** (istiod en Istio) les distribuye la configuración y emite los certificados para mTLS. En el modo *ambient* de Istio, el data plane lo forman ztunnel (L4) y los waypoint proxies (L7) en lugar de sidecars.

### [2/Networking/2]
Which proxy is used as the data plane by Istio and by many other CNCF projects?
- [ ] NGINX
- [ ] HAProxy
- [x] Envoy
- [ ] CoreDNS
> **Envoy** (graduado en la CNCF, creado en Lyft) es el proxy L7 que usan Istio, Contour, Emissary-ingress y muchas implementaciones de Gateway API. Linkerd, en cambio, usa su propio micro-proxy escrito en Rust (linkerd2-proxy).

### [2/Networking/2]
On a bare-metal cluster, a Service of type `LoadBalancer` stays with `EXTERNAL-IP <pending>` forever. Why?
- [ ] LoadBalancer Services require at least three nodes to work
- [x] No controller provisions load balancers there; MetalLB can fill the gap
- [ ] kube-proxy must run in IPVS mode for LoadBalancer Services
- [ ] The Service also needs an Ingress resource that points to it
> En la nube, el cloud-controller-manager crea el balanceador. En bare metal no hay nadie que lo haga, así que la IP externa queda `<pending>`. MetalLB (u opciones como kube-vip o el soporte BGP de Cilium/Calico) asigna IPs y las anuncia en la red.

### [2/Networking/3]
Backend Pods must see the original client IP address for traffic that arrives through a NodePort or LoadBalancer Service. Which setting helps?
- [ ] `sessionAffinity: ClientIP`
- [x] `externalTrafficPolicy: Local`
- [ ] `internalTrafficPolicy: Cluster`
- [ ] `publishNotReadyAddresses: true`
> Con `externalTrafficPolicy: Cluster` (por defecto) el tráfico puede saltar a otro nodo y se aplica SNAT, perdiendo la IP de origen. Con `Local` solo se envía a Pods del nodo que recibió el tráfico y se conserva la IP del cliente, a cambio de un reparto menos uniforme. `sessionAffinity` solo fija el backend por cliente.

### [2/Networking/2]
What does `sessionAffinity: ClientIP` on a Service do?
- [ ] It preserves the client's source IP for the backend
- [x] It sends a given client's requests to the same Pod
- [ ] It restricts access to an allow-list of client IPs
- [ ] It encrypts traffic using the client's certificate
> La afinidad de sesión por IP de cliente hace que las conexiones de un mismo cliente vayan al mismo Pod (durante un tiempo configurable). No restringe el acceso (eso sería una NetworkPolicy o un firewall) ni conserva la IP de origen.

### [2/Networking/2]
Which technology lets CNI plugins such as Cilium implement networking, load balancing and security directly in the Linux kernel, without iptables?
- [ ] WebAssembly
- [x] eBPF
- [ ] SELinux
- [ ] cgroups v2
> **eBPF** permite ejecutar programas seguros dentro del kernel. Cilium lo usa para enrutar, balancear Services (pudiendo reemplazar a kube-proxy), aplicar políticas de red incluso en L7 y ofrecer observabilidad (Hubble) con muy bajo costo.

### [2/Networking/2]
A Pod in namespace `web` calls `http://api` and gets a DNS error, while `http://api.backend` works. Why?
- [ ] CoreDNS is down, so only names that include a namespace still resolve
- [x] The Service is in `backend`; short names resolve only in the Pod's namespace
- [ ] Service names must always be written as fully qualified domain names in Kubernetes
- [ ] A NetworkPolicy blocks DNS lookups for names without a namespace
> El `resolv.conf` del Pod busca primero en `<su-namespace>.svc.cluster.local`, así que `api` se intenta como `api.web.svc.cluster.local`, que no existe. Con `api.backend` (o el FQDN) sí se encuentra. Si CoreDNS estuviera caído, tampoco funcionaría `api.backend`.

### [2/Networking/2]
Which Kubernetes feature lets a cluster give Pods and Services both IPv4 and IPv6 addresses?
- [ ] IPVS proxy mode
- [x] Dual-stack networking
- [ ] Topology-aware routing
- [ ] Multus CNI
> Kubernetes soporta *dual-stack* (estable desde 1.23): Pods y Services pueden tener direcciones IPv4 e IPv6, siempre que el CNI y la infraestructura lo admitan. Multus permite varias interfaces de red por Pod, que es otra cosa.

### [2/Networking/2]
Which Kubernetes object stores the IP addresses and ports of the Pods currently backing a Service?
- [ ] ConfigMap
- [x] EndpointSlice
- [ ] Ingress
- [ ] NetworkPolicy
> El controlador de EndpointSlices observa los Pods que coinciden con el selector del Service y guarda sus IPs, puertos y condiciones (`ready`, `serving`, `terminating`) en objetos EndpointSlice, el reemplazo escalable de Endpoints. kube-proxy y los service mesh leen esos objetos y solo envían tráfico a los endpoints listos.

### [2/Networking/2]
Which TWO Service types make an application reachable from outside the cluster? (Choose two.)
- [x] NodePort
- [x] LoadBalancer
- [ ] ClusterIP
- [ ] A headless Service
- [ ] ExternalName
> **NodePort** abre un puerto en cada nodo y **LoadBalancer** (que se apoya en NodePort) pide un balanceador externo. ClusterIP y los headless solo son accesibles dentro del clúster, y ExternalName es un alias DNS hacia fuera, no una forma de exponer Pods. Para HTTP también se usan Ingress o Gateway API.

### [2/Security/1]
What are the 4Cs of cloud native security, from the outermost layer to the innermost?
- [ ] Code, Container, Cluster, Cloud
- [x] Cloud, Cluster, Container, Code
- [ ] Cluster, Cloud, Code, Container
- [ ] Compute, Cloud, Container, Code
> El modelo de las 4C organiza la seguridad en capas: **Cloud** (o datacenter), **Cluster**, **Container** y **Code**. Cada capa interna depende de la seguridad de la externa: no puedes proteger bien el código si el clúster o la nube están comprometidos.

### [2/Security/2]
Which authorization mode is enabled in most clusters to grant permissions through Roles and RoleBindings?
- [ ] ABAC
- [x] RBAC
- [ ] AlwaysAllow
- [ ] Webhook
> **RBAC** (Role-Based Access Control) es el modo estándar: los permisos se definen en Roles/ClusterRoles y se asignan a usuarios, grupos o ServiceAccounts mediante RoleBindings/ClusterRoleBindings. Suele combinarse con el autorizador `Node` (`--authorization-mode=Node,RBAC`). `AlwaysAllow` nunca debe usarse en producción.

### [2/Security/2]
What is the difference between a Role and a ClusterRole?
- [ ] A Role binds only to users, while a ClusterRole binds only to ServiceAccounts
- [x] A Role is limited to one namespace; a ClusterRole is cluster-wide
- [ ] A ClusterRole can only grant read verbs, while a Role can also write
- [ ] They are identical; ClusterRole is simply the newer name for Role
> Un Role vive en un namespace y solo da permisos dentro de él. Un ClusterRole no tiene namespace: puede cubrir recursos de clúster (Nodes, PersistentVolumes), endpoints no-recurso (`/healthz`) o recursos de todos los namespaces mediante un ClusterRoleBinding. Ambos pueden asignarse a usuarios, grupos o ServiceAccounts.

### [2/Security/3]
A RoleBinding in namespace `dev` references the ClusterRole `view`. What access does the subject get?
- [ ] Read access to every namespace in the cluster
- [x] Read access only within the `dev` namespace
- [ ] No access, since RoleBindings cannot use ClusterRoles
- [ ] Full administrative access inside `dev`
> Un RoleBinding puede referenciar un ClusterRole: los permisos se aplican **solo en el namespace del RoleBinding**. Es la forma habitual de reutilizar roles comunes (`view`, `edit`, `admin`) por namespace. Para darlos en todo el clúster haría falta un ClusterRoleBinding.

### [2/Security/1]
Which identity do processes inside a Pod use when they call the Kubernetes API?
- [ ] The identity of the node's kubelet
- [x] The Pod's ServiceAccount
- [ ] The user who created the Pod
- [ ] An anonymous, unauthenticated identity
> Cada Pod corre con un ServiceAccount (si no se indica, el `default` de su namespace). Kubernetes le monta un token de corta duración, proyectado y rotado automáticamente, que lo identifica ante el API server; RBAC decide qué puede hacer.

### [2/Security/2]
How are human users represented in Kubernetes?
- [ ] As `User` objects stored in etcd and managed with `kubectl create user`
- [x] There is no User object; identity comes from certs, OIDC tokens, etc.
- [ ] As ServiceAccounts created in the `kube-system` namespace
- [ ] As entries in a cluster-wide ConfigMap called `users`
> Kubernetes no gestiona usuarios humanos: no existe un objeto `User`. La identidad la aporta el mecanismo de autenticación (certificados X.509 firmados por la CA del clúster, tokens OIDC de un proveedor de identidad, webhooks…). RBAC referencia luego esos nombres de usuario y grupos. Los ServiceAccounts sí son objetos, pero son para cargas de trabajo.

### [2/Security/2]
Which `securityContext` setting prevents a container from running as the root user?
- [ ] `privileged: false`
- [x] `runAsNonRoot: true`
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: true`
> `runAsNonRoot: true` hace que el kubelet se niegue a arrancar el contenedor si fuera a ejecutarse con UID 0. `readOnlyRootFilesystem` impide escribir en el sistema de archivos del contenedor y `allowPrivilegeEscalation: false` evita ganar privilegios (por ejemplo con binarios setuid); son complementarios.

### [2/Security/2]
What are the three Pod Security Standards profiles?
- [ ] Low, Medium and High
- [x] Privileged, Baseline and Restricted
- [ ] Open, Default and Locked
- [ ] Permissive, Enforced and Audited
> Los Pod Security Standards definen tres niveles: **Privileged** (sin restricciones), **Baseline** (evita escaladas de privilegio conocidas) y **Restricted** (buenas prácticas de endurecimiento). El controlador Pod Security Admission los aplica por namespace con los modos `enforce`, `audit` y `warn`.

### [2/Security/2]
How do you enforce the `restricted` Pod Security Standard in the namespace `payments` with the built-in admission controller?
- [ ] Create a PodSecurityPolicy named `restricted`
- [x] Label the namespace `pod-security.kubernetes.io/enforce=restricted`
- [ ] Annotate every Pod with `security.kubernetes.io/profile: restricted`
- [ ] Start every kubelet with `--pod-security=restricted`
> Pod Security Admission funciona con **labels en el namespace**: `pod-security.kubernetes.io/<modo>=<nivel>`, donde el modo es `enforce`, `audit` o `warn`. PodSecurityPolicy se eliminó en Kubernetes 1.25.

### [2/Security/1]
Which resource controls which Pods may communicate with each other at the network level?
- [ ] Role
- [x] NetworkPolicy
- [ ] PodSecurityAdmission
- [ ] ServiceAccount
> Las **NetworkPolicies** definen qué tráfico de entrada y salida se permite a los Pods seleccionados (por labels de Pod, de namespace o bloques IP). Son la base de la microsegmentación, siempre que el CNI las aplique.

### [2/Security/2]
Which statement best describes the principle of least privilege in Kubernetes?
- [ ] Give every developer cluster-admin so that nobody is ever blocked
- [x] Grant each user and workload only the permissions it actually needs
- [ ] Run all workloads in the `default` namespace to simplify RBAC
- [ ] Disable RBAC and rely on network firewalls around the cluster
> Mínimo privilegio significa dar a cada identidad (persona o ServiceAccount) solo lo necesario: Roles con verbos y recursos concretos, por namespace, evitando comodines (`*`) y `cluster-admin`. Así se reduce el impacto si unas credenciales se filtran.

### [2/Security/2]
Which CNCF project is a runtime security tool that detects unexpected behavior, such as a shell spawned inside a container, by monitoring system calls?
- [ ] OPA Gatekeeper
- [x] Falco
- [ ] Harbor
- [ ] cert-manager
> **Falco** (graduado en la CNCF) observa llamadas al sistema (vía eBPF o un módulo del kernel) y eventos de Kubernetes, y genera alertas según reglas como "shell en un contenedor" o "escritura en /etc". OPA Gatekeeper es política de admisión, Harbor es un registro y cert-manager gestiona certificados.

### [2/Security/2]
Which tools are policy engines commonly used as admission controllers to enforce rules such as "images must come from our registry"?
- [ ] Prometheus and Grafana
- [x] OPA Gatekeeper and Kyverno
- [ ] Helm and Kustomize
- [ ] Fluentd and Fluent Bit
> OPA Gatekeeper (políticas en Rego) y Kyverno (políticas en YAML) se instalan como webhooks de admisión y pueden validar, mutar o generar recursos. Kubernetes también incluye ValidatingAdmissionPolicy, con expresiones CEL y sin webhooks externos.

### [2/Security/2]
Which statement about Kubernetes Secrets is true?
- [ ] Base64 encoding makes Secrets safe to store in public Git repositories
- [x] Anyone who can create Pods in a namespace can read its Secrets
- [ ] Secrets are encrypted by default using the cluster CA certificate
- [ ] Secrets can be mounted as volumes but never used as env variables
> Quien puede crear un Pod en un namespace puede montar cualquier Secret de ese namespace (o usarlo como variable de entorno) y leer su valor; por eso el permiso de crear Pods es sensible. Base64 no es cifrado, el cifrado en reposo hay que configurarlo y los Secrets sí pueden exponerse como variables de entorno.

### [2/Security/2]
Which statement about ServiceAccount tokens in current Kubernetes versions is correct?
- [ ] Each ServiceAccount automatically gets a non-expiring token stored in a Secret
- [x] Pods get short-lived, audience-bound tokens that are rotated automatically
- [ ] ServiceAccount tokens are disabled by default and must be requested per Pod
- [ ] Tokens are only issued to Pods that run in the `kube-system` namespace
> Gracias a la API TokenRequest, los Pods reciben tokens con caducidad y audiencia, montados en un volumen proyectado que el kubelet renueva. Desde 1.24 ya no se crean automáticamente Secrets con tokens sin caducidad. Los tokens se montan por defecto en cualquier namespace; si un Pod no necesita la API, se puede usar `automountServiceAccountToken: false`.

### [2/Security/2]
A Pod does not need to talk to the Kubernetes API. What is a good hardening step?
- [x] Set `automountServiceAccountToken: false`
- [ ] Bind it to `cluster-admin` so it never sees errors
- [ ] Run it with `hostNetwork: true`
- [ ] Delete the `default` ServiceAccount of the namespace
> Si la aplicación no usa la API, no hay razón para montar un token: `automountServiceAccountToken: false` (en el Pod o en el ServiceAccount) elimina esa credencial del sistema de archivos del contenedor y reduce el riesgo si el contenedor es comprometido.

### [2/Security/2]
What does mutual TLS (mTLS) provide in a service mesh?
- [ ] Load balancing based on the CPU usage of each backend
- [x] Encryption in transit and authentication of both workloads
- [ ] Automatic vulnerability scanning of container images
- [ ] Compression of HTTP payloads between microservices
> Con mTLS ambos extremos presentan certificados: el tráfico va cifrado y cada servicio verifica la identidad del otro (por ejemplo, identidades SPIFFE). Istio o Linkerd lo automatizan y rotan los certificados sin cambiar el código.

### [2/Security/2]
What happened to PodSecurityPolicy (PSP)?
- [ ] It became generally available (GA) in Kubernetes 1.25
- [x] It was removed in Kubernetes 1.25 in favor of Pod Security Admission
- [ ] It was renamed to NetworkPolicy and moved to a new API group
- [ ] It is still the recommended way to restrict privileged Pods
> PodSecurityPolicy se declaró obsoleto en 1.21 y se eliminó en 1.25. Su reemplazo integrado es **Pod Security Admission**, que aplica los Pod Security Standards por namespace. Para reglas más finas se usan Kyverno, OPA Gatekeeper o ValidatingAdmissionPolicy.

### [2/Security/2]
Which RBAC verbs allow a subject to read objects? (Choose two.)
- [x] `get`
- [x] `list`
- [ ] `patch`
- [ ] `escalate`
- [ ] `bind`
> `get` lee un objeto concreto y `list` obtiene colecciones, incluido su contenido; `watch` permite recibir cambios. `patch` modifica. `escalate` y `bind` son verbos especiales de RBAC que permiten crear o asignar roles con más permisos que los propios, y son peligrosos.

### [2/Security/2]
Which settings in a container's `securityContext` reduce its privileges? (Choose two.)
- [x] `allowPrivilegeEscalation: false`
- [x] `capabilities: {drop: ["ALL"]}`
- [ ] `privileged: true`
- [ ] `runAsUser: 0`
- [ ] `procMount: Unmasked`
> Desactivar la escalada de privilegios y eliminar todas las *capabilities* de Linux reduce lo que un proceso comprometido puede hacer. `privileged: true` y `runAsUser: 0` hacen lo contrario, y `procMount: Unmasked` quita las máscaras de seguridad de `/proc`.
