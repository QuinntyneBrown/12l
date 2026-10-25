# Estimate — Edit profile

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. The listings photo pipeline (`IImageInspector`, `IPhotoStorage`, `PhotoProcessingJob`, `ImageSharpPhotoProcessor`) already exists, so the avatar path adds a processor and a message type rather than new image handling. The region list is assumed to be US states and the District of Columbia (`<TO SUPPLY>`).
[Detailed design](../../detailed-designs/accounts/edit-profile/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `EditProfilePage` with `loading`, `error`, `invalid`, `submitting`, `success` and conflict states | 8 |
| `AvatarPicker` with client pre-checks, upload progress and preview | 6 |
| `ProfileApi` | 1 |
| `ProfileController` (3 endpoints) | 3 |
| `GetMyProfileQuery`, `UpdateProfileCommand`, validator and handler with row-version check | 6 |
| `Bio` and `PublicLocation` value objects and the region list | 2 |
| `UploadAvatarCommandHandler` | 4 |
| `AvatarPhotoProcessor` and `ProcessAvatarPhoto` dispatch | 5 |
| `MemberDisplayNameChanged` event publication | 1 |
| Migration for profile columns | 1 |
| Acceptance tests for `L2-004` criteria 1 to 5 | 7 |
| **Total** | **44** |

## Minimal scope

The minimal scope keeps display name, bio and public location editing with server validation, and avatar upload through the shared pipeline, satisfying `L2-004`. It drops the optimistic-concurrency check (last write wins), the upload progress and local preview (the avatar appears once processed), and the display-name change event (cached cards refresh on their normal expiry). Removing these items saves 6 hours.

**Minimal scope total: 38 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Row-version check and conflict state | Concurrent edits from 2 devices overwrite each other | 2 |
| Upload progress and local preview | The member waits for processing with no preview | 3 |
| `MemberDisplayNameChanged` event | Cached listing cards show the old name until their cache expires | 1 |
