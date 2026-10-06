# KCNA · Dominio 1 · Kubernetes Fundamentals · Administration y Scheduling

### [1/Administration/1]
Which command lists Pods in all namespaces?
- [ ] `kubectl get pods --namespace=*`
- [x] `kubectl get pods -A`
- [ ] `kubectl get pods --all`
- [ ] `kubectl list pods --everywhere`
> `-A` es la forma corta de `--all-namespaces`. `--namespace=*` no es válido, `--all` sirve para otros comandos (como `delete`) y `kubectl list` no existe.

### [1/Administration/1]
Which command shows every resource type available in the cluster, including short names and whether each one is namespaced?
- [ ] `kubectl get all`
- [x] `kubectl api-resources`
- [ ] `kubectl api-versions`
- [ ] `kubectl explain --all`
> `kubectl api-resources` lista cada tipo (incluidos los CRDs) con su nombre corto, grupo/versión, si es namespaced y su `kind`. `kubectl api-versions` solo lista grupos/versiones, y `kubectl get all` muestra algunos objetos comunes de un namespace, no todos los tipos.

### [1/Administration/1]
You want to read the documentation of the `spec.strategy` field of a Deployment from the command line. Which command do you use?
- [x] `kubectl explain deployment.spec.strategy`
- [ ] `kubectl describe deployment.spec.strategy`
- [ ] `kubectl get deployment --help strategy`
- [ ] `kubectl docs deployment strategy`
> `kubectl explain` muestra la documentación del esquema de cualquier recurso y campo, obtenida del API server (incluye CRDs). `kubectl describe` muestra el estado de objetos concretos, no la documentación del esquema.

### [1/Administration/2]
Where does kubectl look for its configuration by default, and which environment variable overrides it?
- [ ] `/etc/kubernetes/kubectl.conf`; `KUBECTL_CONFIG`
- [x] `~/.kube/config`; `KUBECONFIG`
- [ ] `~/.kubectl/settings`; `KUBE_HOME`
- [ ] `/var/lib/kubelet/config`; `KUBE_CONFIG_PATH`
> Por defecto kubectl lee `~/.kube/config`. La variable `KUBECONFIG` puede apuntar a otro archivo o a varios (separados por `:` en Linux/macOS), que se fusionan. También existe la opción `--kubeconfig` en cada comando.

### [1/Administration/2]
In a kubeconfig file, what does a *context* combine?
- [ ] A cluster, a node and a container runtime
- [x] A cluster, a user and optionally a default namespace
- [ ] A user, a Role and the RoleBinding that grants it
- [ ] An API group, a version and a resource
> Un *context* une tres cosas: qué clúster (endpoint y CA), con qué usuario/credenciales y, opcionalmente, qué namespace usar por defecto. Se cambia con `kubectl config use-context <nombre>`.

### [1/Administration/2]
Which command changes the default namespace of your current context to `dev`?
- [ ] `kubectl namespace set dev --default`
- [x] `kubectl config set-context --current --namespace=dev`
- [ ] `kubectl use namespace dev --save-to-config`
- [ ] `kubectl config use-context dev`
> `kubectl config set-context --current --namespace=dev` modifica el contexto activo para que los comandos usen `dev` sin poner `-n`. `use-context dev` cambiaría a un *contexto* llamado dev, que no es lo mismo que un namespace.

### [1/Administration/2]
What is the main difference between `kubectl create -f app.yaml` and `kubectl apply -f app.yaml`?
- [ ] `create` validates the manifest against the schema; `apply` skips validation
- [x] `create` fails if the object exists; `apply` creates or updates it
- [ ] `apply` only works with Helm charts; `create` works with any manifest
- [ ] There is no difference; `apply` is just an alias of `create`
> `kubectl create` es imperativo: crea el objeto y da error si ya existe. `kubectl apply` es declarativo: crea si no existe y, si existe, calcula el parche para llevarlo al estado del archivo. Es la base de los flujos declarativos y de GitOps. Ambos pasan por la validación del API server.

