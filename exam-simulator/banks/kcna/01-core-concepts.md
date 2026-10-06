# KCNA · Dominio 1 · Kubernetes Fundamentals · Core Concepts

### [1/Core Concepts/1]
Which control plane component is the only one that communicates directly with etcd?
- [ ] kube-scheduler
- [x] kube-apiserver
- [ ] kube-controller-manager
- [ ] kubelet
> El **kube-apiserver** es la única puerta de entrada al estado del clúster: es el único componente que lee y escribe en etcd. El scheduler, el controller-manager y los kubelets hablan con el API server (REST y *watch*), nunca directamente con etcd. Así se centralizan autenticación, autorización, admisión y validación.

### [1/Core Concepts/1]
What is the primary role of etcd in a Kubernetes cluster?
- [ ] Schedule Pods onto healthy nodes based on available resources
- [x] Persist all cluster state in a consistent key-value store
- [ ] Provide DNS-based service discovery for Pods and Services
- [ ] Collect and aggregate container metrics for the autoscalers
> etcd es un almacén clave-valor distribuido y fuertemente consistente (usa el algoritmo de consenso Raft) donde vive todo el estado del clúster: objetos, configuración, Secrets, etc. El scheduling lo hace kube-scheduler, el DNS lo da CoreDNS y las métricas las recogen metrics-server o Prometheus.

### [1/Core Concepts/2]
A new Pod has been created but has no `nodeName` yet. Which component is responsible for choosing a node for it?
- [ ] kubelet
- [ ] kube-controller-manager
- [x] kube-scheduler
- [ ] kube-proxy
> El kube-scheduler observa Pods sin `nodeName`, filtra los nodos que cumplen los requisitos (recursos, taints, afinidad…), los puntúa y crea un *binding* al mejor. Ojo: el scheduler **no** arranca contenedores; eso lo hace el kubelet del nodo elegido cuando ve el Pod asignado.

### [1/Core Concepts/2]
Which component runs on every node and ensures that the containers described in PodSpecs are running and healthy?
- [x] kubelet
- [ ] kube-proxy
- [ ] containerd-shim
- [ ] cloud-controller-manager
> El **kubelet** es el agente de cada nodo: recibe los PodSpecs (del API server o de manifiestos estáticos), le pide al runtime vía CRI que cree los contenedores, ejecuta las probes y reporta el estado. kube-proxy gestiona reglas de red para Services, el shim es un detalle interno de containerd y el cloud-controller-manager corre en el control plane.

### [1/Core Concepts/2]
What is the main responsibility of kube-proxy?
- [ ] Proxy kubectl requests from users to the API server
- [ ] Encrypt the traffic between Pods that run on different nodes
- [x] Maintain node network rules that implement Service virtual IPs
- [ ] Assign IP addresses to new Pods from each node's Pod CIDR range
> kube-proxy corre en cada nodo y programa reglas de red (iptables por defecto, o nftables; el modo IPVS está obsoleto desde v1.35) para que el tráfico hacia la IP virtual de un Service llegue a alguno de sus Pods.
>
> No hace de proxy para `kubectl` (eso es `kubectl proxy`), no cifra tráfico (eso lo hace un service mesh o el CNI) ni asigna IPs a los Pods (eso es del plugin CNI/IPAM).

### [1/Core Concepts/2]
Which control plane component runs controllers such as the Node, ReplicaSet, EndpointSlice and ServiceAccount controllers?
- [ ] kube-apiserver
- [x] kube-controller-manager
- [ ] kube-scheduler
- [ ] cloud-controller-manager
> El **kube-controller-manager** es un único binario que ejecuta muchos controladores (Node, ReplicaSet, Deployment, Job, EndpointSlice, ServiceAccount, Namespace…). Cada uno es un bucle de reconciliación. El cloud-controller-manager solo contiene los controladores que dependen del proveedor de nube.

