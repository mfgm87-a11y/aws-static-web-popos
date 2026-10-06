# KCNA · Dominio 4 · Cloud Native Architecture

### [4/Observability/1]
Which are commonly called the three pillars of observability?
- [ ] CPU, memory and disk
- [x] Metrics, logs and traces
- [ ] Alerts, dashboards and reports
- [ ] Pods, Services and Ingresses
> Las tres señales clásicas son las **métricas** (valores numéricos en el tiempo), los **logs** (eventos con texto) y las **trazas** (el recorrido de una petición entre servicios). OpenTelemetry añade los *profiles* como señal emergente.

### [4/Observability/2]
How does Prometheus usually collect metrics from applications?
- [ ] Applications push their metrics to Prometheus over SMTP
- [x] It periodically pulls (scrapes) an HTTP endpoint such as `/metrics`
- [ ] It reads metrics directly from etcd with a client certificate
- [ ] The kubelet forwards every metric to it through a webhook
> Prometheus usa un modelo **pull**: descubre objetivos (por ejemplo con el service discovery de Kubernetes) y raspa periódicamente sus endpoints HTTP en formato de texto. Para trabajos efímeros que no viven lo suficiente para ser raspados existe el **Pushgateway**.

### [4/Observability/2]
A short-lived batch job finishes before Prometheus can scrape it. Which component is designed for this case?
- [ ] Alertmanager
- [x] Pushgateway
- [ ] node-exporter
- [ ] Grafana
> El **Pushgateway** recibe las métricas que le empujan los trabajos efímeros y las conserva para que Prometheus las raspe después. Alertmanager gestiona alertas, node-exporter expone métricas del nodo y Grafana visualiza.

### [4/Observability/2]
Which Prometheus metric type only goes up (or resets to zero on restart), such as the total number of HTTP requests?
- [ ] Gauge
- [x] Counter
- [ ] Histogram
- [ ] Summary
> Un **counter** solo aumenta (vuelve a cero si el proceso se reinicia) y se analiza con funciones como `rate()`. Un **gauge** sube y baja (memoria en uso, temperatura). **Histogram** y **summary** describen distribuciones, como las latencias.

### [4/Observability/2]
Which TWO of the following are Prometheus metric types? (Choose two.)
- [x] Gauge
- [x] Counter
- [ ] Span
- [ ] Event
- [ ] Trace
> Los tipos de métrica de Prometheus son **counter**, **gauge**, **histogram** y **summary**. *Span* y *trace* son conceptos de trazado distribuido, y los *events* son otra señal (Kubernetes los usa para notificar lo que ocurre con los objetos).

### [4/Observability/2]
What does Alertmanager do in the Prometheus ecosystem?
- [ ] It scrapes metrics from every target found by service discovery
- [x] It deduplicates, groups and routes alerts to receivers
- [ ] It stores metrics for years in object storage
- [ ] It draws dashboards from PromQL queries
> Prometheus evalúa las reglas de alerta y envía las alertas a **Alertmanager**, que las agrupa, deduplica, silencia o inhibe y las enruta al canal adecuado (correo, Slack, PagerDuty…). El almacenamiento a largo plazo suele resolverse con Thanos o Cortex, y los dashboards con Grafana.

### [4/Observability/1]
Which query language does Prometheus use?
- [ ] SQL
- [x] PromQL
- [ ] LogQL
- [ ] GraphQL
> **PromQL** es el lenguaje de consultas de Prometheus, por ejemplo `rate(http_requests_total[5m])`. LogQL es el de Loki (logs), SQL el de las bases de datos relacionales y GraphQL un lenguaje para APIs.

### [4/Observability/2]
What is OpenTelemetry?
- [ ] A fork of Prometheus that only stores distributed traces
- [x] A vendor-neutral standard and toolkit for telemetry data
- [ ] A commercial APM product sold by a single cloud vendor
- [ ] A container logging driver built into the kubelet
> **OpenTelemetry** (CNCF) estandariza cómo instrumentar aplicaciones y exportar telemetría (trazas, métricas, logs) a cualquier backend, sin depender de un proveedor. Ofrece APIs, SDKs y el **Collector**, que recibe, procesa y exporta datos.