### [1/Administration/2]
You need the YAML manifest of a new Deployment without creating it in the cluster. Which command produces it?
- [x] `kubectl create deployment web --image=nginx --dry-run=client -o yaml`
- [ ] `kubectl get deployment web --template --output-only`
- [ ] `kubectl run web --image=nginx --export`
- [ ] `kubectl create deployment web --image=nginx --generate-only`
> `--dry-run=client -o yaml` simula la creación en el cliente e imprime el manifiesto, sin enviarlo al clúster. Es un truco clásico para generar plantillas rápidamente. `--export` fue eliminado y `--generate-only` no existe.

### [1/Administration/1]
Which command scales the `web` Deployment to 5 replicas?
- [ ] `kubectl resize deployment web 5`
- [x] `kubectl scale deployment web --replicas=5`
- [ ] `kubectl set replicas deployment/web 5`
- [ ] `kubectl autoscale deployment web --replicas=5`
> `kubectl scale` cambia el número de réplicas de Deployments, ReplicaSets o StatefulSets. `kubectl autoscale` crea un HorizontalPodAutoscaler (con `--min`, `--max` y `--cpu-percent`), no fija un número.

### [1/Administration/2]
A new image version broke your application. Which command returns the `web` Deployment to its previous revision?
- [ ] `kubectl rollback deployment web`
- [x] `kubectl rollout undo deployment/web`
- [ ] `kubectl revert deployment web --to-previous`
- [ ] `kubectl apply deployment web --previous`
> `kubectl rollout undo` vuelve a la revisión anterior (o a una concreta con `--to-revision=N`). `kubectl rollout history` muestra las revisiones y `kubectl rollout status` el progreso. Los otros comandos no existen.

### [1/Administration/2]
You updated a Secret that the `api` Deployment consumes as environment variables, and you want all its Pods to be recreated gradually. Which command does this?
- [ ] `kubectl restart deployment api --all-pods`
- [x] `kubectl rollout restart deployment/api`
- [ ] `kubectl delete deployment api --restart`
- [ ] `kubectl replace --force deployment api --rolling`
> `kubectl rollout restart` añade al Pod template una anotación con la fecha, lo que dispara un rolling update normal (respetando `maxSurge`/`maxUnavailable`) sin downtime. Borrar el Deployment provocaría una caída del servicio.

### [1/Administration/2]
A node needs kernel maintenance. Which sequence safely moves its workloads away and brings it back afterwards?
- [ ] `kubectl delete node`, reboot, `kubectl create node`
- [x] `kubectl drain <node>`, perform maintenance, `kubectl uncordon <node>`
- [ ] `kubectl cordon <node>`, reboot, `kubectl drain <node>`
- [ ] `kubectl taint <node> maintenance=true:NoSchedule`, reboot, untaint
> `kubectl drain` marca el nodo como no programable (cordon) y desaloja sus Pods respetando los PodDisruptionBudgets; tras el mantenimiento, `kubectl uncordon` lo vuelve a habilitar. Un simple `cordon` evita Pods nuevos, pero no mueve los existentes.

### [1/Administration/2]
What does `kubectl cordon node-1` do?
- [ ] Evicts all Pods from node-1 while respecting PodDisruptionBudgets
- [x] Marks node-1 unschedulable while existing Pods keep running
- [ ] Removes node-1 from the cluster and deletes its Node object
- [ ] Restarts the kubelet and the container runtime on node-1
> `cordon` pone `spec.unschedulable: true`: el scheduler no colocará Pods nuevos allí, pero los que ya corren siguen. Para desalojarlos se usa `drain`, que incluye el cordon.

### [1/Administration/3]
`kubectl drain node-2` fails with an error that mentions DaemonSet-managed Pods. What is the usual fix?
- [ ] Delete the DaemonSet before draining and recreate it later
- [x] Run the drain again with `--ignore-daemonsets`
- [ ] Add a toleration for the drain to the DaemonSet's Pod template
- [ ] Use `kubectl cordon` instead, which also evicts DaemonSet Pods
> Los Pods de un DaemonSet están ligados a cada nodo y el controlador los recrearía de inmediato, así que `drain` se niega a continuar salvo que indiques `--ignore-daemonsets`, que los deja en el nodo y desaloja el resto. Si hay Pods sin controlador o con `emptyDir`, pueden hacer falta `--force` o `--delete-emptydir-data`.

