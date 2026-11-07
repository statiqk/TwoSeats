// Service worker de Deux Places.
// - Installabilité (Chrome/Android) : passthrough réseau, aucun cache applicatif
//   (pour ne jamais servir une version périmée de l'appli).
// - Notifications push : affiche la notification envoyée par la base quand
//   l'ajout / le vote / le match de l'autre personne arrive, appli fermée ou non.
self.addEventListener("install", function (event) {
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  self.clients.claim();
});

self.addEventListener("fetch", function (event) {
  event.respondWith(fetch(event.request));
});

self.addEventListener("push", function (event) {
  var data = {};
  try { data = event.data ? event.data.json() : {}; } catch (e) { data = { body: event.data ? event.data.text() : "" }; }
  var title = data.title || "Deux Places";
  event.waitUntil(self.registration.showNotification(title, {
    body: data.body || "",
    tag: data.tag || undefined,
    icon: "./icon-192.png",
    badge: "./icon-192.png",
    data: { url: data.url || "./" }
  }));
});

self.addEventListener("notificationclick", function (event) {
  event.notification.close();
  var target = (event.notification.data && event.notification.data.url) || "./";
  event.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
    for (var i = 0; i < list.length; i++) {
      if ("focus" in list[i]) return list[i].focus();
    }
    return self.clients.openWindow(target);
  }));
});
