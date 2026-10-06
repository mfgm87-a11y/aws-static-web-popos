# KCSA · Dominio 6 · Compliance and Security Frameworks

### [6/Compliance Frameworks/1]
Which standard applies to organizations that store, process or transmit payment card data?
- [ ] HIPAA
- [x] PCI DSS
- [ ] GDPR
- [ ] FedRAMP
> **PCI DSS** (Payment Card Industry Data Security Standard) aplica a quien maneja datos de tarjetas de pago: segmentación de red, cifrado, control de acceso, registro y monitoreo, gestión de vulnerabilidades. En Kubernetes suele implicar aislar las cargas que manejan esos datos (namespaces, nodos, NetworkPolicies).

### [6/Compliance Frameworks/1]
Which regulation protects the personal data of people in the European Union?
- [ ] SOC 2
- [x] GDPR
- [ ] PCI DSS
- [ ] HIPAA
> El **GDPR** (Reglamento General de Protección de Datos) regula el tratamiento de datos personales de personas en la UE: base legal, minimización, derechos de los titulares, notificación de brechas y medidas técnicas como el cifrado. Aplica aunque la empresa esté fuera de la UE si trata esos datos.

### [6/Compliance Frameworks/1]
HIPAA mainly applies to which kind of data?
- [ ] Payment card numbers processed by online stores
- [x] Protected health information in the United States
- [ ] Personal data of European Union residents
- [ ] Classified data of the US federal government
> **HIPAA** es la ley de EE. UU. que protege la información de salud (PHI) que manejan proveedores de salud, aseguradoras y sus socios. Exige salvaguardas administrativas, físicas y técnicas, como control de acceso, auditoría y cifrado.

### [6/Compliance Frameworks/2]
What is SOC 2?
- [ ] A Kubernetes benchmark published by the Center for Internet Security
- [x] An audit report based on the Trust Services Criteria
- [ ] A European regulation on the protection of personal data
- [ ] A container image signing standard from the OpenSSF
> **SOC 2** (del AICPA) es un informe de auditoría sobre los controles de una organización según los *Trust Services Criteria*: seguridad, disponibilidad, integridad del procesamiento, confidencialidad y privacidad. Es común para proveedores SaaS; los controles de Kubernetes (RBAC, auditoría, cambios) aportan evidencias.

### [6/Compliance Frameworks/2]
Which NIST publication is the Application Container Security Guide?
- [ ] NIST SP 800-53
- [x] NIST SP 800-190
- [ ] NIST SP 800-218
- [ ] NIST SP 800-63
> **NIST SP 800-190** describe los riesgos y contramedidas de las tecnologías de contenedores (imágenes, registros, orquestadores, contenedores, sistema operativo del host). SP 800-53 es el catálogo general de controles, SP 800-218 es el SSDF (desarrollo seguro) y SP 800-63 trata de identidad digital.

### [6/Compliance Frameworks/2]
Which set lists the core functions of the NIST Cybersecurity Framework 2.0?
- [ ] Identify, Protect, Detect, Respond, Recover and Report
- [x] Govern, Identify, Protect, Detect, Respond and Recover
- [ ] Spoofing, Tampering, Repudiation and Disclosure
- [ ] Develop, Distribute, Deploy and Runtime
> El **NIST CSF 2.0** (2024) organiza la ciberseguridad en seis funciones: **Govern** (nueva en la versión 2.0), Identify, Protect, Detect, Respond y Recover. La versión 1.1 tenía cinco funciones (sin Govern) y ninguna versión incluye "Report".
>
> Spoofing, Tampering, Repudiation… son categorías de STRIDE, y Develop, Distribute, Deploy y Runtime son las fases del ciclo de vida cloud native.

### [6/Compliance Frameworks/2]
Which guidance document was published by the NSA and CISA specifically for hardening Kubernetes?
- [ ] The OWASP Kubernetes Top 10
- [x] The Kubernetes Hardening Guide
- [ ] The CIS Docker Benchmark
- [ ] NIST SP 800-207 (Zero Trust Architecture)
> La NSA y CISA publicaron la **Kubernetes Hardening Guide** (2021, actualizada en 2022) con recomendaciones sobre escaneo de imágenes, Pods sin privilegios, separación de red, autenticación y autorización, auditoría y actualizaciones. Herramientas como Kubescape pueden comprobar un clúster contra ella.

### [6/Compliance Frameworks/2]
What does ISO/IEC 27001 specify?
- [ ] The configuration checks for each Kubernetes component
- [x] Requirements for an information security management system
- [ ] A file format for software bills of materials
- [ ] A threat model for container runtimes and registries
> **ISO/IEC 27001** define los requisitos de un **sistema de gestión de seguridad de la información** (SGSI/ISMS): evaluación de riesgos, políticas, controles (Anexo A) y mejora continua. Es una norma certificable a nivel de organización, no una guía específica de Kubernetes.

