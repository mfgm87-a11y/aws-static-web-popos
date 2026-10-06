# KCNA · Dominio 3 · Cloud Native Application Delivery

### [3/Application Delivery/1]
What is GitOps?
- [ ] Storing container images and their layers inside a Git repository
- [x] Using Git as the source of truth for declarative, reconciled state
- [ ] Running highly available Git servers inside a Kubernetes cluster
- [ ] A CI tool that compiles and tests the code on every single commit
> GitOps gestiona infraestructura y aplicaciones declarando el estado deseado en Git (versionado y auditable). Agentes dentro del clúster (Argo CD, Flux) **traen** ese estado y lo reconcilian continuamente. Los cambios se hacen con commits y pull requests, no con `kubectl` manual.

### [3/Application Delivery/2]
Which are the four OpenGitOps principles?
- [ ] Declarative; Versioned and Mutable; Pushed Automatically; Periodically Synced
- [x] Declarative; Versioned and Immutable; Pulled Automatically; Continuously Reconciled
- [ ] Imperative; Versioned and Immutable; Pulled Manually; Continuously Reconciled
- [ ] Declarative; Encrypted and Signed; Pulled Automatically; Manually Approved
> Los principios de OpenGitOps (proyecto de la CNCF) son: el estado deseado es **declarativo**; se guarda **versionado e inmutable**; los agentes lo **obtienen automáticamente (pull)**; y lo **reconcilian continuamente** con el estado real.

### [3/Application Delivery/1]
Which two CNCF graduated projects are the most widely used GitOps tools for Kubernetes?
- [ ] Jenkins and Spinnaker
- [x] Argo CD and Flux
- [ ] Helm and Kustomize
- [ ] Tekton and Buildpacks
> Argo (que incluye Argo CD) y Flux son proyectos graduados de la CNCF que implementan GitOps: observan repositorios Git (o registros OCI/Helm) y sincronizan el clúster con ellos. Helm y Kustomize generan manifiestos; Jenkins y Tekton son herramientas de CI/CD de propósito general.

### [3/Application Delivery/2]
What is a key security advantage of pull-based GitOps compared with a push-based CI pipeline?
- [ ] It removes the need for RBAC inside the cluster
- [x] Cluster credentials never have to leave the cluster
- [ ] It encrypts every container image before it is deployed
- [ ] It forces all Pods to run as non-root automatically
> En el modelo *push*, el pipeline de CI necesita credenciales con permisos amplios sobre el clúster, un objetivo valioso para un atacante. En *pull*, el agente GitOps corre dentro del clúster y solo necesita leer Git, así que las credenciales del clúster nunca salen de él.

### [3/Application Delivery/2]
Someone changes a Deployment directly with `kubectl edit` in a cluster managed by Argo CD with automated self-heal enabled. What happens?
- [ ] Argo CD commits the manual change back to the Git repository
- [x] Argo CD detects the drift and restores the state defined in Git
- [ ] The change is kept, and Git is ignored from that point on
- [ ] Argo CD deletes the Deployment because it was modified by hand
> Al comparar continuamente Git con el clúster, el agente detecta la **deriva (drift)**. Con self-heal activado, vuelve a aplicar lo que dice Git y deshace el cambio manual. Sin self-heal, la aplicación aparece como `OutOfSync` hasta que alguien sincronice.

### [3/Application Delivery/2]
What distinguishes continuous deployment from continuous delivery?
- [ ] It only builds container images and never runs any automated tests
- [x] Every change that passes the pipeline goes to production automatically
- [ ] It requires GitOps, while continuous delivery forbids using it
- [ ] It deploys only once per sprint, after a manual review meeting
> En **entrega continua** cada cambio queda listo para producción, pero el paso final suele requerir aprobación manual. En **despliegue continuo**, todo cambio que pasa las pruebas se despliega automáticamente. Ninguna de las dos exige GitOps, aunque GitOps encaja bien con ambas.

