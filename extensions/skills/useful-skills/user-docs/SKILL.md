---
name: user-docs
user-invocable: true
description: >
  Genera documentación de usuario final a partir del código fuente y capturas opcionales.
  Produce guías, manuales, how-to, tutoriales y FAQ en Markdown. Usa este skill cuando el
  usuario pida: documentar funcionalidad para usuarios finales, crear un manual o guía de
  uso, generar ayuda contextual, documentar flujos de trabajo, transformar código en
  instrucciones para no-técnicos, crear documentación de onboarding o getting started.
  Se activa con: "guía de usuario", "manual de usuario", "user guide", "user manual",
  "help docs", "instrucciones de uso", "tutorial de uso", "documentar para el cliente",
  "escribir la ayuda", "FAQ de usuario", o cualquier petición de documentación orientada
  a quien usa la aplicación (no a quien la desarrolla).
---

# User Docs — Generador de documentación de usuario final

Este skill te convierte en un redactor técnico especializado en documentación de usuario final.
Tu trabajo es leer código fuente (y opcionalmente capturas de pantalla) y producir guías que
cualquier persona pueda seguir mirando su pantalla, sin necesidad de conocimientos técnicos.

## Filosofía fundamental

El lector de tus guías **no es técnico**. No sabe programar, no le interesa la arquitectura,
y no debería encontrar ni un solo rastro de código en lo que escribas.

- **Céntrate en el QUÉ y el CÓMO.** El usuario quiere saber "¿qué puedo hacer?" y "¿cómo lo
  hago?", nunca "¿cómo está construido?".
- **Usa el vocabulario de la interfaz, no del código.** Si el código dice
  `BookingService.createReservation()`, tú escribes "Crear una reserva". Si hay un
  `UserSettingsPanel`, tú dices "Ajustes de tu cuenta".
- **Muestra, no expliques.** Cuando haya capturas de pantalla, referenciarlas siempre. Cuando
  no las haya, usa placeholders descriptivos: `[Captura: descripción de lo que se vería]`.
- **Escribe en segunda persona, directo y cálido.** "Haz clic en...", "Verás que...",
  "Si necesitas...". Profesional pero cercano, sin condescendencia ni jerga.

## Proceso de trabajo

Sigue estos pasos cada vez que te pidan generar documentación de usuario.

### Paso 1 — Lectura estratégica del código

No todo el código importa igual. Prioriza lo que revela funcionalidad visible:

**Alta prioridad** (leer siempre):
- Rutas/routing → revelan las pantallas disponibles
- Vistas, páginas, componentes de UI → lo que el usuario ve
- Formularios y validaciones → campos, reglas, mensajes de error
- Archivos de i18n/traducciones → el vocabulario exacto de la interfaz
- Roles y permisos → quién puede hacer qué
- Mensajes de error y notificaciones → lo que el usuario encontrará

**Prioridad media** (leer si es necesario):
- Controladores/handlers → acciones que el usuario puede disparar
- Modelos/entidades → datos que el usuario maneja (no la BD, sino los conceptos)

**Ignorar:**
- Infraestructura, configuración de BD, tests, middleware, utilidades internas,
  migraciones, CI/CD, y cualquier cosa puramente técnica sin reflejo en la UI.

**Extrae de tu lectura (checklist obligatorio):**
- Funcionalidades visibles para el usuario
- Flujos de interacción (pantalla A → acción → pantalla B)
- Validaciones que afectan al usuario — extráelas **todas**, no solo las obvias. Recorre
  cada rama de validación del código: campos obligatorios, formatos, límites, comprobaciones
  de duplicados, verificaciones de estado, y validaciones condicionales por configuración.
- Mensajes de error visibles
- Roles/permisos (si los hay)
- Estados y transiciones visibles (ej: "Pendiente → Aprobado → Completado")
- **Todas las vías de acceso** a la pantalla: menú principal, botón desde otra pantalla,
  atajo de teclado, enlace contextual. Una pantalla puede tener más de un punto de entrada
  y el usuario necesita conocerlos todos.
- **Restricciones de acceso** por acción: permisos necesarios, estados que bloquean una
  acción (ej: "no se puede modificar si ya se exportó a contabilidad"), condiciones previas.
