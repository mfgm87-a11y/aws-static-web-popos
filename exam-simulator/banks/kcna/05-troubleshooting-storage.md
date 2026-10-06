# KCNA · Dominio 2 · Container Orchestration · Troubleshooting y Storage

### [2/Troubleshooting/2]
A Pod shows the status `ImagePullBackOff`. What is the most likely cause?
- [ ] The container ran out of memory and was killed
- [x] A wrong image name or tag, or missing registry credentials
- [ ] The readiness probe keeps failing on the container
- [ ] Every node carries a NoSchedule taint the Pod does not tolerate
> `ErrImagePull` / `ImagePullBackOff` indican que el kubelet no pudo descargar la imagen: nombre o tag inexistente, registro privado sin `imagePullSecrets`, límites de descarga o problemas de red. `kubectl describe pod` muestra el error exacto en Events, y Kubernetes reintenta con esperas crecientes (*back-off*).

### [2/Troubleshooting/2]
A Pod is in `CrashLoopBackOff`. Which command is most useful to see why the previous container instance failed?
- [ ] `kubectl get pod <pod> -o wide`
- [x] `kubectl logs <pod> --previous`
- [ ] `kubectl top pod <pod> --containers`
- [ ] `kubectl rollout status pod/<pod>`
> CrashLoopBackOff significa que el contenedor arranca, falla y se reinicia con esperas cada vez mayores. Como el contenedor actual puede no tener logs todavía, `kubectl logs --previous` muestra la salida de la ejecución anterior. `kubectl describe pod` también ayuda (código de salida, motivo y eventos).

### [2/Troubleshooting/2]
A Pod stays `Pending`, and its events show "0/4 nodes are available: 4 Insufficient memory". What should you do?
- [ ] Increase the memory limit of the container to fit the node
- [x] Lower the memory request or add capacity to the cluster
- [ ] Restart the kube-scheduler on the control plane
- [ ] Change the image pull policy of the Pod to Always
> El scheduler no encuentra ningún nodo con memoria *asignable* suficiente para el **request** del Pod. Opciones: bajar el request si estaba sobredimensionado, liberar capacidad o añadir nodos (manualmente o con un autoscaler). Subir el limit no ayuda, porque el scheduler usa requests.

### [2/Troubleshooting/2]
A Pod's status is `CreateContainerConfigError`. What is a common cause?
- [ ] The node has run out of disk space for container images
- [x] A ConfigMap or Secret it references does not exist
- [ ] The container image is too large for the node
- [ ] The Service selector does not match the Pod's labels
> `CreateContainerConfigError` aparece cuando el kubelet no puede construir la configuración del contenedor, típicamente porque falta un ConfigMap o Secret, o una clave referenciada en `env`/`envFrom`. Los eventos del Pod indican qué recurso falta.

### [2/Troubleshooting/2]
A Service has no endpoints, although its Pods are Running and Ready. What is the most likely cause?
- [ ] CoreDNS is not running in the cluster
- [x] The Service selector does not match the Pod labels
- [ ] The Pods are managed with the Recreate strategy
- [ ] The Service type must be NodePort instead of ClusterIP
> Un Service encuentra sus Pods por **selector de labels**. Con una errata (por ejemplo `app: web` frente a `app: frontend`) no habrá EndpointSlices con IPs. Compara el *Selector* de `kubectl describe svc` con `kubectl get pods --show-labels`.

### [2/Troubleshooting/2]
`kubectl describe pod web-7d9` shows `Last State: Terminated, Reason: OOMKilled, Exit Code: 137`. What should you investigate?
- [ ] The CPU limit and CPU throttling of the container
- [x] The memory limit and the app's memory usage
- [ ] The image pull secret of the Pod
- [ ] The timeout of the liveness probe
> OOMKilled significa que el contenedor superó su límite de memoria y el kernel lo mató (137 = SIGKILL). Revisa si el límite es demasiado bajo para la carga real o si la aplicación tiene una fuga de memoria. La CPU no provoca OOM: solo throttling.

