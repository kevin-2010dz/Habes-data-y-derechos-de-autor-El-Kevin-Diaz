# Monitoreo del acceso a almacenamiento y activos de información

## Objetivo

Detectar accesos indebidos, cambios no aprobados y actividad anómala en archivos, carpetas compartidas, repositorios, bases de datos, almacenamiento de backups y dispositivos que procesan información.

## Fuentes a revisar

- Registros de inicio de sesión y autenticación: éxito, fallo, MFA y sesión administrativa.
- Auditoría de archivos: lectura, creación, edición, borrado, cambio de permisos y descarga masiva, cuando la plataforma lo registre.
- Acceso remoto, VPN, administración de endpoints, NAS/servidores y consola de respaldos.
- Tickets/cambios aprobados que permitan distinguir tarea autorizada de actividad inesperada.

## Campos mínimos

Marca de tiempo en UTC o zona documentada; identificador de usuario seudónimo; activo/recurso; tipo de acción; resultado; origen técnico proporcional (host o IP si es necesario); identificador de ticket; fuente del evento. Evitar incluir contenido del archivo, credenciales o datos sensibles que no se requieren para auditar.

## Revisión propuesta

| Revisión | Frecuencia inicial | Responsable sugerido |
|---|---|---|
| Alertas de accesos denegados repetidos, privilegio administrativo o cambios de permisos | Diaria en días hábiles; alertas críticas inmediatas | Seguridad / administrador de guardia |
| Cambios en carpetas sensibles y repositorios de backup | Diaria | Propietario del activo |
| Accesos privilegiados y cuentas inactivas | Semanal | Seguridad y administración de sistemas |
| Revisión de excepciones y muestra de accesos | Mensual | Responsable del proceso |
| Revisión de roles y retención de logs | Trimestral | Propietario del dato y seguridad |

Las frecuencias son una línea base académica y deben ajustarse a volumen, riesgo, servicio y capacidad de respuesta. En los sistemas críticos se requiere cobertura y escalamiento fuera de horario definidos.

## Priorización y respuesta

- **Alta:** cuenta privilegiada inesperada, modificación de ACL sin cambio aprobado, lectura/descarga masiva inusual, borrado de backups o señales de exfiltración. Abrir incidente inmediatamente, proteger evidencia, contener de forma coordinada y escalar.
- **Media:** fallos de autenticación concentrados, intento de acceso denegado a recurso restringido o cuenta fuera de horario. Correlacionar con cambios, validar con responsable y documentar.
- **Baja:** evento esperado con cambio/ticket asociado. Revisar por muestreo y conservar según retención aprobada.

## Procedimiento de revisión

1. Confirmar integridad, zona horaria y fuente del registro.
2. Correlacionar usuario, activo, rol y ticket aprobado.
3. Identificar desviaciones y registrar evidencia mínima, sin copiar el contenido del dato.
4. Asignar dueño, prioridad, plazo y acción de contención/investigación.
5. Cerrar solo con explicación, evidencia de corrección y, si aplica, aprobación del propietario del activo.

## Ejemplo reproducible

`examples/sample_access_events.jsonl` contiene identidades ficticias. Para ejecutar reglas básicas:

```powershell
python scripts/audit_access_log.py examples/sample_access_events.jsonl
```

El script busca resultados denegados, acciones privilegiadas, descargas masivas marcadas y cambios de permisos. Es un analizador didáctico por reglas; no sustituye un SIEM, la revisión humana ni la validación de integridad del origen.
