# Third-party notices

MrT PDFlover bundles the following third-party components in `app/lib/`, unmodified unless noted.
License texts are in `licenses/`.

| Component | Version | License | File(s) in `app/lib` |
|---|---|---|---|
| pdf-lib | 1.17.1 | MIT | `pdf-lib.min.js` |
| @pdf-lib/fontkit | 1.1.1 | MIT | `fontkit.umd.min.js` |
| PDF.js (pdfjs-dist) | 3.11.174 | Apache-2.0 | `pdf.min.js`, `pdf.worker.min.js` |
| JSZip | 3.10.1 | MIT or GPL-3.0-or-later (used under MIT) | `jszip.min.js` |
| Tesseract.js | 5.1.1 | Apache-2.0 | `tesseract.min.js`, `tess-worker.js` ¹ |
| tesseract.js-core | 5.1.1 | Apache-2.0 | `tess-core.js`, `tess-core-simd.js` ² |
| Tesseract trained data (eng, vie) via @tesseract.js-data | 1.0.0 | MIT (package); data from tesseract-ocr/tessdata, Apache-2.0 | `lang-eng.js`, `lang-vie.js` ² |
| docx-preview | 0.3.3 | Apache-2.0 | `docx-preview.min.js` |
| docx | 8.5.0 | MIT | `docx.umd.js` |
| pptx-preview | 1.0.5 | ISC (per package.json) | `pptx-preview.umd.js` |
| PptxGenJS | 3.12.0 | MIT | `pptxgen.min.js` |
| SheetJS Community Edition (xlsx) | 0.18.5 | Apache-2.0 | `xlsx.full.min.js` |
| html2canvas | 1.4.1 | MIT | `html2canvas.min.js` |
| DejaVu Fonts (Sans, Serif; regular/bold) | 2.37 | Bitstream Vera / Arev fonts license (free) | `font-dejavu*.js` ² |
| Bricolage Grotesque (via Fontsource) | 5.0.8 | SIL OFL 1.1 | `ui-fonts.css` ² |
| IBM Plex Sans / Plex Mono (via Fontsource) | 5.0.x | SIL OFL 1.1 | `ui-fonts.css` ² |

¹ Modified to work offline: default CDN URLs replaced with `offline-disabled:`; small fix in language loading.
² Repackaged as base64 / data-URI JavaScript or CSS so they load over `file://` without network access.

`icc-srgb.js` contains an sRGB ICC profile generated with Little CMS for PDF/A output.

Licenses for @pdf-lib/fontkit (MIT), pptx-preview (ISC) and @tesseract.js-data (MIT) are declared in their
package metadata; those packages do not ship a separate license file.
