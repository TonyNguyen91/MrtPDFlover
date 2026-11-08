# MrT PDFlover – ghi chú kỹ thuật

## Cấu trúc
- `src/app.src.html`: nguồn chính (không có doctype). `python build.py` bọc doctype, `meta charset`, CSP và ghi ra `app/index.html`.
- `app/lib/`: toàn bộ thư viện, font, dữ liệu OCR, nạp bằng `<script>`/`<link>` cục bộ.
- `python build.py --zip` tạo `dist/MrT-PDFlover-offline.zip`.

## Chạy offline tuyệt đối (v1.5)
- **CSP do `build.py` chèn vào:**
  - `default-src 'none'`.
  - Script, style và worker chỉ từ `'self'`, `file:`, `blob:`. Ảnh chỉ từ `file:`, `data:`, `blob:`.
  - Font và `connect-src` chỉ từ `data:`, `blob:`.
  - Kèm `referrer no-referrer`.
- **Font giao diện** (Bricolage Grotesque, IBM Plex Sans/Mono, có dấu tiếng Việt) nhúng sẵn trong `lib/ui-fonts.css` dưới dạng data URI. Không còn Google Fonts.
- **HTML→PDF:** `offlineHtml()` gỡ script, iframe, link, ảnh/CSS/@import trỏ ra Internet và thuộc tính `on*`. Ứng dụng báo số tài nguyên đã bỏ qua.
- **Tesseract:** địa chỉ CDN mặc định trong `tesseract.min.js` và `tess-worker.js` đã thay bằng `offline-disabled:`.
- **Dữ liệu cục bộ:** localStorage chỉ giữ 3 khóa giao diện (`pdfl-side`, `pdfl-layers`, `pdfl-lang`).
- **Kiểm thử bằng Puppeteer** (ghi lại mọi request qua `file://`): toàn bộ chức năng đều chạy, 0 request ra mạng.
  - Riêng HTML có ảnh/CSS từ Internet: các tài nguyên đó bị lọc bỏ trước khi dựng trang.

## Ngôn ngữ VI/EN + chặn bôi đen giao diện (v2.0)
- **Chặn bôi đen:** `body{user-select:none}`; riêng `input`, `textarea`, `[contenteditable]` vẫn chọn chữ được. `img,svg{-webkit-user-drag:none}`. Thanh tab `.tabs` ẩn thanh cuộn ngang.
- **Nút đổi ngôn ngữ:**
  - Ở header: `.seg.lang` (VI | EN), đặt cuối hàng với `margin-left:auto`. `.brand` co lại (`flex:1 1 200px`, dòng mô tả cắt bằng dấu …) để header giữ trên một hàng.
  - Trong trình xem: `#v-lang`, nằm cạnh nút đóng.
  - Lựa chọn lưu ở localStorage `pdfl-lang`; đổi luôn `<html lang>`.
- **Cách dịch:** mã nguồn và giao diện gốc vẫn là tiếng Việt, bản EN được dịch lúc chạy.
  - `I18N_EN`: từ điển VI→EN, khoảng 580 cụm.
  - `trEN(s)`: khớp nguyên chuỗi trước. Nếu không khớp, dùng một RegExp gồm mọi khóa, khóa dài trước, có biên chữ `\p{L}\p{N}` (chỉ áp ở đầu/cuối khóa là chữ hoặc số) để dịch được chuỗi ghép động.
  - Chỉ dịch chuỗi có dấu tiếng Việt, hoặc chứa vài từ không dấu: Elip, xoay, tr., trang, ngang, sang.
  - Duyệt text node và các thuộc tính `title`, `placeholder`, `aria-label`. Bản gốc giữ trong WeakMap để đổi lại VI.
  - MutationObserver dịch nội dung mới sinh (toast, hộp thoại, danh sách) khi đang ở EN; có cờ `LANG.busy` và `takeRecords` để không lặp.
