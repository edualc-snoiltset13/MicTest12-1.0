# Software Requirements Specification

**Project:** MicTest12-1.0
**Version:** 1.0
**Date:** 2026-05-02
**Status:** Draft

> Product scope was confirmed on 2026-05-02: MicTest12-1.0 is a browser-based
> microphone testing utility. The document follows the IEEE 830-1998 outline.

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
- Function offline after first successful load via a service-worker-cached
  app shell.

Out of scope for v1.0:
- Server-side storage or sharing of recordings.
- Speech-to-text, voice biometrics, or pitch/musical analysis.
- Multi-microphone mixing.
- Native desktop/mobile builds.
- PWA installability prompt and in-page "update available" UX.
- Background sync and push notifications.
- Telemetry / analytics of any kind.
- Advanced audio metrics (THD, frequency-response sweep, loopback latency
  calibration).

### 1.3 Definitions, Acronyms, and Abbreviations
| Term | Meaning |
| --- | --- |
| SRS | Software Requirements Specification |
| UA | User Agent (web browser) |
| dBFS | Decibels relative to full scale |
| RMS | Root mean square (signal level metric) |
| SNR | Signal-to-noise ratio |
| PWA | Progressive Web App |
| SW | Service Worker |
| WCAG | Web Content Accessibility Guidelines |
| MUST / SHOULD / MAY | Requirement levels per RFC 2119 |

### 1.4 References
- IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*.
- W3C *MediaStream Recording* (MediaRecorder API).
- W3C *Web Audio API* (AudioContext, AnalyserNode).
- W3C *Media Capture and Streams* (getUserMedia).
- W3C *Service Workers*.
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
The app registers a service worker that precaches its app shell so the tool
remains usable offline after first load.

### 2.2 Product Functions (summary)
1. Enumerate audio input devices.
2. Request microphone permission and open a capture stream.
3. Visualize live input (level meter + waveform).
4. Compute and display diagnostics.
5. Record, play back, and download a test clip.
6. Expose troubleshooting guidance when no signal is detected.
7. Cache the application shell for offline use.

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

### 2.5 Design and Implementation Constraints
- Must run in the browser sandbox; no native binaries.
- Audio data MUST NOT be transmitted off-device.
- Bundle size SHOULD be < 250 KB gzipped for first load. The service-worker
  precache MAY include additional assets beyond the first-load critical path.
- Source must be deployable as static files.
- UI styling is minimal/in-house; no third-party design system in v1.0.

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

**FR-12 Offline app shell**
The system MUST register a service worker on first load that precaches the
HTML, JS, CSS, fonts, and icons required for the core mic-test flow.
Subsequent loads MUST succeed with the network offline and reach the
device-selection state without errors.

**FR-13 Service worker update**
When a new service-worker version activates, the system SHOULD serve the
updated cached assets on the next navigation. v1.0 does not require an
in-page "update available" banner.

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

**NFR-9 Offline reliability**
With the network disabled after first successful load, the app MUST start
and reach the device-selection state without errors. Microphone permission
and capture themselves do not require network and MUST continue to work
offline.

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
- Service Worker API (`navigator.serviceWorker`) and Cache Storage API for
  the offline app shell.

**3.3.4 Communications interfaces**
- HTTPS for static asset delivery only. No application-level network
  protocols in v1.0.

---

## 4. Acceptance Criteria (per requirement)

| ID | Verification method | Pass condition |
| --- | --- | --- |
| FR-1 | Manual + automated | All OS-reported input devices appear in dropdown. |
| FR-2 | Manual | Denying permission shows recovery instructions. |
| FR-3 | Automated (synthetic tone) | 1 kHz @ −20 dBFS reads −20 ± 1 dBFS. |
| FR-5 | Automated | Diagnostics values match injected stream within tolerance. |
| FR-6 | Manual | 30 s clip records, plays, downloads. |
| FR-9 | Manual (muted mic) | Guidance appears within 5–6 s. |
| NFR-1 | Lighthouse / WebPageTest | FCP < 1.5 s on Moto G4 / 4G profile. |
| NFR-3 | Code review + network tap | No outbound audio traffic during capture. |
| NFR-4 | axe-core + manual SR pass | No critical violations; full keyboard flow works. |
| FR-12 | Automated (Playwright, `context.setOffline(true)` after first load) | App boots and reaches the device-selection state offline. |
| FR-13 | Manual | Deploying a new SW version, the next reload picks it up within one navigation cycle. |
| NFR-9 | Same Playwright offline run | No console errors; capture path remains usable offline. |

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
- **Offline E2E:** Playwright test that loads the app online, then re-navigates
  with `context.setOffline(true)` and asserts the device-selection UI renders
  without console errors.

---

## 6. Open Questions
Resolved on 2026-05-02:
- Product scope confirmed as a browser-based microphone testing utility.
- Offline app-shell PWA support is in scope for v1.0; installability and
  background features are out.
- Supported locales at launch: English (`en`) only.
- No third-party design system; minimal in-house styling. Accessibility
  constraints remain WCAG 2.1 AA only.
- Advanced metrics (THD, frequency-response sweep) are deferred to a
  future version.

Still open:
1. Target launch date.

---

## Appendix A. Revision History
| Version | Date | Author | Notes |
| --- | --- | --- | --- |
| 0.1 | 2026-04-26 | Claude (draft) | Initial draft based on placeholder repo. |
| 0.2 | 2026-05-02 | Claude (refine) | Resolved scope assumptions; added PWA app-shell scope (FR-12, FR-13, NFR-9); resolved Open Questions. |