### [4/Observability/2]
Which two projects merged to form OpenTelemetry?
- [ ] Prometheus and Thanos
- [x] OpenTracing and OpenCensus
- [ ] Jaeger and Zipkin
- [ ] Fluentd and Fluent Bit
> OpenTelemetry nació en 2019 de la fusión de **OpenTracing** (CNCF) y **OpenCensus** (Google) para tener un único estándar. OpenTracing fue archivado después.

### [4/Observability/2]
In Kubernetes, where should a containerized application write its logs so that standard node-level agents can collect them?
- [ ] To a file inside the container image
- [x] To standard output and standard error
- [ ] Directly into etcd through the API
- [ ] To the Kubernetes event stream
> El runtime captura stdout y stderr de cada contenedor y los guarda en archivos del nodo (los que lee `kubectl logs`). Agentes como Fluent Bit o Fluentd, desplegados como DaemonSet, recogen esos archivos y los envían a un backend (Elasticsearch, Loki…).

### [4/Observability/2]
Which CNCF graduated projects are mainly used to collect and forward logs?
- [ ] Jaeger and Zipkin
- [x] Fluentd and Fluent Bit
- [ ] Envoy and Linkerd
- [ ] etcd and TiKV
> **Fluentd** es un proyecto graduado de la CNCF y **Fluent Bit** es su subproyecto ligero, bajo el mismo paraguas. Ambos recogen, procesan y enrutan logs; Fluent Bit es ideal como DaemonSet por su bajo consumo. Jaeger es trazado; Envoy y Linkerd son proxy y service mesh; etcd y TiKV son almacenes clave-valor.

### [4/Observability/2]
Which CNCF graduated project is a distributed tracing platform?
- [ ] Prometheus
- [x] Jaeger
- [ ] Fluentd
- [ ] Harbor
> **Jaeger** (graduado en la CNCF, creado en Uber) almacena y visualiza trazas distribuidas. Su versión 2 está construida sobre el OpenTelemetry Collector.

### [4/Observability/2]
What is the relationship between SLI, SLO and SLA?
- [ ] They are three different names for the same latency metric
- [x] SLI is the measured indicator, SLO its target, SLA the contract
- [ ] SLA is a Prometheus metric; SLI and SLO are legal contracts
- [ ] SLO applies to batch jobs; SLI and SLA apply to Services
> El **SLI** es lo que mides (p. ej. % de peticiones exitosas). El **SLO** es el objetivo interno (99,9 % en 30 días). El **SLA** es un compromiso con clientes que tiene consecuencias (compensaciones), normalmente menos exigente que el SLO. La diferencia entre el 100 % y el SLO es el *error budget*.

### [4/Observability/2]
What is an error budget in SRE practice?
- [ ] The money set aside to fix bugs after a release
- [x] The unreliability allowed by an SLO, e.g. 0.1% for 99.9%
- [ ] The maximum number of Pods that may fail at the same time
- [ ] A Prometheus metric that counts HTTP 5xx errors
> Si el SLO es 99,9 %, se tolera un 0,1 % de fallos: ese es el *error budget*. Mientras quede presupuesto se pueden desplegar cambios con más riesgo; si se agota, se prioriza la estabilidad. Sirve para equilibrar velocidad y confiabilidad.

### [4/Observability/2]
What is the difference between metrics-server and kube-state-metrics?
- [ ] They are the same component, renamed in recent Kubernetes versions
- [x] metrics-server gives live resource usage; kube-state-metrics exports object state
- [ ] metrics-server stores long-term history; kube-state-metrics only sends alerts
- [ ] kube-state-metrics feeds the HPA, while metrics-server feeds dashboards
> **metrics-server** recoge el uso actual de CPU y memoria de los kubelets y lo sirve en la Metrics API (para el HPA y `kubectl top`), sin guardar historial. **kube-state-metrics** convierte el estado de los objetos (réplicas deseadas vs disponibles, fases de Pods…) en métricas para Prometheus.

