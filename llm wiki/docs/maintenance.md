# Wiki & Source Management Guide

Este documento describe los procedimientos para mantener la integridad de la base de conocimientos de la Academia de Tenis.

---

## 📂 Gestión de Fuentes (`raw/`)

Las "Raws" son los documentos originales (mails, folletos, etc.) que sirven como base para la Wiki.

### Borrar una fuente
*   **Acción**: Borrá el archivo de `llm wiki/raw/`.
*   **Impacto**: La Wiki correspondiente queda sin respaldo.
*   **Procedimiento**: Después de borrar, pedí al agente que limpie las referencias en la Wiki y el `index.md`.

### Actualizar una fuente
*   **Acción**: Reemplazá el archivo en `raw/` con la nueva versión.
*   **Procedimiento**: Pedí al agente: *"Actualicé la fuente [Nombre], volvé a procesarla"*.

---

## 📝 Gestión de Wikis (`wiki/`)

Las "Wikis" son la información curada y sanitizada.

### Actualizar una Wiki
*   **Manual**: Editá el archivo `.md` directamente. 
    *   Actualizá el campo `Last updated` en el frontmatter.
    *   Registrá el cambio en `wiki/log.md`.
*   **Automático**: Si tenés un mail nuevo, usá `scripts/sync_emails.py`.

### Borrar una Wiki
*   **Acción**: Borrá el archivo `.md` de `wiki/`.
*   **Mantenimiento Obligatorio**: 
    1.  Eliminá el link en `wiki/index.md`.
    2.  Registrá la eliminación en `wiki/log.md`.

---

## 🧩 Consolidación de Conocimiento

Cuando existen múltiples archivos para el mismo tema (ej: `re-` duplicados o hilos de mail largos):

### Procedimiento
1. **Unificar**: Elegí el archivo con el nombre más claro y mergeá la información relevante de los otros.
2. **Borrar Duplicados**: Borrá las Wikis y las Raws sobrantes.
3. **Redirigir**: Actualizá `index.md` y cualquier link en otras páginas (`pricing.md`, etc.).
4. **Log**: Registrá la consolidación en `wiki/log.md`.

---

## 🛠️ Herramientas Útiles

*   **`scripts/sync_emails.py`**: Sincroniza mails nuevos desde Gmail.
*   **`scripts/cleanup_wiki.py`**: Normaliza nombres de archivos y elimina duplicados exactos.
*   **`scripts/cleanup_pii.py`**: Sanitiza información personal en todo el proyecto.
