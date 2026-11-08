# MrT PDFlover

Bộ công cụ PDF chạy hoàn toàn trong trình duyệt, **offline 100%**: không cần cài đặt, không cần mạng, tệp không rời khỏi máy.
*A fully offline, in-browser PDF toolkit — no install, no network, your files never leave your computer.*

Giao diện song ngữ **Tiếng Việt / English** (nút VI / EN ở góc trên bên phải).

## Chạy thử

**Dùng trực tuyến:** mở trang GitHub Pages của repo (ví dụ `https://<tài-khoản>.github.io/MrtPDFlover/`), trang sẽ tự chuyển vào app.

**Dùng offline:**

1. Tải repo (Code → Download ZIP) hoặc tệp `MrT-PDFlover-offline.zip` ở mục Releases.
2. Mở `app/index.html` bằng Google Chrome hoặc Microsoft Edge (bấm đúp tệp).
3. Xong. Không cần server, không cần Node, không cần quyền quản trị.

> Giữ nguyên thư mục `app/lib` nằm cạnh `index.html`.

## Tính năng

**Bàn làm việc**
- Gộp nhiều PDF và ảnh, kéo thả sắp xếp trang, xoay, xóa, nhân đôi, chèn trang trắng.
- Tách theo từng trang, mỗi N trang hoặc theo khoảng trang.
- Đánh số trang, watermark, nén, sửa thông tin tài liệu, mở khóa PDF có mật khẩu.
- Xuất ảnh JPG/PNG, trích văn bản.
- OCR tiếng Việt + tiếng Anh ra PDF tìm kiếm được.

**Chuyển đổi**
- Sang PDF: Ảnh, Word (.docx), PowerPoint (.pptx), Excel (.xlsx/.xls/.csv/.ods), HTML.
- Từ PDF: Ảnh (JPG/PNG), Word (.docx), PowerPoint (.pptx), Excel (.xlsx), PDF/A-2b.

**Trình xem & chỉnh sửa toàn trang**
- Danh sách trang bên trái, lăn chuột để zoom.
- Công cụ vẽ: ô chữ, ảnh, chữ nhật, elip, đường, mũi tên, bút, bôi vàng, che trắng.
- Bảng đối tượng kiểu layer: ẩn, khóa, đổi tên, đổi thứ tự, sao chép/dán.
- Sửa nội dung PDF gốc: chữ, ảnh, nét vẽ vector. Bản gốc được xóa thật khi xuất, không chỉ bị che.
- Đo kích thước kiểu bản vẽ 2D (dài, đường kính, bán kính, góc) theo khổ giấy, tỉ lệ, mm/inch, có bắt điểm theo nét vector của PDF.
- Bong bóng đánh số (balloon).

**Phiên làm việc `.plt`**: lưu toàn bộ tài liệu, chú thích, kích thước, kết quả OCR để mở lại làm tiếp.

Hướng dẫn chi tiết: [`app/HUONG-DAN.txt`](app/HUONG-DAN.txt).

## An toàn dữ liệu

- `index.html` có Content-Security-Policy chặn mọi kết nối mạng ở mức trình duyệt (`default-src 'none'`, `connect-src data: blob:`).
- Tất cả thư viện và font đều nằm sẵn trong `app/lib`. Không tải gì từ Internet, không thống kê, không kiểm tra cập nhật.
- Khi chuyển HTML sang PDF, mọi tài nguyên trỏ ra Internet đều bị bỏ qua.
- Trình duyệt chỉ nhớ 3 tùy chọn giao diện (localStorage): ẩn/hiện danh sách trang, danh sách đối tượng, ngôn ngữ.
- Tự kiểm tra: mở app, nhấn F12 → tab Network rồi dùng thử. Danh sách chỉ có `file://`, `data:` và `blob:`.

## Cấu trúc thư mục

```
src/app.src.html     Mã nguồn chính (HTML + CSS + JS, một tệp)
build.py             Đóng gói src → app/index.html (chèn doctype, charset, CSP)
index.html           Trang chuyển hướng vào app/ (cho GitHub Pages)
app/index.html       Bản chạy đã build
app/lib/             Thư viện bên thứ ba + font + dữ liệu OCR (đều chạy cục bộ)
app/HUONG-DAN.txt    Hướng dẫn sử dụng
docs/ky-thuat.md     Ghi chú kỹ thuật cho người phát triển
licenses/            Giấy phép của các thư viện bên thứ ba
```

## Phát triển

Sửa `src/app.src.html`, rồi build lại:

```bash
python build.py          # ghi app/index.html
python build.py --zip    # ghi thêm dist/MrT-PDFlover-offline.zip để mang sang máy khác
```

Chỉ cần Python 3, không có bước cài thư viện. Thêm chuỗi giao diện mới thì nhớ bổ sung bản dịch vào từ điển `I18N_EN` trong `src/app.src.html`.

## Thư viện bên thứ ba

Xem [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