### [3/Application Delivery/2]
Which deployment strategy runs the new version alongside the old one and switches all traffic at once, allowing an instant rollback by switching back?
- [ ] Canary
- [x] Blue/green
- [ ] Recreate
- [ ] Rolling update
> En **blue/green** existen dos entornos completos (azul = actual, verde = nuevo). Se valida el verde y se cambia todo el tráfico de golpe, por ejemplo cambiando el selector del Service; el rollback es volver a apuntar al azul. Requiere el doble de recursos durante el cambio.

### [3/Application Delivery/2]
Which strategy sends a small percentage of real traffic to the new version first, then increases it gradually while metrics are monitored?
- [x] Canary
- [ ] Blue/green
- [ ] Recreate
- [ ] Shadow (dark launch)
> En un **canary**, una pequeña parte del tráfico (p. ej. 5 %) va a la nueva versión; si las métricas son buenas, se aumenta progresivamente. Argo Rollouts o Flagger, junto con un service mesh o un Ingress/Gateway, lo automatizan. En *shadow* se copia tráfico a la nueva versión sin devolver sus respuestas a los usuarios.

### [3/Application Delivery/2]
Which Deployment strategy terminates all old Pods before creating the new ones, causing downtime?
- [ ] RollingUpdate
- [x] Recreate
- [ ] BlueGreen
- [ ] Canary
> Un Deployment ofrece de forma nativa dos estrategias: `RollingUpdate` (por defecto) y `Recreate`. `Recreate` elimina todos los Pods viejos antes de crear los nuevos (útil si dos versiones no pueden convivir), pero causa una interrupción. Blue/green y canary requieren herramientas o configuración adicional.

### [3/Application Delivery/3]
A Deployment with 10 replicas uses `maxSurge: 2` and `maxUnavailable: 0`. What happens during a rolling update?
- [ ] All 10 Pods are replaced at the same moment
- [x] Up to 12 Pods may exist, and available Pods never drop below 10
- [ ] Only 8 Pods remain available while the update runs
- [ ] The update is rejected, because maxUnavailable cannot be 0
> `maxSurge` permite crear Pods extra por encima de las réplicas deseadas (aquí, hasta 12) y `maxUnavailable: 0` exige que nunca haya menos de 10 disponibles. Así se actualiza sin perder capacidad, a cambio de recursos extra temporales. Ambos valores pueden ser números o porcentajes (por defecto 25 %).

### [3/Application Delivery/2]
Which TWO update strategies can you set natively in a Deployment's `spec.strategy.type`? (Choose two.)
- [x] RollingUpdate
- [x] Recreate
- [ ] Canary
- [ ] BlueGreen
- [ ] Shadow
> El Deployment solo admite `RollingUpdate` (por defecto) y `Recreate`. Canary, blue/green o shadow se implementan con herramientas como Argo Rollouts o Flagger, con service mesh, o manipulando Services e Ingress.

### [3/Application Delivery/1]
What is Helm?
- [ ] A network plugin that implements the Kubernetes network model
- [x] A package manager that installs applications from charts
- [ ] A container runtime that implements the CRI
- [ ] A GitOps controller that ships built into Kubernetes
> Helm (graduado en la CNCF) empaqueta aplicaciones en **charts** (plantillas + `values.yaml`). `helm install` crea un *release*, `helm upgrade` lo actualiza y `helm rollback` vuelve a una revisión anterior. Helm 3 ya no usa el componente de servidor Tiller.

### [3/Application Delivery/2]
In Helm, what is the purpose of the `values.yaml` file?
- [ ] It stores the full history of every release of the chart
- [x] It provides default values injected into the chart templates
- [ ] It lists the Kubernetes versions that the chart is tested against
- [ ] It contains the manifests after they were rendered
> Las plantillas del chart (en `templates/`) usan los valores de `values.yaml`, que el usuario puede sobrescribir con `-f mis-valores.yaml` o `--set clave=valor`. `Chart.yaml` contiene los metadatos del chart (nombre, versión, dependencias).

