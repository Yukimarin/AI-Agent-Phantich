# THIẾT KẾ ĐỀ XUẤT CẢI TIẾN CHƯƠNG TRÌNH ĐÀO TẠO KỲ IV & V - KS24 (CẬP NHẬT ĐỐI SOÁT HỌC THUẬT GỐC)

## 1. Nhận xét về chương trình học KS24 (Tải lượng & Học phần tiên quyết)
* **Thực trạng Kỳ III:** Ghi nhận tỷ lệ trượt môn rất cao: **70 SV trượt Java Advanced**, **46 SV trượt Java Web App**, và **42 SV trượt Java Web Service**.
* **Đánh giá bối cảnh:** Mặc dù chương trình chính thức (PM) thiết kế rất tốt các công nghệ phân tán (Saga, Kafka, Gateway...), việc gần 40% sinh viên bị hổng nền tảng Java Web ở Kỳ III sẽ tạo áp lực cực lớn lên Kỳ IV. Cần có lớp bổ trợ cầu nối.

## 2. Đối soát sự phù hợp nội dung Ôn tập vs. Đề thi (MCQ & Thực hành)
*   **Trắc nghiệm (MCQ) - Độ phù hợp ~90%:** Ôn tập và đề thi lý thuyết khớp nhau hoàn toàn về các chủ đề (OOP, Spring Boot syntax, React Hooks, Agile Scrum). Học viên thi đúng phần được ôn tập.
*   **Thực hành (Tự luận) - Độ phù hợp ~90%:** Đề thi thực hành bám sát trực tiếp các chủ đề cốt lõi đã ôn tập hè, không đòi hỏi các công nghệ nâng cao ngoài phạm vi. Học viên chỉ cần rà soát một đoạn code Spring Boot ngắn để chỉ ra các lỗi logic nghiệp vụ căn bản (như thiếu `@Transactional`, tin tưởng tham số giá của client truyền lên, thiếu check patientId).

## 3. Phân tích thống kê & Đánh giá chất lượng đề trắc nghiệm (KS24)
Chất lượng đề trắc nghiệm dựa trên điểm thi thực tế của 164 học viên KS24 dự thi:
*   **Điểm trung bình:** `72.57 / 100` (Phản ánh học viên nắm khá chắc lý thuyết cơ bản đã được ôn tập).
*   **Độ lệch chuẩn (Std Dev):** `16.88` (Độ phân tán tốt, chứng tỏ đề thi phân loại rõ rệt trình độ học viên giỏi/khá/trung bình).
*   **Phân bổ dải điểm (Dạng Bell-curve):**
    *   *Xuất sắc (90 - 100):* **16.5%** (27 SV - Nhận diện chính xác nhóm xuất sắc).
    *   *Khá - Giỏi (80 - 89):* **18.3%** (30 SV - Lực lượng nòng cốt).
    *   *Khá (70 - 79):* **25.0%** (41 SV - Nhóm chuẩn khá).
    *   *Trung bình (50 - 69):* **36.0%** (59 SV - Cần bồi dưỡng thêm).
    *   *Yếu kém (< 50):* **4.3%** (7 SV - Tỷ lệ trượt lý thuyết rất thấp nhờ ôn tập đúng trọng tâm).

## 4. Chỉ số phù hợp tổng thể để triển khai ĐGNL đạt: 90%
Cả hai phần thi trắc nghiệm (MCQ) và tự luận (thực hành) đều bám sát 90% chương trình ôn tập hè. Đề thi hoàn toàn phù hợp để triển khai làm chuẩn ĐGNL.

## 5. Đề xuất Chi tiết về Chương trình đào tạo Kỳ IV & Kỳ V

### Ghi nhận về khung PM hiện tại (Thiết kế bài bản của Ban Đào tạo):
*   **Microservices (IT214):** Đầy đủ công nghệ phân tán hiện đại (Saga, Kafka, API Gateway, Eureka, Resilience4j, Spring Cache/Redis).
*   **DevOps (IT209):** Lộ trình bài bản từ VPS hosting, Nginx, Linux CLI, Docker/Docker Compose đến GitHub Actions CI/CD.
*   **AI Integration (IT213):** Rất đón đầu xu hướng với Spring AI, pgvector RAG, Function Calling, AI Agent, Langfuse, và MCP.