### [1/Core Concepts/2]
In a cluster running on a public cloud, which component creates an external load balancer when a Service of type `LoadBalancer` is created?
- [ ] kube-proxy
- [ ] The Ingress controller
- [x] cloud-controller-manager
- [ ] kube-scheduler
> El **cloud-controller-manager** integra Kubernetes con la API del proveedor: su *service controller* crea y actualiza balanceadores externos para Services `LoadBalancer`, y también gestiona rutas y el ciclo de vida de nodos en la nube. En bare metal no existe ese controlador; por eso se usan soluciones como MetalLB.

### [1/Core Concepts/1]
What is the smallest deployable unit of computing that you can create and manage in Kubernetes?
- [ ] Container
- [x] Pod
- [ ] Deployment
- [ ] Node
> El **Pod** es la unidad mínima desplegable: agrupa uno o más contenedores que comparten red (misma IP, se comunican por `localhost`) y pueden compartir volúmenes. Kubernetes no gestiona contenedores sueltos; Deployments, StatefulSets, etc. son controladores que crean Pods.

### [1/Core Concepts/2]
Two containers in the same Pod need to communicate over the network. How can container A reach container B listening on port 8080?
- [x] `localhost:8080`
- [ ] Container B's name, resolved by cluster DNS, on port 8080
- [ ] Container B's own IP address on port 8080
- [ ] `127.0.0.2:8080`, because each container has its own loopback
> Todos los contenedores de un Pod comparten el mismo *network namespace*: misma IP y mismo espacio de puertos, así que se comunican por `localhost`.
>
> No existe una IP ni un loopback distinto por contenedor, y el DNS del clúster no crea registros con nombres de contenedores: solo crea registros para Services y Pods.

### [1/Core Concepts/2]
What is the purpose of init containers in a Pod?
- [ ] They run alongside the app containers for the entire lifetime of the Pod
- [x] They run to completion, one at a time, before the app containers start
- [ ] They restart the app containers when liveness probes fail
- [ ] They prepare the node's network and storage before the kubelet starts
> Los init containers se ejecutan en orden, uno tras otro, y cada uno debe terminar con éxito antes de que arranque el siguiente; solo después arrancan los contenedores de la aplicación. Sirven para preparar configuración, esperar dependencias o ejecutar migraciones.
>
> Seguir corriendo junto a la app toda la vida del Pod es lo que hace un *sidecar* (un init container con `restartPolicy: Always`), no un init container normal. Reiniciar contenedores cuando falla la liveness probe lo hace el kubelet, y los init containers viven dentro del Pod: no preparan el nodo.

### [1/Core Concepts/3]
How do you declare a native sidecar container that starts before the main containers and keeps running for the whole life of the Pod?
- [ ] Add it under `spec.containers` with `sidecar: true`
- [x] Add it under `spec.initContainers` with `restartPolicy: Always`
- [ ] Add it under `spec.ephemeralContainers`
- [ ] Add the annotation `kubernetes.io/sidecar: "true"` to the Pod
> Los **sidecars nativos** (estables desde Kubernetes 1.33) se declaran como init containers con `restartPolicy: Always`: arrancan antes que la app, siguen corriendo en paralelo y se detienen después de ella. No existe un campo `sidecar: true` ni esa anotación, y los ephemeral containers son solo para depuración.

### [1/Core Concepts/1]
Which workload resource is the best fit for a stateless web application that needs rolling updates and rollbacks?
- [x] Deployment
- [ ] StatefulSet
- [ ] DaemonSet
- [ ] Job
> El **Deployment** gestiona ReplicaSets y permite actualizaciones progresivas (*rolling updates*), pausar y revertir (`kubectl rollout undo`). StatefulSet es para apps con identidad o almacenamiento estable, DaemonSet pone un Pod por nodo y Job ejecuta tareas que terminan.

### [1/Core Concepts/2]
What is the relationship between a Deployment and a ReplicaSet?
- [ ] A ReplicaSet manages one or more Deployments and their rollouts
- [x] A Deployment manages ReplicaSets, one per Pod template revision
- [ ] They are two aliases for exactly the same API object
- [ ] A Deployment replaces ReplicaSets, which were removed from the API
> El Deployment no crea Pods directamente: crea y escala ReplicaSets. Cada cambio en el *Pod template* (imagen, variables, etc.) genera un ReplicaSet nuevo; durante el rolling update se escala el nuevo hacia arriba y el viejo hacia abajo. Los ReplicaSets anteriores (según `revisionHistoryLimit`) permiten el rollback.

