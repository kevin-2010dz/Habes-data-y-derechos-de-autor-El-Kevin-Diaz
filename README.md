# Guía 4 de Ciberseguridad: Habeas Data, derechos de autor y copias de seguridad

Repositorio académico para desarrollar la **Actividad 4** de la guía `03_04_HABEAS_DATA_DERECHOS_DE_AUTOR_Y_TIPOS_DE_COPIA_DE_SEGURIDAD` y organizar los controles de ciberseguridad solicitados para la mesa de ayuda.

> **Carácter académico:** los procedimientos, formatos, frecuencias y datos de contacto son modelos para adaptar. No representan una política aprobada por una empresa ni asesoría jurídica. Antes de aplicarlos, el responsable debe completar los campos pendientes, validar las normas vigentes y aprobar los controles.

## Contexto de formación

- **Programa:** Técnico en Sistemas Teleinformáticas, código 233108 V1.
- **Proyecto:** Integración de servicios tecnológicos, hardware, software y redes de datos en una mesa de ayuda (2093369).
- **Fase:** Planeación.
- **Actividad de proyecto:** diseñar planes de mantenimiento preventivo y correctivo de sistemas de cómputo y equipos activos de red de acuerdo con las necesidades del cliente.
- **Competencia:** 220501121, Operación de herramientas informáticas.
- **Resultado de aprendizaje:** RAP 03, planificar la información según criterios de ciberseguridad.

## Introducción

La información de una mesa de ayuda puede contener datos de usuarios, inventarios, credenciales, registros de incidentes, configuraciones de red y documentos con licencia. Su tratamiento requiere controlar quién accede, registrar operaciones relevantes, corregir debilidades y poder recuperar información cuando se pierde o se altera. También exige reconocer los derechos de los titulares de datos personales y de los autores de obras.

Este repositorio convierte la guía en materiales prácticos: análisis de casos colombianos, políticas modelo, matrices y formularios, una guía de herramientas de respaldo y dos scripts pequeños para crear/verificar copias ZIP y revisar eventos de auditoría JSONL.

## Objetivos

1. Clasificar la información y asignar accesos de acuerdo con el rol y el principio de mínimo privilegio.
2. Definir qué accesos a archivos y activos registrar, revisar y escalar.
3. Proponer un ciclo de mejora para tratar la información de manera segura y respetar Habeas Data y derechos de autor.
4. Planificar respaldos con tipos, frecuencia, retención, verificación y recuperación.
5. Entregar formatos y scripts reproducibles para practicar los controles en un entorno de laboratorio.

## Justificación

El acceso excesivo, la divulgación sin autorización, el uso de datos para finalidades distintas, la pérdida de evidencia y las copias no probadas pueden afectar la confidencialidad, integridad y disponibilidad de la información. Definir responsables, autorizaciones, registros y recuperación antes de un incidente reduce errores operativos y ayuda a demostrar que se aplican controles. La guía también pide distinguir datos personales y sensibles, respetar licencias y construir un consentimiento informado.

## Desarrollo de la guía

La carpeta [`docs/05_habeas_data_derechos_autor/`](docs/05_habeas_data_derechos_autor/) responde a las seis partes del documento original:

1. Resuelve los casos de contacto financiero sin fuente clara y de distribución de un libro sin licencia.
2. Distingue los datos personales, sensibles y de niñas, niños y adolescentes en los casos de Carlos, la clínica y el colegio.
3. Resume el marco colombiano, identifica a la SIC y a la DNDA, y documenta una sanción SIC de 2025 con fuente primaria.
4. Incluye un formulario modelo de autorización con casillas sin marcar, finalidades explícitas, alternativa para no consentir y campos editables para la política y canales reales.
5. Presenta un póster SVG con las familias de herramientas de backup citadas en la guía.
6. Describe una práctica de respaldo y recuperación segura, con evidencias que el estudiante puede completar al ejecutar el ejercicio.

Los ejes de ciberseguridad solicitados están desarrollados en las carpetas [`docs/01_control_accesos/`](docs/01_control_accesos/), [`docs/02_monitoreo/`](docs/02_monitoreo/), [`docs/03_mejora/`](docs/03_mejora/) y [`docs/04_backups/`](docs/04_backups/).

## Estructura