### [1/Administration/2]
What is the purpose of a PodDisruptionBudget (PDB)?
- [ ] Limit the CPU that Pods may consume during an outage
- [x] Limit how many replicas can be down during voluntary disruptions
- [ ] Automatically restart Pods that crash too often in a row
- [ ] Reserve capacity on every node for business-critical Pods
> Un PDB define `minAvailable` o `maxUnavailable` para un conjunto de Pods. Las interrupciones **voluntarias** que usan la API de *eviction* (`kubectl drain`, el autoscaler de nodos) lo respetan. No protege contra fallos involuntarios como la caída de un nodo.

### [1/Administration/2]
What is the difference between a ResourceQuota and a LimitRange?
- [x] ResourceQuota caps a namespace's total usage; LimitRange sets per-container defaults and bounds
- [ ] ResourceQuota applies to whole nodes, while LimitRange applies to namespaces and their Pods
- [ ] LimitRange caps the number of objects, while ResourceQuota sets default container requests
- [ ] They are the same object exposed under two different API versions for compatibility
> ResourceQuota limita el **agregado** de un namespace (CPU/memoria totales, número de Pods, PVCs…). LimitRange actúa por contenedor/Pod/PVC: valores por defecto de requests/limits y mínimos/máximos. Suelen usarse juntos: si hay una cuota de CPU, cada Pod debe declarar requests, y un LimitRange puede ponerlos por defecto.

### [1/Administration/3]
A namespace has a ResourceQuota on `requests.cpu`. A developer applies a Deployment whose containers do not set CPU requests, and there is no LimitRange. What happens?
- [ ] The Pods are created with a default CPU request of 100m
- [x] The Pods are rejected because they must declare CPU requests
- [ ] The Pods are created as BestEffort and ignored by the quota
- [ ] The Deployment object itself is rejected by the API server
> Cuando una ResourceQuota limita `requests.cpu`, cada Pod nuevo debe declarar ese request; si no, la admisión lo rechaza. Ojo: el Deployment sí se crea, pero su ReplicaSet no logra crear los Pods (lo verás en sus eventos). Un LimitRange con valores por defecto evitaría el problema.

### [1/Administration/2]
When upgrading a kubeadm cluster, what is the correct general order?
- [ ] Upgrade the worker nodes first, then the control plane
- [x] Control plane first, then the workers, one minor version at a time
- [ ] Upgrade everything at once, skipping minor versions when needed
- [ ] Upgrade etcd last, after every kubelet has been upgraded
> La política de *version skew* exige que el API server nunca sea más antiguo que los kubelets. Por eso se actualiza primero el control plane (`kubeadm upgrade apply`) y luego cada nodo (drain → `kubeadm upgrade node` → actualizar kubelet/kubectl → uncordon), sin saltar versiones menores (1.36 → 1.37).

### [1/Administration/3]
According to the Kubernetes version skew policy, which kubelet version is NOT supported with a v1.37 kube-apiserver?
- [ ] v1.37
- [ ] v1.35
- [ ] v1.34
- [x] v1.38
> El kubelet puede ser hasta **tres** versiones menores más antiguo que el kube-apiserver (desde Kubernetes 1.28), pero **nunca más nuevo**. Con un API server 1.37 los kubelets 1.34–1.37 son válidos; un kubelet 1.38 no está soportado.

### [1/Administration/2]
How often does the Kubernetes project publish new minor releases?
- [ ] Every month, with a new patch every week
- [x] About three times per year
- [ ] Once per year, with long-term support
- [ ] Every two years, aligned with KubeCon
> Desde 2021 Kubernetes publica unas tres versiones menores al año (más o menos cada 15 semanas). Cada versión menor recibe parches durante unos 14 meses y el proyecto mantiene las tres más recientes. No hay una versión LTS oficial upstream.

### [1/Administration/2]
Which command creates a ClusterIP Service for the `web` Deployment that listens on port 80 and forwards to container port 8080?
- [x] `kubectl expose deployment web --port=80 --target-port=8080`
- [ ] `kubectl create service web --from=deployment --port=8080:80`
- [ ] `kubectl port-forward deployment/web 80:8080 --permanent`
- [ ] `kubectl expose pod web --type=Ingress --port=80`
> `kubectl expose` crea un Service usando el selector del Deployment: `--port` es el puerto del Service y `--target-port` el del contenedor. `port-forward` solo abre un túnel temporal desde tu máquina, y no existe un tipo de Service "Ingress".