### [3/Application Delivery/2]
Which command rolls back the Helm release `shop` to revision 3?
- [ ] `helm undo shop 3`
- [x] `helm rollback shop 3`
- [ ] `kubectl rollout undo release/shop --to-revision=3`
- [ ] `helm upgrade shop --revision=3`
> Helm guarda el historial de cada release (`helm history shop`) y `helm rollback <release> <revisión>` vuelve a aplicar esa versión. `kubectl rollout undo` trabaja con Deployments, no con releases de Helm.

### [3/Application Delivery/2]
How does Kustomize customize Kubernetes manifests?
- [ ] With its own templating language, similar to Go templates
- [x] By patching plain YAML bases with overlays, without templates
- [ ] By compiling Helm charts into standalone binaries
- [ ] By storing per-environment differences as objects inside etcd
> Kustomize parte de YAML "base" sin plantillas y aplica *overlays* por entorno (parches, prefijos, labels, imágenes). Está integrado en kubectl: `kubectl apply -k <directorio>`. Helm, en cambio, usa plantillas Go.

### [3/Application Delivery/2]
Which statement about Argo CD is correct?
- [ ] It builds container images from the source code on every Git commit
- [x] Its `Application` resource maps a Git or Helm source to a target cluster
- [ ] It only works with Helm charts and cannot apply plain YAML manifests
- [ ] It requires the CI system to push every change into the target cluster
> En Argo CD, cada `Application` define de dónde sale el estado deseado (repo Git, chart Helm, Kustomize, OCI) y dónde se aplica (clúster y namespace). Argo CD muestra si está *Synced* u *OutOfSync* y si está *Healthy*. No construye imágenes: eso es tarea del CI.

### [3/Application Delivery/3]
Which Flux component fetches artifacts from Git repositories, Helm repositories and OCI registries?
- [ ] helm-controller
- [x] source-controller
- [ ] kustomize-controller
- [ ] notification-controller
> Flux está formado por controladores: **source-controller** obtiene artefactos (Git, Helm, OCI, buckets); kustomize-controller y helm-controller los aplican al clúster; notification-controller gestiona alertas y webhooks.

### [3/Application Delivery/2]
You want to keep Kubernetes Secrets in a public Git repository for GitOps. Which approach is appropriate?
- [ ] Commit the base64-encoded Secret manifests, since base64 hides them
- [x] Encrypt them (Sealed Secrets, SOPS) or reference an external store
- [ ] Store the values in a ConfigMap instead of a Secret
- [ ] Add them to `.gitignore` and apply them by hand
> Base64 no protege nada. Con **Sealed Secrets** o **SOPS** el secreto se guarda cifrado en Git y solo el clúster puede descifrarlo; con **External Secrets Operator**, Git solo guarda una referencia y el valor vive en un gestor externo (Vault, AWS Secrets Manager…). Aplicarlos a mano rompe el modelo GitOps.

### [3/Application Delivery/2]
What is the typical order of stages in a CI pipeline for a containerized application?
- [ ] Deploy → build image → test → scan → push to the registry
- [x] Compile → test → build image → scan → push to the registry
- [ ] Build image → push to the registry → compile → test → scan
- [ ] Scan → deploy → compile → build image → test
> Un pipeline de CI típico compila, ejecuta pruebas, construye la imagen, la escanea (vulnerabilidades, secretos) y la publica en el registro, idealmente firmada. Después, el CD (o GitOps) actualiza el manifiesto con la nueva versión y la despliega.

### [3/Application Delivery/2]
Which Kubernetes-native framework defines CI/CD pipelines with custom resources such as `Task` and `Pipeline`?
- [ ] Jenkins
- [x] Tekton
- [ ] Spinnaker
- [ ] Prometheus
> **Tekton** (proyecto de la CD Foundation) define pipelines con CRDs (`Task`, `Pipeline`, `PipelineRun`) que se ejecutan como Pods en el clúster. Jenkins y Spinnaker son herramientas de CI/CD que no nacieron como recursos nativos de Kubernetes.

