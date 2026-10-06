# KCSA · Dominio 3 · Kubernetes Security Fundamentals

### [3/Pod Security Standards/1]
Which Pod Security Standards profile is intended for system and infrastructure workloads that need privileged access?
- [x] Privileged
- [ ] Baseline
- [ ] Restricted
- [ ] Hardened
> El perfil **Privileged** no impone restricciones y está pensado para cargas de sistema gestionadas por administradores de confianza (CNI, agentes de almacenamiento, etc.). **Baseline** evita escaladas de privilegio conocidas y **Restricted** aplica las mejores prácticas de endurecimiento. "Hardened" no existe.

### [3/Pod Security Standards/2]
Which of these settings is disallowed by the Baseline profile?
- [ ] `runAsNonRoot: false`
- [x] `hostNetwork: true`
- [ ] `readOnlyRootFilesystem: false`
- [ ] `seccompProfile: RuntimeDefault`
> *Baseline* prohíbe compartir los namespaces del host (`hostNetwork`, `hostPID`, `hostIPC`), los contenedores privilegiados, los volúmenes `hostPath`, añadir capabilities fuera de una lista segura, `hostPort` y perfiles seccomp `Unconfined`, entre otros. Exigir usuario no root es un control de *Restricted*, y el sistema de archivos de solo lectura no forma parte de los PSS.