### [1/Administration/2]
Which command checks whether you are allowed to delete Pods in the `prod` namespace?
- [ ] `kubectl get rolebindings -n prod --mine`
- [x] `kubectl auth can-i delete pods -n prod`
- [ ] `kubectl describe rbac delete pods -n prod`
- [ ] `kubectl access check pods delete prod`
> `kubectl auth can-i <verbo> <recurso>` le pregunta al API server (SelfSubjectAccessReview) si la acción está permitida y responde yes/no. Con `--as=<usuario>` lo compruebas para otro usuario (si puedes impersonar) y con `--list` ves todos tus permisos.

### [1/Administration/2]
`kubectl top pods` fails with an error saying that the metrics API is not available. What is missing?
- [ ] Prometheus
- [x] metrics-server
- [ ] kube-state-metrics
- [ ] The Kubernetes Dashboard
> `kubectl top` y el HPA basado en CPU/memoria usan la Metrics API (`metrics.k8s.io`), que normalmente implementa **metrics-server** a partir de los datos del kubelet. Prometheus y kube-state-metrics sirven para monitoreo, pero no implementan esa API por sí solos.

### [1/Administration/1]
Which tool is the official community tool to bootstrap a minimum viable Kubernetes cluster on existing machines?
- [ ] kind
- [x] kubeadm
- [ ] Helm
- [ ] Kustomize
> `kubeadm` (`kubeadm init` y `kubeadm join`) crea un clúster que sigue las buenas prácticas sobre máquinas existentes. *kind* corre clústeres dentro de contenedores (para pruebas y CI), Helm es un gestor de paquetes y Kustomize personaliza manifiestos.

### [1/Administration/2]
Which tool runs a whole Kubernetes cluster inside containers and is commonly used for local testing and CI pipelines?
- [x] kind
- [ ] kubeadm
- [ ] kubelet
- [ ] Kubespray
> **kind** (Kubernetes IN Docker) usa contenedores como "nodos" y es muy popular para pruebas y pipelines de CI. minikube y k3d son otras opciones locales; Kubespray usa Ansible para desplegar clústeres reales y kubeadm arranca clústeres en máquinas existentes.

### [1/Administration/2]
In a managed Kubernetes service such as EKS, GKE or AKS, what does the provider typically manage for you?
- [ ] Your application Deployments and how they scale
- [x] The control plane, including the API server and etcd
- [ ] The RBAC permissions granted to each of your users
- [ ] The security of the container images you deploy
> En un servicio gestionado, el proveedor opera el control plane (API server, etcd, scheduler, controller-manager): disponibilidad, parches y backups. Tú sigues siendo responsable de tus cargas, su configuración, el RBAC y la seguridad de tus imágenes (modelo de responsabilidad compartida).

### [1/Administration/2]
Which command shows the rollout revisions of the `web` Deployment?
- [ ] `kubectl get revisions deployment/web`
- [ ] `kubectl describe rollout web --all`
- [x] `kubectl rollout history deployment/web`
- [ ] `kubectl logs deployment/web --revisions`
> `kubectl rollout history` lista las revisiones guardadas (los ReplicaSets antiguos que conserva `revisionHistoryLimit`). Con `--revision=N` ves el detalle del template de esa revisión.

### [1/Administration/3]
Which kubectl output option prints only the IP addresses of the Pods by using a template expression?
- [ ] `-o wide --columns=IP`
- [x] `-o jsonpath='{.items[*].status.podIP}'`
- [ ] `-o yaml --field=status.podIP`
- [ ] `--output=ip --show-pod-addresses`
> `-o jsonpath` permite extraer campos concretos del JSON del objeto. `-o wide` añade columnas (incluida la IP), pero muestra toda la tabla. Las opciones `--columns`, `--field`, `--output=ip` y `--show-pod-addresses` no existen.

### [1/Administration/2]
Which file on a kubeadm control plane node grants full administrative access and should be protected like a root password?
- [ ] `/var/lib/kubelet/config.yaml`
- [x] `/etc/kubernetes/admin.conf`
- [ ] `/etc/cni/net.d/10-calico.conflist`
- [ ] `/etc/containerd/config.toml`
> kubeadm genera `/etc/kubernetes/admin.conf`, un kubeconfig con credenciales de administrador. Quien lo tenga controla el clúster, así que no debe compartirse: lo correcto es dar a cada persona sus propias credenciales con RBAC de mínimo privilegio.