### [6/Compliance Frameworks/2]
What is the difference between Level 1 and Level 2 profiles in a CIS Benchmark?
- [ ] Level 1 applies only to the control plane; Level 2 applies only to workers
- [x] Level 1 is a basic baseline; Level 2 adds stricter, more disruptive checks
- [ ] Level 1 is meant for test clusters; Level 2 is meant only for managed services
- [ ] Level 2 replaces Level 1 entirely and removes all of its checks
> Los perfiles **Level 1** son recomendaciones básicas, de bajo impacto en la operación. Los **Level 2** añaden defensa en profundidad para entornos donde la seguridad es prioritaria, aunque puedan reducir funcionalidades o complicar la operación.

### [6/Compliance Frameworks/2]
What is FedRAMP?
- [ ] A Kubernetes admission controller built for US federal agencies
- [x] A US program that authorizes cloud services for federal use
- [ ] A CNCF certification for Kubernetes security professionals
- [ ] An open source tool that scans clusters for misconfigurations
> **FedRAMP** estandariza la evaluación y autorización de servicios en la nube que usan las agencias federales de EE. UU., basándose en los controles de NIST SP 800-53. Muchos servicios gestionados de Kubernetes tienen variantes autorizadas por FedRAMP.

### [6/Threat Modeling/1]
What does STRIDE stand for?
- [ ] Spoofing, Tampering, Revocation, Information leakage, Denial of service, Encryption failure
- [x] Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege
- [ ] Sniffing, Tampering, Repudiation, Intrusion, Data exfiltration, Elevation of privilege
- [ ] Spoofing, Theft, Replay, Information disclosure, Disruption of service, Escalation of access
> **STRIDE** (creado en Microsoft) clasifica amenazas en seis categorías, cada una opuesta a una propiedad de seguridad: Spoofing ↔ autenticación, Tampering ↔ integridad, Repudiation ↔ no repudio, Information disclosure ↔ confidencialidad, Denial of service ↔ disponibilidad y Elevation of privilege ↔ autorización.

### [6/Threat Modeling/2]
In STRIDE, which threat category is mainly mitigated by strong authentication such as mTLS or OIDC?
- [x] Spoofing
- [ ] Tampering
- [ ] Repudiation
- [ ] Denial of service
> **Spoofing** es hacerse pasar por otra identidad (usuario, servicio, nodo). Se mitiga con autenticación fuerte: certificados, mTLS entre servicios, OIDC para personas, tokens de corta duración. Tampering se mitiga con integridad (firmas, hashes) y Repudiation con auditoría.

### [6/Threat Modeling/2]
An attacker modifies a ConfigMap and swaps a container image for a malicious one. Which STRIDE category does this represent?
- [ ] Spoofing
- [x] Tampering
- [ ] Information disclosure
- [ ] Repudiation
> **Tampering** es la modificación no autorizada de datos o código: cambiar configuración, imágenes, manifiestos o datos en tránsito. Se mitiga con RBAC estricto, firmas de imágenes y digests, GitOps con revisión, admisión e integridad en tránsito (TLS).

### [6/Threat Modeling/2]
A user denies having deleted a production Deployment, and there are no audit logs to prove what happened. Which STRIDE threat is this?
- [ ] Spoofing
- [ ] Tampering
- [x] Repudiation
- [ ] Elevation of privilege
> **Repudiation** es poder negar haber hecho una acción porque no hay evidencias. El control principal es el **audit log** del API server (con identidades individuales, no credenciales compartidas), protegido contra manipulación y enviado fuera del clúster.

### [6/Threat Modeling/2]
A process escapes from a container and becomes root on the node. Which STRIDE category is this?
- [ ] Information disclosure
- [ ] Denial of service
- [x] Elevation of privilege
- [ ] Repudiation
> Obtener más privilegios de los concedidos (de proceso en un contenedor a root en el host, o de un ServiceAccount limitado a cluster-admin) es **Elevation of privilege**. Se mitiga con Pod Security, mínimo privilegio en RBAC, seccomp/AppArmor, user namespaces y runtimes con sandbox.

### [6/Threat Modeling/2]
What is MITRE ATT&CK?
- [ ] A scoring system that rates the severity of vulnerabilities
- [x] A knowledge base of real-world adversary tactics and techniques
- [ ] A compliance standard for companies that process payment cards
- [ ] A tool that automatically patches Kubernetes clusters
> **MITRE ATT&CK** recopila tácticas y técnicas de atacantes observadas en la realidad, organizadas en matrices (empresa, nube, contenedores…). Sirve para modelar amenazas, diseñar detecciones y evaluar la cobertura de controles. La severidad de vulnerabilidades se puntúa con CVSS.