### [3/Application Delivery/2]
What do feature flags allow teams to do?
- [ ] Mark Pods as experimental so the scheduler treats them differently
- [x] Decouple deploying code from releasing a feature to users
- [ ] Turn on alpha Kubernetes APIs in the control plane
- [ ] Encrypt sensitive configuration values at rest
> Los *feature flags* permiten desplegar código con una funcionalidad desactivada y activarla después (para todos o para un porcentaje de usuarios) sin redeploy. OpenFeature (proyecto de la CNCF) define un estándar para ello. Los *feature gates* de Kubernetes son otra cosa: activan funcionalidades del propio Kubernetes.

### [3/Application Delivery/2]
Which statement about immutable infrastructure is correct?
- [ ] Servers are patched in place with configuration management tools
- [x] Running instances are replaced with new ones instead of being modified
- [ ] Containers can never be updated once they are first released
- [ ] It can only be implemented on dedicated bare-metal servers
> Con infraestructura inmutable no se modifican servidores ni contenedores en ejecución: se construye una nueva imagen o versión y se reemplaza la anterior. Así se evita la deriva de configuración y los despliegues son reproducibles y fáciles de revertir ("cattle, not pets").

### [3/Application Delivery/2]
Which project manages cloud infrastructure (databases, buckets…) through Kubernetes custom resources, so that it is reconciled like any other Kubernetes object?
- [ ] Helm hooks
- [x] Crossplane
- [ ] Kustomize overlays
- [ ] kubeadm
> **Crossplane** (CNCF) extiende Kubernetes con proveedores y CRDs para recursos de nube, y sus controladores los reconcilian continuamente, lo que permite gestionar infraestructura con GitOps. Terraform también es IaC, pero no usa el modelo de reconciliación de Kubernetes.

### [3/Application Delivery/2]
What is progressive delivery?
- [ ] Deploying only on weekends, when there is less traffic
- [x] Gradually exposing changes to more users, guided by metrics
- [ ] Building container images progressively, layer by layer
- [ ] Upgrading Kubernetes one minor version at a time
> La entrega progresiva amplía CI/CD: expone los cambios poco a poco (canary, blue/green, feature flags) y analiza métricas para promover o revertir automáticamente. Argo Rollouts y Flagger son herramientas típicas.

### [3/Application Delivery/2]
Where should environment-specific differences (dev, staging, prod) live in a GitOps workflow?
- [ ] In manual `kubectl patch` commands that run after each Argo CD sync
- [x] In versioned config, such as per-environment overlays or values files
- [ ] In the container image itself, rebuilt for every environment
- [ ] In annotations that operators add by hand to live objects
> En GitOps todo lo que define el estado deseado debe estar en Git: overlays de Kustomize, archivos de valores de Helm por entorno o directorios/repos por entorno. La misma imagen debería promoverse entre entornos; reconstruirla para cada uno rompe la trazabilidad.

### [3/Application Delivery/2]
What does `revisionHistoryLimit` control in a Deployment?
- [ ] How many Pods can be updated at the same time
- [x] How many old ReplicaSets are kept for rollbacks
- [ ] How many times a container is allowed to restart
- [ ] How long a rollout may take before it fails
> `revisionHistoryLimit` (10 por defecto) indica cuántos ReplicaSets antiguos se conservan. Son los que permiten `kubectl rollout undo`; si lo pones en 0, no podrás revertir.

### [3/Application Delivery/1]
What is the main purpose of a Helm chart repository or an OCI registry in Helm workflows?
- [ ] To execute Helm releases on behalf of users
- [x] To store and share packaged, versioned charts
- [ ] To hold the values of Kubernetes Secrets
- [ ] To replace the Kubernetes API server
> Los charts empaquetados (`.tgz`) se publican en repositorios Helm o en registros OCI y se instalan por nombre y versión, por ejemplo `helm install mi-app oci://registro/charts/mi-app --version 1.2.0`. Así se versionan y comparten aplicaciones.

### [3/Application Delivery/2]
A team wants a self-service developer portal with software templates, a service catalog and technical documentation. Which CNCF project is commonly used?
- [ ] Prometheus
- [x] Backstage
- [ ] Envoy
- [ ] etcd
> **Backstage** (CNCF, creado por Spotify) es un framework para construir *Internal Developer Portals*: catálogo de servicios, plantillas para crear proyectos y documentación técnica. Es una pieza común de la ingeniería de plataformas.