### [2/Troubleshooting/2]
A node shows `NotReady`. What is a good first check on that node?
- [ ] Whether the Deployment still has enough replicas
- [x] Whether the kubelet and the container runtime are running
- [ ] Whether CoreDNS has enough replicas in kube-system
- [ ] Whether the Ingress controller reports itself healthy
> Un nodo pasa a NotReady cuando el kubelet deja de reportar o reporta problemas (runtime caído, CNI no inicializado, presión de recursos). En el nodo: `systemctl status kubelet`, `journalctl -u kubelet` y el estado de containerd. `kubectl describe node` muestra las *Conditions* (MemoryPressure, DiskPressure, PIDPressure, Ready).

### [2/Troubleshooting/1]
Which command shows a Pod's recent events, such as scheduling failures or image pull errors?
- [ ] `kubectl logs <pod>`
- [x] `kubectl describe pod <pod>`
- [ ] `kubectl exec <pod> -- dmesg`
- [ ] `kubectl get pod <pod> -o name`
> `kubectl describe` muestra el estado detallado del Pod y, al final, sus **Events** (programación, descarga de imágenes, probes fallidas, OOM…). `kubectl logs` muestra la salida de la aplicación, que no incluye estos eventos del clúster.

### [2/Troubleshooting/2]
A Pod is `Running`, but its RESTARTS counter grows every couple of minutes and the logs look normal until each restart. What is a likely cause?
- [ ] The readiness probe is failing on every check
- [x] The liveness probe fails, e.g. due to a wrong path
- [ ] The Service in front of the Pod has no endpoints
- [ ] The node where the Pod runs has been cordoned by an admin
> Si la *liveness probe* está mal configurada (ruta o puerto incorrectos, timeout muy corto), el kubelet considera muerto el contenedor y lo reinicia aunque la aplicación esté bien. Los eventos mostrarán "Liveness probe failed". Una readiness fallida no reinicia nada; solo quita tráfico.

### [2/Troubleshooting/2]
Pods cannot resolve any Service names at all. Where should you look first?
- [ ] The logs of the kube-scheduler
- [x] The CoreDNS Pods and the Pod's `/etc/resolv.conf`
- [ ] The member list of the etcd cluster
- [ ] The configuration of the Ingress controller
> Si falla toda la resolución, revisa que los Pods de CoreDNS estén Running (`kubectl get pods -n kube-system -l k8s-app=kube-dns`), sus logs, el Service `kube-dns` y que el `resolv.conf` del Pod apunte a su IP. Una prueba típica: `kubectl run tmp --rm -it --image=busybox -- nslookup kubernetes.default`.

### [2/Troubleshooting/2]
A Pod has been stuck in `ContainerCreating` for several minutes. Which is a plausible cause?
- [ ] The application has a bug that makes it exit with code 1
- [x] A volume cannot be mounted, or the CNI failed to set up networking
- [ ] The readiness probe is configured with a very strict threshold
- [ ] The Deployment that owns the Pod has too many replicas
> En `ContainerCreating` el Pod ya está asignado a un nodo, pero el kubelet aún no logra crear el contenedor: volúmenes que no se adjuntan o montan (PVC, Secret inexistente), fallos del CNI o la descarga lenta de una imagen enorme. Un bug de la aplicación daría CrashLoopBackOff.

### [2/Troubleshooting/2]
A Pod shows `Init:CrashLoopBackOff`. What does that mean?
- [ ] The main container crashed while the node was initializing
- [x] An init container keeps failing, so the app containers never start
- [ ] The Pod is waiting for a PersistentVolume to become available
- [ ] The container image is still being pulled from the registry
> El prefijo `Init:` indica que el problema está en un init container: falla una y otra vez y, como debe terminar con éxito antes de arrancar la app, los contenedores principales nunca inician. Revisa sus logs con `kubectl logs <pod> -c <init-container>`.

### [2/Troubleshooting/3]
A Deployment rollout is stuck, and `kubectl rollout status` eventually reports `ProgressDeadlineExceeded`. What does this mean?
- [ ] The Deployment object was deleted while the rollout was still running
- [x] New Pods did not become available within `progressDeadlineSeconds`
- [ ] The HorizontalPodAutoscaler blocked the rollout on purpose
- [ ] The cluster ran out of IP addresses for Services
> Si los Pods nuevos no llegan a estar disponibles (imagen errónea, probes fallando, falta de recursos) dentro de `progressDeadlineSeconds` (600 s por defecto), el Deployment marca la condición `Progressing=False` con motivo `ProgressDeadlineExceeded`. Kubernetes no hace rollback automático: hay que corregir el problema o ejecutar `kubectl rollout undo`.