### [1/Core Concepts/2]
Which workload resource gives each replica a stable network identity (for example `db-0`, `db-1`) and its own persistent volume?
- [ ] Deployment
- [x] StatefulSet
- [ ] ReplicaSet
- [ ] DaemonSet
> El **StatefulSet** asigna nombres ordinales estables (`nombre-0`, `nombre-1`…), crea y elimina Pods en orden y, con `volumeClaimTemplates`, da a cada réplica su propio PVC, que la sigue aunque el Pod se reprograme. Es típico de bases de datos y sistemas con quórum.

### [1/Core Concepts/2]
A StatefulSet needs to provide stable DNS names for each of its Pods. Which kind of Service must it reference in `spec.serviceName`?
- [ ] A NodePort Service with a fixed `nodePort`
- [ ] A LoadBalancer Service with one IP per Pod
- [x] A headless Service (`clusterIP: None`)
- [ ] An ExternalName Service
> El StatefulSet usa un Service *headless* (`clusterIP: None`) para crear registros DNS por Pod, como `db-0.db.mi-ns.svc.cluster.local`. Al no tener IP virtual, el DNS devuelve directamente las IPs de los Pods, que es lo que necesitan los clientes que deben hablar con una réplica concreta.

### [1/Core Concepts/1]
You need exactly one log-collector Pod running on every node, including nodes added later. Which resource should you use?
- [ ] A Deployment with replicas equal to the node count
- [x] DaemonSet
- [ ] StatefulSet
- [ ] CronJob
> Un **DaemonSet** garantiza una copia del Pod en cada nodo elegible y la crea automáticamente cuando se añaden nodos (y la elimina al quitarlos). Es el patrón para agentes de logs, monitoreo (node-exporter) o agentes de red. Un Deployment con N réplicas no garantiza una por nodo.

### [1/Core Concepts/1]
Which resource should you use to run a database backup every night at 02:00?
- [ ] Job
- [x] CronJob
- [ ] DaemonSet
- [ ] A Deployment with a sleep loop
> El **CronJob** crea Jobs según un horario en formato cron (por ejemplo `0 2 * * *`), y cada Job ejecuta Pods hasta completar la tarea. Un Job se ejecuta una sola vez, y usar un Deployment con `sleep` es un antipatrón.

### [1/Core Concepts/2]
What is the main difference between labels and annotations?
- [x] Labels are for selecting objects; annotations hold other metadata
- [ ] Labels can only be set on Pods; annotations work on every object
- [ ] Annotations can be used in label selectors, but labels cannot
- [ ] Labels are stored in etcd, while annotations live only in memory
> Las **labels** son pares clave/valor para identificar y agrupar objetos: los selectores de Services, Deployments o `kubectl -l` las usan. Las **annotations** guardan metadatos que no sirven para seleccionar (información de build, configuración de herramientas, URLs…). Ambas existen en cualquier objeto y se guardan en etcd.

### [1/Core Concepts/2]
Which of the following resources is cluster-scoped (not namespaced)?
- [ ] ConfigMap
- [ ] PersistentVolumeClaim
- [x] PersistentVolume
- [ ] ServiceAccount
> PersistentVolume, Node, Namespace, StorageClass, ClusterRole y CustomResourceDefinition son de ámbito de clúster. ConfigMap, PVC, ServiceAccount, Pod, Service y Role pertenecen a un namespace. Puedes comprobarlo con `kubectl api-resources --namespaced=false`.

