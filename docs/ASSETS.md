# Asset provenance and distribution boundary

The Git repository contains Python source and one audio file:
`sounds/eon_startup.wav`. Its generator is `sounds/startup_sound.py`; publication
audit compares the distributed WAV against a freshly generated file.

The owner-supplied Fusion design and its extracted preview are in `cad/`.
The owner confirmed rights to the model and selected CC BY 4.0 for those files;
see `cad/README.md` and `cad/LICENSE.md`. They are separate from downloaded
models and runtime packages, which remain excluded below.

The following local resources are excluded from Git and must stay excluded:

| Resource | Local location | Review before redistribution |
| --- | --- | --- |
| Vosk speech model | `models/vosk/` | Exact model identity, source URL, license, notices |
| Piper runtime and dependencies | `tools/piper/` | Exact release, bundled dependency licenses and notices |
| Ukrainian Piper voice | `tools/piper/voices/` | Exact voice model card, license and attribution |
| Downloaded sound recordings | `freesound_community-*.wav` | Original asset pages, creators, licenses and attribution |
| Optional detection models | `models/` | Model-specific license and source |

Filenames alone do not establish permission to redistribute. Source URLs and
license records for these local downloads have not been established by this
audit. They are not part of the publication candidate. Do not upload an archive
of the working directory, which would bypass these exclusions.

Runtime recordings, photos, camera frames, personal memory and backups are
private data, not distributable project assets. Keep them outside commits.

Project software is licensed under GPL-3.0-only; the owner confirmed the
license choice and rights to their code. See the root LICENSE. This does not
relicense external dependencies or third-party assets. CAD has its own terms
in cad/README.md.