- **Không dịch:** `script`, `style`, `svg`, `textarea`, `[contenteditable]`, `[data-noi18n]`, `.nm`, `.fitem span`, `#v-src`, `.vl-name`, `.result b`. Tức là không đụng tới tên tệp, chữ người dùng gõ và nội dung PDF.
- **Nhãn layer:** `annLabel` gọi `trUI()` cho phần chữ cố định. Vector gốc ở EN hiển thị "Original …"; đối tượng `gone` hiển thị "Deleted original …".
- **Lưu ý khi thêm chuỗi giao diện mới:**
  - Thêm cụm tương ứng vào `I18N_EN`.
  - `<option>` có chữ tiếng Việt phải có `value`, vì dịch text sẽ đổi `.value` của option không có `value`.
  - "Vừa" nghĩa là Fit (nút zoom); tùy chọn độ nét đổi thành "Trung bình".
- **Đã kiểm thử:** sau khi bật EN, không còn chuỗi tiếng Việt chưa dịch ở bàn làm việc, các tab, 10 bộ chuyển đổi, hộp thoại Phiên mới, trình xem, các công cụ và hộp thiết lập bản vẽ. Đổi qua lại VI/EN được, lựa chọn được nhớ sau khi tải lại, 0 request mạng. Bộ test hồi quy cũ vẫn đạt.

## Sửa nét vẽ gốc + bấm đúp (v1.9)
- **Bấm đúp:** tự nhận bấm đúp trong `pointerdown` (hai lần bấm cách nhau dưới 450 ms và dưới 6 px).
  - Lý do: lớp SVG được dựng lại giữa hai lần bấm nên `ev.detail` của trình duyệt bị đặt lại về 1.
  - Ở công cụ Chọn: bấm đúp ô chữ thì sửa; bấm đúp chữ gốc của PDF thì chuyển thành ô chữ và sửa luôn (`editClick(..., noBand)`).
  - Ở công cụ Sửa nội dung: bấm vào đối tượng đã có thì chọn nó (ô chữ thì vào chế độ sửa).
- **Nét vẽ gốc:** `pageEditables()` lấy thêm `paths` từ operator list.
  - Theo dõi kiểu nét qua save/restore: LW, cap, join, dash, màu RGB, ExtGState (LW/CA/ca).
  - Mỗi lệnh tô (S/s/f/f*/B/B*/b/b*/n) ở cấp trang (ngoài form và appearance của annotation) có số thứ tự `k`, khớp 1-1 với lệnh tô trong content stream.
  - Bỏ qua hình tô kín chiếm hơn 85% trang (nền).
- **Đối tượng `type:'vec'`:**
  - Trường: `segs` (M/L/C/Z theo tọa độ base), `tf` (ma trận dịch chuyển/co giãn), `color`, `width` (0 = không viền), `fill`, `dash`, `cap`, `join`, `eo`, `opacity`, `orig:{k, bb}`.
  - Delete → đổi thành `type:'gone'` (không vẽ gì). Xóa mục đó → nét gốc hiện lại.
  - Đối tượng bị ẩn → nét gốc hiện lại.
- **Xóa nét gốc:**
  - `pageDels(e)` → `delsUser` → `purgePageContent(..., dels)`: lệnh tô thứ k có khung khớp (sai số ≥1,5 pt hoặc 3%) được thay bằng `n` (kết thúc đường mà không vẽ).
  - Khi xuất luôn xóa, không phụ thuộc tùy chọn "Xóa hẳn" (nếu không sẽ thành 2 bản).
  - Trình xem, thumbnail và các bản xuất dạng ảnh dùng `pdfPageFor(e)`: một bản sao 1 trang đã bỏ nét gốc, cache theo `src:index:danh sách k`.
- **Dán:** khi dán sang chỗ khác, bỏ `orig`/`cover`/`erased` để không xóa nhầm nội dung của trang đích.
- **Đã kiểm thử** trên trang mẫu: đường tâm nét chấm gạch → kéo đi, đổi màu đỏ, nét 4, nét đứt; khung vuông → tô vàng. Xuất PDF không còn bản gốc trùng lặp. Bấm đúp ô chữ và bấm đúp chữ gốc đều sửa được.

