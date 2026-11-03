# Evidencia de copia y restauración de laboratorio

**Fecha local:** 2026-11-02  
**Herramienta:** WinRAR 7.23 x64 (edición de evaluación)  
**Conjunto:** `examples/sample_access_events.jsonl`, archivo JSONL sintético de 671 bytes sin datos reales.  
**Archivo de respaldo local:** `tmp/actividad4-backup/Actividad4-Prueba-Backup.rar` (ignorado por Git y no incluido en el repositorio público).  
**Tamaño del archivo RAR:** 352 bytes.

## Resultado comprobable

- WinRAR creó el archivo RAR correctamente.
- La prueba de integridad del archivo RAR terminó con **“Todo correcto”**.
- Se restauró el archivo a una carpeta separada; la extracción terminó con **“Todo correcto”**.
- SHA-256 del archivo fuente: `03E9DE440307215CFD9F94C982580E99E71C1E5548E45954B221682D3F76E099`.
- SHA-256 del archivo restaurado: `03E9DE440307215CFD9F94C982580E99E71C1E5548E45954B221682D3F76E099`.
- Los hashes coinciden; el contenido restaurado es idéntico al original.
- Registro de la prueba: [`../../templates/registro_prueba_restauracion.csv`](../../templates/registro_prueba_restauracion.csv).

## Alcance y limitaciones

Esta es una prueba académica con datos ficticios. El RAR quedó en el mismo disco local que la carpeta de prueba y no está cifrado; por tanto, **no** demuestra una estrategia 3-2-1 ni protege datos de producción. El archivo RAR no se versiona porque los respaldos no deben almacenarse en este repositorio público. Si el instructor solicita el archivo, adjuntar el archivo local de prueba por el canal de entrega que él indique; nunca sustituirlo por un respaldo con datos personales.
