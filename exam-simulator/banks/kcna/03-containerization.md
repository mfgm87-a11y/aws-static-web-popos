# KCNA · Dominio 1 · Kubernetes Fundamentals · Containerization

### [1/Containerization/1]
What is the main difference between containers and virtual machines?
- [ ] Containers include a full guest operating system and kernel
- [x] Containers share the host kernel; each VM runs its own kernel
- [ ] Virtual machines usually start faster than containers do
- [ ] Containers only run on Linux hosts that have Docker installed
> Los contenedores son procesos aislados que comparten el kernel del host (aislamiento con namespaces y cgroups), por eso son ligeros y arrancan muy rápido. Las VMs virtualizan hardware y cada una tiene su propio kernel y sistema operativo: más aislamiento, pero más sobrecarga.

### [1/Containerization/2]
Which Linux kernel features provide the isolation and resource limits that containers rely on?
- [ ] SELinux and AppArmor
- [x] Namespaces and cgroups
- [ ] iptables and conntrack
- [ ] systemd and journald
> Los **namespaces** aíslan lo que un proceso ve (PIDs, red, montajes, hostname, IPC, usuarios) y los **cgroups** limitan y contabilizan recursos (CPU, memoria, PIDs). SELinux y AppArmor añaden control de acceso obligatorio, pero no son la base del aislamiento.

### [1/Containerization/2]
What is a container image made of?
- [ ] A single compressed virtual disk that includes a kernel
- [x] Read-only layers plus a manifest and runtime configuration
- [ ] A snapshot of a running process, including its memory
- [ ] The Dockerfile together with its whole build context
> Una imagen OCI es un conjunto de **capas** de sistema de archivos de solo lectura, más un *manifest* y una configuración (entrypoint, variables, usuario…). Al arrancar un contenedor se añade una capa escribible encima (copy-on-write). La imagen no incluye kernel ni memoria de procesos.

### [1/Containerization/2]
Why do multi-stage Dockerfile builds produce smaller and safer images?
- [ ] They compress every layer with a stronger algorithm
- [x] The final stage keeps only the build output, not the build tools
- [ ] They build each stage on a different node in parallel to save time
- [ ] They remove the need for any base image at all
> En un build multi-etapa compilas en una etapa con todas las herramientas y copias solo el binario o artefacto a una imagen final mínima (por ejemplo, distroless). Menos paquetes significa una imagen más pequeña y menos superficie de ataque.

### [1/Containerization/2]
In a Dockerfile, what is the difference between `ENTRYPOINT` and `CMD`?
- [ ] `CMD` runs at build time, while `ENTRYPOINT` runs at container start
- [x] `ENTRYPOINT` sets the executable; `CMD` gives default, overridable arguments
- [ ] They are identical, and whichever appears last in the file wins
- [ ] `ENTRYPOINT` is only honored by Windows container runtimes
> `ENTRYPOINT` fija el ejecutable principal y `CMD` aporta argumentos por defecto (o el comando completo si no hay ENTRYPOINT). En Kubernetes, `command` reemplaza al ENTRYPOINT y `args` al CMD. Lo que se ejecuta en tiempo de build es `RUN`.

### [1/Containerization/3]
A Pod spec sets `args: ["--port", "9090"]` and no `command`. The image has `ENTRYPOINT ["/app"]` and `CMD ["--port", "8080"]`. What runs?
- [ ] `/app --port 8080`
- [x] `/app --port 9090`
- [ ] `--port 9090` (the ENTRYPOINT is dropped)
- [ ] `/app --port 8080 --port 9090`
> En Kubernetes `args` reemplaza al `CMD` de la imagen y `command` reemplaza al `ENTRYPOINT`. Como solo se definió `args`, se conserva el ENTRYPOINT `/app` con los nuevos argumentos: `/app --port 9090`.

### [1/Containerization/2]
Why is referencing an image by digest (`nginx@sha256:...`) safer than by tag (`nginx:1.27`)?
- [ ] Images referenced by digest download noticeably faster
- [x] A digest pins immutable content, while a tag can be moved
- [ ] Tags are not supported by containerd or by CRI-O
- [ ] Digests embed the results of the vulnerability scan
> Un tag es un puntero mutable: alguien puede volver a publicar `nginx:1.27` con otro contenido. El digest es el hash del contenido: siempre la misma imagen, byte a byte. Por eso se recomienda usar digests en producción y en cadenas de suministro seguras.

