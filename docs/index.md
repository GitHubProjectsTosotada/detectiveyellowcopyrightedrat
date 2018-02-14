Detective Pikachu es un bot de Telegram especializado en crear listados de participantes en incursiones de Pokémon GO.

Puedes pedir ayuda en el grupo [@detectivepikachuayuda](https://t.me/detectivepikachuayuda) y estar informado de las novedades en el canal [@detectivepikachunews](https://t.me/detectivepikachunews).

1. [Ayuda para entrenadores](#ayuda-para-entrenadores)
   1. [Registrarse en el bot](#registrarse-en-el-bot)
   2. [Crear una incursión](#crear-una-incursión)
   3. [Editar, cancelar, borrar y reflotar una incursión](#editar-cancelar-borrar-y-reflotar-una-incursión)
   4. [Apuntarse a una incursión](#apuntarse-a-una-incursión)
   5. [Alertas de incursiones](#alertas-de-incursiones)
   6. [Estadístcas](#estadísticas)
   7. [Más ayuda](#más-ayuda)
2. [Ayuda para administradores](#ayuda-para-administradores)
   1. [Grupos y canales](#grupos-y-canales)
   2. [Añadir el bot a un grupo o canal](#añadir-el-bot-a-un-grupo-o-canal)
   3. [Configuración](#configuración)
   4. [Ubicaciones](#ubicaciones)
   5. [Modo niñero](#modo-niñero)
   6. [Zona horaria](#zona-horaria)
   7. [Rankings](#rankings)
   8. [Otros comandos exclusivos para administradores](#otros-comandos-exclusivos-para-administradores)

## Ayuda para entrenadores ##

### Registrarse en el bot ###

El registro es obligatorio en algunos grupos (a discreción de los administradores), pero sea obligatorio o no, te permite **mostrar tu nombre de entrenador, equipo y nivel** en las incursiones y **participar en los rankings**.

Para registrarte tienes dos opciones:

1. En un privado con [@detectivepikachubot](https://t.me/detectivepikachubot), escribe el comando `/register` y comenzarás el proceso de registro y validación. El proceso es automatizado y te pedirá que hagas una captura de pantalla del juego con unas condiciones.

2. Si estás registrado y validado con [@profesoroak_bot](https://t.me/profesoroak_bot), puedes sencillamente preguntarle `quién soy?` y reenviar la respuesta a [@detectivepikachubot](https://t.me/detectivepikachubot).

### Crear una incursión ###

Se puede crear una incursión de forma interactiva con el comando:

    /raid

También se pueden especificar los parámetros directamente, algo que es necesario si alguno de los parámetros no aparece en el menú de creación interactivo. La sintaxis para crear una incursión nueva de esta forma es sencilla:

    /raid pokemon hora gimnasio

Es importante seguir este mismo orden, sino lo más seguro es que el bot no te entienda. También se puede añadir una hora a la que desaparece el Pokémon.

    /raid pokemon hora gimnasio horafin

Algunos ejemplos:

    /raid Raikou 14:30 Alameda
    /raid Entei 3:30 Plaza de la verdura
    /raid Metapod 12 Plaza Mayor 12:15

En lugar de especificar un Pokémon, se puede especificar un huevo, por ejemplo, para un huevo de nivel 4 se pondría *N4*:

    /raid N4 13:00 Alameda

Para crear incursiones EX se debe utilizar la palabra *EX* y especificar el día de la incursión con el siguiente formato:

    /raid EX dia/hora gimnasio

Por ejemplo, para una incursión EX el día 12 a las 15:30 en el gimnasio Crucero:

    /raid EX 12/15:30 Crucero

Para poder crear una incursión es **necesario tener un alias** definido en Telegram y. Además, algunos grupos exigen **estar validado** en el bot. Si no puedes crear una incursión por alguno de estos motivos, el bot te informará.

### Editar, cancelar, borrar y reflotar una incursión ###

Se pueden editar y añadir todos los detalles de la incursión después de crearla: cambiar la hora, el gimnasio, el Pokémon (o el huevo) y la hora a la que desaparece.

Para editar o añadir cualquiera de estos detalles, el creador de la incursión puede contestar al mensaje de la incursión con uno de estos comandos:

    /hora 12:00
    /pokemon Wartortle
    /gimnasio Plaza de Abastos
    /horafin 12:30

Una incursión también se puede cancelar contestando con el comando `/cancelar`, ser borrada con el comando `/borrar` y ser reflotada con el comando `/reflotar`.

Los participantes recibirán **avisos por privado** cuando se edite, cancele o borre una incursión.

Ten en cuenta que los comandos `/borrar` y `/reflotar` por defecto solo están activados para los administradores de los grupos y solo algunos grupos permiten que los usen los propios creadores de las incursiones.

Al editar una hora hay las mismas restricciones que al crear la incursión. Con `/hora` es **necesario especificar el día** si no es el día actual. Con `/horafin`, sin embargo, no es necesario, ya que por defecto se toma el mismo día en que se realiza la incursión.

### Apuntarse a una incursión ###

Una vez creada la incursión, puedes apuntarse pulsando en el botón **Voy**. Si te apuntas unos pocos minutos antes de la hora fijada, o incluso después, podrías aparecer con un icono de un caracol 🐌 en el listado, dependiendo de cómo esté configurado el grupo.

Si vas con acompañantes, puedes pulsar el botón **+1** por cada acompañante adicional. Si te has pasado, pulsa en **Voy** para poner esta cuenta a cero y volver a empezar. Ten en cuenta que los administradores de los grupos pueden limitar el número de acompañantes permitidos o deshabilitar completamente esta opción.

Cuando estés en el lugar de la incursión, puedes pulsar el botón **Estoy ahí** para indicarlo.

Si te has apuntado pero no vas a ir, pulsa en **No voy**. Si han pasado más de cinco minutos desde que te apuntaste, permanecerás en la lista con una ❌ para que la gente sepa que te has desapuntado.

Una vez llegue la hora de la incursión y hasta seis horas más tarde, puedes informar si has capturado al Pokémon de la incursión pulsando en **Lo tengo** o **Ha escapado**. Ten en cuenta que estos botones no están activados por defecto y los administradores de los grupos pueden decidir no habilitarlos.

Para poder apuntarse a una incursión es **necesario tener un alias** definido en Telegram. Además, algunos grupos exigen **estar validado** en el bot. Si no puedes apuntarte por alguno de estos motivos, el bot te informará.

### Alertas de incursiones ###

Los usuarios pueden configurar alertas por mensaje privado cuando se creen incursiones en determinados gimnasios. Para configurarlas, utiliza el comando `/alerts` por privado al bot y sigue las instrucciones.

Ten en cuenta que antes de configurar las alertas tienes que haber participado en alguna incursión en un grupo con las ubicaciones de los gimnasios coniguradas y la opción de permitir alertas activada.

### Estadísticas ###

Los usuarios pueden solicitar sus estadísticas de participación de la semana pasada con el comando `/stats`. Las estadísticas tan sólo cuentan las incursiones en las que ha pulsado el botón de **Estoy** y se ha apuntado antes de la hora de inicio de la incursión.

### Más ayuda ###

Si necesitas ayuda que no se encuentre en este manual, puedes preguntar en [@detectivepikachuayuda](https://t.me/detectivepikachuayuda). Si estás administrando un grupo o un canal, mira más abajo para ver la ayuda para administradores.

## Ayuda para administradores ##

### Grupos y canales ###

El bot se puede añadir a grupos y a canales, pero funciona de manera ligeramente distinta en ambos casos, en parte por el propio funcionamiento de Telegram.

En **grupos** el bot ya se puede utilizar tan pronto entra al grupo y envía un saludo. Conviene configurarlo, no obstante. Ten cuidado porque, si una vez añadas el bot conviertes el grupo a supergrupo, tendrás que volver a configurarlo. Un supergrupo es la mejor opción en la mayoría de los casos.

En **canales** el bot no saluda al entrar y necesita configurarse con `/settings` antes de poder utilizarse. También funciona algo más lento y hay algunas diferencias más. En un canal, no mostrará el creador de la incursión porque la incursión siempre la crea el canal, no un usuario. Además, algunas de las opciones no tienen sentido para canales. Usar un canal es una opción sencilla si se quiere integrar con otros bots, ya que un bot no puede leer el mensaje de otro bot en un grupo.

### Añadir el bot a un grupo o canal ###

Para **añadir el bot a un grupo** tienes tres alternativas:

1. Vete al perfil de [@detectivepikachubot](https://t.me/detectivepikachubot). En el menú, selecciona la opción *Añadir a un grupo* y escoge el grupo de la lista.

2. Pulsa en [este enlace](https://telegram.me/detectivepikachubot?startgroup=true) en un dispositivo donde tengas Telegram instalado.

3. Puedes intentar añadirlo como un contacto más desde el grupo con su alias `@detectivepikachubot`, pero en versiones recientes de Telegram hay problemas usando este método.

Para **añadir el bot a un canal** las opciones son más limitadas. Tienes que ir a la gestión de administradores y **añadirlo directamente como administrador**, buscándolo como un contacto más con su alias `@detectivepikachubot`.

Con versiones recientes de Telegram no se pueden añadir bots de esta forma. Si es tu caso, descarga la beta para Android desde [el canal Beta de Telegram](http://t.me/tgrambeta) buscando el archivo `tgrambeta.apk` más reciente. Telegram Beta se instala como una aplicación aparte y, una vez añadas el bot, puedes desinstalarla.

### Configuración ###

Para hacer la configuración básica del bot utiliza el comando `/settings`. La configuración está dividida en varios submenús:

#### Funcionamiento del grupo/canal ####

1. **Ubicaciones**. Activa o desactiva la integración de las ubicaciones. Para poder utilizar esta opción, debes [configurar las ubicaciones](#ubicaciones). Si no vas a hacerlo, es mejor que la desactives. Opción activada por defecto.

2. **Permitir configurar alertas**. Requiere la opción *Ubicaciones* (se marca automáticamente si es necesario). Permite o no que los usuarios encuentren los gimnasios configurados en este grupo/canal a la hora de configurarse alertas por privado. Opción activada por defecto.

3. **Modo niñero**. Borra todos los mensajes excepto los mensajes de creación de incursiones y los comandos permitidos. Mira el  [apartado del modo niñero](#modo-niñero) para más información. Opción desactivada por defecto.

4. **Validación obligatoria**. Si está activada, obliga a todos los usuarios a validarse en el bot antes de poder participar en incursiones o crearlas. Opción desactivada por defecto.

5. **Reflotar automático**. Si está activada, esta opción hace que el bot reflote todas las incursiones activas cada 5, 10, 15 o 30 minutos. Las incursiones se consideran activas si falta **menos de una hora y media para que comiencen** o si acaban de comenzar (una vez comenzadas, se reflotarán una única vez). Opción desactivada por defecto.

#### Comandos disponibles para usuarios ####

1. **Consultar gimnasios (comando /gym)**. Si está activada, permite que los usuarios consulten localizaciones de los gimnasios. Opción desactivada por defecto.

2. **Crear incursiones (comando /raid)**. Si está activada, permite que los usuarios creen incursiones. Opción activada por defecto.

3. **Reflotar incursiones (comando /reflotar)**. Si está activada, permite que los creadores de las incursiones las refloten utilizando el comando `/reflotar`. Opción desactivada por defecto.

4. **Borrar incursiones (comando /borrar)**. Si está activada, permite que los creadores de las incursiones las borren utilizando el comando `/borrar`. Si desactivas esta opción, todavía pueden cancelarlas con el comando `/cancelar`. Opción activada por defecto.

#### Opciones de vista de incursiones ####

1. **Mostrar totales disgregados**. Si está activada, en lugar de mostrar un único total de entrenadores apuntados, lo disgrega además por equipos. Opción desactivada por defecto.

2. **Mostrar «+1» disgregados por línea**. Requiere la opción *Boton «+1» por cada equipo* del apartado *Funcionamiento de incursiones* (se marca automáticamente si es necesario). Si está activada, muestra los +1 con el color correspondiente en cada línea. Opción desactivada por defecto.

3. **Mostrar horas en formato AM/PM**. Si está activada, muestra las horas con el formato de 12 horas seguido de AM o PM. Solo afecta a la visualización de las incursiones. Opción desactivada por defecto.

4. **Tema de iconos**. Permite cambiar el tema de iconos entre uno de los disponibles. Cada vez que lo pulsas, cambia el tema por otro entre los temas disponibles.

5. **Agrupar apuntados por nivel/equipo**. En lugar de mostrar los apuntados por orden temporal, los agrupa por equipo y por nivel. Opción desactivada por defecto.

6. **Marcar apuntados tarde**. Marca en el listado los entrenadores que se hayan apuntado tarde con un 🐌. Se puede configurar para 1, 3, 5 o 10 minutos antes de la hora fijada de la incursión. Opción activada por defecto con 1 minuto.

#### Funcionamiento de incursiones ####

1. **Botón «Tardo»**. Si está activada, aparecerá un nuevo botón en las incursiones para que los entrenadores puedan avisar si van a llegar tarde. Opción desactivada por defecto.

2. **Botones «¡Lo tengo!»**. Si está activada, aparecerán unos botones que permiten mostrar si has capturado o no el Pokémon de la incursión. Los botones solo aparecen a partir de la hora de inicio de la incursión y durante las siguientes seis horas. Opción desactivada por defecto.

3. **Botón «+1»**. Si está activada, aparecerá un botón que permite indicar que vas con acompañantes a la incursión. Se puede configurar un máximo de 1, 2, 3, 5 y 10 acompañantes. Opción activada por defecto y configurada con 5 acompañantes como máximo.

4. **Botón «+1» por cada equipo**. Requiere la opción *Botón «+1»* (se marca automáticamente si es necesario). Si está activada, muestra tres botones «+1», uno por equipo, en vez de un único botón. Esta opción solo tiene sentido si tienes activada la opción de vista de incursión *Mostrar totales disgregados* o *Mostrar «+1» disgregados por línea*. Opción desactivada por defecto.

### Ubicaciones ###

Las ubicaciones de los gimnasios tienen que configurarse en cada grupo de forma independiente. Un grupo no conoce las ubicaciones de los demás grupos.

Para comenzar, debes crear una [hoja de cálculo de Google](https://docs.google.com/spreadsheets/u/0/) con 4 columnas:

1. Nombre del gimnasio
2. Latitud en formato numérico (por ejemplo 42.211345)
3. Longitud también en formato numérico
4. Palabras clave separadas por comas (pueden tener espacios)
5. Etiquetas (opcional)

Esta lista se puede generar a partir de los gimnasios de Gymhuntr [siguiendo esta guía](http://telegra.ph/Lista-de-gimnasios-para-Detective-Pikachu-10-06). Ahorra muchísimo tiempo, así que es recomendable hacerlo así.

Por defecto, Google intenta formatear los números y los estropea. Antes de empezar a escribir los datos, debes seleccionar las columnas B y C y eliminar el formato, como se muestra en la siguiente animación.

![Esto nos pasa por utilizar las hojas de cálculo como tablas](gsp.gif)

La cuarta columna es **muy importante**, ya que es la que permite encontrar los gimnasios. Revisa la sección sobre [mejorar la búsqueda de ubicaciones](#mejorar-la-búsqueda-de-ubicaciones) con calma.

La quinta columna es opcional y siempre puedes cubrirla más tarde. Revisa la sección sobre [etiquetas](#etiquetas) donde se explica un poco más en detalle.

Una vez tengas lista la hoja de cálculo, debes pulsar en el botón **Compartir** para obtener un enlace público a la hoja de cálculo y establecerlo con el comando `/setspreadsheet` en el grupo. Por ejemplo:

    /setspreadsheet https://docs.google.com/spreadsheets/d/1s2K8_hayc1aHt8bZeKucRz0s4G4rn9YUrDB2ZvvEJ4A/edit?usp=sharing

Una vez establecida, debes utilizar el comando `/refresh` para que la cargue. Cada vez que hagas cambios, debes volver a utilizar `/refresh` para recargar la lista. No es necesario volver a utilizar `/setspreadsheet` a no ser que cambies la hoja de cálculo por otra.

Se pueden probar las ubicaciones preguntando por ellas con el comando `/gym`. Por ejemplo:

    /gym león de boca abierta

Para listar todos los gimnasios conocidos puedes usar el comando `/list`. Este comando puede mostrar la lista cortada si hay demasiados gimnasios, sobre 120 gimnasios o más.

**¡Importante!** Si les cambias el nombre (primera columna), los gimnasios se borran y se vuelven a crear, y todas las alertas que los usuarios tuvieran creadas se pierden. También puede afectar a incursiones en curso.

#### Mejorar la búsqueda de ubicaciones ####

Cuando crees las palabras clave ten en cuenta que las tildes y mayúsculas se ignoran. Además, los caracteres como «ç» y «ñ» se transforman a «c» y «n». Es decir, la palabra clave *Peñíscola* a efectos de búsqueda es la misma que *peniscola*. Puede haber varias palabras clave separadas por comas y se ignoran los espacios entre las comas y las palabras.

El bot utiliza las palabras clave para encontrar la ubicaciones. Busca por orden de arriba a abajo en el documento y empezando por la primera hasta la última palabra clave si alguna de las palabras clave esté **contenida** en el texto que escribe el usuario.

Por ejemplo, el usuario puede buscar *Estación de trenes*. Supongamos que además el gimnasio se llama así. Unas buenas palabras clave serían: *estación tren, estación de tren*.

Supongamos que el gimnasio en realidad se llama *Escultura al trabajo bien hecho*, pero el usuario se ha referido a él como *Estación de trenes* porque habitualmente se le llama así. Unas buenas palabras clave en este caso serían: *estación tren, estación de tren, escultura al trabajo, escultura trabajo, trabajo bien*.

Por un momento supongamos que hay otro gimnasio en una estación de autobuses. El gimnasio se llama *Monolito de piedra* por un monolito que hay allí, pero la gente habitualmente le llama *estación de autobuses*. Unas buenas palabras clave serían: *estación auto, estación de auto, monolito piedra, monolito de piedra*.

Habiendo dos estaciones, es importante que **no** se utilice la palabra *estación* suelta, porque podría coincidir el gimnasio equivocado. Tendría que ir acompañada siempre de otras palabras.

##### ¿Qué hacer si se reconoce el gimnasio equivocado? #####

Te recomendamos leer con atención el apartado anterior, pero lo explicamos una vez más con otro ejemplo un poco más complicado.

Supongamos que hay dos gimnasios llamados *Fuente*. Si utilizas como palabra clave *Fuente* de forma suelta, reconocerá uno de los dos, el primero que hayas puesto en el listado.

Si ambos gimnasios tienen la misma importancia, deberías mejorar las palabras clave añadiendo más información. Aunque se llamen igual en el juego, la gente los llamará de otra forma para diferenciarlos. Aprovecha eso para mejorar las palabras clave. Por ejemplo, una podría tener de palabra clave *fuente de la alameda* y la otra *fuente de la plaza de toros*.

Si uno de los gimnasios apenas se utiliza porque está muy lejos o no suelen salir incursiones allí, puedes hacer esto mismo pero dejando la palabra clave *fuente* al gimnasio con mayor importancia.

#### Etiquetas ####

Las etiquetas sirven para marcar los gimnasios con determinados emojis, que sirven para identificarlos mejor como potenciales receptores de una incursión EX. Las etiquetas se ponen en la quinta columna como las palabras clave, separadas por comas. Las soportadas son las siguientes:

* `parque` - El gimnasio se encuentra dentro de un parque (🌳).
* `jardín` (se puede poner con o sin tilde) - El gimnasio se encuentra dentro de un jardín (🌷).
* `juegos` - El gimnasio se encuentra dentro de un parque de juegos (⚽️).
* `hierba` o `campo` - El gimnasio se encuentra en un campo o terreno con hierba (🌱).
* `patrocinado` - Es un gimnasio patrocinado (💵).
* `ex` - Ha tenido incursiones EX en el pasado fuera del periodo de pruebas (🌟).

Para saber si un gimnasio está realmente considerado como potencial receptor de una incursión EX, puedes utilizar [guías como esta](https://www.reddit.com/r/TheSilphRoad/comments/7pq1cx/how_i_created_a_map_of_potential_exraids_and_how/). Ten en cuenta que el criterio no está completamente definido y puede cambiar con el tiempo.

### Modo niñero ###

El modo niñero evita que la gente hable en un grupo, borrando todos los mensajes que pongan los usuarios (no los administradores).

El comando `/settalkgroup` permite definir un grupo para hablar. Si está el modo niñero activado, el bot recordará el enlace al grupo para hablar cada vez que hable alguien. Por ejemplo:

    /settalkgroup @PGSDC
    /settalkgroup https://t.me/joinchat/XXs3XkzYsXXxnvbtxxe11x

### Zona horaria ###

El bot reconoce la hora que escriben los usuarios y hace operaciones con ellas, por lo que es importante que la hora que utilice el bot se corresponda con la hora real de tu grupo.

Para establecer la zona horaria correcta se debe utilizar el comando `/settimezone` con la zona horaria correspondiente como parámetro siguiendo el formato del [listado de zonas horarias de la IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Por ejemplo:

    /settimezone Europe/Madrid
    /settimezone Atlantic/Canary

### Rankings ###

El bot puede mostrar los rankings de la **semana pasada** (contando de lunes a domingo) y del **mes pasado**, con los comandos `/ranking week` (o simplemente `/ranking`) y `/ranking month`.

En estos rankings aparecen solo los 10 usuarios con mayor participación en incursiones. En caso de empate en número de incursiones, se muestran en la misma posición. Solo se tienen en cuenta los usuarios que se han apuntado a la incursión **antes de la hora de inicio** y que han pulsado el botón de **Estoy**.

### Otros comandos exclusivos para administradores ###

Para revertir la cancelación de una incursión puedes usar el comando `/descancelar`. Se utiliza exactamente igual que el `/cancelar`, pero sobre incursiones canceladas.

Un administrador siempre puede cancelar incursiones con el comando `/cancelar`, aunque sean antiguas. Normalmente, un creador de incursión solo puede cancelar incursiones que no sean más antiguas de tres horas.

Para reflotar todas las incursiones activas una vez, sin necesidad de usar el reflotado automático, se puede usar el comando `/reflotaractivas`. También se pueden reflotar todas las incursiones, incluídas las EX que transcurrirán dentro de varias horas o días, con `/reflotartodas`.