### [1/Administration/2]
Which command checks the expiration dates of the control plane certificates in a kubeadm cluster?
- [ ] `kubectl get certificates --all-namespaces`
- [x] `kubeadm certs check-expiration`
- [ ] `openssl kube-certs --list-expiry`
- [ ] `kubectl describe node --show-certs`
> `kubeadm certs check-expiration` muestra el vencimiento de los certificados que gestiona kubeadm (por defecto válidos un año; la CA, diez). Se renuevan con `kubeadm certs renew` o automáticamente al hacer `kubeadm upgrade`.

### [1/Administration/2]
How do you back up the cluster state stored in etcd?
- [x] `etcdctl snapshot save backup.db`
- [ ] `kubectl get all -A -o yaml > backup.yaml`
- [ ] `kubeadm backup create --all`
- [ ] Copy `/etc/kubernetes/manifests` to another node
> `etcdctl snapshot save` toma una instantánea consistente de etcd (usando sus certificados para autenticarse). `kubectl get all` solo incluye algunos tipos (no Secrets, ConfigMaps ni CRDs), `kubeadm backup` no existe y los manifiestos estáticos no contienen el estado del clúster.

### [1/Scheduling/1]
What is the simplest way to constrain a Pod so that it only runs on nodes labeled `disktype=ssd`?
- [x] Set `nodeSelector: {disktype: ssd}` in the Pod spec
- [ ] Add a toleration for `disktype=ssd` to the Pod
- [ ] Create a NetworkPolicy that selects `disktype=ssd`
- [ ] Annotate the Pod with `scheduler/disktype: ssd`
> `nodeSelector` es la forma más simple: el Pod solo se programa en nodos que tengan **todas** esas labels. Para expresiones más ricas (In, NotIn, Exists, preferencias) se usa node affinity. Las tolerations no atraen Pods a nodos; solo les permiten tolerar taints.

### [1/Scheduling/2]
What does the "IgnoredDuringExecution" part of `requiredDuringSchedulingIgnoredDuringExecution` mean?
- [ ] The rule is skipped whenever the scheduler is overloaded
- [x] Pods are not evicted if node labels change after scheduling
- [ ] The rule only applies to the Pod's init containers
- [ ] The Pod ignores the rule every time it is restarted
> La regla se exige al **programar** el Pod, pero si después cambian las labels del nodo y dejan de cumplirse, el Pod sigue corriendo allí. La variante `preferredDuringScheduling...` es una preferencia con peso, no una obligación.

### [1/Scheduling/2]
A node has the taint `gpu=true:NoSchedule`. Which Pods can be scheduled on it?
- [ ] Any Pod that has the nodeSelector `gpu=true`
- [x] Only Pods that carry a matching toleration
- [ ] Only Pods that are managed by a DaemonSet
- [ ] No Pods at all until the taint is removed
> Un taint `NoSchedule` repele a los Pods que no lo toleran: solo los que tienen una toleration que coincida pueden programarse allí. Los Pods que ya corrían antes del taint no se ven afectados (eso sería `NoExecute`). Un nodeSelector por sí solo no permite saltarse el taint.

### [1/Scheduling/3]
You want GPU nodes to run ONLY GPU workloads, and GPU workloads to run ONLY on GPU nodes. What is the correct combination?
- [ ] Give GPU Pods a matching toleration, without tainting any node
- [ ] Give GPU Pods node affinity for GPU nodes, without any taint
- [x] Taint GPU nodes; give GPU Pods a toleration and node affinity
- [ ] Taint all non-GPU nodes so that GPU Pods are repelled from them
> El taint mantiene fuera a los Pods que no son de GPU; la toleration deja entrar a los de GPU; y la node affinity (o un nodeSelector) obliga a los de GPU a ir a esos nodos, porque una toleration **no atrae**, solo permite. Se necesitan las dos piezas para lograr la dedicación en ambos sentidos.
>
> Solo la toleration no fuerza nada, solo la affinity deja que otros Pods sigan entrando a los nodos GPU, y poner taints a todos los demás nodos sacaría de ellos al resto de cargas.