### [1/Core Concepts/2]
What is stored in the `kube-node-lease` namespace?
- [ ] Certificates used for kubelet TLS bootstrapping
- [x] One Lease per node, used as a kubelet heartbeat
- [ ] DaemonSet Pods that must run on every node
- [ ] The Lease used for kube-scheduler leader election
> Cada nodo tiene un objeto Lease en `kube-node-lease`, y su kubelet lo renueva cada pocos segundos. Es un *heartbeat* liviano: el control plane lo usa para detectar si un nodo dejó de responder, sin tener que actualizar todo el objeto Node en cada latido.
>
> Ojo: no todos los Leases viven ahí. Por defecto, los Leases de elección de líder del kube-scheduler y del kube-controller-manager están en `kube-system`. Los Pods de un DaemonSet van en el namespace del propio DaemonSet.

### [1/Core Concepts/1]
Which namespace contains control plane and system add-on components such as CoreDNS in most clusters?
- [ ] default
- [ ] kube-public
- [x] kube-system
- [ ] kube-node-lease
> `kube-system` aloja los componentes del sistema (CoreDNS, kube-proxy, el CNI y, en kubeadm, los Pods estáticos del control plane). `default` es para objetos sin namespace explícito, `kube-public` es legible por todos (incluso sin autenticar) y `kube-node-lease` guarda los Leases de los nodos.

### [1/Core Concepts/1]
A container needs a non-sensitive configuration file. Which object is designed for this?
- [x] ConfigMap
- [ ] Secret
- [ ] PersistentVolumeClaim
- [ ] ServiceAccount
> El **ConfigMap** guarda configuración no sensible y se consume como variables de entorno, argumentos o archivos montados en un volumen. Para datos sensibles (contraseñas, tokens, llaves) se usa un Secret.

### [1/Core Concepts/2]
By default, how are the values of a Kubernetes Secret stored in etcd?
- [ ] Encrypted with AES-256 using a cluster-wide key generated at install
- [x] Unencrypted, unless encryption at rest is configured
- [ ] Hashed with SHA-256 so that nobody can ever read the values back
- [ ] Encrypted by the kubelet before they are sent to the API server
> Por defecto los Secrets se guardan **sin cifrar** en etcd: quien tenga acceso a etcd o a sus backups puede leerlos. El base64 que ves en el campo `data` de un Secret es solo una codificación, no un cifrado.
>
> Para protegerlos hay que habilitar el cifrado en reposo (EncryptionConfiguration, idealmente con KMS), restringir el acceso con RBAC y proteger etcd. Kubernetes no aplica AES ni hashes por defecto, y el kubelet no cifra los Secrets antes de enviarlos.

### [1/Core Concepts/3]
A ConfigMap is consumed by a Pod both as environment variables and as a mounted volume (without `subPath`). You update the ConfigMap. What happens?
- [ ] Both the environment variables and the mounted files update automatically
- [x] Files update after a delay; env vars keep their old values
- [ ] The Pod is restarted automatically so that it picks up the new values
- [ ] Neither changes until the Pod is deleted and created again by its owner
> Las variables de entorno se leen solo al arrancar el contenedor, así que no cambian. Los archivos de un volumen ConfigMap sí se actualizan (con cierto retraso por la sincronización del kubelet), salvo si se montan con `subPath`. Kubernetes no reinicia Pods por cambios en ConfigMaps; para eso se usa, por ejemplo, `kubectl rollout restart`.

### [1/Core Concepts/2]
A Pod's containers all have CPU and memory requests equal to their limits. What QoS class does Kubernetes assign to the Pod?
- [x] Guaranteed
- [ ] Burstable
- [ ] BestEffort
- [ ] Critical
> Si **todos** los contenedores tienen requests y limits de CPU y memoria, y requests = limits, la clase es *Guaranteed*. Si al menos uno define algún request o limit sin cumplir eso, es *Burstable*. Si ninguno define requests ni limits, es *BestEffort*. "Critical" no es una clase QoS (la criticidad se maneja con PriorityClass).

### [1/Core Concepts/2]
A node is under memory pressure and the kubelet must evict Pods. All else being equal, which Pods are evicted first?
- [ ] Guaranteed Pods
- [ ] Burstable Pods that use less than their requests
- [x] BestEffort Pods
- [ ] The Pods that were created most recently
> En la expulsión por presión de recursos, el kubelet prioriza los Pods cuyo uso supera sus requests (teniendo en cuenta la prioridad). Como los BestEffort no tienen requests, son los primeros candidatos, y los Guaranteed los últimos. Por eso definir requests es clave para la estabilidad.

