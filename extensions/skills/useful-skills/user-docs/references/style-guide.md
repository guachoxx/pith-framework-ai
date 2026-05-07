# Guía de estilo para documentación de usuario final

Esta guía define las convenciones de escritura para toda la documentación generada por el
skill user-docs. Síguela en cada guía que redactes.

## Tono y voz

- **Segunda persona directa:** "Haz clic", "Selecciona", "Verás". El usuario es "tú".
- **Voz activa** siempre que sea posible. "Haz clic en **Guardar**" en lugar de
  "El botón Guardar debe ser presionado".
- **Frases cortas y directas.** Máximo 25 palabras por frase como regla general.
  Si una frase necesita ser más larga, asegúrate de que sigue siendo fácil de seguir.
- **Un concepto por párrafo.** No mezcles instrucciones de dos acciones distintas en el
  mismo párrafo.
- **Profesional pero cercano.** Imagina que estás explicando algo a un compañero de trabajo
  que no es técnico: respetuoso, claro, sin condescendencia.

### Qué evitar en el tono

- No uses lenguaje infantilizante: "¡Muy fácil!" o "¡No te preocupes, es sencillísimo!"
- No uses lenguaje burocrático: "Proceda a realizar la acción de..."
- No uses lenguaje de desarrollador: "El componente renderiza..." o "Se instancia el objeto..."
- No uses humor forzado ni metáforas rebuscadas.

## Convenciones tipográficas

Estas convenciones mantienen la consistencia visual y ayudan al usuario a distinguir rápidamente
qué es un elemento de interfaz, qué es un valor a introducir y qué es texto explicativo.

### Negrita — Elementos interactivos de la interfaz

Usa **negrita** para botones, enlaces, nombres de menú, pestañas y cualquier elemento con el
que el usuario interactúa directamente.

Ejemplos:
- Haz clic en **Guardar**.
- Selecciona **Archivo** > **Exportar**.
- Activa la opción **Notificaciones por correo**.

### Cursiva — Campos de formulario y valores

Usa *cursiva* para campos de formulario, etiquetas y valores que el usuario debe observar
o introducir.

Ejemplos:
- En el campo *Correo electrónico*, escribe tu dirección.
- El valor del campo *Estado* cambiará a *Aprobado*.
- Asegúrate de que *País* muestra la opción correcta.

### Código inline — Valores literales

Usa `código inline` SOLO para valores literales que el usuario debe escribir exactamente
tal cual: URLs, códigos, comandos (si aplica), o valores técnicos que la interfaz muestra
tal cual.

Ejemplos:
- Introduce el código `DESCUENTO20` en el campo *Código promocional*.
- Accede a `https://app.ejemplo.com/configuracion`.

No uses código inline para nombres de botones, menús o campos. Eso es negrita o cursiva.

### Comillas — Nombres de secciones y ventanas

Usa "comillas" para nombres de ventanas, diálogos, pestañas, o secciones de la pantalla
que no son interactivas per se sino contenedores.

Ejemplos:
- Ve a la pestaña "Configuración".
- En la sección "Datos personales", revisa tu información.
- Se abrirá la ventana "Confirmar eliminación".

### Mayúsculas

Nunca uses MAYÚSCULAS para enfatizar. Solo para acrónimos conocidos: PDF, URL, FAQ, CRM.

## Listas y pasos

### Listas numeradas — Acciones secuenciales

Cada vez que el usuario deba seguir un orden, usa lista numerada. Cada paso empieza con un
verbo en imperativo.

```markdown
1. Abre el menú **Reservas**.
2. Haz clic en **Nueva reserva**.
3. Completa los campos del formulario.
4. Haz clic en **Confirmar**.
```

### Listas con viñetas — Enumeraciones sin orden

Para listar opciones, características, o elementos sin secuencia:

```markdown
Desde esta pantalla puedes:
- Ver el historial de reservas.
- Filtrar por fecha o estado.
- Exportar los resultados a PDF.
```

### Resultado esperado

Al final de una secuencia de pasos (o tras un paso clave), indica qué debería ver el
usuario:

```markdown
4. Haz clic en **Confirmar**.

Verás un mensaje de confirmación en pantalla y recibirás un correo con los detalles.
```

