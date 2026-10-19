# ADR-001 — Render test Forward+ bằng Vulkan software trên host hiện tại

Trạng thái: ACCEPTED cho verification local. Không đổi renderer sản phẩm, engine pin, benchmark hoặc release target.

Native host Windows 10, NVIDIA NVS 310/driver 10.18.13.5362 không khởi tạo được D3D12/Vulkan. Godot tự fallback OpenGL và vẫn trả exit 0, nên exit code đơn độc không đủ xác nhận baseline. Raw probe tại `reports/tasks/T-010301/render_probe.*` lưu lỗi thật; fixture đã bổ sung kiểm tra renderer thực.

SwiftShader là Vulkan CPU implementation, Apache-2.0 theo [nguồn chính thức](https://github.com/google/swiftshader). Dùng ICD đã cài cùng Chrome ở host, chỉ đọc binary, không sửa cài đặt, không phân phối DLL cùng game. [README chính thức](https://github.com/google/swiftshader#usage) chỉ cách chọn ICD qua `VK_ICD_FILENAMES`. Biến môi trường chỉ truyền vào subprocess test; không đổi môi trường người dùng/máy.

Probe thứ hai với ICD này chạy non-headless, báo `Vulkan 1.3.0`, `Forward+`, `SwiftShader Device (Subzero)`, capture PNG 1280×720, exit 0 và không có engine error. Đã mở ảnh: khối lập phương có mặt sáng/tối, không phải ảnh đen hoặc render giả. Đây là fixture capability, không phải final art/gameplay.

Cho phép tiếp tục functional/rendered tests bằng renderer Forward+ thật trên CPU, ghi software=true trong mọi report liên quan. Mỗi rendered test phải xác nhận actual method/driver, viewport frame/capture và non-headless display, từ chối automatic Compatibility fallback. Không lấy FPS trên SwiftShader làm benchmark GPU hoặc retail minimum spec.

Native hardware Forward+ performance, physical gamepad và audio listening vẫn chưa được xác minh. Gate/task đòi GPU performance hoặc thiết bị vật lý phải chặn nếu chưa có môi trường phù hợp. Không hạ ngưỡng để qua gate. Packaging không phụ thuộc driver path của máy dev; driver này là test-only environment.
