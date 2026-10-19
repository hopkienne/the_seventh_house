# 12 — Release, external gates và permissions

## Agent vẫn là người thực thi
RELEASE_AGENT chuẩn bị build, QA, metadata, store copy, screenshots/trailer thực, licensing/credits, manifests, release notes, rollback và support runbook. Khi công cụ/tài khoản được cấp đúng scope, agent thực hiện các thao tác được ủy quyền. Chủ dự án không bị giao task lập trình, tạo 3D, mix âm thanh hoặc dịch.

Tuy nhiên “triển khai toàn bộ dự án” không tự cấp quyền ký hợp đồng, dùng danh tính, chi tiền hoặc bấm public release. Ghi record authorization cụ thể thay vì ký thay. Account/platform approval là sự kiện ngoài code; agent chỉ đọc và ghi lại trạng thái thật.

## Permission matrix
| Thao tác | Default | Cần lưu |
|---|---|---|
| Sửa code/assets/docs local trong repo | Cho phép theo nhiệm vụ và sandbox | Task/paths/diff/tests |
| Xóa data có sẵn, force push, reset history | Không | Owner authorization cụ thể + backup |
| Dùng paid API/asset/cloud service | Không, spend limit 0 | Service/task/cap/currency/expiry được duyệt |
| Upload build private/store draft | Không mặc định | App/channel/operation + account scope |
| Giá bán/vùng bán/ngày công khai | Owner decision | Proposal và quyết định thật |
| Publish/patch/rollback public | Không mặc định | Exact build hash/app/channel/operation/window + authorization |
| Identity/tax/payment/legal declarations | Owner/account-holder | Trạng thái xác minh, không lộ tài liệu/credential |
| Thu telemetry/dữ liệu người chơi | Không mặc định | Phạm vi/consent/privacy/retention được duyệt |

## Technical và public hoàn thành khác nhau
**TECHNICALLY_COMPLETE:** R01–R14/R16/R17 đạt phần sản phẩm: full content + native runtime tests + final assets/rights/rebuild. **READY_FOR_RELEASE:** RC package/support/metadata/checklists xong, G7_TECH pass, external queue rõ. **PUBLISHED:** platform thực public đúng version và public smoke pass; G8, không được giả có nếu chỉ tạo ZIP.

G7 record chứa `technical_status` và `public_status`. G7_TECH có thể PASS dù account/approval chưa đủ. Khi đó chỉ dừng public branch, tiếp tục local QA/archive/doc việc không phụ thuộc. Không sửa permission JSON `public_release=true` chỉ vì muốn next selector tiến tới S35; record phải có owner authorization thật.

## Release sequence
1. Chuẩn bị app/store assets và build manifest đúng product, không screenshot mockup quảng bá feature chưa có.
2. Đối chiếu current platform documentation và account prerequisites tại ngày thực thi; lưu checked_at/URL/observed. Không giữ con số chờ kế thừa v2 chưa đối chiếu.
3. Có quyền thì upload test/private build; kiểm cài/save/content/entitlements. Không public để thử nghiệm.
4. Submit store/build theo yêu cầu nền tảng; chờ/đọc trạng thái review thật bằng các phiên được kích hoạt, không bịa approved.
5. G7_TECH + G7_PUBLIC, no Sev-0/1; exact RC hash, backup, notes, support, rollback.
6. Thực thi publish đúng authorization; ghi timestamp/platform result; tải từ channel public và smoke lại.
7. Release notes và known issues phải khớp version public, không hứa thời điểm fix chưa test.

Steam release gồm checklists store/build, review và điều kiện Coming Soon; hai quyền Publish app changes và Manage pricing/discounts được official docs nêu [SRC06]. Luôn recheck trước thao tác. Pack không giữ mặc định “21 ngày” của v2 làm quy tắc; điều kiện payment/identity/region cụ thể phải lấy từ nguồn và app thực.

## Rollback và save
Trước patch schema: snapshot golden saves/backups, test old→new, không coi new→old luôn được. Public rollback cần authorization riêng nếu quyền trước không bao gồm. Restore known-good depot/build và dữ liệu đúng schema, thông báo rõ tác động; không copy đè save người chơi để giả sửa. Rehearsal chỉ private branch.

## External request format
Request ID, reason, exact permission/data/capability cần, cách đã thử, task bị chặn, nhánh khác vẫn làm được, spend cap nếu có, giới hạn/expiry, expected response và cách verify. Đặt trong `state/external_requests.json`; không gửi secret/password trong task card.