### [2/Troubleshooting/2]
A Deployment's Pods are not being created, and the ReplicaSet events show `exceeded quota`. What is happening?
- [ ] Every node in the node pool is already full
- [x] The new Pods would exceed a ResourceQuota in the namespace
- [ ] The container image is too big for the registry's quota
- [ ] The HorizontalPodAutoscaler has reached `maxReplicas`
> La admisión de ResourceQuota rechaza los Pods que harían superar los límites del namespace (CPU, memoria, número de Pods…). El error aparece en los eventos del ReplicaSet, no en los del Deployment. La solución es ajustar la cuota, los requests o el número de réplicas.

### [2/Troubleshooting/2]
A container exits immediately with exit code 127. What does that usually indicate?
- [ ] It was killed for exceeding its memory limit
- [x] The command or binary to run was not found
- [ ] It received SIGTERM during a normal shutdown
- [ ] It finished its work successfully
> Cuando el comando se ejecuta a través de un shell (`sh -c ...` o la forma shell de CMD), 127 significa "command not found": un nombre mal escrito o un binario que no existe en la imagen. Si el runtime ni siquiera encuentra el ejecutable del ENTRYPOINT, el contenedor falla con `StartError` (código 128). 137 = SIGKILL (a menudo OOM), 143 = SIGTERM y 0 = éxito.

### [2/Troubleshooting/2]
A Pod has been `Terminating` for a long time after you deleted it. What typically causes this?
- [ ] The Pod defines a readiness probe that keeps failing
- [x] A pending finalizer, or a node that is unreachable
- [ ] The Pod is still selected by at least one Service
- [ ] The container image is still cached on the node
> El borrado de un Pod termina cuando el kubelet confirma que paró los contenedores y se quitan los finalizers. Si el nodo está caído o un finalizer no se resuelve, el Pod queda en Terminating. `--grace-period=0 --force` lo quita del API server, pero úsalo con cuidado: el proceso podría seguir corriendo en el nodo.

### [2/Troubleshooting/2]
Several Pods on one node show the status `Evicted`. What is the most likely reason?
- [ ] The Pods kept failing their readiness probes
- [x] The node ran short of memory or disk space
- [ ] A NetworkPolicy blocked all of their traffic
- [ ] The Pods went over their CPU limits for too long
> El kubelet expulsa Pods cuando el nodo cruza umbrales de presión (memoria, disco o ephemeral-storage, PIDs). Los Pods quedan como `Evicted` (fase Failed) y su controlador crea reemplazos en otro sitio. Superar el límite de CPU solo produce throttling.

### [2/Troubleshooting/3]
Your Pods are Running and Ready, the Service has endpoints and DNS resolution works, but requests coming from another namespace time out. What should you check next?
- [ ] The tag of the container image in the Deployment
- [x] NetworkPolicies that might be blocking the traffic
- [ ] The logs of the kube-scheduler on the control plane
- [ ] The QoS class assigned to the backend Pods
> Si hay endpoints y el DNS resuelve, pero las conexiones expiran, algo bloquea el tráfico: típicamente una NetworkPolicy (por ejemplo un *default deny* que solo permite el propio namespace) o un `targetPort` que apunta a un puerto donde la app no escucha. Revisa las políticas que seleccionan a los Pods de destino.

### [2/Troubleshooting/2]
Which command lists the recent events of a namespace, sorted by time?
- [ ] `kubectl logs --events --sort-by=time --namespace=dev`
- [x] `kubectl get events --sort-by=.metadata.creationTimestamp`
- [ ] `kubectl describe namespace dev --events-only --sorted`
- [ ] `kubectl top events --namespace=dev --sort-by=timestamp`
> `kubectl get events` muestra los eventos del namespace; ordenarlos por `.metadata.creationTimestamp` (o usar `kubectl events`, que ya los ordena) facilita ver la secuencia de lo ocurrido. Los eventos se conservan poco tiempo (una hora por defecto).