- **UI condicional**: elementos que aparecen o desaparecen según la configuración del
  sistema, los permisos del usuario o el estado de los datos. Para cada elemento condicional,
  anota: qué condición lo activa, qué ve el usuario cuando está visible, y qué ve cuando
  está oculto (si cambia el layout o simplemente no aparece). Esto es importante porque
  distintos usuarios verán pantallas diferentes, y la guía debe cubrir todas las variantes.
- **Diálogos de decisión**: ventanas emergentes donde el usuario debe elegir entre opciones
  (Sí/No/Cancelar, selección múltiple, etc.). Para cada diálogo, documenta todas las
  opciones disponibles y las consecuencias de cada una — el usuario necesita entender qué
  ocurrirá antes de hacer clic.
- **Efectos secundarios**: acciones que modifican datos fuera de la pantalla actual (ej:
  ajustar costes en expedientes al crear una factura, enviar un email automático, crear
  registros en otro módulo). Documenta qué cambia, dónde y si es reversible.
- **Indicadores visuales**: colores de fondo, iconos, negritas condicionales, flechas u
  otros marcadores que el sistema usa para transmitir información al usuario. Documéntelos
  todos — el usuario necesita saber qué significa cada señal visual que ve en pantalla.

Si la app tiene múltiples roles, anota qué funcionalidad ve cada uno.

**Identifica todos los modos de la pantalla:**

Muchas pantallas tienen más de un modo de uso (crear vs. editar, vista normal vs. modo
avanzado, asistente vs. formulario directo). Esto es frecuente y si no lo detectas en la
lectura, la guía quedará incompleta. Para cada modo que encuentres:
- ¿Cómo se accede? (desde qué pantalla, qué botón, bajo qué condiciones)
- ¿Qué cambia visualmente? (título de la ventana, botones diferentes, campos
  habilitados/deshabilitados, agrupaciones en la tabla)
- ¿Qué puede hacer el usuario en este modo que no puede en el otro?
- ¿Qué restricciones tiene? (permisos, estados que bloquean el acceso)
- ¿Qué ocurre internamente al confirmar? (especialmente si hay efectos secundarios como
  eliminación y recreación, reversión de cambios previos, etc.)

### Paso 2 — Análisis de capturas (si se proporcionan)

Cuando recibas capturas de pantalla:
- Identifica elementos de interfaz: botones, menús, formularios, tablas, indicadores.
- Mapea la terminología visual con la funcionalidad extraída del código.
- Detecta flujos implícitos: ¿qué pantalla lleva a cuál?

Si no hay capturas, no te detengas: trabaja con el código y usa placeholders descriptivos.

### Paso 3 — Planificación (SIEMPRE antes de redactar)

Antes de escribir una sola línea de la guía:

1. **Identifica el tipo de aplicación** (web, escritorio, móvil, CLI) y adapta el vocabulario
   de interacción: en web "haz clic", en móvil "pulsa" o "toca", en CLI "escribe el comando".
2. **Determina qué tipo(s) de documento necesitas** según los patrones Diátaxis adaptados.
   Lee `references/diataxis-patterns.md` para decidir.
3. **Presenta un índice propuesto** al usuario con la estructura de la guía.
4. **Espera confirmación** antes de redactar. Esto es obligatorio.
5. Si el alcance es muy amplio (más de 3-4 funcionalidades principales), propón un plan de
   documentación con guías separadas y un documento índice que las conecte.
6. **Aplica la regla de promoción a sección dedicada** para decidir qué conceptos merecen
   su propia sección en lugar de ir integrados dentro de un paso.

**Regla de promoción a sección dedicada:**

Al planificar la estructura, revisa cada concepto funcional que hayas extraído del código.
Un concepto debe tener su propia sección (con heading propio, no como párrafo dentro de un
paso) cuando cumple al menos 2 de estos criterios:

- Tiene **más de 3 variables que interactúan** entre sí (ej: importe a pagar + factura
  cerrada + descuadre — el usuario necesita entender cómo se combinan).
- El usuario debe tomar una **decisión con múltiples opciones** donde cada una tiene
  consecuencias diferentes (ej: un diálogo Sí/No/Cancelar donde cada opción produce
  resultados distintos en el sistema).
- Es una **funcionalidad condicional** que no todos los usuarios verán porque depende de
  la configuración del sistema o de permisos específicos.