### [1/Core Concepts/2]
What happens when a container's liveness probe keeps failing?
- [ ] The Pod is removed from Service endpoints but keeps running
- [x] The kubelet restarts the container per its restart policy
- [ ] The scheduler moves the Pod to another healthy node
- [ ] The Deployment is rolled back to the previous revision
> La *liveness probe* indica si el contenedor sigue vivo; si falla repetidamente, el kubelet lo mata y lo reinicia según `restartPolicy`. Sacar el Pod de los endpoints es lo que hace la *readiness probe*. Ninguna probe mueve el Pod de nodo ni hace rollback.

### [1/Core Concepts/2]
A Pod is `Running` but does not receive traffic from its Service, and its READY column shows `0/1`. Which probe is most likely failing?
- [x] Readiness probe
- [ ] Liveness probe
- [ ] A startup probe that already succeeded
- [ ] The preStop hook
> Cuando la *readiness probe* falla, el contenedor no se marca Ready y el Pod aparece como no listo en los EndpointSlices del Service, así que deja de recibir tráfico, pero no se reinicia. Si fallara la liveness verías reinicios (RESTARTS creciendo).

### [1/Core Concepts/2]
A legacy application takes up to 3 minutes to start. Which probe should you configure so that the liveness probe does not kill it during startup?
- [ ] A readiness probe with a long `periodSeconds`
- [x] A startup probe
- [ ] A preStop lifecycle hook
- [ ] An init container that sleeps for 3 minutes
> La *startup probe* desactiva las probes de liveness y readiness hasta que tiene éxito, dando margen a apps de arranque lento (`failureThreshold × periodSeconds`). Así no hace falta un `initialDelaySeconds` enorme en la liveness. Un init container con `sleep` solo retrasa el arranque sin comprobar nada.

### [1/Core Concepts/1]
Which of these is NOT a valid Pod phase?
- [ ] Pending
- [ ] Succeeded
- [x] CrashLoopBackOff
- [ ] Unknown
> Las fases de un Pod son Pending, Running, Succeeded, Failed y Unknown. *CrashLoopBackOff* es el **motivo** del estado de espera de un contenedor que se reinicia una y otra vez; `kubectl get pods` lo muestra en STATUS, pero no es una fase.

### [1/Core Concepts/2]
You delete a Deployment with `kubectl delete deployment web`. What happens to its ReplicaSets and Pods by default?
- [ ] They keep running as orphaned objects
- [x] They are deleted too, through cascading deletion
- [ ] Only the Pods are deleted; ReplicaSets are kept for rollback
- [ ] They are deleted only if you add `--cascade=foreground`
> Los ReplicaSets tienen `ownerReferences` que apuntan al Deployment, y los Pods apuntan a su ReplicaSet. Por defecto Kubernetes hace borrado en cascada en *background*: borra el Deployment y el garbage collector elimina después sus ReplicaSets y Pods.
>
> `--cascade=foreground` también borra todo; solo cambia el orden (primero los dependientes y al final el dueño). Para dejarlos corriendo como huérfanos habría que usar `--cascade=orphan`.

### [1/Core Concepts/3]
A namespace has been stuck in `Terminating` for a long time. What is the most likely cause?
- [ ] The namespace still contains a ResourceQuota
- [x] Some resources in it have finalizers that were never removed
- [ ] The kube-scheduler is not running
- [ ] Only the cluster-admin ClusterRole can delete namespaces
> Los *finalizers* impiden borrar un objeto hasta que su controlador termine una limpieza y los quite. Si ese controlador ya no existe o falla (por ejemplo, el operador de un CRD fue desinstalado), los objetos y el namespace que los contiene quedan en Terminating. Hay que buscar qué recursos tienen finalizers pendientes.

