
Para ejecutar:

1º Se debe crear una base de datos en mongodb con las siguientes colleciones:

- messages a partir de messages.json con: mongoimport --db proyecto --collection messages --type json --file messages.json --jsonArray

- users a partir de users.json con: mongoimport --db proyecto --collection users --type json --file users.json --jsonArray

2º Para no instalar paquetes innecesarios, se recomienda iniciar un virtual enviroment, primero ejecutar pipenv install desde la carpeta de la API y luego iniciar el environment con pipenv shell

3º Utilizar gunicorn o Python para correr y entrar en la direccion y puerto especificado al momento de hacer run. 

Ejecutar gunicorn main:app --workers=3 --reload

El archivo donde se encuentra la api de flask es main.py, esta super explicito que hace cada ruta, pero igual las especificaremos acá.

4º Para las rutas GET:

- Una ruta que al recibir el id de un mensaje, obtenga toda la información asociada a ese mensaje:
Ingresar a {dirección}/messages/byid/<int:id>, con <int:id> un número(id mensaje)

- Una ruta que al recibir el id de un usuario, obtenga toda la información de ese usuario, junto con los mensajes emitidos por él:
Ingresar a {dirección}/users/byid/<int:id>, con <int:id> un número (id user)

- Una ruta que al recibir el id de dos usuarios, obtenga todos los mensajes intercambiados entre dichos usuarios:
Ingresar a {dirección}/messages/byusers/<ids>, con <ids>  de a forma id1_id2 (deben ser números)

Hacer búsquedas por texto: 
- Agregar una o más frases que sí o sí deben estar en el mensaje: 
Ingresar a {dirección}/messages/bytext/inorin/<text>, con <text> de la forma frase1_frase2_...
Ej: http://127.0.0.1:5000/messages/bytext/inorin/Hey! Me_ Hola que tal : aquí se buscan mensajes que tengan la frase Hey! Me y hola que tal, no necesariamente juntas.

- Agregar una o más palabras que deseablemente deben estar, pero no son necesarias.
Ingresar a {dirección}/messages/bytext/deseable/<text>, con <text> de la forma palabra1_palabra2_...
Ej: http://127.0.0.1:5000/messages/bytext/deseable/Hey!_Me: aquí se buscan mensajes que tengan deseablemente la palabra Hey!  y la palabra Me, no necesariamente juntas y pueden no tenerlas.

- Agregar un conjunto de palabras que no pueden estar en el mensaje.
Ingresar a {dirección}/messages/bytext/notin/<text>, con <text> de la forma palabra1_palabra2_...
Ej: http://127.0.0.1:5000/messages/bytext/notin/Hey!_Hola!: aquí se buscan mensajes que no tengan la palabra Hey! Ni Hola!.

- Además, se pueden hacer las tres búsquedas al mismo tiempo: 
Ingresar a {dirección}/messages/bytext/consulta/<text>, con <text> de la forma frasedebeestar1_frasedebeestar2_...+palabradeseable1_palabradeseable2_...-palabrano1_palabrano2...
Ej: http://127.0.0.1:5000/messages/bytext/consulta/Hey!+Me-encanta: aquí queremos que Hey! esté sí o sí, Me deseable y no esté la palabra encanta.
Pueden poner consultas como "+me-encanta", "-encanta" ,"+encanta", etc. Cualquiera que tenga una o más de las cosas es válida

- Si se desea hacer la busqueda anterior pero para un "sender" en especifico, se debe agregar la id al final despues de un = EJ: {dirección}/messages/bytext/consultaid/quiero_Sucede+jugar-Megaman-jaja-que=103

5º Para las rutas POST
- Dado dos ids de usuarios i y j, una ruta que inserte un mensaje a la base de datos que esta ́ enviando el usuario i al usuario j.
Ingresar a {dirección}/messages/enviar/<ids>: con <ids> de la forma id1_id2. Además, los atributos de POST deben ser 'message', 'lat', 'long y 'date' validos. Ahí, la id1 sería el sender, id2 sería el receptan  y el mensaje con los atributos dados se agregan a la base de datos de mensaje.

6º Para las rutas DELETE
- Dado un id de mensaje, se debe eliminar ese mensaje.
Ingresar a {dirección}/messages/eliminar/<int:id>: con <int_id> un número que corresponde al id del mensaje. Ahí, el mensaje será retirado de la base de datos.