## Sửa nội dung PDF có sẵn (v1.8)
- **Công cụ "Sửa nội dung"** (phím E):
  - `pageEditables()` lấy các dòng chữ (gộp item của `getTextContent` theo đường chân chữ) và các ảnh (`paintImageXObject` / `paintInlineImageXObject` cùng CTM), tọa độ base.
  - Bỏ qua chữ xoay và ảnh chiếm hơn 85% trang (ảnh scan).
  - Bấm vào một dòng → tạo `type:'text'` kèm `cover:{x,y,w,h,fill}`. Cỡ chữ = chiều cao dòng, đậm/nghiêng/có chân lấy từ thông tin phông của pdf.js.
  - Màu chữ và màu nền lấy mẫu từ canvas đang hiển thị (`sampleColors`).
  - Chữ một dòng có `autoW`: ô chữ giãn theo nội dung thay vì xuống dòng.
  - Kéo khung → gộp các dòng thành một đoạn (xuống dòng trong khung).
- **Ảnh có sẵn:**
  - Lấy điểm ảnh từ `page.objs.get(id)` (bitmap, hoặc data kind 1/2/3), vẽ đúng hướng theo CTM. Nếu không lấy được thì cắt từ bản dựng 220 dpi.
  - Tạo `type:'image'` kèm `cover`. Có nút "Thay ảnh…".
- **Cover:**
  - Vẽ trước mọi chú thích: lớp SVG riêng `#v-svg-cov`, rồi đến canvas, rồi PDF.
  - Nhấn Delete trên đối tượng có cover → đổi thành `type:'white'` mang `erased`. Xóa tiếp mục đó → bản gốc hiện lại.
  - Ô chữ rỗng mà có cover thì vẫn giữ lại (để tiếp tục che bản gốc).