### [1/Core Concepts/1]
In the API path `/apis/apps/v1/namespaces/prod/deployments`, what is `apps`?
- [ ] The namespace
- [x] The API group
- [ ] The resource kind
- [ ] The name of the API server
> Las APIs de Kubernetes se organizan en grupos versionados: `/apis/<grupo>/<versión>/...`. Aquí `apps` es el grupo y `v1` la versión. El grupo *core* (Pods, Services, ConfigMaps…) es la excepción: vive en `/api/v1` y en los manifiestos se escribe solo `apiVersion: v1`.

### [1/Core Concepts/1]
Which `apiVersion` should you use in a Deployment manifest?
- [ ] `v1`
- [x] `apps/v1`
- [ ] `extensions/v1beta1`
- [ ] `deployments/v1`
> Deployment, ReplicaSet, StatefulSet y DaemonSet pertenecen al grupo `apps`, versión estable `v1`. `extensions/v1beta1` se eliminó hace años. Pods, Services y ConfigMaps usan `v1` (grupo core).

### [1/Core Concepts/1]
Which four top-level fields appear in almost every Kubernetes object manifest?
- [x] `apiVersion`, `kind`, `metadata`, `spec`
- [ ] `name`, `image`, `ports`, `replicas`
- [ ] `version`, `type`, `labels`, `status`
- [ ] `apiGroup`, `object`, `namespace`, `template`
> Un manifiesto típico tiene `apiVersion` (grupo/versión), `kind` (tipo), `metadata` (nombre, namespace, labels…) y `spec` (estado deseado). El campo `status` lo escribe el sistema, no el usuario. Algunos objetos, como ConfigMap, usan `data` en lugar de `spec`.

### [1/Core Concepts/2]
What is the difference between `spec` and `status` in a Kubernetes object?
- [ ] `spec` is written by controllers; `status` is written by the user
- [x] `spec` is the desired state; `status` is the observed state
- [ ] `status` is stored in etcd; `spec` exists only on the client
- [ ] They are synonyms kept for backward compatibility
> El usuario declara en `spec` lo que quiere; los controladores trabajan para llevar la realidad a ese estado y reportan lo observado en `status` (réplicas listas, condiciones, IP del Pod…). Este modelo declarativo con bucles de reconciliación es la base de Kubernetes.

### [1/Core Concepts/2]
What is the core idea behind Kubernetes controllers?
- [ ] They execute imperative scripts exactly once when an object is created
- [x] They continuously reconcile the current state toward the desired state
- [ ] They replace etcd as the source of truth whenever etcd is unavailable
- [ ] They schedule new Pods onto nodes based on CPU and memory requests
> Un controlador observa objetos en el API server, compara el estado deseado (`spec`) con el actual y actúa para reducir la diferencia, una y otra vez. Por eso Kubernetes se "autorrepara": si borras un Pod de un ReplicaSet, el controlador crea otro. El scheduling es tarea del kube-scheduler.

### [1/Core Concepts/2]
Which mechanism lets you add your own resource types, such as `Database` or `Certificate`, to the Kubernetes API without modifying the API server code?
- [ ] Admission webhooks
- [x] CustomResourceDefinitions (CRDs)
- [ ] ConfigMaps with a special label
- [ ] API Priority and Fairness
> Un **CRD** registra un nuevo tipo de recurso que se gestiona con kubectl como cualquier otro. Junto con un controlador propio forma el **patrón Operator**. Los webhooks de admisión validan o mutan objetos, pero no crean tipos nuevos.

### [1/Core Concepts/2]
What is a Kubernetes Operator?
- [ ] A person who holds the cluster-admin role and operates the cluster
- [x] A custom controller that manages an app through custom resources
- [ ] A kubectl plugin that adds new commands to manage applications
- [ ] A built-in controller in kube-controller-manager for StatefulSets
> Un Operator codifica el conocimiento operativo de una aplicación (instalar, escalar, hacer backups, actualizar) en un controlador que observa *custom resources*. Ejemplos: operadores de PostgreSQL, Prometheus Operator o cert-manager. Los plugins de kubectl (krew) son otra cosa.

