# Software Requirements Specification

**Project:** MicTest12-1.0
**Version:** 1.0.1
**Date:** 2026-04-26
**Status:** Draft

## Table of Contents
1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Specific Requirements](#3-specific-requirements)
4. [Acceptance Criteria](#4-acceptance-criteria-per-requirement)
5. [Verification and Validation](#5-verification-and-validation)
6. [Open Questions](#6-open-questions)
7. [Appendix A. Revision History](#appendix-a-revision-history)

> **Note on assumptions.** The repository currently contains only a placeholder
> README ("Tester test 1.0"). This SRS assumes MicTest12-1.0 is a **web-based
> microphone testing utility** that helps end users verify that their
> microphone hardware is working, measure basic audio characteristics
> (input level, signal-to-noise, latency), and record short test clips. The
> document follows the IEEE 830-1998 outline. If the actual product scope is
> different (desktop app, CLI, voice analysis, etc.), revise Sections 1.3, 2,
> and 3 accordingly.

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the functional and
non-functional requirements for **MicTest12-1.0**, a browser-based application
that lets users confirm their microphone is working correctly and inspect
basic audio properties before joining calls, recording content, or
troubleshooting hardware. It is intended for the development team,
QA engineers, product owners, and external reviewers.

### 1.2 Scope
MicTest12-1.0 will:
- Detect available audio input devices in the user's browser.
- Capture a live audio stream from the user-selected microphone.
- Display a real-time input-level meter and waveform.
- Allow the user to record a short clip (up to 30 seconds), play it back, and
  download it.
- Report basic diagnostics: sample rate, channel count, peak level,
  RMS level, estimated noise floor, and round-trip latency.
- Run entirely client-side; no audio leaves the user's device.

Out of scope for v1.0:
- Server-side storage or sharing of recordings.
- Speech-to-text, voice biometrics, or pitch/musical analysis.
- Multi-microphone mixing.
- Native desktop/mobile builds.

### 1.3 Definitions, Acronyms, and Abbreviations
| Term | Meaning |
| --- | --- |
| SRS | Software Requirements Specification |
| UA | User Agent (web browser) |
| dBFS | Decibels relative to full scale |
| RMS | Root mean square (signal level metric) |
| SNR | Signal-to-noise ratio |
| PWA | Progressive Web App |
| WCAG | Web Content Accessibility Guidelines |
| MUST / SHOULD / MAY | Requirement levels per RFC 2119 |

### 1.4 References
- IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*.
- W3C *MediaStream Recording* (MediaRecorder API).
- W3C *Web Audio API* (AudioContext, AnalyserNode).
- W3C *Media Capture and Streams* (getUserMedia).
- WCAG 2.1, Level AA.
- RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.

### 1.5 Overview
Section 2 gives the overall product context, user classes, constraints, and
assumptions. Section 3 lists the specific functional and non-functional
requirements. Section 4 covers external interfaces. Section 5 covers
verification.

---

## 2. Overall Description

### 2.1 Product Perspective
MicTest12-1.0 is a self-contained, single-page web application. It depends on
the browser's `getUserMedia`, Web Audio, and MediaRecorder APIs. It has no
backend services in v1.0; static assets are served from a CDN or static host.

### 2.2 Product Functions (summary)
1. Enumerate audio input devices.
2. Request microphone permission and open a capture stream.
3. Visualize live input (level meter + waveform).
4. Compute and display diagnostics.
5. Record, play back, and download a test clip.
6. Expose troubleshooting guidance when no signal is detected.

### 2.3 User Classes and Characteristics
| Class | Description | Technical skill |
| --- | --- | --- |
| End user | Wants to confirm their mic works before a meeting/recording. | Low |
| Support agent | Walks an end user through diagnostics. | Medium |
| Developer/QA | Validates browser/device coverage. | High |

### 2.4 Operating Environment
- Modern evergreen browsers: Chrome, Edge, Firefox, Safari (last two major versions).
- Desktop and mobile form factors.
- HTTPS origin (required by `getUserMedia`).
- No specific OS dependency.
- Note: `MediaRecorder` codec support varies on Safari; FR-6 mandates a
  capability check via `MediaRecorder.isTypeSupported` and graceful fallback
  to the UA's default container/codec.

### 2.5 Design and Implementation Constraints
- Must run in the browser sandbox; no native binaries.
- Audio data MUST NOT be transmitted off-device.
- Bundle size SHOULD be < 250 KB gzipped for first load.
- Source must be deployable as static files.

### 2.6 Assumptions and Dependencies
- The user has at least one functioning audio input device.
- The browser supports the Web Audio API and `MediaRecorder`.
- The user grants microphone permission when prompted.

---

## 3. Specific Requirements

Requirements are tagged `FR-#` (functional) or `NFR-#` (non-functional).
Keywords MUST/SHOULD/MAY follow RFC 2119.

### 3.1 Functional Requirements

**FR-1 Device enumeration**
The system MUST list all available audio input devices reported by
`navigator.mediaDevices.enumerateDevices()` and let the user select one.
Default to the system default device.

**FR-2 Permission handling**
On first capture, the system MUST request microphone permission. If denied,
it MUST display a clear message with steps to re-enable permission for the
current browser.

**FR-3 Live level meter**
While capturing, the system MUST display a real-time input level meter
updating at ≥ 20 Hz. The meter MUST show peak and RMS in dBFS, with a
clipping indicator at ≥ −1 dBFS.

**FR-4 Waveform display**
The system MUST render a scrolling time-domain waveform of the input
signal. Frame rate SHOULD be ≥ 30 fps on desktop.

**FR-5 Diagnostics panel**
The system MUST display: sample rate, channel count, current peak (dBFS),
current RMS (dBFS), estimated noise floor (dBFS, computed over a 1 s window
of the lowest-RMS frames in the last 10 s), and round-trip latency
(`AudioContext.baseLatency` + `outputLatency` when available).

**FR-6 Test recording**
The system MUST allow recording a clip up to 30 seconds. Controls: Start,
Stop, Play, Re-record, Download. Output format SHOULD be WebM/Opus where
supported, falling back to whatever `MediaRecorder.isTypeSupported` reports.

**FR-7 Playback**
Recorded clips MUST be playable in-page via the standard HTML5 audio
controls.

**FR-8 Download**
The user MUST be able to download the recorded clip as a single file with a
timestamped filename (e.g., `mictest-2026-04-26T15-04-22.webm`).

**FR-9 No-signal guidance**
If no audio energy above −60 dBFS is detected for 5 consecutive seconds
during capture, the system MUST display troubleshooting guidance
(check mute switch, check OS input device, try another device).

**FR-10 Device change detection**
The system SHOULD listen for `devicechange` events and refresh the device
list automatically.

**FR-11 Reset / stop**
The user MUST be able to stop capture at any time. Stopping MUST release
the underlying media tracks (`MediaStreamTrack.stop()`).

### 3.2 Non-Functional Requirements

**NFR-1 Performance**
First contentful paint MUST occur within 1.5 s on a 4G connection on a
mid-range 2022 mobile device. Sustained CPU usage during capture SHOULD
remain below 15 % on the same device.

**NFR-2 Reliability**
The application MUST recover gracefully from device disconnection
(e.g., USB mic unplugged) by surfacing an error and returning to the
device-selection state without a page reload.

**NFR-3 Security & Privacy**
- No audio MAY leave the device.
- The site MUST be served over HTTPS.
- No third-party analytics that records audio or PII.
- A privacy notice MUST be visible from the main screen.

**NFR-4 Accessibility**
The UI MUST conform to WCAG 2.1 Level AA. All interactive controls MUST be
keyboard-operable and labeled for screen readers. The level meter MUST have
a non-color-dependent indicator for clipping.

**NFR-5 Internationalization**
All user-visible strings MUST be externalized for translation. v1.0 ships
with English (`en`) only; the architecture MUST allow additional locales
without code changes.

**NFR-6 Browser compatibility**
The application MUST function on the latest two major versions of Chrome,
Edge, Firefox, and Safari on Windows, macOS, Linux, iOS, and Android.

**NFR-7 Maintainability**
Code MUST be linted (ESLint) and type-checked (TypeScript strict). Unit
test coverage SHOULD be ≥ 80 % for non-UI modules.

**NFR-8 Observability (client-only)**
The application MUST log diagnostic events to an in-page console panel
(toggleable) to aid support without sending data off-device.

### 3.3 External Interface Requirements

**3.3.1 User interface**
- Single-page layout: header, device selector, meter+waveform, diagnostics,
  recording controls, troubleshooting drawer.
- Responsive down to 320 px width.
- Light and dark themes following `prefers-color-scheme`.

**3.3.2 Hardware interfaces**
- Any audio input device exposed to the browser via the OS.

**3.3.3 Software interfaces**
- `navigator.mediaDevices.getUserMedia` / `enumerateDevices`.
- Web Audio API: `AudioContext`, `AnalyserNode`, `MediaStreamAudioSourceNode`.
- `MediaRecorder` for clip capture.

**3.3.4 Communications interfaces**
- HTTPS for static asset delivery only. No application-level network
  protocols in v1.0.

---

## 4. Acceptance Criteria (per requirement)

| ID | Verification method | Pass condition |
| --- | --- | --- |
| FR-1 | Manual + automated | All OS-reported input devices appear in dropdown. |
| FR-2 | Manual | Denying permission shows recovery instructions. |
| FR-3 | Automated (synthetic tone) | 1 kHz @ −20 dBFS reads −20 ± 1 dBFS; meter updates ≥ 20 Hz. |
| FR-4 | Automated (frame timing) | Waveform render ≥ 30 fps on desktop reference machine. |
| FR-5 | Automated | Diagnostics values match injected stream within tolerance. |
| FR-6 | Manual | 30 s clip records, plays, downloads; codec falls back when needed. |
| FR-7 | Manual | Recorded clip plays via in-page controls. |
| FR-8 | Manual | Downloaded filename matches `mictest-<ISO timestamp>.<ext>`. |
| FR-9 | Manual (muted mic) | Guidance appears within 5–6 s. |
| FR-10 | Manual (hot-plug) | Device list refreshes without reload. |
| FR-11 | Automated | After Stop, `MediaStreamTrack.readyState === 'ended'`. |
| NFR-1 | Lighthouse / WebPageTest | FCP < 1.5 s on Moto G4 / 4G profile. |
| NFR-2 | Manual (unplug device) | App returns to device-selection state without reload. |
| NFR-3 | Code review + network tap | No outbound audio traffic during capture. |
| NFR-4 | axe-core + manual SR pass | No critical violations; full keyboard flow works. |
| NFR-6 | Cross-browser CI | E2E suite passes on supported browser matrix. |

---

## 5. Verification and Validation
- **Unit tests:** signal math (RMS, peak, dBFS conversion, noise-floor
  estimator).
- **Integration tests:** mocked `MediaStream` driving the audio graph.
- **End-to-end tests:** Playwright across the supported browser matrix using
  fake media (`--use-fake-device-for-media-stream`,
  `--use-file-for-fake-audio-capture`).
- **Manual exploratory:** real hardware on each supported OS.
- **Accessibility:** axe-core in CI plus manual screen-reader pass
  (NVDA, VoiceOver).

---

## 6. Open Questions
1. Confirm product scope — is MicTest12-1.0 actually the mic-testing tool
   described above, or something else (CLI, desktop, voice analytics)?
2. Is offline / PWA support in scope for v1.0?
3. Target launch date and supported-locale list?
4. Any branding, design system, or accessibility constraints beyond WCAG AA?
5. Should diagnostics include advanced metrics (THD, frequency response
   sweep) in a later version?

---

## Appendix A. Revision History
| Version | Date | Author | Notes |
| --- | --- | --- | --- |
| 0.1 | 2026-04-26 | Claude (draft) | Initial draft based on placeholder repo. |
| 1.0.1 | 2026-04-26 | Claude (draft) | Added TOC; expanded acceptance-criteria table to cover FR-4, FR-7, FR-8, FR-10, FR-11, NFR-2, NFR-6; noted Safari `MediaRecorder` codec caveat in §2.4. |