### [6/Threat Modeling/2]
Which threat matrix, adapted from MITRE ATT&CK, was published by Microsoft specifically for Kubernetes?
- [ ] The OWASP Kubernetes Top 10
- [x] The Threat Matrix for Kubernetes
- [ ] The CIS Kubernetes Benchmark
- [ ] The STRIDE-K8s checklist
> Microsoft publicó la **Threat Matrix for Kubernetes** (2020, actualizada después) basándose en la estructura de ATT&CK: acceso inicial, ejecución, persistencia, escalada de privilegios, evasión, acceso a credenciales, descubrimiento, movimiento lateral e impacto, con técnicas propias de Kubernetes.

### [6/Threat Modeling/2]
What does the DREAD model rate?
- [ ] The maturity level of a CNCF project, from sandbox to graduated
- [x] Risk: damage, reproducibility, exploitability, users, discoverability
- [ ] The compliance status of a Kubernetes cluster against the CIS Benchmark
- [ ] The performance impact of security controls on the cluster's workloads
> **DREAD** puntúa amenazas según Damage (daño), Reproducibility (reproducibilidad), Exploitability (facilidad de explotación), Affected users (usuarios afectados) y Discoverability (facilidad de descubrimiento), para priorizarlas. Se suele combinar con STRIDE: STRIDE identifica y DREAD prioriza.

### [6/Threat Modeling/2]
What characterizes the PASTA threat modeling methodology?
- [ ] A six-letter mnemonic for classifying individual threats
- [x] A seven-stage, risk-centric process tied to business objectives
- [ ] A checklist of Kubernetes API server configuration flags
- [ ] A tool that generates NetworkPolicies from traffic captures
> **PASTA** (Process for Attack Simulation and Threat Analysis) es una metodología de siete etapas centrada en el riesgo: desde definir objetivos de negocio y el alcance técnico hasta analizar amenazas, vulnerabilidades, simular ataques y evaluar el impacto. Es más pesada que STRIDE, pero alinea la seguridad con el negocio.

### [6/Threat Modeling/2]
In MITRE ATT&CK, what is the difference between tactics and techniques?
- [ ] Tactics are the attacker's tools; techniques are the vulnerabilities used
- [x] Tactics are the attacker's goals; techniques are how they achieve them
- [ ] Tactics apply to the cloud, and techniques apply to containers
- [ ] There is no difference; they are synonyms in the framework
> Las **tácticas** son el "por qué" (el objetivo del atacante en esa fase: persistencia, escalada de privilegios, movimiento lateral…) y las **técnicas** son el "cómo" (por ejemplo, crear un CronJob o escribir un Pod estático para lograr persistencia).

### [6/Supply Chain Compliance/2]
Which NIST publication defines the Secure Software Development Framework (SSDF)?
- [ ] NIST SP 800-190
- [x] NIST SP 800-218
- [ ] NIST SP 800-37
- [ ] NIST SP 800-171
> **NIST SP 800-218** describe el SSDF: prácticas de desarrollo seguro agrupadas en preparar la organización, proteger el software, producir software bien asegurado y responder a vulnerabilidades. Es una referencia clave de cumplimiento para la cadena de suministro de software.

### [6/Supply Chain Compliance/2]
Which US government action strongly pushed SBOM adoption for software sold to federal agencies?
- [ ] Article 32 of the EU General Data Protection Regulation
- [x] Executive Order 14028 on improving the nation's cybersecurity
- [ ] The Sarbanes-Oxley Act on corporate financial reporting controls
- [ ] The PCI DSS v4.0 update for payment card security
> La **Orden Ejecutiva 14028** (mayo de 2021), tras incidentes como SolarWinds, impulsó requisitos de seguridad de la cadena de suministro para proveedores del gobierno de EE. UU., incluidos los SBOM y prácticas de desarrollo seguro (SSDF).

### [6/Supply Chain Compliance/2]
What does the OpenSSF Scorecard project do?
- [ ] It signs container images with keyless certificates
- [x] It checks open source projects for security practices
- [ ] It scans running Kubernetes clusters for CVEs
- [ ] It stores SBOMs in a public transparency log
> **OpenSSF Scorecard** evalúa automáticamente repositorios open source en aspectos como protección de ramas, revisión de código, dependencias fijadas, uso de herramientas de análisis o mantenimiento activo. Ayuda a valorar el riesgo de las dependencias que adoptas.

### [6/Supply Chain Compliance/2]
In SLSA v1.0, what does moving up the Build track levels primarily improve?
- [ ] The runtime performance of the produced artifacts in production
- [x] How trustworthy and tamper-resistant the build provenance is
- [ ] The number of vulnerability scanners run on the image
- [ ] The amount of documentation shipped with each release
> En SLSA v1.0, el nivel 1 exige que exista procedencia, el 2 que la genere una plataforma de build alojada y esté firmada, y el 3 que la plataforma esté endurecida para que la procedencia sea muy difícil de falsificar. Cada nivel aumenta la confianza en *cómo* se construyó el artefacto.