### [3/Application Delivery/3]
Which resource does Argo Rollouts add to replace a Deployment when you need advanced canary and blue/green strategies?
- [ ] An annotation on the Ingress object
- [x] A `Rollout` custom resource
- [ ] A PodDisruptionBudget per version
- [ ] A Job with `parallelism` set
> Argo Rollouts añade el CRD `Rollout`, parecido a un Deployment pero con estrategias canary y blue/green, pasos, pausas y análisis automático de métricas (AnalysisTemplates). Flagger ofrece algo similar sobre Deployments normales.

### [3/Application Delivery/2]
What does "shift left" mean in DevOps and DevSecOps?
- [ ] Moving workloads back to on-premises datacenters
- [x] Testing and checking security earlier in the lifecycle
- [ ] Rolling back to the previous version on any error
- [ ] Moving operations work to a separate support team
> "Shift left" significa adelantar pruebas, revisiones de seguridad y calidad a etapas tempranas (código, pull requests, CI), donde corregir es más barato, en lugar de descubrir los problemas en producción.

### [3/Application Delivery/2]
Which statement about platform engineering is most accurate?
- [ ] Every developer manages a personal Kubernetes cluster
- [x] A platform team offers self-service tools and golden paths
- [ ] It replaces CI/CD pipelines with manual deployments
- [ ] It is the Kubernetes SIG responsible for kubectl
> La ingeniería de plataformas crea una *plataforma interna* (portales, plantillas, pipelines, guardarraíles) tratada como producto, para que los equipos de desarrollo desplieguen de forma autónoma y segura sin dominar cada detalle de la infraestructura.

### [3/Debugging/1]
Which command streams the logs of a running Pod in real time?
- [ ] `kubectl logs <pod> --watch-events`
- [x] `kubectl logs -f <pod>`
- [ ] `kubectl get logs <pod> -w`
- [ ] `kubectl describe <pod> --follow`
> `kubectl logs -f` (*follow*) sigue la salida en tiempo real, como `tail -f`. Para un contenedor concreto se añade `-c <contenedor>` y para todos los Pods con una label, `-l app=web`.

### [3/Debugging/2]
A Pod has two containers, `app` and `proxy`. How do you view the logs of `proxy`?
- [x] `kubectl logs <pod> -c proxy`
- [ ] `kubectl logs proxy --pod=<pod>`
- [ ] `kubectl logs <pod>/proxy --all`
- [ ] `kubectl exec <pod> -- logs proxy`
> Si un Pod tiene varios contenedores hay que indicar cuál con `-c` (o usar `--all-containers=true`). Sin `-c`, kubectl usa el contenedor por defecto (anotación `kubectl.kubernetes.io/default-container`) o pide elegir.

### [3/Debugging/1]
How do you open an interactive shell inside a running container?
- [ ] `kubectl attach <pod> --shell`
- [x] `kubectl exec -it <pod> -- sh`
- [ ] `kubectl run <pod> -- sh`
- [ ] `kubectl ssh <pod>`
> `kubectl exec -it <pod> -- <comando>` ejecuta un proceso dentro de un contenedor existente; con `-it` obtienes una sesión interactiva. La imagen debe incluir ese shell. `kubectl attach` se conecta al proceso principal y `kubectl ssh` no existe.

### [3/Debugging/2]
You need to debug a running Pod whose image is distroless and has no shell. What is the recommended approach?
- [ ] Rebuild the image with bash included and redeploy it
- [x] Add an ephemeral debug container with `kubectl debug`
- [ ] Run `kubectl exec` with the `--force-shell` flag
- [ ] SSH into the node and edit the container's filesystem
> Los **ephemeral containers** se añaden a un Pod en ejecución sin reiniciarlo: `kubectl debug -it <pod> --image=busybox --target=<contenedor>`. Con `--target` comparten el espacio de procesos del contenedor objetivo. Son ideales para imágenes mínimas sin herramientas.