### [1/Scheduling/2]
Which taint effect also evicts already-running Pods that do not tolerate it?
- [ ] NoSchedule
- [ ] PreferNoSchedule
- [x] NoExecute
- [ ] NoEvict
> `NoExecute` impide programar Pods nuevos sin toleration **y** desaloja los que ya corren y no lo toleran (opcionalmente tras `tolerationSeconds`). `NoSchedule` solo afecta a Pods nuevos y `PreferNoSchedule` es una preferencia suave. `NoEvict` no existe.

### [1/Scheduling/2]
Why are regular application Pods not scheduled on control plane nodes in a kubeadm cluster?
- [ ] The kubelet on control plane nodes refuses any non-system Pod
- [x] Control plane nodes carry a `control-plane:NoSchedule` taint
- [ ] The API server blocks Pods outside kube-system from those nodes
- [ ] Control plane nodes do not have a container runtime installed
> kubeadm añade el taint `node-role.kubernetes.io/control-plane:NoSchedule` a los nodos del control plane. Las cargas normales no lo toleran, así que no se programan allí. En clústeres de laboratorio de un solo nodo se suele quitar ese taint.

### [1/Scheduling/2]
You want the replicas of a Deployment spread across different nodes, so that one node failure cannot take all of them down. Which feature fits best?
- [ ] A nodeSelector on the label `kubernetes.io/hostname`
- [x] Pod anti-affinity or topology spread constraints by hostname
- [ ] A taint on each node that carries the Deployment's name
- [ ] A PriorityClass with a very high value for the Deployment
> La *pod anti-affinity* evita colocar Pods con ciertas labels en el mismo dominio de topología (aquí, el mismo nodo), y las *topology spread constraints* (`maxSkew`) son la forma moderna de repartirlos uniformemente entre nodos o zonas. Un nodeSelector fijaría los Pods a un nodo concreto: justo lo contrario.

### [1/Scheduling/2]
In a topology spread constraint, what does `maxSkew: 1` with `topologyKey: topology.kubernetes.io/zone` mean?
- [ ] At most one Pod may run in each availability zone
- [x] Pod counts in any two zones may differ by at most one
- [ ] Pods may be placed at most one zone away from clients
- [ ] Only one zone may contain unschedulable Pods at a time
> `maxSkew` es la diferencia máxima permitida entre el dominio con más Pods y el que tiene menos. Con 1 y la zona como topología, los Pods se reparten casi por igual (2-2-1 vale; 3-1-1 no). `whenUnsatisfiable` define si es obligatorio (`DoNotSchedule`) o preferente (`ScheduleAnyway`).

### [1/Scheduling/2]
Which two phases does the kube-scheduler go through to pick a node for a Pod?
- [ ] Leader election, then binding
- [x] Filtering, then scoring
- [ ] Draining, then cordoning
- [ ] Admission, then validation
> El scheduler primero **filtra** los nodos que pueden alojar el Pod (recursos, taints, afinidades, puertos, volúmenes) y luego **puntúa** los viables para elegir el mejor. Finalmente hace el *binding* del Pod al nodo elegido.

### [1/Scheduling/2]
When deciding whether a Pod fits on a node, which values does the scheduler use?
- [ ] The containers' resource limits
- [x] The containers' resource requests
- [ ] The node's actual CPU usage right now
- [ ] The total size of the container images
> El scheduler reserva capacidad según los **requests**: suma los de los Pods del nodo y comprueba que quepa el nuevo dentro de lo *allocatable*. No mira el consumo real del momento ni los limits; los limits los aplica el runtime (cgroups) durante la ejecución.

### [1/Scheduling/3]
One container exceeds its CPU limit, and another container exceeds its memory limit. What happens to each of them?
- [ ] Both containers are killed and then restarted
- [x] The first is throttled; the second is OOM-killed
- [ ] Both containers are throttled until usage drops
- [ ] The first is evicted; the second is throttled
> La CPU es un recurso **comprimible**: al llegar al límite el contenedor se ralentiza (throttling) pero no muere. La memoria **no** lo es: si se supera el límite, el kernel mata el proceso (OOMKilled, código 137) y el kubelet lo reinicia según su política.