### [6/Supply Chain Compliance/2]
What is a VEX document used for?
- [ ] To list every file and package contained in a container image
- [x] To state whether a product is affected by a given CVE
- [ ] To grant temporary admin access during an incident
- [ ] To define network policies between microservices
> **VEX** (Vulnerability Exploitability eXchange) permite que un proveedor declare si su producto está afectado o no por una vulnerabilidad concreta (por ejemplo, porque el componente vulnerable no se usa). Complementa al SBOM y reduce falsos positivos de los escáneres.

### [6/Supply Chain Compliance/2]
Which of the following is one of the NTIA minimum elements of an SBOM?
- [ ] The CPU usage of each component at runtime
- [x] The dependency relationships between components
- [ ] The names of the developers' managers
- [ ] The number of downloads of each package per month
> Los elementos mínimos de un SBOM según la NTIA incluyen proveedor, nombre del componente, versión, identificadores únicos, **relaciones de dependencia**, autor de los datos del SBOM y marca de tiempo. Esto permite saber qué contiene el software y de dónde viene.

### [6/Automation & Tooling/1]
Which tool checks a cluster against the CIS Kubernetes Benchmark?
- [ ] Falco
- [x] kube-bench
- [ ] cosign
- [ ] Helm
> **kube-bench** (de Aqua Security) ejecuta en cada nodo las comprobaciones del CIS Kubernetes Benchmark (archivos, permisos, flags del API server, kubelet, etcd…) e informa de lo que pasa o falla. Falco es seguridad en runtime, cosign firma imágenes y Helm instala charts.

### [6/Automation & Tooling/2]
Which CNCF project scans clusters and manifests against frameworks such as the NSA-CISA guidance and MITRE ATT&CK?
- [ ] Prometheus
- [x] Kubescape
- [ ] Linkerd
- [ ] Velero
> **Kubescape** (CNCF) analiza clústeres, manifiestos YAML y charts de Helm contra varios marcos (NSA-CISA, MITRE ATT&CK, CIS) y calcula una puntuación de riesgo con recomendaciones. Puede ejecutarse en CI o dentro del clúster.

### [6/Automation & Tooling/2]
Which tool can scan container images, filesystems, IaC files and Kubernetes clusters for vulnerabilities, misconfigurations and secrets, and also generate SBOMs?
- [ ] kube-bench
- [x] Trivy
- [ ] OpenCost
- [ ] etcdctl
> **Trivy** (de Aqua Security) es un escáner muy versátil: vulnerabilidades en imágenes y dependencias, configuraciones inseguras en Dockerfiles, Terraform y manifiestos de Kubernetes, secretos expuestos y generación de SBOMs (SPDX y CycloneDX). Con el Trivy Operator escanea continuamente lo que corre en el clúster.

### [6/Automation & Tooling/2]
What does "policy as code" mean in a Kubernetes context?
- [ ] Writing security policies in a PDF document that every developer signs
- [x] Versioned, testable policies enforced automatically in CI and admission
- [ ] Hard-coding security checks inside every application binary
- [ ] Letting each developer decide which policies to follow
> Con políticas como código (Rego en Gatekeeper, YAML en Kyverno, CEL en ValidatingAdmissionPolicy), las reglas se guardan en Git, se revisan, se prueban y se aplican de forma automática y consistente en el pipeline y en la admisión, generando además evidencias para auditorías.

### [6/Automation & Tooling/2]
Which tools scan Terraform and Kubernetes YAML for security misconfigurations before deployment?
- [ ] Falco and Tetragon running on every node
- [x] Checkov, KICS or Trivy config scanning
- [ ] CoreDNS and kube-proxy in kube-system
- [ ] Prometheus and Alertmanager
> Herramientas de análisis estático de IaC como **Checkov**, **KICS** o `trivy config` detectan configuraciones inseguras (Pods privilegiados, buckets públicos, falta de cifrado) antes de aplicarlas, idealmente en cada pull request. Falco y Tetragon trabajan en tiempo de ejecución.

### [6/Automation & Tooling/2]
A team runs Kyverno or Gatekeeper with background (audit) scanning enabled. What does that provide?
- [ ] It blocks every request to the API server until it is reviewed
- [x] Reports on existing resources that violate policies, without blocking
- [ ] Automatic deletion of every non-compliant resource in the cluster
- [ ] Encryption of all policies stored in etcd with a KMS key
> Además de bloquear en la admisión, estos motores revisan periódicamente los recursos ya existentes y generan informes de cumplimiento (por ejemplo, PolicyReports en Kyverno o el estado de las Constraints en Gatekeeper). Es útil para medir el cumplimiento antes de pasar a modo *enforce* y como evidencia de auditoría.
