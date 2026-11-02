# Gestión y planificación de copias de seguridad

## Objetivo y alcance

Proteger la disponibilidad e integridad de documentación, inventarios, configuraciones autorizadas, tickets y registros necesarios para la operación de una mesa de ayuda. Excluir credenciales y secretos del backup genérico; gestionarlos en un almacén dedicado y aprobado. Cada dueño del servicio debe clasificar datos, aprobar RPO/RTO y validar obligaciones de conservación.

## Tipos de copia

| Tipo | Qué copia | Ventaja | Consideración |
|---|---|---|---|
| Completa | Todo el conjunto seleccionado | Restauración simple | Más almacenamiento y ventana |
| Incremental | Cambios desde la copia anterior (según la herramienta) | Menor tiempo y espacio por ejecución | La recuperación puede depender de la cadena |
| Diferencial | Cambios desde la última completa | Cadena más corta que incrementales | Crece hasta la siguiente completa |
| Instantánea / exportación de configuración | Estado puntual de volumen o configuración | Rápida para ciertos activos | No siempre equivale a una copia independiente |
| Archivo versionado | Versiones de archivos y metadatos | Recupera errores y cambios | Validar límites y retención del producto |

## Frecuencia y objetivos propuestos para el ejercicio

| Grupo | Ejemplo | Tipo y frecuencia inicial | RPO objetivo | RTO objetivo |
|---|---|---|---:|---:|
| Crítico | Configuración de autenticación, inventario esencial | Incremental cada 4 h y completa semanal | 4 h | 8 h |
| Operativo | Tickets, documentación de soporte | Incremental diaria y completa semanal | 24 h | 1 día hábil |
| Configuración de red | Exportar después de cambio aprobado y copia semanal | Por cambio + semanal | 1 cambio | 4 h |
| Archivo histórico | Evidencia cerrada y documentos de referencia | Completa mensual | 30 días | 3 días hábiles |

RPO (punto de recuperación) y RTO (tiempo de recuperación) son objetivos de diseño para discutir con el cliente, no garantías. Confirmarlos con impacto de negocio, capacidad, costo y pruebas.

## Retención y protección

- Propuesta inicial: 7 copias diarias, 4 semanales, 12 mensuales y 1 anual cuando el propietario apruebe que se requiere esa duración.
- Aplicar la regla 3-2-1 como objetivo: mantener varias copias, en medios diferentes y al menos una separada del entorno primario. Considerar copia offline/inmutable para amenazas de ransomware si la plataforma lo soporta.
- Cifrar copias en tránsito y reposo en las herramientas elegidas; custodiar llaves separadas y controlar su acceso.
- Proteger consola y repositorio con cuentas separadas, MFA, mínimo privilegio y registro de acciones administrativas.
- Definir retención por clasificación, finalidad, necesidad de recuperación y obligaciones aplicables. No fijar retención indefinida por defecto.
- El script educativo de este repo no cifra, no genera copias externas y no implementa inmutabilidad. No usarlo para datos personales reales.

## Procedimiento de respaldo

1. Aprobar fuente, responsable, clasificación, destino, tipo, frecuencia, RPO/RTO y retención.
2. Confirmar espacio, acceso del operador, sincronización horaria y ventana de mantenimiento.
3. Ejecutar una copia a repositorio separado y protegido; registrar hora, conjunto, resultado, tamaño y hash.
4. Verificar el formato/hash de manera automática y revisar alertas o fallos.
5. Cerrar la evidencia con ticket. Ante fallo, abrir incidente, proteger la última copia válida y notificar al dueño del servicio.

## Prueba de restauración de laboratorio

1. Crear un archivo ficticio de texto dentro de `examples/` o una carpeta temporal de laboratorio.
2. Ejecutar: `python scripts/backup.py --source examples --destination backups`.
3. Ejecutar el comando de verificación que se imprime/documenta: `python scripts/backup.py --verify <ruta-del-zip>`.
4. Extraer el ZIP en un directorio temporal vacío. Verificar que el archivo de prueba abra y coincida en tamaño/contenido con la fuente.
5. Eliminar la carpeta temporal manualmente después de validar; no apuntar el ensayo a datos productivos.
6. Completar `../../templates/registro_prueba_restauracion.csv`: fecha, conjunto de prueba, resultado, duración, desviaciones, responsable y aprobación.

## Recuperación ante incidente

1. Declarar incidente y asignar líder técnico y responsable de negocio.
2. Contener el activo afectado; no montar una copia sospechosa sobre el entorno limpio.
3. Identificar última copia conocida como válida, verificar manifiesto y proteger evidencia.
4. Restaurar primero en entorno aislado; escanear y validar integridad, permisos y dependencias.
5. Obtener aprobación del dueño del sistema para pasar a operación.
6. Documentar RPO/RTO real, datos faltantes, causa, comunicaciones y acciones correctivas.
7. Revisar accesos a repositorio/consola y rotar secretos si pudieron verse comprometidos.