### [1/Scheduling/2]
What does a PriorityClass let you do?
- [ ] Give some namespaces a bigger share of CPU than other namespaces
- [x] Schedule important Pods first and preempt lower-priority ones
- [ ] Prioritize the network traffic between a set of selected Services
- [ ] Control the start order of the containers that run inside a Pod
> Los Pods con un `priorityClassName` de mayor valor se ordenan antes en la cola del scheduler y, si no caben, el scheduler puede **expulsar (preempt)** Pods de menor prioridad para hacerles sitio. `system-cluster-critical` y `system-node-critical` son clases incorporadas para componentes esenciales.

### [1/Scheduling/2]
A Pod spec sets `nodeName: worker-3` directly. What happens?
- [ ] The scheduler validates worker-3 and binds the Pod if it fits
- [x] The scheduler is bypassed and worker-3's kubelet tries to run it
- [ ] The Pod is rejected because `nodeName` is a read-only field
- [ ] worker-3 is tainted so that it only accepts this specific Pod
> Si `nodeName` ya viene definido, el scheduler no interviene: el kubelet de ese nodo intenta correr el Pod directamente. Si no hay recursos o el nodo no existe, el Pod falla. Por eso se recomienda usar nodeSelector o afinidad en lugar de `nodeName`.

### [1/Scheduling/2]
How can a Pod ask to be scheduled by a custom scheduler instead of the default one?
- [ ] By adding a toleration for the custom scheduler
- [x] By setting `spec.schedulerName` to that scheduler's name
- [ ] By labeling its namespace with the scheduler's name
- [ ] By creating a SchedulerBinding object that targets it
> Kubernetes admite varios schedulers a la vez. Cada Pod indica cuál debe programarlo con `spec.schedulerName` (por defecto `default-scheduler`); los demás schedulers lo ignoran.

### [1/Scheduling/2]
What does the HorizontalPodAutoscaler (HPA) do?
- [ ] Adds nodes to the cluster when Pods are pending
- [x] Adjusts the replica count based on observed metrics
- [ ] Raises the CPU and memory requests of running Pods
- [ ] Moves busy Pods to bigger nodes in the cluster
> El HPA escala horizontalmente: cambia `replicas` de un Deployment o StatefulSet según métricas (CPU, memoria, custom o externas). Ajustar requests/limits es tarea del VPA, y añadir nodos es tarea del Cluster Autoscaler o de Karpenter.

### [1/Scheduling/3]
An HPA targets 60% average CPU utilization, but it never scales and shows `<unknown>` as the current value. What is the most likely cause?
- [ ] The Deployment uses the Recreate update strategy
- [x] The Pods lack CPU requests, or metrics-server is missing
- [ ] The HPA requires a PodDisruptionBudget to be present
- [ ] CPU-based autoscaling requires a LoadBalancer Service
> La utilización de CPU se calcula como porcentaje del **request**: sin requests no hay porcentaje posible. Además, el HPA obtiene CPU/memoria de la Metrics API, normalmente servida por metrics-server; si no está instalado, la métrica aparece como `<unknown>`.

### [1/Scheduling/2]
Which autoscaler adjusts the CPU and memory requests of Pods based on their historical usage?
- [ ] HorizontalPodAutoscaler
- [x] VerticalPodAutoscaler
- [ ] Cluster Autoscaler
- [ ] KEDA
> El **VPA** recomienda o aplica requests/limits ajustados al uso real (escalado vertical). El HPA cambia el número de réplicas, el Cluster Autoscaler cambia el número de nodos y KEDA escala según eventos externos (colas, streams), incluso a cero.

### [1/Scheduling/2]
Several Pods are `Pending` because no node has enough free capacity. Which component can add nodes automatically?
- [ ] The HorizontalPodAutoscaler, by raising `maxReplicas`
- [ ] The kube-scheduler, through its preemption logic
- [x] The Cluster Autoscaler or a provisioner like Karpenter
- [ ] The VerticalPodAutoscaler, by resizing existing nodes
> El Cluster Autoscaler detecta Pods no programables por falta de recursos y pide más nodos al proveedor (y retira nodos infrautilizados). Karpenter es una alternativa que aprovisiona nodos a la medida de los Pods pendientes. El scheduler solo asigna Pods a nodos que ya existen.

