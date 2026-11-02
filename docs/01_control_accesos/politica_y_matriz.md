# Política modelo de clasificación de privilegios y acceso

**Estado:** propuesta académica para aprobación. **Responsable:** completar por la organización. **Revisión:** semestral y ante cambios relevantes.

## 1. Propósito y alcance

Definir cómo solicitar, aprobar, otorgar, revisar y revocar acceso a equipos, sistemas, redes, carpetas, respaldos y registros de la mesa de ayuda. Aplica a funcionarios, aprendices, contratistas y proveedores con acceso autorizado.

## 2. Clasificación de información

| Nivel | Ejemplos | Reglas mínimas |
|---|---|---|
| Pública | Manuales aprobados, información publicada | Integridad y publicación autorizada |
| Interna | Inventario sin datos de usuarios, procedimientos | Solo cuentas institucionales; no publicar sin aprobación |
| Confidencial | Tickets identificables, configuraciones, logs, datos de contacto | Acceso por necesidad, cifrado en tránsito/almacenamiento cuando aplique, registro de accesos |
| Restringida | Credenciales, secretos, biometría, información sensible o copias completas de datos personales | Acceso excepcional, aprobación reforzada, almacenamiento dedicado, auditoría y retención limitada |

Asignar el nivel más alto que corresponda a los datos contenidos. Reducir o anonimizar datos antes de usarlos en capacitación o evidencia.

## 3. Principios

- Mínimo privilegio y necesidad de saber: cada cuenta recibe solo permisos requeridos para su función y por el tiempo necesario.
- Cuenta individual; no compartir credenciales. Las cuentas de servicio tienen propietario, propósito, alcance y rotación definidos.
- Separación entre quien solicita y quien aprueba accesos privilegiados.
- Autenticación reforzada para administración y acceso remoto cuando la plataforma lo permita.
- Acceso temporal para proveedores, con vencimiento y supervisión.
- Revisiones trimestrales para permisos privilegiados y semestrales para los demás; al terminar una relación o función, revocar de inmediato.
- Las excepciones registran justificación, responsable, alcance y fecha de expiración.

## 4. Matriz inicial de roles

| Rol | Tickets asignados | Inventario | Logs de seguridad | Gestión de cuentas | Respaldos | Configuración de red |
|---|---:|---:|---:|---:|---:|---:|
| Usuario solicitante | Propios, lectura | No | No | No | No | No |
| Agente mesa de ayuda | Asignados, según caso | Lectura/actualización limitada | Eventos de sus casos | No | No | No |
| Técnico de infraestructura | Necesarios para soporte | Lectura/actualización | Lectura operativa | No | Operación por cambio aprobado | Según cambio aprobado |
| Administrador de sistemas | Necesarios | Administración | Lectura/gestión | Administración con MFA | Administración | Según alcance |
| Responsable de seguridad/auditor | Lectura bajo alcance | Lectura | Lectura y revisión | Revisión, no administración rutinaria | Evidencia y revisión | Lectura/auditoría |
| Proveedor | Solo caso y ventana aprobada | No por defecto | No por defecto | No | No | Temporal y supervisado |

La matriz es inicial: se debe ajustar por sistema y validar con el responsable del activo. El acceso a datos personales debe obedecer la finalidad autorizada y las instrucciones del responsable del tratamiento.

## 5. Flujo de alta, cambio y baja

1. El jefe o responsable del proceso registra usuario, sistema, rol, finalidad, alcance, duración y ticket de cambio.
2. El propietario del activo valida necesidad y clasificación de datos. Para privilegio administrativo, un segundo aprobador confirma.
3. El administrador crea una cuenta individual, aplica rol/grupo y autenticación requerida; registra fecha, aprobador y evidencia.
4. Al cambiar de función, comparar permisos anteriores y nuevos; retirar lo innecesario.
5. Al retiro o vencimiento, deshabilitar la cuenta y revocar tokens, llaves, sesiones, VPN y accesos de terceros; conservar evidencia según política aprobada.
6. Cada trimestre revisar cuentas privilegiadas y cada semestre el resto; cerrar hallazgos con responsable y fecha.

## 6. Evidencia de auditoría

Registrar mínimo: usuario/identificador seudónimo, recurso, acción, resultado, fecha/hora sincronizada, origen técnico necesario y ticket/justificación cuando sea una acción administrativa. No registrar contraseñas, tokens ni contenido completo de documentos. Restringir acceso a logs y definir una retención aprobada según finalidad, riesgo y obligaciones aplicables.

## 7. Excepciones y violaciones

Acceso sin autorización, cuenta compartida, privilegio innecesario o manipulación de logs se reporta por el proceso de incidentes. Preservar evidencia, contener el acceso y escalar al propietario del activo y responsable de seguridad. No borrar ni alterar evidencia durante la respuesta.