### [3/Debugging/2]
How can you reach port 80 of a Service from your laptop for quick testing, without exposing it externally?
- [ ] Change the Service to type LoadBalancer and open its external IP
- [x] Run `kubectl port-forward svc/web 8080:80` and open `localhost:8080`
- [ ] Run `kubectl expose svc web --local --port=8080` on your laptop
- [ ] Add a NodePort and open the firewall to your IP
> `kubectl port-forward` crea un túnel desde tu máquina (a través del API server y del kubelet) hacia un Pod o Service. Es temporal y no expone nada públicamente, ideal para depurar.

### [3/Debugging/2]
How can you troubleshoot a node using `kubectl`, without SSH access?
- [ ] `kubectl exec node/<node> -- bash`
- [x] `kubectl debug node/<node> -it --image=busybox`
- [ ] `kubectl logs node/<node> --shell`
- [ ] `kubectl describe node <node> --interactive`
> `kubectl debug node/...` crea un Pod en ese nodo que comparte sus namespaces (red, PID, IPC) y monta el sistema de archivos del host en `/host`, útil para revisar logs o configuración. Requiere permisos elevados, así que su uso debe estar controlado.

### [3/Debugging/3]
You want to test a fix without touching a broken production Pod. What does `kubectl debug <pod> -it --copy-to=web-debug --container=app -- sh` do?
- [ ] It replaces the original Pod in place with a debugging image
- [x] It creates a separate copy of the Pod, leaving the original untouched
- [ ] It copies the files of the Pod's `app` container to your laptop
- [ ] It live-migrates the running Pod to another node for debugging
> `--copy-to` crea un Pod nuevo basado en el original, en el que puedes cambiar la imagen o el comando (por ejemplo, arrancar un shell en lugar de la app que falla). El Pod original no cambia. Para copiar archivos se usa `kubectl cp`.

### [3/Debugging/2]
Which command copies a file from a container to your local machine?
- [ ] `kubectl get file <pod>:/tmp/dump.txt`
- [x] `kubectl cp <pod>:/tmp/dump.txt ./dump.txt`
- [ ] `kubectl exec <pod> -- download /tmp/dump.txt`
- [ ] `kubectl logs <pod> --file /tmp/dump.txt`
> `kubectl cp` copia archivos entre tu máquina y un contenedor (internamente usa `tar` dentro del contenedor, así que la imagen debe incluirlo).

### [3/Debugging/2]
Which command starts a temporary Pod to test DNS resolution and deletes it when you exit?
- [x] `kubectl run tmp --rm -it --image=busybox -- nslookup kubernetes.default`
- [ ] `kubectl exec dns-test --rm -it -- nslookup kubernetes.default`
- [ ] `kubectl create job dns --image=busybox --rm --interactive -- nslookup`
- [ ] `kubectl debug svc/kubernetes --dns-check --image=busybox`
> `kubectl run ... --rm -it` crea un Pod interactivo que se elimina al salir: perfecto para pruebas puntuales de DNS o conectividad (`nslookup`, `wget`, `curl`) desde dentro del clúster.

### [3/Debugging/2]
How can you see why a container was last restarted, including its exit code and reason?
- [ ] `kubectl logs <pod> --exit-code --last-state`
- [x] `kubectl describe pod <pod>`, under Last State
- [ ] `kubectl rollout status pod/<pod>`
- [ ] `kubectl top pod <pod> --restarts`
> El estado de cada contenedor incluye `lastState.terminated` con `exitCode`, `reason` (OOMKilled, Error, Completed…) y fechas. `kubectl describe pod` lo muestra como *Last State*; también se ve en `kubectl get pod -o yaml` bajo `status.containerStatuses`.

### [3/Debugging/2]
A user reports intermittent slowness on a request that crosses five microservices. Which observability signal helps most to find the service that adds the latency?
- [ ] Node-level CPU metrics
- [x] Distributed traces
- [ ] Logs of the first service only
- [ ] Kubernetes events
> Una traza distribuida sigue una petición a través de todos los servicios, con *spans* que miden cuánto tardó cada salto. Es la señal ideal para encontrar cuellos de botella en microservicios. Jaeger y OpenTelemetry son herramientas habituales.

