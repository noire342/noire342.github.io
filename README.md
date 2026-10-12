# Lorenzo Garrone — static project website

Public-only English project pages. No application binaries, private source,
source modules, catalogue, credentials or analytics are included.

The Nyanime card opens the official website at https://owouwuiwi.github.io/.
`/nyanime/` also redirects there, preserving section anchors without forwarding
query parameters. Existing privacy, licence and component-source archive URLs
remain available for the earlier Play development candidate they document;
the shared-content landing page and its Android association are unchanged.

Serve this directory as the web root; all navigation is rooted at `/`. GitHub Pages can serve it as the `noire342.github.io` user site. Generation alone does not publish anything.

`/approssimazione/` presents the approximate-time Wear OS project in English.
The interactive clock is an original web illustration of the concept, not an
app screenshot or a reproduction of its implementation. It runs locally, with
no network requests, storage or analytics. The project information reflects the
creator's description; no unverified download or availability claim is made.
Its styles and script are isolated from the Nyanime pages. The root homepage
remains a two-card project index.

The root index loads `assets/projects-motion.css` for a staggered entrance and
subtle card, logo and arrow feedback. Motion uses CSS only, runs once on entry,
respects reduced-motion preferences and cancels entrance effects for keyboard
focus. Project subpages and their scripts remain independent of this layer.

Approssimazione uses a floating, sticky glass navigation bar, matching the
official Nyanime site's proportions in its own cool palette. Narrow layouts
keep the project identity and compact, labelled project/contact controls.

`/nyanime/open/` opens a shared reference in the app after an explicit tap. The
fragment is processed locally with no network requests, analytics or storage;
titles are displayed as text. Source references remain opaque and are resolved
only by the app's enabled modules. The site never fetches source content.

`.well-known/assetlinks.json` contains public certificate fingerprints for
`it.lorelore.nyanime`: the actual Play Console app-signing certificate and the
local upload-signed test build. These are hashes of DER certificates, not PEM
file checksums or private signing keys.
