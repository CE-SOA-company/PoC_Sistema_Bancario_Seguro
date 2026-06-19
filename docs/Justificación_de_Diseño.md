# Justificación de Value Objects — SecureBankito

## ¿Por qué un elemento es un Value Object?

Un Value Object se define por tres propiedades: no tiene identidad propia, es inmutable, y se compara por valor. En el proyecto, los siguientes elementos cumplen estrictamente esas propiedades.

---

## ClearanceLevel e IntegrityLevel

Son enums que representan niveles de seguridad. No tienen identidad: un `ClearanceLevel.ORO` es exactamente igual a cualquier otro `ClearanceLevel.ORO` en cualquier parte del sistema. No tiene sentido preguntarse *cuál* ORO es, porque son indistinguibles. Al heredar de `IntEnum` son inmutables por definición y se comparan por valor, lo que permite escribir directamente `actor.integrity < cuenta.required_integrity_level` en las reglas Biba.

## NivelSeguridad

Agrupa `ClearanceLevel` e `IntegrityLevel` en un único objeto. Se modela como Value Object porque las etiquetas de seguridad de un sujeto no tienen identidad propia: lo que importa es *qué niveles tiene*, no *qué objeto los contiene*. Dos instancias con `clearance=ORO, integrity=NIVEL_3` son intercambiables. Su inmutabilidad (`frozen=True`) garantiza que un token JWT emitido siempre refleje el nivel con el que fue firmado, sin posibilidad de mutación posterior.

## Credenciales

El par `username` / `password_hash` describe datos de acceso, no una persona. Dos conjuntos de credenciales idénticos son equivalentes en términos de autenticación. Si un usuario cambia su contraseña, se producen nuevas `Credenciales`; no se muta el objeto existente. Esto obliga a que cualquier cambio pase por el repositorio, evitando actualizaciones silenciosas en memoria.

## Dinero

Cien dólares son cien dólares sin importar de qué cuenta provienen. `Dinero(100, 'USD')` es igual a cualquier otro `Dinero(100, 'USD')`: no hay un "cuál" que diferenciarlos. Las operaciones de suma y resta no modifican el objeto sino que producen uno nuevo, haciendo imposible la corrupción de saldos por referencia compartida.

## Usuario (Entity)

Usuario es una Entity porque tiene identidad propia representada por su campo id. Dos usuarios con exactamente el mismo username, mismo clearance y misma integridad son personas distintas en el sistema: tienen historiales de transacciones propios, accesos propios y ciclos de vida independientes.