```text
.
├── README.md
├── SECURITY.md
├── .gitignore
├── docs/
│   ├── 00_contexto/                 # alcance, trazabilidad y supuestos
│   ├── 01_control_accesos/         # política y matriz de privilegios
│   ├── 02_monitoreo/                # eventos, revisión y escalamiento
│   ├── 03_mejora/                   # evaluación de riesgos y acciones
│   ├── 04_backups/                  # estrategia, recuperación y póster
│   └── 05_habeas_data_derechos_autor/ # seis partes de la guía
│   └── 06_evidencias_pendientes.md   # pasos para producir evidencia externa real
├── examples/
│   └── sample_access_events.jsonl
├── output/
│   └── pdf/Actividad 4.pdf        # entrega integrada en PDF
├── scripts/
│   ├── backup.py
│   ├── audit_access_log.py
│   └── build_activity_pdf.py
└── templates/
    ├── inventario_activos.csv
    ├── matriz_riesgos.csv
    └── registro_prueba_restauracion.csv
```

## Entrega integrada

El PDF [`output/pdf/Actividad 4.pdf`](output/pdf/Actividad%204.pdf) reúne el contexto académico, la introducción, objetivos, justificación y el desarrollo de los seis apartados de la guía, junto con el consentimiento modelo, el guion de presentación y el plan de respaldo. Para regenerarlo con Python y ReportLab, ejecutar `python scripts/build_activity_pdf.py` en un entorno que tenga ReportLab instalado. El archivo PDF listo para revisión ya está incluido; el script de generación es reproducible.

La presentación Powtoon narrada y la evidencia de ejecución/restauración en una herramienta de backup deben generarse desde las cuentas o equipos donde se utilizan. El repositorio ya contiene el guion, el póster, el procedimiento y un registro para documentarlas. Sigue [`docs/06_evidencias_pendientes.md`](docs/06_evidencias_pendientes.md); no subas respaldos reales o datos sensibles.

## Uso rápido de los scripts

Requiere Python 3.10 o posterior, sin dependencias externas.

```powershell
python scripts/backup.py --source .\examples --destination .\backups
python scripts/backup.py --verify .\backups\backup-AAAAmmdd-HHMMSS.zip
python scripts/audit_access_log.py .\examples\sample_access_events.jsonl
```

El primer comando crea un archivo ZIP y un manifiesto SHA-256; el segundo comprueba la estructura del ZIP y los hashes del manifiesto; el tercero informa eventos permitidos/denegados y patrones marcados por reglas básicas. Son demostraciones locales: no cifran, no sincronizan con nube ni sustituyen un sistema de copias empresarial o un SIEM.

## Verificación y uso responsable

- Los scripts usan únicamente la biblioteca estándar y no envían datos a Internet.
- `backup.py` no elimina copias antiguas de forma automática. La limpieza requiere `--apply-retention` explícito.
- `audit_access_log.py` espera JSONL con identificadores seudónimos; no incluyas contraseñas, tokens ni datos reales de clientes en los ejemplos.
- La copia no se considera recuperable hasta completar una restauración de prueba y registrar su resultado.
- No subas a un repositorio público archivos de clientes, credenciales, bases de datos, backups, logs reales ni materiales de terceros sin permiso.
- La visibilidad pública del repositorio no concede por sí sola una licencia sobre las obras o contenidos incluidos. Consulta [`RIGHTS.md`](RIGHTS.md).

## Fuentes normativas y de consulta

Las fuentes principales están enlazadas junto al análisis en [`docs/05_habeas_data_derechos_autor/marco_normativo_y_casos.md`](docs/05_habeas_data_derechos_autor/marco_normativo_y_casos.md). Entre ellas: Constitución Política (artículos 15 y 61), Ley 1581 de 2012 y Decreto 1074 de 2015 para protección de datos; Ley 1266 de 2008 para información financiera, crediticia y comercial; Ley 23 de 1982, Ley 1915 de 2018 y Decisión Andina 351 de 1993 para derecho de autor. La SIC ejerce funciones de vigilancia y sanción en protección de datos personales; la DNDA es la autoridad nacional en derecho de autor.

## Mantenimiento del material

Revisar periódicamente las normas, enlaces, responsables, frecuencias de respaldo, permisos y retenciones; registrar cambios; comprobar que las copias puedan restaurarse; y actualizar la matriz de accesos cuando cambien funciones o se retiren usuarios. El responsable académico puede completar nombre del aprendiz, ficha, instructor y fecha de entrega en [`docs/00_contexto/entrega_academica.md`](docs/00_contexto/entrega_academica.md).