### [4/Observability/2]
Which practice is part of cloud cost management (FinOps) in Kubernetes?
- [ ] Removing all resource requests so that Pods cost less
- [x] Right-sizing requests and attributing costs, e.g. with OpenCost
- [ ] Running every workload on the largest available node type
- [ ] Disabling autoscaling so that the monthly bill is predictable
> FinOps busca visibilidad y optimización del gasto: ajustar requests al uso real, usar autoscaling, aprovechar instancias spot para cargas tolerantes a fallos y asignar costos por namespace o equipo con herramientas como **OpenCost** (CNCF). Quitar los requests empeora el scheduling y la estabilidad.

### [4/Observability/2]
Which are the "four golden signals" for monitoring a user-facing service?
- [ ] CPU, memory, disk and network
- [x] Latency, traffic, errors and saturation
- [ ] Logs, metrics, traces and events
- [ ] Availability, durability, consistency and partition tolerance
> Los cuatro *golden signals* del libro de SRE de Google son **latencia**, **tráfico**, **errores** y **saturación**. Los métodos RED (Rate, Errors, Duration) y USE (Utilization, Saturation, Errors) son variantes populares.

### [4/Ecosystem & Principles/1]
According to the CNCF definition, which of the following exemplify the cloud native approach?
- [ ] Monoliths, pet servers, manual deployments, mutable infrastructure, imperative scripts
- [x] Containers, microservices, service meshes, immutable infrastructure, declarative APIs
- [ ] Mainframes, nightly batch jobs, fixed capacity planning and change boards
- [ ] Hand-configured VMs, SSH sessions, snowflake servers and manual scaling
> La definición de la CNCF dice que las tecnologías cloud native permiten construir y ejecutar aplicaciones escalables en entornos modernos y dinámicos (nubes públicas, privadas e híbridas), y que contenedores, service meshes, microservicios, infraestructura inmutable y APIs declarativas ejemplifican el enfoque, con sistemas resilientes, gestionables y observables.

### [4/Ecosystem & Principles/2]
Which is a typical trade-off when moving from a monolith to microservices?
- [ ] Deployments become slower and much less frequent
- [x] Independent deploys and scaling, but more distributed complexity
- [ ] Every service must be written in the same programming language
- [ ] Isolating failures between components becomes impossible
> Los microservicios permiten desplegar, escalar y evolucionar cada parte por separado (incluso en distintos lenguajes) y aíslan fallos. A cambio hay más llamadas por red, latencia, datos distribuidos y necesidad de buena observabilidad y automatización.

### [4/Ecosystem & Principles/1]
What is a defining characteristic of serverless (Functions as a Service) platforms?
- [ ] Developers must patch the operating systems of the servers
- [x] The platform scales code on demand, often down to zero
- [ ] Applications always run at a fixed capacity, all day long
- [ ] Functions can only be written in JavaScript
> En serverless el desarrollador entrega código o un contenedor y la plataforma se encarga de los servidores, del escalado (incluso a cero) y del cobro por uso. "Serverless" no significa que no haya servidores, sino que no los gestionas tú. Knative u OpenFaaS llevan este modelo a Kubernetes.

### [4/Ecosystem & Principles/2]
Which CNCF project adds serverless capabilities to Kubernetes, including request-driven autoscaling to zero and eventing?
- [ ] Flux
- [x] Knative
- [ ] Rook
- [ ] CoreDNS
> **Knative** tiene dos partes: *Serving* (servicios HTTP con revisiones, división de tráfico y escalado a cero según peticiones) y *Eventing* (enrutamiento de eventos basado en CloudEvents).

### [4/Ecosystem & Principles/2]
What is CloudEvents?
- [ ] A managed event bus offered by a single cloud provider
- [x] A CNCF specification for describing event data consistently
- [ ] A Kubernetes resource type that stores the cluster's events
- [ ] The logging format used internally by Fluentd
> **CloudEvents** (graduado en la CNCF) define atributos estándar (`id`, `source`, `type`, `time`…) para describir eventos, de modo que productores y consumidores interoperen entre plataformas. Knative Eventing y muchos servicios de nube lo usan.