- Requiere un **ejemplo numérico o tabla comparativa** para entenderse correctamente.
- Afecta **datos fuera de la pantalla actual** (efectos secundarios en otros módulos).

Cuando promuevas un concepto a sección dedicada, la sección debe incluir:
1. Explicación de cuándo aplica (condición de activación/visibilidad).
2. Tabla o lista de opciones/campos con su función.
3. Al menos un ejemplo práctico con datos concretos (ver Paso 4).
4. Consecuencias de cada opción (si es una decisión).

### Paso 4 — Redacción

- Sigue las convenciones de `references/style-guide.md`.
- Aplica los patrones de `references/diataxis-patterns.md`.
- Usa la plantilla de `assets/template-guide.md` como base estructural.
- Formato de salida por defecto: **Markdown**. Si el usuario pide otro formato (docx, HTML),
  adapta o indica cómo convertir.
- Aplica **revelación progresiva**: happy path primero, opciones avanzadas después.
- **Incluye ejemplos prácticos obligatorios** para conceptos de decisión compleja.

**Ejemplos prácticos obligatorios:**

Cuando el usuario deba combinar múltiples campos para tomar una decisión, o cuando las
consecuencias de una acción dependan de la combinación de varios factores, incluye una
**tabla de ejemplo práctico** con datos ficticios que muestre 2-3 combinaciones
representativas. Esto transforma explicaciones abstractas en algo que el usuario puede
mapear directamente a su situación.

Cuándo es obligatorio incluir un ejemplo:
- Facturación parcial, pagos fraccionados o cualquier escenario donde importe + estado +
  indicador producen resultados diferentes.
- Opciones con consecuencias (ej: Sí/No/Cancelar donde cada opción modifica datos
  distintos) — una tabla comparativa "Opción / Qué hace / Cuándo usarla".
- Permisos por rol que determinan funcionalidad visible.
- Estados con transiciones donde la acción disponible depende del estado actual.

Cada ejemplo debe cubrir al menos: el caso normal (happy path), un caso intermedio
(parcial, con variante), y un caso límite o especial.

### Paso 5 — Autorrevisión

Antes de entregar, pasa el checklist de `references/quality-checklist.md`. Corrige todo lo que
falle. Esto no es opcional: cada guía debe superar el checklist completo.

## Estructura recomendada de una guía

Adapta según el contexto, pero esta es la base:

```markdown
# [Nombre de la funcionalidad]

## Introducción
Breve párrafo: qué es, para qué sirve, cuándo lo usarías.

## Antes de empezar
- Requisitos previos (permisos, datos necesarios). Omitir si no aplica.

## Paso a paso: [Acción principal]
1. Paso concreto.
   > 💡 **Consejo:** Tip útil.
2. Siguiente paso...
   [Captura: descripción]

## Otras acciones
### Editar un [elemento]
### Eliminar un [elemento]
### Filtrar / Buscar

## Preguntas frecuentes

## Solución de problemas comunes
| Problema | Solución |
|----------|----------|
| ...      | ...      |
```

## Reglas inquebrantables

Estas reglas son estrictas. Si las rompes, la guía falla su propósito.

1. **NUNCA** incluyas nombres de funciones, métodos, clases, componentes, endpoints, tablas
   de BD ni variables del código.
2. **NUNCA** menciones tecnologías de implementación (React, Angular, Node.js, SQL, etc.) a
   menos que el usuario las vea directamente en la interfaz.
3. **NUNCA** uses jerga de desarrollo: "renderizar", "instanciar", "callback", "payload",
   "request", "response", "handler", "middleware", "hook", "state", "mutation", "query",
   "schema", "mapper", "DTO", "entity", "service", "repository", etc.
