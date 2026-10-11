# Manage your Nyanime data

These controls describe the development candidate. Local deletion, remote deletion and credential revocation are separate actions.

## On this device

Remove individual downloads in Nyanime. To reset private library data, progress, preferences and local sessions, use Android Settings → Apps → Nyanime → Storage → Clear data. Uninstalling normally removes private app storage. Files saved in external/shared storage may remain and need separate deletion.

## Exported and periodic backups

Delete exports in the folder you selected and any location to which you copied or shared them. Periodic backup retention applies only to its managed location and policy. A local `.nyabk` can contain credentials without encryption. Clearing app data does not erase independent copies. If a copy was exposed, revoke affected tokens or change credentials at the relevant service; deleting the file alone is insufficient.

## Telegram backup files and synchronization

Disable scheduled backups or device synchronization to stop future activity. Delete individual copies through the backup controls or Telegram channel, including old version-1 plaintext files you no longer need. Pinned/protected copies may be excluded from automatic retention. Turning features off, revoking a device or disconnecting Telegram does not delete existing channel files.

Logout ends the Nyanime Telegram session and clears its local session/cache state. Use Telegram's account controls for other active sessions or account deletion. Do not erase your only recovery code or last approved device before confirming that you no longer need to recover encrypted content. Device removal cannot erase copies or secrets a device already received.

## Trackers, modules and receivers

Disconnect trackers in Nyanime, then revoke account access through each external service where needed. External progress/history and account deletion are managed by that provider. Removing a source module does not revoke credentials at its host. Disconnect receivers and delete shared files on those devices separately.

## Rooms and recipients

Leaving a together room ends participation. It does not guarantee deletion of previously delivered events or information held by relays and participants. Keep invitation keys private.

## No Nyanime account to delete

This candidate requires no Nyanime account and has no enabled public profile/friend system. There is no developer-held account library to erase remotely. If a future release introduces account creation, its deletion controls and policy must be supplied for that release.

## Ask the developer

For information actually held by Lorenzo Garrone, such as an email conversation, send a request to [lorenzogarrone2000@gmail.com](mailto:lorenzogarrone2000@gmail.com). Do not send passwords, tokens, recovery codes or complete backups. The developer cannot remotely erase your device-only library or another service's account.