### [1/Scheduling/2]
Which CNCF project autoscales workloads based on events such as queue length, and can scale them down to zero?
- [ ] Knative Eventing
- [x] KEDA
- [ ] Argo Events
- [ ] Prometheus Adapter
> **KEDA** (Kubernetes Event-Driven Autoscaling, graduado en la CNCF) usa *scalers* para colas (Kafka, RabbitMQ, SQS…), métricas y otros eventos; gestiona un HPA por debajo y puede escalar a cero réplicas. Knative Serving también escala a cero, pero para cargas HTTP.

### [1/Scheduling/2]
Which HorizontalPodAutoscaler API version supports scaling on several metrics at once, including custom and external metrics?
- [ ] `autoscaling/v1`
- [x] `autoscaling/v2`
- [ ] `apps/v1`
- [ ] `metrics.k8s.io/v1beta1`
> `autoscaling/v1` solo admite CPU. `autoscaling/v2` (estable) admite varias métricas a la vez —de recursos, de Pods, de objetos y externas— y permite configurar el comportamiento de escalado (`behavior`).

### [1/Scheduling/3]
How are DaemonSet Pods scheduled in current Kubernetes versions?
- [ ] The DaemonSet controller sets `nodeName` and bypasses the scheduler
- [x] The default scheduler places them using node affinity set by the controller
- [ ] Each node's kubelet creates them from a static manifest on disk
- [ ] A separate daemon-scheduler component is responsible for them
> El controlador de DaemonSet crea un Pod por nodo con una afinidad que apunta a ese nodo concreto, y el **scheduler por defecto** lo programa. Además, el controlador añade automáticamente tolerations para taints como `not-ready` o `unreachable`, para que estos Pods sigan funcionando en esas situaciones.

### [1/Scheduling/2]
A Pod is Pending with the event "0/3 nodes are available: 3 node(s) didn't match Pod's node affinity/selector". What should you check first?
- [ ] The container image name and the tag used in the Pod
- [x] The Pod's selector or affinity rules against node labels
- [ ] The label selector of the Service in front of the Pod
- [ ] The timeouts configured for the liveness probe
> El mensaje dice que ningún nodo cumple las reglas de selección. Compara las labels de los nodos (`kubectl get nodes --show-labels`) con el `nodeSelector` o la afinidad del Pod: puede ser una errata o una label que falta.

### [1/Scheduling/2]
Which Pod setting expresses "prefer nodes in zone A, but use other nodes if needed"?
- [ ] `nodeSelector` with the zone A label
- [x] Node affinity of type `preferredDuringSchedulingIgnoredDuringExecution`
- [ ] A `NoSchedule` taint on the nodes outside zone A
- [ ] Node affinity of type `requiredDuringSchedulingIgnoredDuringExecution`
> La afinidad *preferred* asigna un **peso** a los nodos que cumplen la regla, pero si no hay ninguno disponible el Pod se programa en otro. `nodeSelector` y la afinidad *required* son obligatorias, y un taint `NoSchedule` impediría usar los otros nodos.

### [1/Scheduling/3]
What is the difference between node-pressure eviction and API-initiated eviction?
- [x] The kubelet evicts to reclaim resources; API evictions such as drain honor PodDisruptionBudgets
- [ ] Node-pressure eviction honors PodDisruptionBudgets, while API evictions always ignore them
- [ ] Both kinds of eviction are performed by the kube-scheduler during its scoring phase
- [ ] API-initiated eviction only applies to DaemonSet Pods during cluster upgrades
> La expulsión por presión del nodo la hace el **kubelet** cuando falta memoria, disco o PIDs, y no respeta PDBs. La expulsión iniciada por la API (Eviction API, usada por `kubectl drain` o por los autoscalers) sí respeta los PodDisruptionBudgets.

### [1/Scheduling/1]
What does a toleration on a Pod do?
- [ ] It forces the Pod onto the nodes that carry the matching taint
- [x] It allows the Pod onto nodes with a matching taint, without requiring it
- [ ] It removes the matching taint from the node where the Pod lands
- [ ] It prevents the Pod from being evicted for any reason at all
> Una toleration solo **permite** que el Pod se programe (o permanezca) en nodos con ese taint; no lo obliga a ir allí. Para forzar la ubicación hay que combinarla con un nodeSelector o node affinity.