### [2/Troubleshooting/2]
A Pod is Running, but `kubectl get pods` shows READY `1/2`. What does that tell you?
- [ ] One of the two replicas of the Deployment is down
- [x] One of the Pod's two containers is not ready
- [ ] The Pod is using half of its memory limit
- [ ] The Pod is halfway through a rolling update
> La columna READY indica cuántos contenedores del Pod están listos frente al total. `1/2` significa que un contenedor (la app o un sidecar) no supera su readiness o no ha arrancado. Investiga con `kubectl describe pod` y con los logs de ese contenedor (`-c`).

### [2/Troubleshooting/3]
A PersistentVolumeClaim stays `Pending` and no PersistentVolume is created. A CSI driver is installed. What is a likely cause?
- [ ] The Pod that uses the claim has no resource limits
- [x] The PVC sets no StorageClass and none is the default
- [ ] PersistentVolumeClaims must be created in kube-system
- [ ] The access mode of every PVC must be ReadWriteMany
> Para el aprovisionamiento dinámico, el PVC debe referenciar una StorageClass o debe existir una por defecto. También puede quedarse Pending si la clase usa `WaitForFirstConsumer` y todavía no hay un Pod que lo use, o si no hay ningún PV estático compatible.

### [2/Troubleshooting/2]
`kubectl` returns: `Error from server (Forbidden): pods is forbidden: User "ana" cannot list resource "pods" in API group "" in the namespace "prod"`. What does this indicate?
- [ ] The API server is down or unreachable from Ana's laptop
- [x] Ana is authenticated but not authorized by RBAC
- [ ] Ana's client certificate has expired and must be renewed
- [ ] The `prod` namespace does not exist in this cluster
> Un error 403 *Forbidden* significa que la autenticación funcionó (el API server sabe que eres "ana"), pero la **autorización** lo negó. Un problema de credenciales daría 401 *Unauthorized*. Se resuelve con un Role y un RoleBinding adecuados; `kubectl auth can-i list pods -n prod --as ana` ayuda a verificarlo.

### [2/Storage/1]
What is the lifetime of an `emptyDir` volume?
- [ ] It persists on the node forever, even after the Pod is gone
- [x] It lives as long as the Pod and survives container restarts
- [ ] It is wiped every time any container in the Pod restarts
- [ ] It is backed up to etcd and restored on the next Pod start
> Un `emptyDir` se crea vacío cuando el Pod se asigna a un nodo y se borra cuando el Pod se elimina. Sobrevive a los reinicios de contenedores y sirve para compartir archivos entre contenedores del Pod o como espacio temporal. Con `medium: Memory` usa tmpfs (RAM).

### [2/Storage/1]
What is the relationship between a PersistentVolume (PV) and a PersistentVolumeClaim (PVC)?
- [ ] A PV is a user's request; a PVC is the actual piece of storage
- [x] A PV is the storage resource; a PVC is a request that binds to one
- [ ] They are the same object, just created in different namespaces
- [ ] A PVC is only used to mount ConfigMaps and Secrets into Pods
> El PV representa almacenamiento real (aprovisionado por un admin o dinámicamente) y es de ámbito de clúster. El PVC es la petición de un usuario (tamaño, modo de acceso, clase) dentro de un namespace: Kubernetes lo enlaza (*bind*) a un PV compatible, y el Pod usa el PVC.

### [2/Storage/2]
What enables PersistentVolumes to be created automatically when a PVC is submitted?
- [ ] A DaemonSet that runs on every node
- [x] A StorageClass with a provisioner
- [ ] A ResourceQuota on storage requests
- [ ] The kube-scheduler's volume plugin
> La StorageClass define un *provisioner* (normalmente un driver CSI) y parámetros (tipo de disco, replicación…). Cuando un PVC pide esa clase, el provisioner crea el volumen y su PV: es el **aprovisionamiento dinámico**. Sin StorageClass, un admin tendría que crear los PVs a mano.