---

### A. Kiến thức cần bổ sung vào các môn học hiện tại (Dựa trên thiếu sót ĐGNL & Xu hướng mới)
Các phần bổ sung dưới đây được thiết kế **trực tiếp dựa trên các thiếu sót cốt lõi của sinh viên trong đợt ĐGNL Lần 1** (như việc thiếu kỹ năng khóa concurrency, hổng bảo mật IDOR/Input validation, và lỗi nghẽn RAM/bộ nhớ). Đồng thời, đề xuất sử dụng **các công nghệ mới nhất đón đầu xu hướng hiện nay** thay vì các công nghệ cũ:

* **Môn Thiết kế Hệ thống Microservices (IT214-K24):**
  - *Bridge Module (Cầu nối - 2 buổi đầu):* Ôn tập lại `@Transactional` monolithic nâng cao và thực hành **Pessimistic/Optimistic Locking trong JPA** để chống race condition.
  - *OAuth2 Token Propagation:* Cấu hình Feign Client RequestInterceptor truyền JWT token qua API Gateway xuống các downstream service nhằm ngăn chặn lỗ hổng IDOR.
  - *Modern Distributed Tracing:* Tích hợp **Micrometer Tracing + OpenTelemetry (OTel) + Grafana Tempo / Jaeger** (chuẩn hiện đại nhất cho Spring Boot 3+) để thay thế cho Spring Cloud Sleuth đã lỗi thời.
  - *Lưu ý:* Không dạy lại Docker Compose trong môn này vì PM DevOps Session 9 đã thiết kế bài bản, giảng viên hướng dẫn học sinh cách tái sử dụng.
* **Môn DevOps Fundamentals (IT209-K24):**
  - *Lightweight DevSecOps Pipeline:* Tích hợp các tool quét lỗ hổng bảo mật tĩnh hiện đại, nhanh gọn như **Semgrep hoặc Snyk** (chạy trực tiếp trong GitHub Actions) thay vì setup SonarQube server cồng kềnh.
  - *Lightweight Observability Stack (PLG Stack):* Setup **Prometheus + Loki + Promtail + Grafana** để theo dõi tài nguyên RAM/CPU và log của VPS. Đây là xu hướng hiện đại thay thế cho ELK Stack rất nặng, dễ gây lỗi Out of Memory (OOM) trên VPS cấu hình thấp.
  - *Database Migration:* Sử dụng Flyway hoặc Liquibase tích hợp trong pipeline để tự động hóa cập nhật schema DB.
* **Môn AI Integration in Action (IT213-K24):**
  - *Semantic Caching with Redis VL:* Sử dụng thư viện vector chuyên dụng của Redis (RedisVL) hoặc GPTCache để cache các câu trả lời LLM tương đồng nhằm tối ưu chi phí API LLM và tăng tốc phản hồi.
  - *Advanced AI Agents:* Xây dựng các AI Agent dạng đồ thị đa tác vụ sử dụng **LangGraph / CrewAI** (xu hướng mới thay thế cho LangChain Chain tuần tự cũ).
  - *Server-Sent Events (SSE) / Streaming:* Cấu hình endpoint trả kết quả AI dạng stream về ReactJS để tránh nghẽn RAM khi tạo câu trả lời dài và nâng cao trải nghiệm UI.

### B. Môn học bổ sung để mở rộng vị trí việc làm theo xu hướng thị trường (Kỳ V)
* **Python & Data Engineering / Analytics Fundamentals (Tự chọn mới):** Học xử lý dữ liệu bằng Python (Pandas/SQL) kết hợp trực quan hóa bằng PowerBI.
  - *➔ Định hướng vị trí:* Chuyên viên phân tích dữ liệu (Data Analyst), BI Developer.
* **Cloud Native & Kubernetes Scaling (Tự chọn mới):** Học các dịch vụ Cloud nâng cao (AWS EC2, S3, RDS, IAM) và điều phối Kubernetes (K8s).
  - *➔ Định hướng vị trí:* Kỹ sư Cloud (Cloud Engineer), DevOps/SRE.
