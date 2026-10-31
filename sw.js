// Service worker volontairement minimal : sa seule raison d'être ici est de
// satisfaire le critère d'installabilité de Chrome/Android (manifest +
// service worker + icônes) — voir la discussion avec Julien à ce sujet.
// Ne fait aucun cache applicatif pour l'instant afin de ne surtout pas
// risquer de servir une version périmée de v3.html pendant que Julien
// itère dessus ; passthrough réseau pur.
self.addEventListener("install", function (event) {
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  self.clients.claim();
});

self.addEventListener("fetch", function (event) {
  event.respondWith(fetch(event.request));
});