### [2/Storage/2]
Which access mode allows a volume to be mounted read-write by many nodes at the same time?
- [ ] ReadWriteOnce (RWO)
- [ ] ReadOnlyMany (ROX)
- [x] ReadWriteMany (RWX)
- [ ] ReadWriteOncePod (RWOP)
> **RWX** permite lectura/escritura desde muchos nodos (p. ej. NFS, CephFS, EFS). **RWO** permite lectura/escritura desde un solo nodo (varios Pods de ese nodo pueden usarlo), **ROX** solo lectura desde muchos nodos y **RWOP** lectura/escritura por un único Pod.

### [2/Storage/2]
A PV has `persistentVolumeReclaimPolicy: Retain`. What happens when its PVC is deleted?
- [ ] The PV and all of its data are deleted immediately
- [x] The PV is released with its data kept for manual reclaim
- [ ] The PV is automatically bound to the next pending PVC
- [ ] The data is moved into an emptyDir on the same node
> Con `Retain`, al borrar el PVC el PV queda en estado `Released` con los datos intactos, y no se reutiliza hasta que un admin lo limpie. Con `Delete` (lo habitual en el aprovisionamiento dinámico) se borran el PV y el volumen subyacente. `Recycle` está obsoleto.

### [2/Storage/1]
What does CSI stand for in Kubernetes storage?
- [ ] Cluster Storage Interface
- [x] Container Storage Interface
- [ ] Cloud Storage Integration
- [ ] Container Snapshot Index
> El **Container Storage Interface** es un estándar que permite a los proveedores de almacenamiento escribir drivers fuera del código de Kubernetes ("out-of-tree"). Los antiguos plugins de volumen incluidos en el código ("in-tree") se migraron a CSI.

### [2/Storage/3]
A StorageClass uses `volumeBindingMode: WaitForFirstConsumer`. What is the benefit?
- [ ] Volumes are created faster, as soon as the PVC appears
- [x] The volume is created after scheduling, in the Pod's zone
- [ ] A single PVC can be bound to several Pods at once
- [ ] Data is encrypted before the first write reaches disk
> Con `Immediate`, el volumen se crea al crear el PVC, quizá en una zona donde luego el Pod no puede programarse. `WaitForFirstConsumer` retrasa el aprovisionamiento hasta que el scheduler elige nodo, respetando la topología (zona) del Pod.

### [2/Storage/2]
How does a StatefulSet give each replica its own PersistentVolumeClaim?
- [ ] By sharing a single ReadWriteMany PVC across all of its replicas
- [x] Through `volumeClaimTemplates`, which create one PVC per Pod
- [ ] By giving every replica its own `emptyDir` volume
- [ ] By labeling each PersistentVolume with the Pod name
> Los `volumeClaimTemplates` generan un PVC por réplica con nombre estable (por ejemplo `data-db-0`, `data-db-1`). Si `db-1` se reprograma en otro nodo, vuelve a conectarse a su propio PVC. Al escalar hacia abajo, los PVCs se conservan por defecto para no perder datos.

### [2/Storage/2]
Why is mounting a `hostPath` volume generally discouraged for application workloads?
- [ ] hostPath volumes are much slower than emptyDir volumes
- [x] It exposes the node's filesystem and ties data to that node
- [ ] hostPath volumes only work on Windows worker nodes
- [ ] hostPath volumes are wiped automatically every hour
> `hostPath` monta un directorio del nodo en el contenedor: puede dar acceso a archivos sensibles del host (o al socket del runtime) y facilitar escapes; además, los datos quedan atados a ese nodo. Los Pod Security Standards *baseline* y *restricted* lo prohíben. Se reserva para agentes del sistema que de verdad lo necesitan.

### [2/Storage/2]
Which volume type combines several sources (Secret, ConfigMap, downward API, ServiceAccount token) into a single directory?
- [ ] emptyDir
- [ ] hostPath
- [x] projected
- [ ] csi
> Un volumen `projected` agrupa varias fuentes en un mismo punto de montaje. Kubernetes lo usa para inyectar el token del ServiceAccount, el certificado de la CA y el namespace en `/var/run/secrets/kubernetes.io/serviceaccount`.