### [1/Containerization/2]
A container specifies `image: myapp` with no tag and no `imagePullPolicy`. Which pull policy does Kubernetes apply?
- [ ] IfNotPresent
- [x] Always
- [ ] Never
- [ ] OnFailure
> Si se omite el tag (o se usa `:latest`), Kubernetes asume `imagePullPolicy: Always`. Con cualquier otro tag, la política por defecto es `IfNotPresent`. `OnFailure` es un valor de `restartPolicy`, no de pull policy.

### [1/Containerization/1]
Which organization defines the open standards for container image format, runtime and distribution?
- [ ] The CNCF Technical Oversight Committee
- [x] The Open Container Initiative (OCI)
- [ ] Docker, Inc.
- [ ] Kubernetes SIG Node
> La **OCI** (bajo la Linux Foundation) define tres especificaciones: *runtime-spec* (cómo ejecutar un contenedor), *image-spec* (formato de imagen) y *distribution-spec* (API de registros). Gracias a ellas, una imagen creada con Docker, Buildah o BuildKit corre en containerd o CRI-O.

### [1/Containerization/2]
What does the Container Runtime Interface (CRI) define?
- [ ] The image format that registries must store and serve
- [x] The gRPC API the kubelet uses to talk to container runtimes
- [ ] How Pods receive IP addresses on each node
- [ ] How storage volumes are attached to nodes
> El CRI es la interfaz gRPC entre el kubelet y el runtime, lo que permite usar containerd, CRI-O u otros sin cambiar el kubelet. Las IPs las gestiona el CNI y los volúmenes el CSI; el formato de imagen lo define la OCI.

### [1/Containerization/2]
Kubernetes 1.24 removed dockershim. What happens to images built with `docker build`?
- [ ] They no longer run on Kubernetes clusters at all
- [x] They still run, because they are standard OCI images
- [ ] They must be converted with a special tool first
- [ ] They can now only run on Windows worker nodes
> Se eliminó el *dockershim* (el adaptador para usar Docker Engine como runtime), no la compatibilidad con las imágenes. Docker genera imágenes OCI estándar que cualquier runtime CRI ejecuta. Quien necesite Docker Engine como runtime puede usar el adaptador externo cri-dockerd.

### [1/Containerization/2]
Which of the following is a low-level OCI runtime rather than a high-level CRI runtime?
- [ ] containerd
- [ ] CRI-O
- [x] runc
- [ ] Docker Engine
> Los runtimes de alto nivel (containerd, CRI-O) gestionan imágenes, snapshots y la API CRI, y delegan la creación real del contenedor en un runtime OCI de bajo nivel como **runc** o crun (o en alternativas con más aislamiento, como gVisor `runsc` o Kata Containers).

### [1/Containerization/2]
Which TWO of the following are CRI-compatible container runtimes that the kubelet can use directly? (Choose two.)
- [x] containerd
- [x] CRI-O
- [ ] runc
- [ ] Docker Engine without an adapter
- [ ] Podman
> **containerd** y **CRI-O** implementan el CRI y son los runtimes más usados en Kubernetes. runc es un runtime OCI de bajo nivel que ellos invocan; Docker Engine necesita el adaptador cri-dockerd, y Podman es una herramienta para ejecutar contenedores fuera de Kubernetes.

### [1/Containerization/2]
How does a Pod pull an image from a private registry that requires authentication?
- [ ] By passing the registry password as an environment variable
- [x] By listing a `dockerconfigjson` Secret in `imagePullSecrets`
- [ ] By annotating the Pod with the registry URL and username
- [ ] It cannot; Kubernetes only pulls from public registries
> Se crea un Secret de tipo `kubernetes.io/dockerconfigjson` (por ejemplo con `kubectl create secret docker-registry`) y se referencia en `spec.imagePullSecrets` del Pod, o se asocia al ServiceAccount para que lo usen todos sus Pods. El kubelet usa esas credenciales al descargar la imagen.

### [1/Containerization/1]
In the image reference `registry.example.com/team/api:2.4.1`, what is `2.4.1`?
- [ ] The registry port
- [ ] The repository name
- [x] The tag
- [ ] The image digest
> El formato es `[registro/]repositorio[:tag][@digest]`. Aquí `registry.example.com` es el registro, `team/api` el repositorio y `2.4.1` el tag. Si no se indica registro, se asume Docker Hub (`docker.io`).

### [1/Containerization/2]
Why are minimal base images such as distroless or scratch recommended?
- [ ] They ship extra debugging tools for production incidents
- [x] They shrink the attack surface by leaving out shells and tools
- [ ] containerd refuses to run images built on larger bases
- [ ] They make the containers run as the root user by default
> Menos software en la imagen significa menos vulnerabilidades (CVEs) y menos herramientas para un atacante: sin shell ni gestor de paquetes. El costo es que depurar es más difícil; para eso existen los *ephemeral containers* (`kubectl debug`).

