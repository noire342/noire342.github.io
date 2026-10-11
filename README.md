# Lorenzo Garrone — static project website

Public-only English pages for Approssimazione and Nyanime. No application binaries, private source, source modules, catalogue, credentials or analytics are included. Nyanime's proposed licence remains explicitly scoped and under review.

Serve this directory as the web root; all navigation is rooted at `/`. GitHub Pages can serve it as the `noire342.github.io` user site. Generation alone does not publish anything.

`/nyanime/open/` opens a shared reference in the app after an explicit tap. The
fragment is processed locally with no network requests, analytics or storage;
titles are displayed as text. Source references remain opaque and are resolved
only by the app's enabled modules. The site never fetches source content.

`.well-known/assetlinks.json` contains public certificate fingerprints for
`it.lorelore.nyanime`: the actual Play Console app-signing certificate and the
local upload-signed test build. These are hashes of DER certificates, not PEM
file checksums or private signing keys.