### [2/Storage/2]
A PVC is `Bound`, and you want to grow it from 10Gi to 20Gi. What is required?
- [ ] Delete the PVC and recreate it with the new size
- [x] A StorageClass that sets `allowVolumeExpansion: true`
- [ ] Editing the capacity field of the bound PV directly
- [ ] Nothing works; volumes can never be resized
> Si la StorageClass lo permite (`allowVolumeExpansion: true`) y el driver CSI soporta expansión, basta con aumentar `spec.resources.requests.storage` del PVC. Reducir el tamaño no está soportado.

### [2/Storage/2]
Which objects let you take point-in-time snapshots of persistent volumes with CSI drivers that support it?
- [ ] PVCBackup and PVCRestore
- [x] VolumeSnapshot and VolumeSnapshotClass
- [ ] StorageClass and StorageProfile
- [ ] PersistentVolumeSnapshotPolicy
> La API de snapshots (VolumeSnapshot, VolumeSnapshotContent y VolumeSnapshotClass) permite crear instantáneas con drivers CSI compatibles y restaurarlas creando un PVC cuyo `dataSource` apunta a la snapshot.

### [2/Storage/2]
A PVC does not set `storageClassName`, and the cluster has several StorageClasses. Which one is used for dynamic provisioning?
- [ ] The StorageClass that was created most recently
- [x] The StorageClass marked as the cluster default
- [ ] The StorageClass whose name sorts first alphabetically
- [ ] None, because a PVC must always name its StorageClass
> Si un PVC no indica `storageClassName`, el admission controller *DefaultStorageClass* le asigna la StorageClass marcada como predeterminada (anotación `storageclass.kubernetes.io/is-default-class: "true"`; `kubectl get storageclass` la muestra con "(default)").
>
> No se elige por fecha ni por orden alfabético, y el campo no es obligatorio. Si no hay ninguna clase por defecto, el PVC solo puede enlazarse a un PV estático compatible.

### [2/Storage/2]
Which CNCF graduated project orchestrates Ceph to provide block, file and object storage inside Kubernetes?
- [ ] Longhorn
- [x] Rook
- [ ] Velero
- [ ] Vitess
> **Rook** es un operador graduado en la CNCF que automatiza el despliegue y la operación de Ceph en Kubernetes. Longhorn (CNCF) es almacenamiento de bloques distribuido, Velero sirve para backups y Vitess es una capa de escalado para MySQL.

### [2/Storage/2]
A Secret is mounted as a volume in a Pod. Where does its content live on the node?
- [ ] On the node's root disk, under `/var/secrets`
- [x] In a memory-backed tmpfs, not on the node's disk
- [ ] Only in etcd, read again on every file access
- [ ] Inside a writable layer of the container image
> Los volúmenes de Secret se montan en tmpfs (RAM) para no persistirlos en el disco del nodo, y el kubelet solo los entrega a nodos que ejecutan Pods que los necesitan. Al borrarse el Pod, se eliminan.

### [2/Storage/2]
What is a generic ephemeral volume?
- [ ] A volume that stores its data inside etcd
- [x] A per-Pod volume backed by a PVC that is deleted with the Pod
- [ ] A hostPath volume that the kubelet wipes after 24 hours
- [ ] A ConfigMap mounted with `ephemeral: true` so it can be edited
> Los volúmenes efímeros genéricos (`ephemeral.volumeClaimTemplate`) crean un PVC dedicado al Pod con cualquier StorageClass; sirven para espacio temporal grande o con características específicas. El Pod es dueño del PVC, así que se elimina con él.

### [2/Storage/2]
Which of these volumes keeps its data after the Pod is deleted?
- [ ] An `emptyDir` volume with `medium: Memory`
- [ ] A generic ephemeral volume with a StorageClass
- [x] A PVC bound to a PV with the `Retain` policy
- [ ] A `downwardAPI` volume exposing Pod labels
> Los datos de un PVC/PV sobreviven al Pod (y con `Retain`, incluso al borrado del PVC). `emptyDir` y los volúmenes efímeros desaparecen con el Pod, y `downwardAPI` solo expone metadatos del Pod.