### [1/Containerization/2]
What happens to files written to a container's writable layer when the container restarts?
- [ ] They are saved into the image for the next start
- [x] They are lost; persistent data belongs in volumes
- [ ] They are copied into etcd by the kubelet
- [ ] They are moved to the node's `/tmp` directory
> El sistema de archivos del contenedor es efímero: al reiniciarse, el contenedor empieza de nuevo desde la imagen. Para conservar datos se usan volúmenes: un `emptyDir` sobrevive a reinicios del contenedor dentro del mismo Pod, y un PersistentVolume sobrevive al Pod.

### [1/Containerization/2]
Which statement about Cloud Native Buildpacks is correct?
- [ ] They are Kubernetes Operators that package Helm charts
- [x] They turn source code into OCI images without a Dockerfile
- [ ] They are a replacement for container registries
- [ ] They are a type of Kubernetes volume plugin
> Cloud Native Buildpacks (proyecto de la CNCF) detectan el lenguaje del código fuente y construyen una imagen OCI con buenas prácticas, sin necesidad de Dockerfile, y permiten actualizar la imagen base ("rebase") rápidamente para aplicar parches.

### [1/Containerization/2]
Which Kubernetes object lets a Pod select a different container runtime handler, for example a sandboxed runtime such as gVisor or Kata Containers?
- [ ] PriorityClass
- [x] RuntimeClass
- [ ] StorageClass
- [ ] IngressClass
> Un **RuntimeClass** asocia un nombre a un *handler* configurado en el runtime del nodo (por ejemplo `runsc` de gVisor o Kata). El Pod lo elige con `spec.runtimeClassName`. Es la forma de dar más aislamiento a cargas no confiables.

### [1/Containerization/2]
A container terminated with exit code 137. What does that usually indicate?
- [ ] The application exited successfully after finishing its work
- [x] It was killed with SIGKILL, often for exceeding its memory limit
- [ ] The container image could not be pulled from the registry
- [ ] A mounted configuration file was missing at startup
> 137 = 128 + 9 (SIGKILL). Suele aparecer con `OOMKilled` cuando el contenedor supera su límite de memoria, o cuando no termina a tiempo tras el periodo de gracia. 143 = 128 + 15 (SIGTERM, terminación ordenada) y 1 suele ser un error de la aplicación.

### [1/Containerization/1]
Which file tells the image build which local files to exclude from the build context?
- [ ] `.gitignore`
- [x] `.dockerignore`
- [ ] `Dockerfile.exclude`
- [ ] `.buildignore`
> `.dockerignore` excluye archivos del contexto de build (secretos, `node_modules`, `.git`…), lo que acelera el build y evita que información sensible termine en la imagen. Buildah/Podman también aceptan `.containerignore`.

### [1/Containerization/2]
Why should you avoid putting secrets, such as API keys, in a Dockerfile `ENV` or `COPY` instruction?
- [ ] Because secrets make the image layers much larger
- [x] Because they remain in image layers that anyone can inspect
- [ ] Because Kubernetes rejects images with environment variables
- [ ] Because containerd re-encrypts them with a random key
> Todo lo que se copia o define en una capa queda en la imagen (aunque una capa posterior lo borre) y se puede inspeccionar con `docker history` o extrayendo las capas. Los secretos deben inyectarse en tiempo de ejecución (Secrets de Kubernetes o gestores externos) y, durante el build, con mecanismos de *build secrets*.

### [1/Containerization/1]
What does a container registry do?
- [ ] It runs containers on behalf of the kubelet
- [x] It stores and distributes container images
- [ ] It schedules container images onto nodes
- [ ] It builds images from source code on every commit
> Un registro (Docker Hub, Harbor, GHCR, ECR…) almacena repositorios de imágenes y las sirve mediante la *OCI distribution spec*. Harbor es un registro graduado en la CNCF con RBAC, escaneo de vulnerabilidades, firma y replicación.

### [1/Containerization/2]
Which statement about container images and CPU architectures is correct?
- [ ] A single image binary always runs on every CPU architecture
- [x] A multi-arch image index lets each node pull its own variant
- [ ] Kubernetes translates x86 binaries to ARM at runtime
- [ ] The architecture is chosen with the `imagePullPolicy` field
> Una imagen multi-arquitectura es un *image index* (manifest list) que apunta a variantes por plataforma (amd64, arm64…), y el runtime descarga la que corresponde al nodo. Si la imagen solo existe para otra arquitectura, el contenedor falla, típicamente con `exec format error`.
