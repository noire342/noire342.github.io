# Nyanime Privacy Policy

Last reviewed: 11 October 2026. This notice describes the development candidate and this website. It must be checked against each actual application release. This website does not offer an application download.

## Who to contact

Nyanime is developed by Lorenzo Garrone. Contact [lorenzogarrone2000@gmail.com](mailto:lorenzogarrone2000@gmail.com) for privacy questions or requests concerning information held by the developer. No Nyanime account is required. Public Nyanime profiles and friend features are disabled in this candidate.

## Your library and local information

Nyanime stores library entries, titles and source identifiers, viewing and reading progress, history, preferences, downloaded media, cache files and configured service credentials on your device. They support the features you use. They are not automatically uploaded to a developer-operated library server. Network features described below send necessary information to the services involved.

Clearing private app storage removes local app information. Downloads and exported files outside private app storage need separate deletion. This candidate disables Android automatic app backup; backups you export or configure in Nyanime are separate.

## Exported backups can contain credentials

Local and periodic `.nyabk` exports are compressed files, not encrypted vaults. Depending on selected options they can include library data, history, progress, settings, source configuration and credentials or tokens. They exclude downloaded videos and manga pages. Protect copies in shared folders or other cloud services.

An encrypted Telegram backup and a local export are different files. Restoring an encrypted cloud backup makes its contents available to the app locally. Deleting a backup does not revoke credentials it contained.

## User-selected sources and network requests

The planned public base app has no preinstalled content sources or developer-managed source catalogue. Portable `.nyasource` modules require user import and approval. The candidate validates declared hosts and routes permitted requests through its network broker. This development feature does not certify a third-party module's practices or content rights.

When you use a source or remote media, its host can receive your IP address, request timing, requested titles/content and technical headers. Authentication, cookies or tokens may be sent where required by your configuration. A module signature identifies its signing key and package integrity; it is not a privacy audit, copyright certificate or authorization from a content owner. Review the publisher, permissions and host policy before approval.

## Metadata, images and connected trackers

Catalogue, artwork and work-information features query external metadata and image services. This candidate includes AniList and Kitsu catalogue queries; optional work-information enrichment uses AniList, TVmaze and Wikidata. Requests can contain search text, titles or public work identifiers. Image hosts receive image requests and technical data. Work-information enrichment does not send source media URLs, source cookies, credentials or personal progress to these metadata providers. Results may be cached locally.

When a tracker is available and you connect it, the service handles authentication and library/progress updates. OAuth connections are disabled where this candidate lacks its own application registration. Disconnecting does not delete the external account or stored history; use the service's controls to revoke access.

Optional AniSkip requests include a MyAnimeList identifier, episode number and episode duration, plus normal network information. They do not include the stream URL or authentication token. Identifier conversion may also query AniList. Optional schedule, guide or news features contact their enabled service or user-approved module when available. This notice does not promise that a future integration is already enabled.

## Together rooms

Watch and read together sessions exchange encrypted room payloads through third-party Nostr relays. Participants holding the invitation/key receive coordination information such as display names, selected media and progress. Relays can observe connection IP addresses and public event metadata, including identifiers, timestamps and traffic patterns. Payload encryption does not hide this metadata.

Share invitations only with intended participants. Leaving stops participation; it cannot guarantee deletion of copies retained by participants or relays. Rooms do not automatically publish your full library history.

## Optional Telegram backups and device synchronization

Telegram Cloud uses TDLib and a private channel in your Telegram account. This candidate requires authenticated encryption of new backup contents in the app before upload. Archive keys are available through approved devices or the recovery flow. It refuses new plaintext uploads rather than falling back to Telegram cloud encryption alone. Old unencrypted version-1 backups remain readable for restore compatibility; they are not encrypted retroactively.

Keep your recovery code private and independently available. Telegram login alone does not recover the app's encryption keys. Losing all approved devices and the recovery code can make protected backups inaccessible. Anyone obtaining recovery authority or authorized-device keys may access protected contents. This application-layer protection is under development and is not yet a completed-release security guarantee.

Telegram still handles login data, account/channel association, file sizes, message timing, backup manifest metadata and technical connection information. Ordinary Telegram cloud channels are not Secret Chats. See [Telegram's Privacy Policy](https://telegram.org/privacy) for its processing and retention.

Device synchronization is a separate explicit option using the Telegram archive. When enabled for associated devices, it transfers encrypted portable library changes, progress and selected settings. Portable-credential sharing is separately configurable and off by default. Creating backup protection alone does not enable continuous synchronization. Downloaded media and Telegram session credentials are excluded from backup contents.

Disabling automatic backup or synchronization stops future scheduled activity, not existing channel messages. Delete remote copies in the backup controls or Telegram channel. Disconnecting ends the app's session and removes its local session/cache state through logout; it does not delete the Telegram account or previously uploaded channel files.

## Cast, receivers and system services

Casting or receiver pairing sends session information and media locations to that device. Depending on the transport, it can receive media URLs, subtitles and required request headers, potentially including sensitive authorization data. A local relay may request media on the receiver's behalf. Use a trusted receiver and network.

Network/DNS providers, Android and distribution platforms have their own processing practices. A future Play release would use its platform's delivery/update mechanisms. This notice does not assert identical network behavior across distributions.

## This website and email

These static pages do not embed analytics, advertising, remote fonts, contact forms or third-party scripts, write browser storage or set application cookies. Assets are served with the pages. If hosted on GitHub Pages, GitHub logs visitors' IP addresses for security purposes: see [GitHub's Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) and [Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). External links lead to services with their own policies.

If you email the developer, the developer and email provider process your address, message and attachments to handle your request. Avoid sending passwords, tokens, recovery codes or full backups. Correspondence is retained while needed to handle the request and applicable legal obligations. Responding and maintaining necessary correspondence relies on the developer's legitimate interest in supporting the project and handling requests, subject to applicable data-protection law.

## Retention, rights and deletion

Local information remains until removed or app storage is cleared. Rebuildable caches may be replaced or cleared. Automatic backup retention can remove older unprotected copies under its configured policy; pinned/protected copies and files outside managed locations may remain. Third parties and recipients apply their own retention and may process data in other countries. Nyanime does not control their retention or international-transfer safeguards.

You can disable optional features, disconnect accounts and delete local files. For information held by the developer, applicable rights may include access, correction, deletion, restriction, portability, objection, withdrawal of consent for consent-based processing and a complaint to your competent data-protection authority. Their scope depends on the law and processing context. The developer cannot remotely erase a device-only library or independently delete another provider's account. See [Manage data](https://noire342.github.io/nyanime/data/) for practical steps.

This notice will change with relevant behavior. Publishing it does not establish release availability, a completed dependency audit or Google Play acceptance.
