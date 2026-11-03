# Evidencias prácticas de cierre

El análisis, el consentimiento modelo, el guion, el póster, las políticas y los scripts están preparados. La prueba de copia y restauración ya se realizó con un archivo ficticio y está registrada en [`evidencia_backup_winrar.md`](04_backups/evidencia_backup_winrar.md). La evidencia externa que falta es publicar o compartir la presentación narrada de Powtoon.

## 1. Presentación Powtoon con narración

Material listo:

- Guion de 6 escenas y texto de narración: [`guion_presentacion.md`](05_habeas_data_derechos_autor/guion_presentacion.md).
- Póster para insertar: [`poster_herramientas_backup.svg`](04_backups/poster_herramientas_backup.svg).
- Contenido de casos, normas y créditos: [`marco_normativo_y_casos.md`](05_habeas_data_derechos_autor/marco_normativo_y_casos.md).

Pasos para producir la evidencia:

1. Crea una presentación/video nuevo en Powtoon y titúlalo **Habeas Data, autoría y respaldo seguro**.
2. Crea seis escenas siguiendo el guion. Incluye el contexto académico y el nombre del aprendiz.
3. Graba o genera la narración en español usando el texto de cada escena. Revisa que el audio se escuche en todas las escenas y que la duración final sea de 3 a 4 minutos.
4. Inserta el póster SVG o una imagen derivada de él. Usa únicamente imágenes, íconos y música propios o con licencia compatible; agrega créditos al final.
5. Reproduce el video completo para verificar sincronización, lectura y pronunciación. Exporta o publica según las opciones habilitadas por tu cuenta y las instrucciones del instructor.
6. Guarda en este repositorio el archivo o enlace final y una captura de la vista de publicación/reproducción. Si la cuenta no permite exportar, conserva el enlace de visualización y una captura donde se vean el título y las escenas.

**Evidencia final:**

- Enlace al proyecto/video: `[pegar enlace]`
- Archivo exportado (si está permitido): `[ruta o nombre]`
- Captura de publicación/reproducción: `[ruta]`
- Duración comprobada: `[mm:ss]`

## 2. Copia y restauración con WinRAR: realizada

Se creó un archivo de prueba con **WinRAR 7.23**, se comprobó el archivo RAR, se restauró en otra carpeta y se comparó SHA-256. Los hashes coincidieron. El origen es el archivo sintético `examples/sample_access_events.jsonl`; no se usaron datos personales.

El informe de evidencia está en [`evidencia_backup_winrar.md`](04_backups/evidencia_backup_winrar.md) y el registro actualizado en [`registro_prueba_restauracion.csv`](../templates/registro_prueba_restauracion.csv). El archivo RAR está guardado localmente en `tmp/actividad4-backup/Actividad4-Prueba-Backup.rar`; se excluyó de GitHub porque es un archivo de respaldo.

La prueba se hizo en el mismo disco local y el archivo no está cifrado. Sirve como práctica verificable con herramienta instalada, pero no es un respaldo externo ni una estrategia de producción. Si el profesor pide el archivo, entrégalo aparte por el canal autorizado.

## Lista de cierre antes de entregar

- [ ] Abrir `output/pdf/Actividad 4.pdf` y revisar que los datos académicos estén correctos.
- [ ] Reemplazar campos entre corchetes del consentimiento si el instructor solicita un caso concreto; no inventar una empresa real.
- [ ] Completar y adjuntar el Powtoon con narración y su evidencia.
- [x] Ejecutar y documentar la copia/restauración de laboratorio con WinRAR.
- [ ] Añadir los enlaces o evidencias no sensibles a este repositorio público.
- [ ] Revisar el contenido y entregar al instructor el enlace al repositorio y el PDF.