### [1/Core Concepts/2]
In what order does the API server process a request that creates an object?
- [ ] Admission → Authentication → Authorization → Persist to etcd
- [x] Authentication → Authorization → Admission control → Persist to etcd
- [ ] Authorization → Authentication → Validation → Persist to etcd
- [ ] Persist to etcd → Authentication → Authorization → Admission
> Cada petición pasa primero por **autenticación** (¿quién eres?), luego por **autorización** (¿puedes hacer esto?, normalmente RBAC) y después por la **admisión** (primero mutante, luego validación de esquema y admisión validante). Solo si todo pasa, el objeto se guarda en etcd.

### [1/Core Concepts/2]
Why is the number of etcd members in a production cluster usually odd (3 or 5)?
- [ ] etcd refuses to start with an even number of members
- [x] Raft needs a majority, so an even member adds no fault tolerance
- [ ] Odd member counts let etcd shard the keyspace evenly across nodes
- [ ] The API server can only connect to an odd number of endpoints
> etcd usa Raft, que necesita mayoría (⌊n/2⌋+1) para escribir. Con 3 miembros se tolera 1 fallo; con 4, también solo 1 (quórum = 3); con 5 se toleran 2. Por eso se usan números impares: un miembro par extra no mejora la tolerancia y sí añade coste y latencia.

### [1/Core Concepts/3]
A 5-member etcd cluster loses 3 members at the same time. What is the result?
- [ ] The cluster keeps accepting writes with the 2 remaining members
- [x] The cluster loses quorum and cannot accept writes
- [ ] The remaining members elect a new 2-member quorum automatically
- [ ] Only reads of Secrets fail
> Con 5 miembros el quórum es 3. Si quedan 2 no hay mayoría: etcd no puede confirmar escrituras, así que el API server no podrá modificar el estado del clúster. Un clúster de 5 tolera como máximo 2 fallos simultáneos.

### [1/Core Concepts/2]
In a highly available control plane with three API server instances, how do clients and nodes usually reach the API server?
- [ ] Each node is pinned to a single API server instance
- [x] Through a load balancer placed in front of the API server instances
- [ ] Only through the ClusterIP of the `kubernetes` Service
- [ ] Through etcd, which forwards requests to the active API server
> Los API servers son *stateless* y pueden correr varios a la vez (activo-activo) detrás de un balanceador; el estado está en etcd. En cambio, kube-scheduler y kube-controller-manager usan *leader election*: solo una instancia trabaja a la vez.

### [1/Core Concepts/3]
In an HA control plane, three kube-scheduler instances are running. How many of them actively schedule Pods at any given moment?
- [x] One, chosen through leader election
- [ ] All three, each handling a third of the nodes
- [ ] All three, coordinating through etcd transactions
- [ ] None until the API server assigns one of them
> kube-scheduler y kube-controller-manager usan *leader election* (con objetos Lease): una instancia es líder y las demás esperan en standby para tomar el relevo. Así se evitan decisiones duplicadas o contradictorias.

### [1/Core Concepts/2]
What are static Pods?
- [ ] Pods that cannot be deleted by anyone, including cluster admins
- [x] Pods run by the kubelet from manifest files on the node
- [ ] Pods that keep the same fixed IP address across every restart
- [ ] Pods created and owned by a StatefulSet with a fixed replica count
> El kubelet vigila un directorio (en kubeadm, `/etc/kubernetes/manifests`) y ejecuta los Pods definidos allí sin pasar por el scheduler. En el API server aparecen como *mirror pods* de solo lectura. kubeadm los usa para correr el API server, etcd, el scheduler y el controller-manager.

### [1/Core Concepts/2]
What happens to the Pods on a node that stays unreachable for an extended period?
- [ ] They are deleted the moment the node misses a single heartbeat
- [x] After about 5 minutes they are evicted and recreated on other nodes
- [ ] They keep running there and are never replaced until an admin acts
- [ ] The scheduler live-migrates the running containers to a healthy node
> El node controller marca el nodo como no listo/inalcanzable y le añade taints `NoExecute`. Los Pods tienen por defecto una tolerancia de 300 s a esos taints; al vencer se desalojan y sus controladores (Deployment, ReplicaSet…) crean reemplazos en otros nodos. Kubernetes no hace migración en vivo de contenedores.