### [3/Debugging/2]
Which command shows the current CPU and memory consumption of Pods?
- [ ] `kubectl describe pods --usage`
- [x] `kubectl top pods`
- [ ] `kubectl get pods -o metrics`
- [ ] `kubectl logs --metrics`
> `kubectl top pods` (y `kubectl top nodes`) muestra el consumo actual usando la Metrics API, normalmente provista por metrics-server. Es útil para detectar Pods cerca de sus limits.

### [3/Debugging/2]
`kubectl apply` fails with `error validating "app.yaml": ... unknown field "replica"`. What is the most likely issue?
- [ ] The cluster does not have enough resources
- [x] A field name has a typo; it should be `replicas`
- [ ] RBAC denies creating Deployments here
- [ ] The container image does not exist
> El API server (y kubectl) validan el esquema: un campo desconocido como `replica` indica una errata. `kubectl explain deployment.spec` ayuda a ver los nombres correctos. RBAC daría un error *Forbidden*, y una imagen inexistente fallaría más tarde, al crear los Pods.

### [3/Debugging/2]
How can you follow the progress of a Deployment rollout until it completes or fails?
- [ ] `kubectl get deployment web --progress`
- [x] `kubectl rollout status deployment/web`
- [ ] `kubectl logs deployment/web --rollout`
- [ ] `kubectl describe rollout web --wait`
> `kubectl rollout status` espera y muestra el progreso del rollout (réplicas actualizadas y disponibles) y termina con éxito o con error (por ejemplo, si se supera `progressDeadlineSeconds`). Se usa mucho en pipelines de CD.

### [3/Debugging/2]
Your app answers when you run `curl` inside its own Pod, but not when another Pod calls it through the Service. Which check isolates the problem quickly?
- [ ] Reinstall the CNI plugin on every node and restart all kubelets
- [x] Check the Service endpoints and that `targetPort` matches the app port
- [ ] Scale the Deployment up so that more replicas can answer requests
- [ ] Delete and recreate the namespace where the app runs
> Si la app responde dentro del Pod pero no a través del Service, revisa la cadena Service → EndpointSlices → puerto: ¿hay endpoints?, ¿coincide el `targetPort` con el puerto real?, ¿la app escucha en `0.0.0.0` y no solo en `127.0.0.1`? Después revisa las NetworkPolicies.

### [3/Debugging/3]
An application in a Pod listens only on `127.0.0.1:8080`. What happens when other Pods call it through its Service?
- [ ] It works, because Services translate traffic to localhost
- [x] Connections fail, because the app does not listen on the Pod IP
- [ ] It works only if `externalTrafficPolicy: Local` is set
- [ ] Kubernetes rewrites the bind address of the app automatically
> El tráfico del Service llega a la IP del Pod. Si la app solo escucha en loopback, solo es accesible desde dentro del propio Pod (`localhost`). Debe escuchar en `0.0.0.0` o en la IP del Pod; es un error clásico al contenerizar aplicaciones.

### [3/Debugging/2]
How do you get the logs of every Pod with the label `app=web` at once?
- [x] `kubectl logs -l app=web`
- [ ] `kubectl logs deployment --all web`
- [ ] `kubectl logs pods/app=web`
- [ ] `kubectl get logs --selector web`
> `kubectl logs -l <selector>` combina los logs de los Pods que coinciden. Añade `--prefix` para ver de qué Pod viene cada línea y `-f` para seguirlos en tiempo real.

### [3/Debugging/2]
After a `helm upgrade`, the application is broken. Which commands help you inspect the release and revert it?
- [ ] `kubectl rollout history` and `kubectl rollout undo` on the chart
- [x] `helm history <release>` and `helm rollback <release> <revision>`
- [ ] `helm lint` and `helm package` on the chart directory
- [ ] `helm repo update` and `helm search repo` for the chart
> `helm history` muestra las revisiones del release con su estado y `helm rollback` vuelve a una revisión anterior. `helm lint`/`package` sirven al crear charts, y `repo update`/`search` para buscarlos.
