# Patrones Diátaxis para documentación de usuario final

El framework Diátaxis distingue cuatro tipos de documentación según la necesidad del lector.
Aquí están adaptados al contexto específico de documentación para usuarios finales no técnicos.

## Los cuatro tipos de documento

### 1. Tutorial (Guía de inicio / Getting Started)

**Para quién:** Usuarios nuevos que no conocen el producto.

**Objetivo:** Que el usuario complete un flujo real de principio a fin y se sienta capaz de
usar la aplicación. Al terminar, debe haber logrado algo tangible (ej: "crear tu primera
reserva", "configurar tu perfil").

**Estructura tipo:**
```
# Tu primera [acción] en [Producto]
## Qué vas a aprender
## Paso 1: [Acción inicial]
## Paso 2: [Siguiente acción]
## ...
## ¡Listo! Qué has conseguido
## Próximos pasos
```

**Principios:**
- Recorrido guiado paso a paso. El usuario no toma decisiones, solo sigue.
- Explica solo lo mínimo necesario para que funcione. No intentes cubrir todo.
- Incluye capturas en cada paso (o placeholders).
- El tono es el de un instructor paciente: "Ahora verás que...", "No te preocupes si...".
- Enlaza a guías más detalladas para quien quiera profundizar.
- Debe poder completarse en 10-15 minutos o menos.

**Señales de que necesitas un tutorial:**
- El usuario es nuevo en la aplicación.
- Se pide "getting started", "primeros pasos", "onboarding".
- El flujo tiene un principio y un fin naturales.

### 2. How-to (Guía de procedimiento)

**Para quién:** Usuarios que ya conocen el producto y necesitan hacer algo específico.

**Objetivo:** Resolver un problema o completar una tarea concreta lo más rápido posible.

**Estructura tipo:**
```
# Cómo [verbo] [objeto]
## Antes de empezar (si aplica)
## Pasos
1. ...
2. ...
## Resultado
## Variantes (si aplica)
## Si algo sale mal
```

**Principios:**
- Empieza directamente con el problema/objetivo. Sin introducciones largas.
- Asume competencia básica. El usuario sabe navegar la aplicación.
- Sin explicaciones de contexto innecesarias. Si algo necesita contexto, enlaza.
- Puede tener bifurcaciones: "Si necesitas X, sigue desde el paso 3.
  Si necesitas Y, ve al paso 5."
- Cada guía cubre UNA tarea. "Cómo exportar un informe a PDF", no "Todo sobre informes".

**Señales de que necesitas un how-to:**
- El usuario pregunta "¿cómo hago para...?"
- El código muestra un flujo con principio y fin claros.
- La tarea es específica y delimitada.

### 3. Referencia de funcionalidades

**Para quién:** Usuarios que necesitan consultar opciones, campos, o configuraciones.

**Objetivo:** Documentar de forma exhaustiva todo lo disponible en una pantalla o módulo.

**Estructura tipo:**
```
# [Nombre de la pantalla / módulo]
## Descripción general
## Secciones de la pantalla
### [Sección 1]
- Campo / opción: descripción, valores posibles, efecto
### [Sección 2]
## Tabla resumen de opciones
## Notas sobre permisos (si aplica)
```

**Principios:**
- Organizada por la estructura de la interfaz: menú → secciones → opciones.
- Cada elemento descrito: qué es, qué valores acepta, qué efecto tiene.
- No es un tutorial: no guía paso a paso. Documenta todo lo disponible.
- Usa tablas cuando hay muchos campos o configuraciones.
- Ideal para pantallas con muchas opciones o ajustes de configuración.

**Señales de que necesitas una referencia:**
- La pantalla tiene muchas opciones o campos.
- El usuario necesita saber "¿qué hace este campo?" o "¿qué opciones tengo?".
- El código muestra una pantalla de configuración compleja.

### 4. FAQ / Resolución de problemas

**Para quién:** Usuarios que tienen un problema o una duda específica.

**Objetivo:** Resolver la duda o el problema de la forma más directa posible.

**Estructura tipo:**
```
# Preguntas frecuentes: [Módulo]

## Problemas comunes

### No puedo [acción]
**Causa probable:** ...
**Solución:** ...

### Veo el mensaje "[mensaje de error]"
**Qué significa:** ...
**Qué hacer:** ...

## Preguntas generales

### ¿Puedo [acción]?
Sí/No. [Explicación breve].

### ¿Qué pasa si [situación]?
[Explicación de lo que ocurre y qué hacer].
```

**Principios:**
- Organizada por **síntoma visible**, no por causa técnica. "No puedo iniciar sesión",
  no "Error de autenticación OAuth".
- Cada entrada: síntoma → causa probable → solución paso a paso.
- Lenguaje empático: "Si ves este error, no te preocupes, tiene solución."
- Los mensajes de error se copian tal cual aparecen en la interfaz, entre comillas.
- Enlaza a la guía how-to correspondiente si la solución requiere un procedimiento largo.

**Señales de que necesitas una FAQ:**
- El código tiene muchas validaciones y mensajes de error.
- Hay restricciones de permisos que pueden confundir.
- Es un módulo complejo donde los usuarios suelen atascarse.

## Cómo elegir el tipo de documento

Usa esta guía para decidir qué tipo (o combinación) de documento generar:

| Situación | Tipo recomendado |
|-----------|-----------------|
| El usuario es nuevo en la aplicación | Tutorial |
| El usuario pide "documentar" algo genérico | How-to + mini-referencia + FAQ al final |
| El código muestra un flujo con principio y fin | How-to |
| El código muestra una pantalla con muchas opciones | Referencia |
| Piden algo para usuarios que están empezando | Tutorial |
| Hay muchas validaciones y errores | FAQ / Resolución de problemas |
| El módulo es complejo y multifacético | Combinación: tutorial + how-to + referencia + FAQ |

### La combinación más común

En la mayoría de casos, una buena guía de funcionalidad combina:

1. **Introducción breve** (del tutorial): qué es y para qué sirve.
2. **Procedimiento principal** (how-to): cómo hacer la acción más importante.
3. **Otras acciones** (mini how-to): editar, eliminar, filtrar.
4. **Referencia** (si hay campos/opciones que explicar): tabla o lista de opciones.
5. **FAQ/Problemas** (al final): errores comunes y preguntas frecuentes.

Este formato híbrido cubre la mayoría de las necesidades de documentación.

## Revelación progresiva

Independientemente del tipo de documento, aplica revelación progresiva:

1. **Primero lo esencial:** el happy path, el flujo más común, lo que el 80% de los
   usuarios necesita.
2. **Después lo complementario:** opciones avanzadas, configuraciones especiales,
   casos menos comunes.
3. **Al final lo excepcional:** problemas, errores, casos límite.

Marca claramente las secciones avanzadas:

```markdown
## Opciones avanzadas

> ℹ️ **Nota:** Esta sección cubre opciones de configuración avanzada. Si acabas de
> empezar, puedes saltarla por ahora y volver cuando la necesites.
```