### [3/Pod Security Standards/2]
Which control is required by the Restricted profile but NOT by Baseline?
- [ ] `privileged` must be false or unset
- [x] `runAsNonRoot` must be set to true
- [ ] `hostPID` must be false or unset
- [ ] `hostPath` volumes must not be used
> *Restricted* incluye todo *Baseline* y además exige `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, eliminar todas las capabilities (`drop: [ALL]`), un perfil seccomp explícito (`RuntimeDefault` o `Localhost`) y solo ciertos tipos de volumen. Prohibir `privileged`, `hostPID` y `hostPath` ya forma parte de *Baseline*.

### [3/Pod Security Standards/2]
Under the Restricted profile, which capability may a container add back after dropping `ALL`?
- [ ] `SYS_ADMIN`
- [x] `NET_BIND_SERVICE`
- [ ] `NET_ADMIN`
- [ ] `SYS_PTRACE`
> *Restricted* exige `capabilities.drop: ["ALL"]` y solo permite añadir de nuevo `NET_BIND_SERVICE`, que deja escuchar en puertos por debajo de 1024. Cualquier otra capability añadida hace que el Pod no cumpla el perfil.

### [3/Pod Security Standards/3]
Under the Restricted profile, which seccomp configuration is compliant?
- [ ] Leaving `seccompProfile` unset on the Pod and every container
- [x] Setting `seccompProfile.type` to `RuntimeDefault` or `Localhost`
- [ ] Setting `seccompProfile.type: Unconfined` on the Pod only
- [ ] Setting `seccompProfile.type: Unconfined` with `privileged: false`
> *Restricted* exige un perfil seccomp **explícito**: `RuntimeDefault` o `Localhost`, a nivel de Pod o de cada contenedor. Tanto `Unconfined` como la ausencia de perfil están prohibidos (en *Baseline* basta con no usar `Unconfined`).

### [3/Pod Security Standards/3]
Which volume type is allowed under the Restricted profile?
- [ ] `hostPath`
- [x] `projected`
- [ ] `nfs`
- [ ] `iscsi`
> *Restricted* solo permite volúmenes `configMap`, `csi`, `downwardAPI`, `emptyDir`, `ephemeral`, `persistentVolumeClaim`, `projected` y `secret`. Los volúmenes de red declarados directamente en el Pod (como `nfs` o `iscsi`) y `hostPath` no cumplen el perfil; para almacenamiento de red se usan PVCs.

### [3/Pod Security Standards/2]
A namespace moves from `enforce=baseline` to `enforce=restricted`. Its Pods already pass Baseline. Which setting must their containers now add?
- [ ] `privileged: false` on every container
- [x] `allowPrivilegeEscalation: false` on every container
- [ ] `hostPID: false` on the Pod spec
- [ ] Removing every `hostPath` volume
> Si los Pods ya cumplen *Baseline*, ya no son privilegiados, no comparten `hostPID` y no usan `hostPath`: eso lo exige *Baseline*. *Restricted* añade, entre otras cosas, `allowPrivilegeEscalation: false` (activa `no_new_privs` e impide ganar privilegios con binarios setuid), además de `runAsNonRoot: true`, `drop: [ALL]` y un perfil seccomp explícito.

### [3/Pod Security Standards/2]
What is the relationship between the Pod Security Standards and Pod Security Admission?
- [ ] They are two names for the same, now deprecated, PodSecurityPolicy API
- [x] PSS define the policy levels; PSA is the built-in controller enforcing them
- [ ] PSA defines the levels, while PSS is a third-party admission policy engine
- [ ] PSS apply to nodes, while PSA applies to the containers of a Pod
> Los **Pod Security Standards** son la definición de los tres niveles (Privileged, Baseline, Restricted). **Pod Security Admission** es el controlador de admisión integrado (estable desde 1.25) que los aplica por namespace mediante labels. Otros motores (Kyverno, Gatekeeper) también pueden implementar los PSS.

### [3/Pod Security Standards/3]
A namespace enforces Restricted. A Pod sets `runAsNonRoot: true` at Pod level, but one container sets `runAsUser: 0`. What happens?
- [ ] It is admitted, because the Pod-level setting takes precedence
- [x] It is rejected, because running as UID 0 is not allowed
- [ ] It is admitted, and the kubelet silently changes the UID to 1000
- [ ] It is admitted only if the container also drops all capabilities
> *Restricted* exige `runAsNonRoot: true` **y** prohíbe fijar `runAsUser: 0` en el Pod o en cualquier contenedor. La admisión rechaza el Pod. Además, aunque se admitiera, el kubelet se negaría a arrancar un contenedor que corre como root con `runAsNonRoot: true`.

### [3/Pod Security Standards/2]
Which capability can a container add and still comply with the Baseline profile?
- [x] `CHOWN`
- [ ] `SYS_ADMIN`
- [ ] `NET_ADMIN`
- [ ] `SYS_MODULE`
> *Baseline* permite añadir solo capabilities de una lista considerada segura (por ejemplo `CHOWN`, `KILL`, `SETUID`, `SETGID`, `NET_BIND_SERVICE`…). `SYS_ADMIN`, `NET_ADMIN` o `SYS_MODULE` (cargar módulos del kernel) dan demasiado poder y no están permitidas.

### [3/Pod Security Admission/1]
Which three modes does Pod Security Admission support?
- [x] enforce, audit and warn
- [ ] allow, deny and log
- [ ] strict, permissive and disabled
- [ ] block, alert and ignore
> PSA admite tres modos por namespace: **enforce** (rechaza los Pods que violan el nivel), **audit** (los permite pero añade una anotación al evento de auditoría) y **warn** (los permite y devuelve una advertencia al usuario). Se pueden combinar con niveles distintos, por ejemplo `enforce=baseline` y `warn=restricted`.

### [3/Pod Security Admission/2]
What does the `warn` mode of Pod Security Admission do with a violating Pod?
- [ ] It rejects the Pod and returns an error to the user
- [x] It allows the Pod and shows a warning to the user
- [ ] It allows the Pod and silently deletes it an hour later
- [ ] It queues the Pod until an administrator approves it
> En modo `warn` la petición se admite, pero el cliente (por ejemplo kubectl) recibe una advertencia que explica qué controles se incumplen. Es útil para preparar un endurecimiento sin romper despliegues.

### [3/Pod Security Admission/2]
What does the `audit` mode of Pod Security Admission do?
- [ ] It rejects the request and writes the Pod to an audit queue
- [x] It allows the request and adds an annotation to the audit event
- [ ] It sends the Pod spec to an external SIEM for approval
- [ ] It scans the Pod's image for vulnerabilities before running it
> En modo `audit` la petición se permite, pero el evento correspondiente del log de auditoría lleva una anotación con la violación. Sirve para medir el impacto de un nivel antes de aplicarlo con `enforce` (requiere tener la auditoría configurada).

### [3/Pod Security Admission/3]
A namespace is labeled `pod-security.kubernetes.io/enforce=restricted`. A user creates a Deployment whose Pod template violates Restricted. What happens?
- [ ] The Deployment is rejected by the API server's admission immediately
- [x] The Deployment is created, but its ReplicaSet cannot create the Pods
- [ ] The Pods are created and then patched to comply automatically
- [ ] The namespace label is removed so that the Pods can run
> El modo `enforce` solo se aplica a los **Pods**, no a los recursos de carga (Deployment, Job…). El Deployment se crea (los modos `warn` y `audit` sí evalúan las plantillas y pueden avisar), pero cuando el ReplicaSet intenta crear los Pods, la admisión los rechaza y verás el error en sus eventos.

### [3/Pod Security Admission/2]
What is the purpose of the label `pod-security.kubernetes.io/enforce-version`?
- [ ] To choose which Kubernetes version the Pods are allowed to run
- [x] To pin the policy definition to a specific Kubernetes minor version
- [ ] To force all Pods to upgrade to the latest container image
- [ ] To select the version of the PodSecurityPolicy API to use
> Los controles de cada nivel pueden evolucionar entre versiones de Kubernetes. Con `<modo>-version: v1.36` (por ejemplo) se fija la definición de esa versión para que una actualización del clúster no cambie de repente lo que se aplica; `latest` usa siempre la definición más reciente.

### [3/Pod Security Admission/2]
Which exemption dimensions does Pod Security Admission support?
- [ ] Labels, annotations and container image names
- [x] Usernames, RuntimeClass names and namespaces
- [ ] Node names, zones and instance types
- [ ] ServiceAccounts, Secrets and ConfigMaps
> Las exenciones de PSA se configuran en el plugin de admisión (AdmissionConfiguration) y pueden basarse en **usuarios** autenticados, nombres de **RuntimeClass** y **namespaces**. Las peticiones exentas se ignoran por completo (ni enforce, ni audit, ni warn). Deben usarse con mucho cuidado.

### [3/Pod Security Admission/2]
How can you check, without changing anything, which existing Pods in a namespace would violate the Restricted level?
- [ ] Delete the namespace and recreate it with the new label applied
- [x] Run `kubectl label --dry-run=server` with the enforce label
- [ ] Restart every Pod in the namespace and watch the kubelet logs
- [ ] Run `kubectl get psp` to list the policy violations in the namespace
> Aplicar la label con `--dry-run=server --overwrite` hace que el API server evalúe los Pods existentes contra el nuevo nivel y devuelva advertencias, sin guardar el cambio. Es una forma segura de planificar el endurecimiento. PodSecurityPolicy (`psp`) ya no existe.

### [3/Pod Security Admission/2]
Which permission would let a user weaken Pod Security Admission for their namespace?
- [ ] `get` on Pods in that namespace
- [x] `patch` or `update` on the Namespace object
- [ ] `create` on ConfigMaps in that namespace
- [ ] `list` on Events in that namespace
> PSA se configura con labels en el objeto Namespace. Quien pueda modificarlo puede cambiar `enforce=restricted` por `enforce=privileged`. Por eso el permiso para editar namespaces debe reservarse a administradores, o protegerse con políticas de admisión adicionales.

### [3/Pod Security Admission/2]
How can an administrator set a default Pod Security level for namespaces that have no PSA labels at all?
- [ ] By editing the `default` ServiceAccount in every namespace of the cluster
- [x] By setting the PodSecurity plugin defaults in an AdmissionConfiguration
- [ ] By setting a pod-security annotation on each node of the cluster
- [ ] By creating a ClusterRole named `pod-security-default` with a level
> El plugin PodSecurity admite una configuración (AdmissionConfiguration pasada al API server) con valores por defecto para enforce/audit/warn y con exenciones. Sin ella, los namespaces sin labels quedan en *privileged*, es decir, sin restricciones.

### [3/Authentication/2]
Which authentication method is commonly used to integrate Kubernetes with an enterprise identity provider for human users?
- [ ] Static token file
- [x] OpenID Connect (OIDC) tokens
- [ ] ServiceAccount tokens
- [ ] Bootstrap tokens
> **OIDC** permite usar un proveedor de identidad (Entra ID, Okta, Keycloak, Google…) para autenticar personas con tokens de corta duración, con usuarios y grupos gestionados de forma central. Los ServiceAccounts son para cargas de trabajo y los bootstrap tokens para unir nodos.

### [3/Authentication/2]
With X.509 client certificate authentication, how does Kubernetes determine the username and the groups?
- [ ] From the certificate's serial number and its issuer field
- [x] The CN becomes the username; the O fields become the groups
- [ ] From a ConfigMap that maps certificate fingerprints to users
- [ ] From the Subject Alternative Names listed in the certificate
> En los certificados de cliente, el **Common Name (CN)** es el nombre de usuario y cada **Organization (O)** es un grupo. Por eso un certificado con `O=system:masters` otorga acceso de superusuario, y quien puede firmar certificados con la CA del clúster puede crear cualquier identidad.

### [3/Authentication/2]
Why is the static token file authentication method discouraged?
- [ ] Because its tokens expire every five minutes and must be re-issued
- [x] Tokens are long-lived plaintext and changes need an API server restart
- [ ] Because it only works for ServiceAccounts, not for users
- [ ] Because it requires an integration with a cloud provider identity service
> Con `--token-auth-file`, los tokens se guardan en texto plano en el control plane, no caducan y la lista solo cambia reiniciando el API server. Es difícil de rotar y auditar, así que no se recomienda para producción.

### [3/Authentication/2]
What are bootstrap tokens mainly used for?
- [ ] Granting cluster-admin rights to newly onboarded human users
- [x] Letting new nodes join the cluster via TLS bootstrapping
- [ ] Encrypting Secrets before they are written to etcd
- [ ] Signing container images in the CI pipeline
> Los bootstrap tokens son tokens simples y de corta vida, guardados como Secrets en `kube-system`, que usan los nodos nuevos (por ejemplo con `kubeadm join`) para autenticarse lo justo para pedir su certificado de kubelet. Deben tener caducidad corta y permisos mínimos.

### [3/Authentication/2]
What does the TokenRequest API provide?
- [ ] Non-expiring ServiceAccount tokens stored as Secrets in etcd
- [x] Short-lived ServiceAccount tokens bound to an audience
- [ ] OIDC tokens issued for human users by the API server
- [ ] Tokens that let anonymous users read cluster information
> La API TokenRequest emite tokens de ServiceAccount con caducidad, una audiencia concreta y, opcionalmente, ligados a un objeto (un Pod o Secret): si el Pod se borra, el token deja de ser válido. Es lo que usa el kubelet para los volúmenes proyectados.

### [3/Authentication/3]
An authenticating proxy passes the user identity to the API server in request headers such as `X-Remote-User`. What must be guaranteed?
- [ ] That the headers are base64-encoded before being sent
- [x] That the API server verifies the proxy's client certificate first
- [ ] That every user also has a static token configured as backup
- [ ] That the proxy runs inside the kube-system namespace
> Con el modo *request header*, el API server confía en las cabeceras de identidad **solo** si la petición viene de un proxy autenticado con un certificado firmado por `--requestheader-client-ca-file` (y con un CN permitido). Si no, cualquiera podría falsificar la cabecera y hacerse pasar por otro usuario.

### [3/Authentication/2]
When a request is authenticated with a ServiceAccount token, which username does it get?
- [ ] `sa:<name>@<namespace>`
- [x] `system:serviceaccount:<namespace>:<name>`
- [ ] `<namespace>/<name>`
- [ ] `serviceaccount.<name>.<namespace>.svc`
> Los ServiceAccounts se autentican como `system:serviceaccount:<namespace>:<nombre>` y pertenecen a los grupos `system:serviceaccounts` y `system:serviceaccounts:<namespace>`. Esos son los nombres que se usan en los `subjects` de RBAC (o el tipo `ServiceAccount` directamente).

### [3/Authentication/2]
What is user impersonation in Kubernetes?
- [ ] Sharing one kubeconfig file between several administrators
- [x] Acting as another user, group or ServiceAccount via headers
- [ ] Creating a copy of a Pod that runs as a different user ID
- [ ] Logging in to a node with the credentials of the kubelet
> Con el verbo `impersonate`, un usuario puede enviar peticiones como si fuera otro (`kubectl --as=...`, `--as-group=...`). Es útil para pruebas y herramientas, pero peligroso: quien puede suplantar a un usuario o grupo privilegiado obtiene sus permisos.

### [3/Authentication/1]
Which statement correctly distinguishes authentication from authorization?
- [ ] Authentication decides the permissions; authorization verifies the identity
- [x] Authentication proves who you are; authorization decides what you may do
- [ ] Both terms describe the same API server step with different names
- [ ] Authorization happens first, and authentication only after admission
> La **autenticación** responde "¿quién eres?" (certificados, tokens, OIDC). La **autorización** responde "¿puedes hacer esta acción sobre este recurso?" (Node, RBAC, Webhook). Después viene la **admisión**, que valida o modifica el objeto.

### [3/Authorization/2]
How are RBAC rules combined in Kubernetes?
- [ ] Deny rules always take precedence over allow rules
- [x] They are purely additive; there are no deny rules
- [ ] The most recently created Role overrides all the others
- [ ] Namespace Roles override ClusterRoles with the same name
> RBAC solo tiene permisos de tipo "permitir", y se suman: si cualquier binding permite la acción, está permitida. No se puede "denegar" una acción concreta con RBAC; para eso hay que no conceder el permiso o usar políticas de admisión u otros autorizadores.

### [3/Authorization/2]
Which RBAC verb lets a user create a RoleBinding to a Role whose permissions they do not hold themselves?
- [ ] `escalate`
- [x] `bind`
- [ ] `impersonate`
- [ ] `approve`
> Normalmente RBAC impide asignar permisos que uno no tiene. El verbo **bind** sobre roles levanta esa protección para crear bindings. **escalate** permite crear o modificar roles con más permisos que los propios, e **impersonate** permite actuar como otra identidad. Los tres son vías de escalada de privilegios.

### [3/Authorization/2]
What does the `escalate` verb on Roles and ClusterRoles allow?
- [ ] Binding existing roles to any user or group in the cluster
- [x] Creating or editing roles with permissions you do not have
- [ ] Temporarily acting as the cluster-admin user
- [ ] Approving pending CertificateSigningRequests
> RBAC impide por defecto crear o modificar un rol con permisos que el usuario no tiene. Con `escalate` esa protección desaparece: el usuario puede añadir cualquier permiso a un rol que ya tenga asignado y escalar sus privilegios.

### [3/Authorization/2]
Why is the `list` verb on Secrets as sensitive as `get`?
- [ ] Because `list` also lets the user delete the listed Secrets
- [x] Because list responses include the full contents of the Secrets
- [ ] Because `list` always grants access to Secrets in all namespaces
- [ ] Because `list` bypasses the audit log of the API server
> Una respuesta de `list` (por ejemplo `kubectl get secrets -o yaml`) devuelve los objetos completos, incluidos sus datos. Lo mismo ocurre con `watch`. Conceder `list` o `watch` sobre Secrets equivale a dejar leerlos.

### [3/Authorization/2]
Which RBAC subject should you use to grant permissions to an application running in a Pod?
- [ ] A User named after the application
- [x] A ServiceAccount
- [ ] The group `system:authenticated`
- [ ] The node's kubelet identity
> Las aplicaciones se identifican con **ServiceAccounts**. Lo correcto es crear uno por aplicación, darle un Role con lo mínimo necesario y referenciarlo en el Pod (`serviceAccountName`). Dar permisos a `system:authenticated` los otorgaría a cualquier identidad autenticada del clúster.

### [3/Authorization/2]
What do aggregated ClusterRoles do?
- [ ] Merge all namespaces into one shared namespace
- [x] Combine the rules of other ClusterRoles selected by labels
- [ ] Grant every permission held by the `system:masters` group
- [ ] Sum up the resource quotas of several namespaces
> Un ClusterRole con `aggregationRule` incorpora automáticamente las reglas de otros ClusterRoles que tengan ciertas labels. Así funcionan `admin`, `edit` y `view`: un CRD puede añadir sus permisos a esos roles. Conviene revisar qué roles se agregan, porque pueden ampliar permisos sin que se note.

### [3/Authorization/2]
How can you list every action that a given ServiceAccount is allowed to perform in a namespace?
- [ ] `kubectl describe serviceaccount <name> -n <ns> --show-permissions`
- [x] `kubectl auth can-i --list --as=system:serviceaccount:<ns>:<name> -n <ns>`
- [ ] `kubectl get rolebindings -n <ns> --for-serviceaccount <name> -o rules`
- [ ] `kubectl explain serviceaccount.permissions --recursive`
> `kubectl auth can-i --list` muestra los permisos efectivos de una identidad, y con `--as` la suplantas (necesitas permiso de `impersonate`). Es útil para auditar el mínimo privilegio de cada aplicación.

### [3/Authorization/2]
Why should wildcards (`*`) be avoided in the verbs and resources of a Role?
- [ ] Because wildcards are rejected by the API server's validation
- [x] They also grant future resources and risky verbs such as `bind`
- [ ] Because wildcards only work for cluster-scoped resources
- [ ] Because they make the Role invisible to `kubectl get roles`
> `*` concede todo, incluidos recursos que se añadan en el futuro (CRDs) y verbos peligrosos como `escalate`, `bind` o `impersonate`. Es contrario al mínimo privilegio: hay que enumerar recursos y verbos concretos.

### [3/Authorization/2]
Which permission lets someone read, and possibly modify, every object admitted to the cluster?
- [ ] `get` and `list` on Events in all namespaces
- [x] Control of mutating or validating webhook configurations
- [ ] `list` and `watch` on Nodes and their status
- [ ] `create` and `delete` on LimitRanges in every namespace
> Quien controla las `MutatingWebhookConfiguration` o `ValidatingWebhookConfiguration` puede hacer que el API server envíe cada objeto admitido a un servicio suyo (viendo su contenido) y, con webhooks mutantes, modificarlo (por ejemplo, inyectar un contenedor malicioso). Es un permiso muy sensible.

### [3/Authorization/1]
Which default ClusterRole grants superuser access when it is bound cluster-wide?
- [ ] `admin`
- [x] `cluster-admin`
- [ ] `edit`
- [ ] `view`
> `cluster-admin` permite cualquier acción sobre cualquier recurso. `admin`, `edit` y `view` están pensados para asignarse por namespace (con RoleBindings) y no dan, por ejemplo, permisos sobre ResourceQuotas o el propio namespace en el caso de `edit`.

### [3/Secrets/2]
In an EncryptionConfiguration, which provider is used to encrypt newly written Secrets?
- [ ] The last provider in the list
- [x] The first provider in the list
- [ ] The provider with the strongest algorithm
- [ ] A random provider chosen on each write
> El API server cifra las escrituras con el **primer** proveedor de la lista y, al leer, prueba todos hasta encontrar uno que pueda descifrar. Por eso, para rotar claves o activar el cifrado, se cambia el orden y luego se reescriben los Secrets.

### [3/Secrets/2]
What does the `identity` provider do in an EncryptionConfiguration?
- [ ] It encrypts data using the identity of the requesting user
- [x] It stores data without encryption
- [ ] It hashes Secrets so that they cannot be read back
- [ ] It encrypts data with a key derived from the node identity
> `identity` significa "sin cifrado": los datos se guardan tal cual. Es el comportamiento por defecto. Suele dejarse al final de la lista para poder leer Secrets antiguos aún sin cifrar mientras se migran.

### [3/Secrets/2]
Which encryption provider is recommended for production encryption at rest?
- [ ] `identity`, because it has the lowest overhead
- [x] `kms` (v2), backed by an external key management service
- [ ] `aescbc`, with the key stored in a ConfigMap
- [ ] `secretbox`, with the key hard-coded in the Pod spec
> Con **KMS v2** (estable desde 1.29) se usa cifrado de sobre: las claves que cifran los datos se protegen con una clave maestra que vive en un KMS externo, fuera del clúster, con rotación y auditoría. Con `aescbc`, `aesgcm` o `secretbox` la clave queda en un archivo del control plane.

### [3/Secrets/3]
After enabling encryption at rest, existing Secrets in etcd are still stored unencrypted. How do you encrypt them?
- [ ] Restart etcd, which re-encrypts every stored key during its startup
- [x] Rewrite them, e.g. `kubectl get secrets -A -o json | kubectl replace -f -`
- [ ] Delete the old EncryptionConfiguration file from every control plane node
- [ ] Wait 24 hours for the API server to migrate them on its own
> El cifrado solo se aplica cuando el objeto se escribe. Para cifrar los existentes hay que reescribirlos a través del API server; la documentación oficial usa `kubectl get secrets --all-namespaces -o json | kubectl replace -f -`.

### [3/Secrets/2]
Why is mounting Secrets as files often preferred over exposing them as environment variables?
- [ ] Files are encrypted automatically by the container runtime
- [x] Env vars leak more easily, e.g. into logs or child processes
- [ ] Environment variables cannot contain more than 64 characters
- [ ] Files are the only way to use Secrets with Deployments
> Las variables de entorno se heredan a procesos hijos, aparecen en volcados de errores o en `/proc/<pid>/environ` y es fácil que acaben en logs. Los archivos montados (en tmpfs) pueden tener permisos restrictivos y actualizarse sin reiniciar el contenedor.

### [3/Secrets/2]
What do you gain by marking a Secret as `immutable: true`?
- [ ] The Secret is encrypted with a stronger algorithm in etcd
- [x] Protection from accidental changes and less API server load
- [ ] The Secret becomes readable by every namespace
- [ ] The Secret is automatically rotated every 30 days by the kubelet
> Un Secret inmutable no se puede modificar (hay que borrarlo y crearlo de nuevo), lo que evita cambios accidentales o maliciosos que rompan aplicaciones. Además, el kubelet deja de vigilarlo, reduciendo la carga del API server en clústeres grandes.

### [3/Secrets/2]
Which tool synchronizes values from external managers such as HashiCorp Vault or AWS Secrets Manager into Kubernetes Secrets?
- [ ] cert-manager
- [x] External Secrets Operator
- [ ] Sealed Secrets
- [ ] kube-bench
> **External Secrets Operator** lee secretos de gestores externos y crea o actualiza Secrets de Kubernetes. El **Secrets Store CSI Driver** es otra opción que los monta directamente como volumen. **Sealed Secrets** cifra Secrets para guardarlos en Git; cert-manager gestiona certificados.

### [3/Secrets/2]
In KMS-based encryption at rest, what is envelope encryption?
- [ ] Encrypting each Secret twice with the same key
- [x] Data keys encrypt the data, and a KMS-held key encrypts the data keys
- [ ] Wrapping each Secret in a base64 envelope before storage
- [ ] Sending every Secret to the KMS to be stored there instead of etcd
> En el cifrado de sobre, cada dato se cifra con una clave de datos (DEK) y esa DEK se cifra con una clave maestra (KEK) que nunca sale del KMS externo. etcd guarda el dato cifrado junto con la DEK cifrada. Si alguien roba etcd, sin acceso al KMS no puede descifrar nada.

### [3/Secrets/1]
A Secret manifest contains `password: cGFzc3dvcmQ=`. What does that tell you?
- [ ] The password is encrypted with the cluster's KMS key
- [x] It is only base64-encoded and decodes to "password"
- [ ] The value is a SHA-256 hash that cannot be reversed
- [ ] The password is stored in Vault and this is a reference
> Los valores de `data` de un Secret solo están codificados en base64 para poder guardar datos binarios; cualquiera puede decodificarlos (`echo cGFzc3dvcmQ= | base64 -d`). Por eso no deben subirse a Git sin cifrar ni compartirse.

### [3/Isolation & Segmentation/2]
What is the most effective way to separate workloads with different trust levels inside one cluster?
- [ ] Put them in one namespace and tell them apart with different labels
- [x] Separate namespaces with RBAC, NetworkPolicies and Pod Security
- [ ] Give every workload its own container image registry
- [ ] Run them all as root so that permissions are consistent
> Los namespaces son la frontera lógica sobre la que se aplican RBAC, NetworkPolicies, Pod Security Admission y cuotas. Para cargas muy sensibles se añaden nodos dedicados o incluso clústeres separados. Etiquetas dentro del mismo namespace no aíslan nada.

### [3/Isolation & Segmentation/2]
How can you ensure that sensitive workloads never share nodes with untrusted workloads?
- [ ] By giving the sensitive Pods a higher PriorityClass
- [x] By using dedicated node pools with taints, tolerations and affinity
- [ ] By placing both kinds of workloads in different namespaces only
- [ ] By setting the same resource requests on all the Pods
> Los taints mantienen fuera de los nodos dedicados a las cargas que no los toleran, y la afinidad obliga a las cargas sensibles a ir a esos nodos. Así no comparten kernel con código no confiable. Los namespaces por sí solos no controlan en qué nodo corre cada Pod.

### [3/Isolation & Segmentation/2]
Which approach provides the strongest isolation between tenants?
- [ ] One namespace per tenant with shared nodes
- [x] A separate cluster for each tenant
- [ ] One Deployment per tenant in a shared namespace
- [ ] One ServiceAccount per tenant with the `edit` role
> Clústeres separados no comparten control plane, nodos ni red, así que ofrecen el aislamiento más fuerte (a cambio de más coste y operación). Los namespaces dan aislamiento lógico (*soft multi-tenancy*) que debe reforzarse con más controles.

### [3/Isolation & Segmentation/2]
What is a virtual cluster (for example vcluster)?
- [ ] A cluster whose nodes all run inside one single virtual machine
- [x] A tenant control plane running inside a namespace of a host cluster
- [ ] A namespace that has been renamed with a cluster prefix
- [ ] A read-only backup copy of the cluster stored in object storage
> En un clúster virtual, cada inquilino tiene su propio API server (y almacén de estado) que corre dentro de un namespace del clúster anfitrión, mientras que los Pods se programan en los nodos reales. Ofrece más aislamiento del control plane que un namespace, con menos coste que un clúster completo.

### [3/Isolation & Segmentation/2]
Why should each application use its own ServiceAccount instead of the namespace's `default` one?
- [ ] Because the `default` ServiceAccount cannot pull images
- [x] For per-app least privilege and auditable identities
- [ ] Because the `default` ServiceAccount is deleted every day
- [ ] Because Pods cannot start without a custom ServiceAccount
> Si todas las aplicaciones comparten el ServiceAccount `default`, cualquier permiso que necesite una lo tienen todas, y en los logs de auditoría no se distingue quién hizo qué. Un ServiceAccount por aplicación permite mínimo privilegio y trazabilidad.

### [3/Audit Logging/2]
Which audit level records request metadata (user, timestamp, resource, verb) but not the request or response bodies?
- [ ] None
- [x] Metadata
- [ ] Request
- [ ] RequestResponse
> Los niveles son **None** (no registra), **Metadata** (quién, qué, cuándo, sin cuerpos), **Request** (metadatos y cuerpo de la petición) y **RequestResponse** (metadatos y ambos cuerpos). Cada regla de la política asigna uno de ellos.

### [3/Audit Logging/2]
Why should requests involving Secrets be logged at the `Metadata` level rather than `RequestResponse`?
- [ ] Because the API server cannot audit Secrets at any other level
- [x] Because the bodies would write the secret values into the audit log
- [ ] Because `RequestResponse` disables encryption at rest for Secrets
- [ ] Because the Metadata level also blocks the request automatically
> Con `Request` o `RequestResponse`, el contenido del Secret (o de un TokenReview) quedaría en los logs de auditoría, que suelen enviarse a otros sistemas. Con `Metadata` se sabe quién leyó o cambió qué Secret, sin exponer su valor.

### [3/Audit Logging/2]
How are the rules of an audit policy evaluated?
- [ ] All matching rules are merged, and the highest level wins
- [x] In order; the first matching rule sets the level
- [ ] In alphabetical order of the resource names
- [ ] Randomly, so that log volume is spread evenly
> El API server compara cada evento con las reglas en orden y la **primera** que coincide determina el nivel. Por eso las reglas específicas (por ejemplo, Secrets a nivel Metadata) deben ir antes que las generales.

### [3/Audit Logging/2]
Which audit stage is generated as soon as the API server receives a request, before it is processed?
- [x] RequestReceived
- [ ] ResponseStarted
- [ ] ResponseComplete
- [ ] Panic
> Las etapas son **RequestReceived** (al recibirla), **ResponseStarted** (enviadas las cabeceras, en peticiones largas como *watch*), **ResponseComplete** (respuesta terminada) y **Panic** (si ocurre un pánico). Con `omitStages` se pueden excluir algunas para reducir volumen.

### [3/Audit Logging/2]
What happens if the kube-apiserver is started without `--audit-policy-file`?
- [ ] It logs every request at the RequestResponse level
- [x] No audit events are logged at all
- [ ] It refuses to start until a policy is provided
- [ ] It logs only requests that were denied by RBAC
> Sin archivo de política no se registra ningún evento de auditoría. Hay que definir una política (puede ser mínima, por ejemplo todo a nivel Metadata) y un backend (archivo con `--audit-log-path` o webhook).

### [3/Audit Logging/2]
Which audit backends does the Kubernetes API server support?
- [ ] Syslog and SNMP traps
- [x] A log file and a webhook to an external service
- [ ] Only the Kubernetes Events API
- [ ] A Prometheus exporter and a Grafana dashboard panel
> El API server puede escribir los eventos en un **archivo** (con rotación configurable) o enviarlos a un **webhook** externo (por ejemplo, un colector que los reenvía a un SIEM). Los Events de Kubernetes son otra cosa: información operativa de corta duración.

### [3/Audit Logging/2]
During an incident investigation, which question can the Kubernetes audit log answer?
- [ ] Which system calls a compromised container made
- [x] Who did what to which API resource, when and from where
- [ ] Which packets crossed the network between two Pods
- [ ] Which vulnerabilities exist in the deployed images
> El audit log registra cada petición al API server: usuario, grupos, verbo, recurso, namespace, IP de origen, momento y resultado. No ve lo que pasa dentro de los contenedores (para eso, Falco o Tetragon) ni el tráfico de red entre Pods.

### [3/Network Policy/3]
Which sources does this ingress rule allow?
```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        team: a
    podSelector:
      matchLabels:
        role: client