- **Xóa hẳn khi xuất** (`purgePageContent`, tùy chọn `#purge`, mặc định bật):
  - Giải mã toàn bộ content stream của trang, tách lệnh bằng `lexContent`.
  - Theo dõi CTM, trạng thái chữ và Tm. Độ rộng glyph lấy từ Widths/FirstChar (phông đơn) hoặc W/DW (Type0 Identity-H).
  - Lệnh vẽ chữ (Tj/TJ/'/") có ≥60% khung nằm trong vùng che sẽ bị xóa.
  - Nếu ngay sau đó có lệnh vẽ chữ chưa đặt lại vị trí: thay bằng `[N] TJ` để giữ vị trí các chữ sau. Chỉ làm khi độ rộng chính xác; nếu không, chỉ che phủ (đếm vào `kept`).
  - Lệnh `Do` ảnh ≥60% trong vùng che và `BI…EI` bị xóa; Form XObject chỉ bị xóa khi ≥95% trong vùng che.
  - Vùng che lấy từ `cover` và từ các đối tượng Che trắng.
- **Đã kiểm thử:**
  - PDF reportlab (TrueType đơn) và Helvetica chuẩn: chữ cũ biến mất khỏi pdftotext, ảnh cũ bị xóa, ảnh mới nhúng dạng JPEG.
  - PDF có phông DejaVu Type0 Identity-H (do app xuất): gộp 3 dòng, chữ cũ bị xóa hẳn.
- **Giới hạn:** không sửa được chữ nằm trong Form XObject (chỉ che), chữ xoay, và bản scan.

## Kích thước, bong bóng, bắt điểm (v1.7)
- **Thiết lập bản vẽ `p.dwg`** (theo từng trang):
  - Các trường: `paper`, `pw`/`ph` (mm), `sn:sd` (tỉ lệ bản vẽ : thực), `unit` mm/in, `prec`, `dec` `.` hoặc `,`, `trim`.
  - Giá trị đo = pt × (cạnh dài giấy mm / cạnh dài trang pt) × sd/sn. Hàm: `dimCtx()`.
  - Giá trị luôn tính lại khi vẽ, nên đổi thiết lập thì mọi kích thước trên trang tự cập nhật.
  - `p.dwg` được lưu trong .plt.
- **Đối tượng `type:'dim'`:**
  - `kind:'lin'`: `p1`, `p2`, `q`, `mode` h/v/a. Mode tự chọn theo vị trí đặt; giữ Shift để đo theo đường xiên.
  - `'dia'` và `'rad'`: `cx`, `cy`, `r`, `q`.
  - `'ang'`: `v`, `a`, `b`, `q`.
  - Thuộc tính tùy chọn: `label` (chữ thay thế, `<>` là giá trị đo) và `prec` (số lẻ riêng).
- **Đối tượng `type:'callout'`:** `x`, `y` (tâm bong bóng), `tx`, `ty` (đầu chỉ), `text`, `end` dot/arrow/none, `fill`. Số mới = số lớn nhất trên mọi trang + 1.
- **Vẽ:** `geomOf()` trả về các primitive: lines, tris, circles, texts. Có 3 renderer dùng chung: SVG (`geomSvgStr`), canvas (`drawGeomCanvas`), PDF (`drawGeomPdf`). Chữ dùng font DejaVu.
- **Bắt điểm:** `pageVectors()` đọc `getOperatorList` của pdf.js 3.11.
  - Theo dõi save/restore/transform và form XObject; đọc các lệnh constructPath (moveTo, lineTo, curveTo 1/2/3, closePath, rectangle).
  - Đổi tọa độ bằng `viewport(rotation=page.rotate).transform`.
  - Kết quả gồm: điểm cuối, trung điểm, tâm cung (bezier khớp đường tròn, sai số 0,6%), đoạn thẳng, và đoạn lấy mẫu từ đường cong.
  - Lưới không gian 24 pt. Giao điểm được tính tại chỗ, tối đa 80 đoạn gần con trỏ.
  - Bán kính bắt điểm 10 px màn hình. Giữ Alt để tạm tắt.
- **Tạo kích thước:** máy trạng thái `ED.pend` (bấm từng điểm). Esc hủy, Backspace lùi một điểm.
- **Phiên mới:** `newSession()` hỏi qua `askBox()` (Lưu rồi tạo mới / Không lưu / Hủy) nếu có tài liệu thật và còn thay đổi chưa lưu.
- **Đã kiểm thử:**
  - Trang mẫu A4 tỉ lệ 1:2: cạnh 340 pt ra 239.89, Ø155.22, R21.17 (đúng theo tính tay).
  - PDF xuất ra khớp với màn hình, chữ chọn được.
  - Trang xoay 90° vẫn đúng.
  - Lưu .plt và mở lại giữ nguyên thiết lập inch.

## Tính năng
- **Bàn làm việc:**
  - Gộp, sắp xếp, xoay, xóa, nhân đôi trang; chèn trang trắng.
  - Tách theo trang, theo N trang hoặc theo khoảng.
  - Số trang, watermark tiếng Việt, nén raster, sửa metadata.
  - Ra ảnh, trích văn bản, mở khóa PDF có mật khẩu.
  - OCR Tesseract tiếng Việt + Anh, xuất PDF có lớp chữ ẩn.
- **Phiên làm việc .plt** (v1.4):
  - "Lưu phiên" (Ctrl+S) và "Mở phiên" (Ctrl+O); cũng mở được bằng cách kéo thả tệp `.plt`.
  - Khi bàn làm việc đang có tài liệu khác, ứng dụng hỏi: thay phiên hiện tại hay gộp vào cuối.
  - Có cờ "chưa lưu": nút Lưu phiên hiện chấm màu, và trình duyệt cảnh báo khi đóng tab lúc còn thay đổi chưa lưu.
- **Trình xem và chỉnh sửa trang** (nút ⛶ trên thẻ trang, hoặc bấm đúp):
  - Danh sách trang bên trái. Lăn chuột để zoom; kéo vùng trống hoặc giữ Space để di chuyển.
  - Công cụ vẽ: ô chữ, ảnh, chữ nhật, elip, đường, mũi tên, bút, bôi vàng, che trắng.
  - Hoàn tác và làm lại: Ctrl+Z / Ctrl+Y.
  - **Bảng đối tượng bên phải** (kiểu layer):
    - Trên cùng danh sách là lớp nằm trên.
    - Thao tác: chọn, kéo thả đổi lớp, đổi tên, ẩn (`hidden`, không xuất ra), khóa (`locked`).
    - Thanh công cụ: nhân bản, sao chép, dán, lên trên cùng / lên một lớp / xuống một lớp / xuống dưới cùng, xóa.
- **Chuyển sang PDF:** Ảnh, DOCX, PPTX, XLSX/XLS/CSV/ODS, HTML. Kết quả là ảnh nét cao kèm lớp chữ ẩn.
- **Chuyển từ PDF:** JPG/PNG, DOCX (sửa được chữ hoặc giữ nguyên hình), PPTX, XLSX, PDF/A-2b.

## Định dạng tệp .plt
- Là một tệp zip, gồm:
  - `manifest.json`, có `format: "mrt-pdflover-session"` và `version: 1`.
  - `sources/<id>.*`: bản gốc của tài liệu.
  - `assets/imgN.*`: ảnh chèn vào chú thích, được tham chiếu bằng `src: "asset:<path>"`.
- `manifest.json` chứa: `sources[]`, `pages[]` (src, index, rot, sel, ann), `ocr`, `settings`.
- Khi mở, id nguồn được ánh xạ lại; PDF có mật khẩu sẽ hỏi lại mật khẩu.

## Chú thích (annotations): cách lưu và xuất
- **Lưu trữ:**
  - `p.ann` là mảng bất biến, nên undo và redo hoạt động đúng.
  - Tọa độ "base" tính bằng pt, gốc ở góc trên bên trái, chưa tính `p.rot`.
- **Trình chỉnh sửa:** 3 lớp SVG (bôi vàng dùng multiply, lớp chính, lớp UI), biến đổi tọa độ bằng `rotXform`.
- **Xuất PDF vector:** `drawAnnPdf` dùng ma trận `cm` theo r0 và cropbox. Chữ nhúng font DejaVu thường + đậm; chữ nghiêng tạo bằng `xSkew` 12°.
- **Xuất raster, ảnh, OCR:** vẽ qua `drawAnnCanvas`. Trình xem gọi `renderEntry(..., {ann:false})` vì đã có lớp SVG.
- **Ngắt dòng:** dùng chung `wrapText` (cùng font DejaVu trên màn hình và trong PDF).

## Thư viện (thư mục lib/, tất cả cục bộ)
- pdf-lib 1.17.1, pdf.js 3.11.174 (fake worker), JSZip 3.10.1, fontkit 1.1.1.
- Font: DejaVu Sans thường/đậm (dùng trong PDF); `ui-fonts.css` (dùng cho giao diện).
- Tesseract.js 5.1.1:
  - Lõi và worker gộp chung trong một blob.
  - Dữ liệu ngôn ngữ base64 trong `lang-*.js`.
  - Đã vá `t.code` khi khởi tạo; đã vô hiệu hóa địa chỉ CDN mặc định.
- docx-preview 0.3.3, docx 8.5.0, pptx-preview 1.0.5, pptxgenjs 3.12.0, SheetJS 0.18.5, html2canvas 1.4.1, hồ sơ màu sRGB ICC.

## Lưu ý khi sửa
- Nguồn chính là `app.src.html` (không có doctype). `build.py` bọc doctype, `meta charset` và CSP.
- Trong CSS phải có `[hidden]{display:none!important}`.
- html2canvas render trắng với phần tử `inline-block` nằm trong khung `overflow:hidden`. Phải đặt `display:block` trước khi cắt trang.

## Đã kiểm thử (Chrome headless qua file://, ghi lại mọi request mạng)
- Cả 10 bộ chuyển đổi, OCR tiếng Việt, PDF tìm kiếm được, số trang, tách trang.
- Chú thích đủ 9 loại; xuất vector; trang xoay 90° khớp giữa PDF và ảnh.
- Phiên .plt: lưu, tải lại trang, mở lại. Khôi phục đủ trang, chú thích, thứ tự lớp, ẩn/khóa và thiết lập.
- 0 request ra mạng.
