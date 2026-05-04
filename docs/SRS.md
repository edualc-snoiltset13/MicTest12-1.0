# Software Requirements Specification — MicTest12

| Field    | Value                                |
|----------|--------------------------------------|
| Project  | MicTest12 (repo: `MicTest12-1.0`)    |
| Document | Software Requirements Specification  |
| Version  | Draft v0.1                           |
| Date     | 2026-05-04                           |
| Status   | Initial draft. Several requirements are placeholders pending product confirmation; see Appendix B. |

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for **MicTest12**, an Android
application for testing the audio input (microphone) capabilities of a
device. It is intended for the project's developers, QA engineers, and any
reviewer who needs to understand what MicTest12 is supposed to do before
code is written.

### 1.2 Scope
MicTest12 is a standalone Android application. It lets a user verify that
their device's microphone — built-in, wired, Bluetooth, or USB — is working
correctly, and surfaces enough information (input level, sample rate,
clipping, latency) to diagnose common audio-input problems. The app is
fully offline; no audio or telemetry leaves the device.

The app is **not** a generic recording studio, a voice-memo app, or a
network speech service.

### 1.3 Definitions, acronyms, abbreviations
- **SRS** — Software Requirements Specification.
- **API level** — Android platform version number.
- **dBFS** — decibels relative to full scale.
- **RMS** — root-mean-square (a measure of average signal level).
- **AAudio / AudioRecord / MediaRecorder** — Android audio-input APIs.
- **TalkBack** — Android's built-in screen reader.
- **WCAG** — Web Content Accessibility Guidelines.
- **TBD** — to be determined.

### 1.4 References
- Android `RECORD_AUDIO` permission documentation.
- Android `AudioRecord` and `AAudio` API references.
- WCAG 2.1, level AA.

### 1.5 Document overview
Section 2 gives the wide-angle view of the product. Section 3 lists the
specific functional and non-functional requirements with stable IDs
(`FR-n`, `NFR-n`) for traceability. Appendices hold the glossary, open
questions, and revision history.

---

## 2. Overall Description

### 2.1 Product perspective
MicTest12 is a standalone Android app. It has no backend, no account
system, and no network dependencies. It interacts only with the local
Android audio stack and the user.

### 2.2 Product functions (high level)
- Request and manage the `RECORD_AUDIO` runtime permission.
- Enumerate available audio input devices.
- Display a live input-level meter (peak and RMS, in dBFS).
- Record a short sample and play it back.
- Display the actually-negotiated sample rate, channel count, and audio
  format.
- Detect "no signal" and "clipping" conditions.
- Export a plain-text diagnostic summary that the user can share.

### 2.3 User classes and characteristics
- **End user** — wants a quick "is my mic working?" answer. Limited
  technical knowledge.
- **QA tester** — wants reproducible measurements and the diagnostic
  export. Comfortable with audio terminology.
- **Developer** — uses the app while debugging audio-stack regressions.
  Reads logs, may attach via ADB.

### 2.4 Operating environment
- Android 8.0 (API level 26) and above.
- ARM and x86 architectures.
- Phones and tablets in both portrait and landscape.
- Microphones: built-in, wired (TRRS / 3.5 mm), USB-C, Bluetooth (SCO/A2DP
  where applicable).

### 2.5 Design and implementation constraints
- Must comply with Android's runtime permission model.
- Must work with at least one of `AudioRecord`, `AAudio`, or
  `MediaRecorder`; the choice and its rationale is a design decision and
  not part of this SRS.
- No `INTERNET` permission may be declared.
- The app must remain functional when the user denies or later revokes
  the microphone permission.

### 2.6 User documentation
- In-app help screen explaining the meter, units, and diagnostic export.
- Repository `README.md` covering build and install.

### 2.7 Assumptions and dependencies
- The device exposes at least one usable audio input.
- The Android audio HAL reports input devices accurately enough for
  enumeration.
- The host PC, where applicable, can sideload the APK or install via
  Play Store internal testing.

---

## 3. Specific Requirements

### 3.1 External interface requirements