```
- [ ] All Pods in `team: a` namespaces, plus `role: client` Pods in the policy's namespace
- [x] Only Pods labeled `role: client` that run in namespaces labeled `team: a`
- [ ] Only Pods labeled `role: client`, in any namespace of the cluster
- [ ] Every Pod in every namespace, because both selectors are combined
> Cuando `namespaceSelector` y `podSelector` están en el **mismo** elemento de la lista `from`, se combinan con **AND**: Pods con `role: client` dentro de namespaces con `team: a`. Si fueran dos elementos separados (cada uno con su guion), sería un **OR**: todos los Pods de esos namespaces o los Pods `role: client` del namespace de la política. Es un error muy común.

### [3/Network Policy/2]
After applying a default-deny egress NetworkPolicy, Pods can no longer resolve DNS names. Why?
- [ ] NetworkPolicies always block the UDP protocol
- [x] Egress to the cluster DNS on port 53 must be explicitly allowed
- [ ] CoreDNS must be restarted after every NetworkPolicy change
- [ ] DNS only works when Pods use `hostNetwork: true`
> Un *default deny* de egress bloquea todo el tráfico saliente, incluidas las consultas a CoreDNS. Hay que añadir una regla que permita el egress hacia los Pods de DNS (normalmente en `kube-system`) en el puerto 53, por UDP y TCP.

### [3/Network Policy/2]
How do several NetworkPolicies that select the same Pod combine?
- [ ] The most restrictive policy wins and the others are ignored
- [x] Their allowed traffic is combined as a union
- [ ] The policy that was created last overrides the earlier ones
- [ ] They conflict, and the API server rejects the newer policy
> Las NetworkPolicies son aditivas: el tráfico permitido a un Pod es la unión de lo que permiten todas las políticas que lo seleccionan. No hay orden ni conflictos, y una política no puede quitar lo que otra permite.

### [3/Network Policy/2]
Can a standard Kubernetes NetworkPolicy explicitly deny one specific source while allowing everything else?
- [ ] Yes, with an `action: Deny` field in the ingress rule
- [x] No; it can only allow traffic, so you deny by not allowing
- [ ] Yes, by giving the policy a higher `priority` value
- [ ] Yes, by setting `policyTypes: [Deny]` on the policy
> La API estándar de NetworkPolicy solo tiene reglas de permiso. Se trabaja con denegación por defecto y permisos explícitos (un `ipBlock` admite `except` para excluir rangos dentro de un bloque permitido). Para reglas de denegación explícitas o con prioridades se usan extensiones del CNI (Calico, Cilium) u otras APIs de políticas.

### [3/Network Policy/2]
Which NetworkPolicy peer type allows traffic from an external CIDR range?
- [ ] `namespaceSelector`
- [ ] `podSelector`
- [x] `ipBlock`
- [ ] `serviceSelector`
> `ipBlock` define rangos CIDR (con `except` opcional) para tráfico que entra o sale del clúster. `podSelector` y `namespaceSelector` seleccionan Pods por labels, y `serviceSelector` no existe en la API.

### [3/Network Policy/2]
At which layers do standard Kubernetes NetworkPolicies operate?
- [ ] Layer 7 only, matching on HTTP paths and methods
- [x] Layers 3 and 4: IP addresses, ports and protocols
- [ ] Layer 2 only, matching on MAC addresses
- [ ] All layers, including the TLS certificates of clients
> Las NetworkPolicies estándar filtran por Pods/namespaces/IPs, puertos y protocolo (TCP, UDP, SCTP). Para reglas de capa 7 (rutas HTTP, métodos, identidades) se usa un service mesh o extensiones del CNI como las políticas L7 de Cilium.

### [3/Network Policy/2]
Which label does Kubernetes set automatically on every namespace, making it easy to select a namespace by name in a `namespaceSelector`?
- [ ] `namespace.kubernetes.io/id`
- [x] `kubernetes.io/metadata.name`
- [ ] `k8s.io/namespace-name`
- [ ] `metadata.kubernetes.io/ns`
> Desde Kubernetes 1.22, cada namespace lleva automáticamente la label `kubernetes.io/metadata.name: <nombre>`, que no se puede cambiar. Permite referirse a un namespace concreto en un `namespaceSelector` sin depender de labels manuales que alguien podría editar.

### [3/Network Policy/2]
What is the scope of a NetworkPolicy object?
- [ ] It is cluster-scoped and applies to every Pod in the cluster by default
- [x] It is namespaced, and its podSelector targets Pods in its namespace
- [ ] It applies to nodes, not to Pods, in the selected namespace
- [ ] It applies only to Services of type LoadBalancer
> Una NetworkPolicy vive en un namespace y su `podSelector` elige Pods de ese mismo namespace (un selector vacío `{}` los elige todos). Las reglas `from`/`to` sí pueden referirse a Pods de otros namespaces mediante `namespaceSelector`.
