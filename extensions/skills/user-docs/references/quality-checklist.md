# Checklist de calidad — Autorrevisión antes de entregar

Pasa este checklist antes de entregar cualquier guía de usuario. Cada punto que falle debe
corregirse. No entregues una guía que no supere todos los apartados.

## Legibilidad

- [ ] ¿Puedo seguir estas instrucciones sin ver el código fuente?
- [ ] ¿Cada paso empieza con un verbo de acción en imperativo?
- [ ] ¿Las frases tienen 25 palabras o menos (salvo excepciones justificadas)?
- [ ] ¿He evitado párrafos de más de 4-5 líneas?
- [ ] ¿El texto se puede escanear visualmente? (headings claros, listas, tablas)
- [ ] ¿He aplicado revelación progresiva? (esencial primero, avanzado después)

## Precisión

- [ ] ¿Cada acción descrita corresponde a algo real en el código o la interfaz?
- [ ] ¿Los nombres de botones, menús y campos coinciden exactamente con la interfaz?
- [ ] ¿He documentado qué pasa cuando algo falla (validaciones, errores)?
- [ ] ¿No he inventado ninguna funcionalidad que no exista en el código?
- [ ] ¿He marcado con "⚠️ Pendiente de verificar" lo que no me queda claro?
- [ ] ¿He incluido el resultado esperado tras cada secuencia de acciones?

## Ausencia de jerga técnica

- [ ] ¿He eliminado TODA referencia a nombres internos del código?
      (funciones, clases, componentes, endpoints, tablas de BD, variables)
- [ ] ¿No menciono tecnologías de implementación innecesarias?
      (React, Angular, Node.js, SQL, REST, etc.)
- [ ] ¿No uso palabras de jerga de desarrollo?
      (renderizar, instanciar, callback, payload, request, response, handler,
      middleware, hook, state, mutation, query, schema, mapper, DTO, entity,
      service, repository, controller)
- [ ] ¿Un usuario no-técnico entendería CADA palabra de este documento?

## Completitud

- [ ] ¿He cubierto el flujo principal (happy path)?
- [ ] ¿He documentado los caminos alternativos más importantes?
- [ ] ¿He documentado los errores y validaciones que el usuario puede encontrar?
- [ ] ¿He incluido requisitos previos si los hay?
- [ ] ¿He incluido el resultado esperado de cada secuencia de acciones?
- [ ] Si hay múltiples roles, ¿he indicado qué funcionalidad corresponde a cada uno?

## Completitud funcional

Esta sección verifica que no se haya omitido funcionalidad visible para el usuario.
Si algún punto aplica pero no está documentado, la guía está incompleta.

- [ ] ¿He documentado **todas las vías de acceso** a la pantalla? (menú, botón desde otra
      pantalla, acceso directo, etc.)
- [ ] ¿He identificado y documentado **todos los elementos condicionales** — campos,
      pestañas, botones o secciones que aparecen/desaparecen según configuración, permisos
      o estado de los datos?
- [ ] ¿He documentado **todos los modos** de la pantalla? (crear/editar/consultar, modo
      normal/avanzado, asistente/directo)
- [ ] Para cada modo alternativo: ¿he explicado cómo acceder, qué cambia visualmente,
      qué restricciones tiene, y qué ocurre al confirmar?
- [ ] ¿He extraído **todas las validaciones** del código — no solo las evidentes, sino
      también las condicionales (por configuración, por estado, por combinación de campos)?
- [ ] ¿He documentado **todos los diálogos de decisión** con todas sus opciones y las
      consecuencias de cada una?
- [ ] Para conceptos complejos con múltiples variables: ¿he incluido un **ejemplo práctico**
      con datos numéricos ficticios?
- [ ] ¿He documentado los **efectos secundarios** de las acciones principales — cambios que
      la acción produce en otros módulos, pantallas o datos fuera de la vista actual?
- [ ] ¿He documentado **todos los indicadores visuales** — colores, iconos, negritas
      condicionales, marcadores — y su significado?

## Estructura

- [ ] ¿La guía tiene una introducción que explica para qué sirve?
- [ ] ¿Los pasos están en orden lógico (el orden en que el usuario los haría)?
- [ ] ¿He usado los callouts apropiados? (💡 Consejo, ⚠️ Importante, ℹ️ Nota, 🚫 No hagas)
- [ ] ¿Los placeholders de capturas son descriptivos y específicos?
- [ ] ¿Ningún procedimiento tiene más de 7 pasos sin dividir?
- [ ] ¿La extensión es razonable? (orientativamente 1500-2000 palabras, pero la completitud
      tiene prioridad — si supera las 2500, valorar si conviene dividir en guías separadas)

## Tono

- [ ] ¿El tono es cálido pero profesional?
- [ ] ¿Uso segunda persona consistentemente? ("tú", no "el usuario")
- [ ] ¿No soy condescendiente? (sin "¡Es muy fácil!" ni "Simplemente haz...")
- [ ] ¿No soy excesivamente informal? (sin chistes, memes, o lenguaje coloquial)
- [ ] ¿Las secciones de errores tienen un tono empático, no acusatorio?
      ("Si ves este error..." no "Si cometiste el error de...")

## Convenciones tipográficas

- [ ] ¿He usado **negrita** para elementos interactivos (botones, menús, enlaces)?
- [ ] ¿He usado *cursiva* para campos de formulario y valores?
- [ ] ¿He usado `código` solo para valores literales a escribir exactamente?
- [ ] ¿He usado "comillas" para nombres de ventanas, secciones y pestañas?
- [ ] ¿No he usado MAYÚSCULAS para enfatizar?

## Accesibilidad y navegación

- [ ] ¿Todas las imágenes/placeholders tienen texto alternativo descriptivo?
- [ ] ¿No transmito información solo con color?
- [ ] ¿Las tablas tienen encabezados claros?
- [ ] ¿Los enlaces tienen texto descriptivo? (no "haz clic aquí")
- [ ] ¿Hay un enlace para volver al índice general al inicio?
- [ ] ¿Hay sección "Ver también" o "Siguiente paso" al final?
- [ ] Si es parte de una serie, ¿indico la posición?

## Versionado

- [ ] ¿He incluido la sección de metadatos al final?
      (Versión, Última actualización, Producto, Módulo)

## Último vistazo

Lee la guía de principio a fin como si fueras un usuario que la ve por primera vez.
¿Podrías completar la tarea solo con esta guía y la pantalla delante?
Si la respuesta es no, revisa y corrige.