## Capturas de pantalla

### Referencia antes de mostrar

Siempre introduce la captura antes de mostrarla:

```markdown
Como puedes ver en la siguiente imagen, el botón **Nueva reserva** se encuentra en la
esquina superior derecha:

![Pantalla de reservas con el botón Nueva reserva resaltado](ruta/imagen.png)
```

### Pie descriptivo

Cada captura debe tener un pie o texto alternativo que la describa por completo, de forma
que un usuario que no pueda verla entienda qué muestra.

### Anotaciones

Si usas anotaciones (flechas, recuadros) en las capturas:
- Usa un color consistente en toda la guía (rojo o naranja recomendado).
- No sobrecargues: máximo 2-3 anotaciones por captura.

### Datos personales

Nunca muestres datos personales reales en las capturas. Usa datos de ejemplo ficticios.

### Placeholders (cuando no hay capturas)

Usa este formato consistente:

```markdown
[Captura: descripción detallada de lo que se vería en la pantalla]
```

Ejemplo:
```markdown
[Captura: formulario de nueva reserva con los campos Fecha de entrada, Fecha de salida,
Huéspedes y Tipo de habitación visibles, y el botón Confirmar reserva al final]
```

## Notas, consejos y advertencias (callouts)

Usa estos callouts con los emojis indicados para mantener consistencia visual:

### 💡 Consejo
Para tips opcionales que mejoran la experiencia o ahorran tiempo.
```markdown
> 💡 **Consejo:** Puedes usar el atajo de teclado Ctrl+S para guardar sin hacer clic
> en el botón.
```

### ⚠️ Importante
Para advertencias que pueden causar pérdida de datos, errores o situaciones difíciles
de revertir.
```markdown
> ⚠️ **Importante:** Una vez eliminada una reserva, no podrás recuperarla. Asegúrate
> de que realmente deseas eliminarla.
```

### ℹ️ Nota
Para información complementaria no esencial pero útil.
```markdown
> ℹ️ **Nota:** Los cambios pueden tardar hasta 5 minutos en reflejarse en el panel
> de estadísticas.
```

### 🚫 No hagas esto
Para anti-patrones comunes que los usuarios tienden a hacer.
```markdown
> 🚫 **No hagas esto:** No cierres el navegador mientras la exportación está en curso.
> Esto cancelará el proceso y tendrás que empezar de nuevo.
```

## Idioma

- Detecta el idioma del usuario y escribe en ese idioma.
- Si no queda claro, pregunta antes de empezar.
- Si la interfaz está en un idioma distinto al de la guía, usa el nombre original del
  elemento en negrita y añade la traducción entre paréntesis la primera vez:
  "Haz clic en **Settings** (Configuración)."
  A partir de ahí, puedes usar solo la traducción si el contexto es claro.

## Accesibilidad

Estas prácticas aseguran que la documentación sea útil para todos los usuarios, incluyendo
aquellos que usen lectores de pantalla u otras tecnologías de asistencia.

- **Texto alternativo en imágenes:** Toda imagen debe tener un `alt` descriptivo que
  transmita la misma información que la imagen. No uses "imagen de..." o "captura de...";
  describe directamente lo que se ve.
- **No dependas solo del color:** En lugar de "haz clic en el botón rojo", escribe
  "haz clic en el botón **Eliminar**, de color rojo". El color complementa, no define.
- **Tablas con encabezados claros:** Toda tabla debe tener una fila de encabezados que
  describa cada columna.
- **Enlaces descriptivos:** En lugar de "haz clic aquí", escribe "consulta la
  [guía de configuración de permisos]". El texto del enlace debe indicar adónde lleva.

## Navegación entre guías

Cada guía es parte de un sistema de documentación, no una isla:

- **Al inicio:** incluye un enlace para volver al índice general:
  `← [Volver al índice general](indice.md)`
- **Al final:** incluye una sección "Ver también" con guías relacionadas y/o
  "Siguiente paso" si hay un flujo natural a seguir.
- **Si es parte de una serie:** indica la posición:
  "Parte 2 de 4: Gestión de reservas".
