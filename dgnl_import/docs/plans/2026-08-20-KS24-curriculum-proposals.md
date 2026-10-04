# ĐỀ XUẤT ĐIỀU CHỈNH CHƯƠNG TRÌNH ĐÀO TẠO & HỖ TRỢ KỲ IV/V - KHÓA KS24 (ĐÃ ĐỐI SOÁT HỌC THUẬT GỐC)

**Đơn vị đề xuất:** Chuyên gia Quản lý Chất lượng và Thiết kế Chương trình Đào tạo (Curriculum Engineer)
**Mục tiêu:** Tăng cường thực chiến, khắc phục các khoảng trống năng lực phát hiện qua ĐGNL Lần 1 và bám sát thực tế PM hiện có.

---

## 1. PHÂN TÍCH BỐI CẢNH LỘ TRÌNH SẮP TỚI CỦA KS24
Khóa KS24 hiện tại đang học Kỳ IV bao gồm các môn nâng cao:
*   `IT209-K24:` DevOps Fundamentals (1.9 tín chỉ)
*   `IT212-K24:` AI Application in Action (1.9 tín chỉ)
*   `IT213-K24:` AI Integration in Action (1.9 tín chỉ)
*   `IT214-K24:` Microservices System Design (2.5 tín chỉ)

---

## 2. GHI NHẬN VỀ KHUNG PM HIỆN TẠI (THIẾT KẾ CỦA BAN ĐÀO TẠO)
*   **Microservices (IT214):** Đầy đủ công nghệ phân tán hiện đại (Saga, Kafka, API Gateway, Eureka, Resilience4j, Spring Cache/Redis).
*   **DevOps (IT209):** Lộ trình bài bản từ VPS hosting, Nginx, Linux CLI, Docker/Docker Compose đến GitHub Actions CI/CD.
*   **AI Integration (IT213):** Rất đón đầu xu hướng với Spring AI, pgvector RAG, Function Calling, AI Agent, Langfuse, và MCP.

---

## 3. PHÂN TÍCH ĐÁNH GIÁ CHẤT LƯỢNG ĐỀ THI ĐGNL (KS24)
*   **Độ phù hợp của đề thi trắc nghiệm (MCQ) - Phù hợp 90%:** Đề thi trắc nghiệm bám sát nội dung ôn tập lý thuyết (OOP, Spring annotations, React Hooks, Scrum).
    - *Thống kê chất lượng đề (KS24):* Điểm trung bình đạt **72.57/100**, Độ lệch chuẩn **16.88** chứng tỏ đề trắc nghiệm có **độ phân hóa rất tốt**, phân loại rõ ràng được năng lực lý thuyết của từng nhóm học viên. Tỷ lệ trượt lý thuyết cực thấp (chỉ 4.3%).
*   **Độ phù hợp của đề thi thực hành (Tự luận) - Phù hợp 90%:** Đề thi thực hành bám sát trực tiếp các chủ đề cốt lõi đã ôn tập hè, không đòi hỏi các công nghệ nâng cao ngoài phạm vi. Học viên chỉ cần rà soát code để chỉ ra các lỗi logic web cơ bản (thiếu `@Transactional`, tin tưởng tham số client, thiếu check patientId).
*   **Độ phù hợp tổng thể để triển khai ĐGNL đạt: 90%** (Phù hợp rất cao). Bộ đề thi hoàn toàn đảm bảo chất lượng, khoa học và thích hợp để làm chuẩn đo lường năng lực học viên.

---

## 4. CÁC ĐỀ XUẤT BỔ SUNG CHI TIẾT (DỰA TRÊN THIẾU SÓT ĐGNL & XU HƯỚNG MỚI)

Các phần bổ sung dưới đây được thiết kế **trực tiếp dựa trên các thiếu sót cốt lõi của sinh viên trong đợt ĐGNL Lần 1** (như việc thiếu kỹ năng khóa concurrency, hổng bảo mật IDOR/Input validation, và lỗi nghẽn RAM/bộ nhớ). Đồng thời, đề xuất sử dụng **các công nghệ mới nhất đón đầu xu hướng hiện nay** thay vì các công nghệ cũ:

### Đề xuất 1: Bổ sung thực chiến môn Thiết kế Hệ thống Microservices (`IT214-K24`)
*   **Bridge Module (Cầu nối - 2 buổi đầu):** Dạy củng cố lý thuyết `@Transactional` monolithic nâng cao và thực hành **Pessimistic/Optimistic Locking trong JPA** để chống race condition.
*   **OAuth2 Token Propagation:** Cấu hình Feign Client RequestInterceptor truyền JWT token qua API Gateway xuống các downstream service nhằm ngăn chặn lỗ hổng IDOR.
*   **Modern Distributed Tracing:** Tích hợp **Micrometer Tracing + OpenTelemetry (OTel) + Grafana Tempo / Jaeger** (chuẩn hiện đại nhất cho Spring Boot 3+) để thay thế cho Spring Cloud Sleuth đã lỗi thời.
*   *Lưu ý:* Không dạy lại Docker Compose trong môn này vì môn DevOps đã dạy, giảng viên hướng dẫn học sinh cách tái sử dụng.

### Đề xuất 2: Bổ sung DevSecOps và Giám sát môn DevOps Fundamentals (`IT209-K24`)
*   **Lightweight DevSecOps Pipeline:** Tích hợp các tool quét lỗ hổng bảo mật tĩnh hiện đại, nhanh gọn như **Semgrep hoặc Snyk** (chạy trực tiếp trong GitHub Actions) thay vì setup SonarQube server cồng kềnh cho các dự án vừa/nhỏ.
*   **Lightweight Observability Stack (PLG Stack):** Setup **Prometheus + Loki + Promtail + Grafana** để theo dõi tài nguyên RAM/CPU và log của VPS. Đây là xu hướng hiện đại thay thế cho ELK Stack rất nặng, dễ gây lỗi Out of Memory (OOM) trên VPS cấu hình thấp.
*   **Database Migration:** Sử dụng Flyway hoặc Liquibase tích hợp trong pipeline để tự động hóa cập nhật schema DB.

### Đề xuất 3: Tối ưu chi phí và hiệu năng môn AI Integration in Action (`IT213-K24`)
*   **Semantic Caching with Redis VL:** Sử dụng thư viện vector chuyên dụng của Redis (RedisVL) hoặc GPTCache để cache các câu trả lời LLM tương đồng nhằm tối ưu chi phí API LLM và tăng tốc phản hồi.
*   **Advanced AI Agents:** Xây dựng các AI Agent dạng đồ thị đa tác vụ sử dụng **LangGraph / CrewAI** (xu hướng mới thay thế cho LangChain Chain tuần tự cũ).
*   **Server-Sent Events (SSE) / Streaming:** Trả kết quả AI dạng stream về ReactJS, tránh nghẽn RAM khi tạo câu trả lời dài và nâng cao trải nghiệm UI.

---

## 5. ĐỀ XUẤT CHO KỲ V (KỲ TỐT NGHIỆP - CAPSTONE PROJECT)
1.  **Hội đồng chấm thi có sự tham gia của Tech Lead Doanh nghiệp:** Đánh giá sản phẩm dưới góc độ hệ thống chạy production.
2.  **Bộ tiêu chuẩn bắt buộc trong Rubric đồ án tốt nghiệp:**
    *   Hệ thống có cơ chế kiểm soát đồng thời (Concurrency Control) được chứng minh qua báo cáo Load Test.
    *   Hệ thống vượt qua bài test bảo mật (không có lỗ hổng IDOR/Path Traversal/SQL Injection).
    *   Sản phẩm được đóng gói Docker và deploy tự động qua CI/CD Pipeline lên Cloud (AWS/DigitalOcean).