### [4/Ecosystem & Principles/2]
Which set lists open interfaces that let Kubernetes plug in different implementations for runtimes, networking and storage?
- [ ] HTTP, SMTP and FTP
- [x] CRI, CNI and CSI
- [ ] YAML, JSON and TOML
- [ ] RBAC, ABAC and Node
> Kubernetes desacopla sus dependencias con interfaces abiertas: **CRI** (runtimes de contenedores), **CNI** (red de Pods) y **CSI** (almacenamiento). Gracias a ellas puedes cambiar containerd por CRI-O, Calico por Cilium o un driver de disco por otro sin modificar Kubernetes.

### [4/Ecosystem & Principles/2]
Why are open standards such as OCI, CNI and CSI important for cloud native adoption?
- [ ] They make every Kubernetes cluster run noticeably faster
- [x] They enable interoperability between vendors and reduce lock-in
- [ ] They are required in order to obtain a CNCF certification
- [ ] They remove the need for a container orchestrator entirely
> Los estándares abiertos permiten que herramientas de distintos proveedores funcionen juntas (por ejemplo, cualquier imagen OCI en cualquier runtime) y facilitan migrar entre nubes o productos, reduciendo la dependencia de un proveedor (*vendor lock-in*).

### [4/Ecosystem & Principles/2]
What does "cattle, not pets" mean in cloud native operations?
- [ ] Each server should be carefully named and maintained by hand
- [x] Instances are disposable and replaced rather than repaired by hand
- [ ] Only stateful workloads should ever run inside containers
- [ ] Clusters should never be upgraded once they are in production
> Las "mascotas" son servidores únicos que se cuidan a mano; el "ganado" son instancias idénticas y reemplazables. En Kubernetes, si un Pod o un nodo falla, se reemplaza automáticamente. El enfoque se apoya en la infraestructura inmutable y en la automatización.

### [4/Ecosystem & Principles/2]
Which design property makes a cloud native application easier to scale horizontally?
- [ ] Keeping user session state in each instance's local memory
- [x] Keeping instances stateless and storing state in backing services
- [ ] Hard-coding the IP addresses of the services it depends on
- [ ] Writing all logs to files on the local disk of each instance
> Las instancias sin estado (*stateless*) son intercambiables: se pueden añadir o quitar réplicas libremente porque el estado vive en servicios externos (bases de datos, caches, almacenamiento de objetos). Es uno de los principios de las *Twelve-Factor Apps*, junto con la configuración en el entorno y los logs como flujos de eventos.

### [4/Ecosystem & Principles/2]
According to the Twelve-Factor App methodology, where should configuration that varies between environments be stored?
- [ ] Hard-coded in the application source code
- [x] In the environment, e.g. environment variables
- [ ] Inside a separate image built for each environment
- [ ] In the application logs, so it can be audited
> El factor III dice "guarda la configuración en el entorno": lo que cambia entre entornos (URLs, credenciales) no va en el código ni en la imagen. En Kubernetes se inyecta con ConfigMaps y Secrets, de modo que la misma imagen sirve para todos los entornos.

### [4/Ecosystem & Principles/2]
What does a declarative API let you do?
- [ ] Describe every step that the system must execute, in strict order
- [x] Describe the end state and let the system reach and keep it
- [ ] Run arbitrary commands directly on the cluster nodes
- [ ] Avoid storing any state anywhere in the system
> Con una API declarativa defines *qué* quieres (por ejemplo, 3 réplicas de esta imagen) y el sistema converge y se mantiene en ese estado aunque haya fallos. En una API imperativa defines *cómo* (los pasos). Kubernetes es fundamentalmente declarativo.