### [1/Core Concepts/1]
Which statement best describes a Kubernetes namespace?
- [ ] A separate virtual cluster with its own control plane
- [x] A logical partition that scopes names, policies and quotas
- [ ] The Linux kernel feature that isolates container processes
- [ ] A group of nodes dedicated to a single team or environment
> Un namespace es una división lógica dentro del mismo clúster: los nombres son únicos dentro de él y sirve para aplicar RBAC, ResourceQuotas, LimitRanges y NetworkPolicies por equipo o entorno. No aísla nodos ni es un clúster aparte. No lo confundas con los *namespaces del kernel* de Linux, que aíslan procesos.

### [1/Core Concepts/2]
Which statement about Kubernetes API versioning is correct?
- [ ] Beta APIs are guaranteed never to change again
- [x] Beta APIs may still change, and new beta APIs are disabled by default
- [ ] Alpha APIs are enabled by default in production clusters
- [ ] Stable APIs are only available in managed Kubernetes services
> Kubernetes usa niveles alpha → beta → estable (GA). Alpha puede cambiar o desaparecer y está desactivada por defecto. Beta está probada pero aún puede cambiar; desde la 1.24 las **nuevas** APIs beta no se habilitan por defecto. Las estables (`v1`, `v2`…) tienen compatibilidad garantizada a largo plazo.

### [1/Core Concepts/2]
How do Kubernetes controllers and kubelets learn about changes to objects efficiently?
- [ ] By polling etcd directly every second
- [x] By using the API server's watch mechanism to receive change events
- [ ] By receiving notifications over SSH from the control plane
- [ ] By reading the audit log of the API server
> Los clientes de Kubernetes (controladores, kubelets, `kubectl get -w`) abren un *watch* contra el API server y reciben eventos ADDED, MODIFIED y DELETED. Esto evita sondeos constantes y es la base de los bucles de control. Solo el API server habla con etcd.

### [1/Core Concepts/2]
Which TWO components run on every worker node in a typical cluster? (Choose two.)
- [x] kubelet
- [x] kube-proxy
- [ ] kube-scheduler
- [ ] etcd
- [ ] kube-controller-manager
> Los componentes de nodo son el **kubelet**, el **kube-proxy** (salvo que el CNI lo reemplace, como Cilium) y el runtime de contenedores. etcd, kube-scheduler y kube-controller-manager son componentes del control plane.

### [1/Core Concepts/3]
A Pod sets `restartPolicy: Never`. Its only container exits with code 1. What is the final Pod phase?
- [ ] Succeeded
- [x] Failed
- [ ] Pending
- [ ] CrashLoopBackOff
> Con `restartPolicy: Never` el kubelet no reinicia el contenedor. Como terminó con un código distinto de 0, el Pod pasa a **Failed**; con código 0 sería **Succeeded**. CrashLoopBackOff solo aparece cuando hay reinicios (`Always` u `OnFailure`) y no es una fase.

### [1/Core Concepts/2]
Which `restartPolicy` values are allowed in the Pod template of a Deployment?
- [ ] `Always`, `OnFailure` and `Never`
- [x] Only `Always`
- [ ] Only `OnFailure`
- [ ] `OnFailure` and `Never`
> Los Pods de Deployments, ReplicaSets, StatefulSets y DaemonSets deben usar `restartPolicy: Always` (el valor por defecto), porque se espera que corran indefinidamente. Los Jobs usan `OnFailure` o `Never` porque son tareas que terminan.

### [1/Core Concepts/2]
What is the role of the `pause` (sandbox) container in a Pod?
- [ ] It pauses the application containers during rolling updates
- [x] It holds the Pod's shared namespaces, like the network one
- [ ] It collects the logs of the other containers and ships them
- [ ] It runs the liveness and readiness probes for the other containers
> El runtime crea primero un *sandbox* (el contenedor `pause` en muchos runtimes) que mantiene los namespaces compartidos del Pod, sobre todo el de red con la IP del Pod. Los contenedores de la app se unen a ellos, así que la IP sobrevive aunque un contenedor se reinicie.