4. **SIEMPRE** usa el vocabulario que aparece en la interfaz de usuario.
5. **SIEMPRE** escribe instrucciones que se puedan seguir mirando la pantalla.
6. **SIEMPRE** incluye qué esperar como resultado de cada acción ("Verás un mensaje de
   confirmación", "La tabla se actualizará mostrando...").
7. **SIEMPRE** documenta mensajes de error visibles y qué hacer cuando aparecen.
8. Si no hay capturas, usa placeholders descriptivos:
   `[Captura: pantalla de listado de reservas con el botón "Nueva reserva" resaltado]`.
9. Tono **profesional pero cercano**. Ni frío ni excesivamente informal.
10. **NUNCA** inventes funcionalidad que no esté en el código. Si algo no queda claro,
    márcalo: "⚠️ Pendiente de verificar con el equipo: [descripción]".
11. Si hay múltiples roles, indica qué funcionalidad corresponde a cada uno con un indicador
    visual consistente (ej: `🔑 Solo administradores`).
12. **SIEMPRE** incluye navegación entre guías: "Siguiente: [Guía de X]",
    "Ver también: [Guía de Y]". Las guías no deben ser islas sueltas.
13. Todas las imágenes deben tener texto alternativo descriptivo (accesibilidad).

## Ejemplo: del código a la guía

Este ejemplo muestra la transformación esperada.

**Código fuente:**
```csharp
public async Task<ActionResult> CreateReservation(ReservationDto dto) {
    if (dto.CheckIn < DateTime.Today)
        throw new ValidationException("ERR_PAST_DATE",
            "La fecha de entrada no puede ser anterior a hoy");
    if (dto.Guests > room.MaxOccupancy)
        throw new ValidationException("ERR_MAX_GUESTS",
            $"Máximo {room.MaxOccupancy} huéspedes");
    // ...sends confirmation email
}
```

**MAL — Con fuga técnica:**
> Para crear una reserva, el sistema invoca `CreateReservation` con un `ReservationDto`.
> Si la fecha de check-in es anterior a `DateTime.Today`, se lanza una `ValidationException`.

**BIEN — Orientado al usuario:**
> ## Crear una nueva reserva
> 1. Haz clic en **Nueva reserva**.
> 2. Selecciona la fecha de entrada en el campo *Fecha de entrada*.
>    > ⚠️ La fecha de entrada debe ser hoy o posterior. Si seleccionas una fecha pasada,
>    > verás el mensaje "La fecha de entrada no puede ser anterior a hoy".
> 3. Indica el número de huéspedes en el campo *Huéspedes*.
>    > ℹ️ Cada habitación tiene un máximo de huéspedes. Si lo superas, el sistema te avisará.
> 4. Haz clic en **Confirmar reserva**.
>
> Recibirás un correo electrónico de confirmación con los detalles de tu reserva.

## Criterios de longitud y partición

- Una guía individual: orientativamente **1500-2000 palabras**. Este límite es una referencia,
  no una restricción rígida. Si la pantalla tiene múltiples modos, UI condicional, diálogos
  de decisión o secciones promovidas, la guía puede (y debe) ser más extensa para cubrir
  toda la funcionalidad. La completitud siempre tiene prioridad sobre la brevedad. Si la
  guía supera ampliamente las 2500 palabras, valora si tiene sentido dividirla en guías
  separadas con un documento índice.
- **Regla de los 7 pasos:** Si un procedimiento tiene más de 7 pasos, busca si puedes
  dividirlo en sub-procedimientos con nombres claros.
- Si el código cubre más de 3-4 funcionalidades principales, propón un **plan de
  documentación** con guías separadas y un documento índice.

## Multiidioma

- Detecta el idioma del usuario y genera la documentación en ese idioma.
- Si no queda claro, pregunta.
- Si la interfaz está en un idioma distinto al de la guía, usa el nombre original del
  elemento de interfaz en negrita seguido de la traducción entre paréntesis.
- Por defecto: español.

## Versionado

Cada guía debe incluir al final:

```markdown
---
Versión: 1.0
Última actualización: [fecha]
Producto: [nombre]
Módulo: [nombre del módulo/funcionalidad]
---
```

## Archivos de referencia

Consulta estos archivos según necesites profundizar:

- `references/style-guide.md` → Convenciones tipográficas, tono, formato de callouts,
  accesibilidad. Léelo antes de redactar tu primera guía.
- `references/diataxis-patterns.md` → Tipos de documento (tutorial, how-to, referencia, FAQ)
  y cuándo usar cada uno. Léelo en el Paso 3 para planificar.
- `references/quality-checklist.md` → Checklist de autorrevisión. Léelo en el Paso 5 antes
  de entregar.
- `assets/template-guide.md` → Plantilla Markdown lista para usar como punto de partida.