### [4/Ecosystem & Principles/2]
Which resiliency pattern stops calling a failing dependency for a while, to prevent cascading failures?
- [ ] Sidecar
- [x] Circuit breaker
- [ ] Blue/green deployment
- [ ] Leader election
> El **circuit breaker** "abre el circuito" cuando una dependencia falla repetidamente y deja de llamarla durante un tiempo, devolviendo un error rápido; luego vuelve a probar. Evita fallos en cascada. Los service mesh (Envoy/Istio) pueden aplicarlo sin cambiar el código, junto con reintentos y timeouts.

### [4/Ecosystem & Principles/2]
What is the CNCF Landscape?
- [ ] A list that only contains the certified Kubernetes distributions
- [x] An interactive map that categorizes cloud native projects and products
- [ ] A Kubernetes dashboard that visualizes the state of your clusters
- [ ] The official roadmap of upcoming Kubernetes features
> El CNCF Landscape (landscape.cncf.io) organiza miles de proyectos y productos en categorías (aprovisionamiento, runtime, orquestación y gestión, definición y desarrollo de aplicaciones, observabilidad y análisis…) y marca los proyectos de la CNCF según su nivel de madurez.

### [4/Ecosystem & Principles/2]
Which statement about multi-tenancy in Kubernetes is correct?
- [ ] Namespaces alone give isolation equivalent to separate clusters
- [x] Namespaces plus RBAC, quotas and policies give soft isolation
- [ ] A single cluster cannot safely host more than one team
- [ ] Multi-tenancy is only possible with a service mesh installed
> Los namespaces son la unidad básica para separar equipos o entornos, pero comparten nodos, kernel y control plane. Con RBAC, ResourceQuotas, NetworkPolicies y Pod Security se logra una separación razonable (*soft*). Para inquilinos que no confían entre sí puede hacer falta más: clústeres separados, clústeres virtuales o runtimes con sandbox.

### [4/Ecosystem & Principles/2]
Which scaling approach is generally preferred for cloud native, stateless services?
- [ ] Vertical scaling of one very large instance
- [x] Horizontal scaling by adding or removing replicas
- [ ] Manual scaling during business hours only
- [ ] Scaling the control plane instead of the workload
> El escalado **horizontal** (más o menos réplicas) encaja con servicios sin estado: es elástico, tolera fallos y no requiere reiniciar instancias para cambiar su tamaño. El vertical tiene límites físicos y suele requerir reinicios. En Kubernetes lo implementa el HPA.

### [4/Community & Collaboration/1]
Which organization hosts Kubernetes and other cloud native projects such as Prometheus and Envoy?
- [ ] The Apache Software Foundation
- [x] The CNCF, part of the Linux Foundation
- [ ] The Open Container Initiative (OCI)
- [ ] The OpenInfra Foundation (OpenStack)
> La **CNCF** se fundó en 2015 bajo la Linux Foundation como hogar neutral para proyectos cloud native. Kubernetes fue su primer proyecto, donado por Google, que lo creó a partir de su experiencia con Borg. La OCI, también de la Linux Foundation, define los estándares de contenedores.

### [4/Community & Collaboration/1]
What are the three maturity levels of CNCF projects?
- [ ] Alpha, Beta and Stable
- [x] Sandbox, Incubating and Graduated
- [ ] Bronze, Silver and Gold
- [ ] Experimental, Preview and General Availability
> Los proyectos de la CNCF avanzan de **Sandbox** (temprano, experimental) a **Incubating** (adopción creciente en producción) y a **Graduated** (maduro, ampliamente adoptado, con gobernanza sólida y auditoría de seguridad). Alpha/Beta/Stable son niveles de las APIs de Kubernetes, no de los proyectos.

### [4/Community & Collaboration/2]
Which CNCF body decides on accepting projects and moving them between maturity levels?
- [ ] The Governing Board
- [x] The Technical Oversight Committee (TOC)
- [ ] Kubernetes SIG Release
- [ ] The End User Technical Advisory Board
> El **TOC** (Technical Oversight Committee) es el órgano técnico de la CNCF: define la visión técnica y aprueba la entrada de proyectos y sus promociones de nivel. El Governing Board gestiona presupuesto y marketing, no las decisiones técnicas sobre proyectos.