#### 3.1.1 User interfaces
The app has four primary screens:
- **Home** — entry point, "Start test" call to action, link to help.
- **Permission** — explanation and request flow for `RECORD_AUDIO`.
- **Test** — live level meter, device picker, record/playback controls,
  format readout.
- **Results** — pass/fail summary, detected issues, "Export diagnostics"
  button.

#### 3.1.2 Hardware interfaces
The app must enumerate and select among: built-in mic, wired mic, USB-C
mic, and Bluetooth mic (subject to OS support).

#### 3.1.3 Software interfaces
The app uses Android's audio-input APIs (`AudioRecord` and/or `AAudio`)
and the standard permission and audio-routing system services.

#### 3.1.4 Communications interfaces
None. The app is fully offline and must not declare network permissions.

### 3.2 Functional requirements

| ID    | Requirement |
|-------|-------------|
| FR-1  | The app shall request the `RECORD_AUDIO` permission on first use, explain *why* it is needed, handle denial gracefully, and detect mid-session revocation without crashing. |
| FR-2  | The app shall enumerate all available audio input devices and present them to the user for selection. The currently active device shall be visually distinguished. |
| FR-3  | The app shall display a live input-level meter showing both peak and RMS values in dBFS, updated at no less than 20 Hz. |
| FR-4  | The app shall record a short audio sample (default 3 seconds; user-adjustable up to 10 seconds) and play it back through the device's default output. |
| FR-5  | The app shall display the sample rate, channel count, and PCM format actually negotiated with the audio framework, distinct from any value requested. |
| FR-6  | The app shall detect a "no signal" condition (sustained level below a configurable floor, default −60 dBFS for ≥ 2 s) and a "clipping" condition (peak ≥ −0.1 dBFS occurring on ≥ 1 % of frames in a 1 s window) and surface both to the user. |
| FR-7  | The app shall export a plain-text diagnostic summary including device model, Android version, selected input device, negotiated format, observed peak/RMS, and any detected issues, via the standard Android Share intent. |

### 3.3 Non-functional requirements

| ID     | Requirement |
|--------|-------------|
| NFR-1  | **Performance** — End-to-end meter latency (acoustic event → UI update) shall not exceed 100 ms on the reference device set. |
| NFR-2  | **Reliability** — The app shall not crash when permission is denied at first prompt or revoked mid-session. All such cases shall route the user back to the Permission screen. |
| NFR-3  | **Usability** — The primary "Start test" action shall be reachable in ≤ 2 taps from a cold launch (excluding the first-run permission prompt). |
| NFR-4  | **Portability** — The app shall run on Android 8.0 (API 26) and above, in both phone and tablet form factors, in both portrait and landscape. |
| NFR-5  | **Privacy** — No audio data, log data, or telemetry shall leave the device. The app shall not request the `INTERNET` permission. |
| NFR-6  | **Accessibility** — All interactive elements shall have TalkBack labels. The level meter shall meet WCAG 2.1 AA contrast in both light and dark themes. |

### 3.4 Other requirements
- **Localization** — v1 ships in English. Strings shall live in
  `res/values/strings.xml` to enable later translation without code
  changes.
- **Logging** — Logs are local-only and disabled by default in release
  builds; a hidden developer toggle may enable verbose logging.
- **Build / release** — Reproducible Gradle build; release builds are
  signed and shrunk (R8). Output: a single APK and an AAB.

---

## Appendix A — Glossary
See §1.3.

## Appendix B — Open questions / TBD
- B-1 Confirm minimum supported Android version (currently API 26).
- B-2 Decide whether USB-C microphones are in scope for v1.
- B-3 Decide whether Bluetooth A2DP input (where the platform allows it)
  is in scope for v1, or only SCO.
- B-4 Decide whether to ship a frequency-sweep / tone-generator test in
  v1 or defer to v2.
- B-5 Choose primary audio-input API (`AudioRecord` vs. `AAudio`).
- B-6 Confirm reference device set used to validate NFR-1 latency.
- B-7 Confirm pass/fail thresholds on the Results screen.

## Appendix C — Revision history
| Version    | Date       | Author | Notes                       |
|------------|------------|--------|-----------------------------|
| Draft v0.1 | 2026-05-04 | Claude | Initial draft for review.   |
