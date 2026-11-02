# Identificación y mejora del tratamiento seguro de información

## Ciclo de mejora

1. **Inventariar:** identificar activo, propietario, ubicación, clase de información, usuarios y dependencias.
2. **Evaluar:** estimar amenaza, debilidad, probabilidad e impacto en confidencialidad, integridad, disponibilidad y derechos de titulares.
3. **Priorizar:** ordenar por riesgo, exposición, facilidad de abuso y consecuencias operativas o para las personas.
4. **Tratar:** reducir, evitar, compartir o aceptar el riesgo mediante un responsable y una fecha; la aceptación requiere autoridad documentada.
5. **Verificar:** revisar evidencia de implementación y probar recuperación/controles con datos ficticios o autorizados.
6. **Aprender:** actualizar políticas, permisos, formación, plantillas y riesgos después de incidentes, cambios y auditorías.

## Controles propuestos

| Área | Control de mejora | Evidencia esperada |
|---|---|---|
| Minimización | Recoger solo datos necesarios para una finalidad concreta | Inventario de datos y formulario revisado |
| Finalidad y autorización | Informar finalidades y obtener autorización previa, expresa e informada cuando corresponda | Versión aprobada de aviso/política y registro de autorización |
| Acceso | Revisar roles, MFA administrativo, altas/bajas y acceso temporal | Matriz de permisos, tickets y revisión periódica |
| Almacenamiento | Restringir carpetas, usar cifrado y ubicación aprobada | Configuración y prueba de acceso autorizado/denegado |
| Monitoreo | Centralizar eventos relevantes y limitar acceso a logs | Alertas, revisión y registro de disposición |
| Integridad | Hash de manifiestos y cambios aprobados | Manifiesto SHA-256 y ticket |
| Respaldo | Copias separadas, protegidas y probadas | Logs de ejecución y restauración |
| Conservación | Retener solo por tiempo definido; borrar de forma segura cuando proceda | Tabla de retención y certificado/registro de disposición |
| Derechos de autor | Mantener licencias y atribuciones; retirar copias no autorizadas | Inventario de contenidos y comprobante de licencia |

## Matriz breve de riesgos

Completar `../../templates/matriz_riesgos.csv` por activo. La calificación 1-5 es una escala relativa del ejercicio, no una evaluación certificada.

| Riesgo | Prob. | Impacto | Tratamiento inicial |
|---|---:|---:|---|
| Cuenta de técnico no revocada tras cambio de rol | 3 | 4 | Revisión de accesos y baja basada en ticket |
| Robo de portátil con tickets locales | 3 | 4 | Cifrado de disco, bloqueo, minimización y borrado remoto autorizado |
| Copia de backup accesible desde la misma cuenta comprometida | 3 | 5 | Cuenta separada, MFA, aislamiento/inmutabilidad cuando esté disponible |
| Consentimiento genérico sin finalidad clara | 2 | 4 | Formularios por finalidad, aviso visible y evidencia de selección voluntaria |
| Archivo de software/libro compartido sin licencia | 2 | 3 | Verificar fuente/licencia, usar alternativas autorizadas y registrar procedencia |

## Indicadores de seguimiento

- Porcentaje de cuentas privilegiadas revisadas en el período.
- Porcentaje de cuentas vencidas o sin propietario con acción de corrección.
- Tiempo medio para revocar acceso tras una baja notificada.
- Éxito de respaldos y porcentaje de restauraciones de prueba exitosas.
- Hallazgos vencidos de seguridad y porcentaje con evidencia de cierre.
- Incidentes relacionados con usos no autorizados o finalidad no documentada.

Definir valores objetivo, periodicidad y responsable con el cliente; no inventar métricas operativas si todavía no existe una línea base.