### [4/Community & Collaboration/2]
How is the Kubernetes project organized to develop areas such as networking, storage or the node?
- [ ] By a single team at Google that owns and reviews all of the code
- [x] Through Special Interest Groups (SIGs), working groups and committees
- [ ] By the CNCF Governing Board, which assigns the work to companies
- [ ] By the major cloud providers, taking turns each release
> Kubernetes se organiza en **SIGs** (SIG Network, SIG Storage, SIG Node, SIG Security…), cada una dueña de un área del código; además hay *working groups* temporales y comités como el Steering Committee. Cualquiera puede participar en sus reuniones abiertas.

### [4/Community & Collaboration/2]
How are significant new features proposed and tracked in Kubernetes?
- [ ] Through a private roadmap that the CNCF maintains
- [x] Through Kubernetes Enhancement Proposals (KEPs)
- [ ] Through feature requests filed by paying vendors
- [ ] Through votes in GitHub Discussions only
> Las mejoras importantes se proponen como **KEPs** (Kubernetes Enhancement Proposals), documentos que describen la motivación, el diseño, los criterios de graduación (alpha → beta → GA) y el plan de pruebas, aprobados por las SIGs correspondientes.

### [4/Community & Collaboration/2]
Which role applies software engineering to operations, defines SLOs and works to reduce toil?
- [ ] Product Owner of the platform
- [x] Site Reliability Engineer (SRE)
- [ ] Machine Learning Engineer (MLE)
- [ ] Scrum Master of the delivery team
> El **SRE** aplica prácticas de ingeniería de software a la operación: define SLIs y SLOs, gestiona error budgets, automatiza para reducir el *toil* (trabajo manual repetitivo) y lidera la respuesta a incidentes. Otros roles cloud native: DevOps engineer, platform engineer, cloud architect, security engineer o FinOps.

### [4/Community & Collaboration/2]
Which role is mainly responsible for an organization's cloud strategy and high-level architecture, choosing services and patterns?
- [x] Cloud architect
- [ ] Site Reliability Engineer
- [ ] Full-stack developer
- [ ] QA tester
> El **cloud architect** diseña la arquitectura y la estrategia de nube: qué servicios y patrones usar, seguridad, costos, multi-cloud. El SRE se enfoca en la confiabilidad en producción y los desarrolladores construyen las aplicaciones.

### [4/Community & Collaboration/2]
Which of the following is a CNCF graduated project?
- [x] Prometheus
- [ ] Jenkins
- [ ] Terraform
- [ ] Docker Swarm
> **Prometheus** fue el segundo proyecto en graduarse en la CNCF, después de Kubernetes. Jenkins pertenece a la CD Foundation, Terraform es de HashiCorp y Docker Swarm es de Docker.

### [4/Community & Collaboration/1]
Which conference is the CNCF's flagship event for the cloud native community?
- [ ] AWS re:Invent
- [x] KubeCon + CloudNativeCon
- [ ] DockerCon
- [ ] Open Source Summit
> **KubeCon + CloudNativeCon** es el evento principal de la CNCF, con ediciones en Norteamérica, Europa, Asia y otras regiones; reúne a mantenedores, usuarios finales y proveedores. re:Invent es de AWS y DockerCon de Docker; el Open Source Summit es un evento general de la Linux Foundation.

### [4/Community & Collaboration/2]
How can someone typically start contributing to Kubernetes?
- [ ] Only employees of CNCF member companies are allowed to contribute
- [x] Join a SIG, pick a good first issue and send a PR after signing the CLA
- [ ] Buy a contributor license from the Linux Foundation first
- [ ] Pass the CKA exam before submitting any pull request
> Kubernetes está abierto a cualquiera: hay una guía de contribución, issues marcados como *good first issue*, reuniones públicas de SIGs, el Slack de Kubernetes y programas de mentoría. Hay que aceptar el CLA de la CNCF. Contribuir no es solo código: documentación, pruebas, revisiones y comunidad también cuentan.
