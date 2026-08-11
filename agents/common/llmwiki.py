import os
import json
import glob
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
try:
    import faiss
    import numpy as np
    from google import genai
except ImportError:
    pass # Will be handled properly when used without dependencies

class LLMWiki:
    def __init__(self):
        self.inputs_dir = "data/inputs"
        self.processed_dir = "data/processed"
        self.index_path = os.path.join(self.processed_dir, "wiki_index.faiss")
        self.texts_path = os.path.join(self.processed_dir, "wiki_texts.json")
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required to use LLMWiki.")
            
        self.client = genai.Client(api_key=api_key)
        self.embedding_model = 'text-embedding-004'
        self.dimension = 768 # text-embedding-004 output dimension
        
        self.index = None
        self.chunks = []
        
        # Tự động nạp index nếu đã có
        self._load_index()

    def _chunk_text(self, text, max_length=500):
        """Cắt nhỏ văn bản theo độ dài xấp xỉ max_length characters, giữ nguyên câu."""
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if len(current_chunk) + len(p) < max_length:
                current_chunk += p + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = p + "\n\n"
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def _get_embedding(self, text):
        response = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
        )
        return response.embeddings[0].values

    def _load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.texts_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.texts_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
            # print("LLMWiki: Đã tải Index từ cache nội bộ.")
        else:
            self.build_index()

    def build_index(self):
        print("LLMWiki: Đang quét tài liệu và xây dựng Vector Index lần đầu...")
        
        md_files = glob.glob(os.path.join(self.inputs_dir, "*.md"))
        all_chunks = []
        
        for filepath in md_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            doc_chunks = self._chunk_text(text)
            # Thêm tiêu đề file vào chunk để giữ ngữ cảnh
            filename = os.path.basename(filepath)
            doc_chunks = [f"[Trích từ tài liệu: {filename}]\n{chunk}" for chunk in doc_chunks]
            all_chunks.extend(doc_chunks)
            
        if not all_chunks:
            print("LLMWiki: Không tìm thấy tài liệu markdown nào trong data/inputs/.")
            return
            
        self.chunks = all_chunks
        embeddings = []
        
        print(f"LLMWiki: Bắt đầu embedding {len(self.chunks)} chunks...")
        # Lặp qua từng chunk để lấy embedding (Có thể batch để nhanh hơn nhưng chạy lần đầu không sao)
        for i, chunk in enumerate(self.chunks):
            vec = self._get_embedding(chunk)
            embeddings.append(vec)
            if (i+1) % 10 == 0:
                print(f"LLMWiki: Đã mã hóa {i+1}/{len(self.chunks)} chunks.")
                
        embedding_matrix = np.array(embeddings).astype('float32')
        
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embedding_matrix)
        
        faiss.write_index(self.index, self.index_path)
        with open(self.texts_path, 'w', encoding='utf-8') as f:
            json.load(self.chunks, f) if hasattr(json, 'dump') else json.dump(self.chunks, f, ensure_ascii=False, indent=2)
            
        print("LLMWiki: Đã lưu Vector Index cục bộ thành công.")

    def query(self, question, top_k=2):
        if self.index is None or not self.chunks:
            return "LLMWiki chưa được khởi tạo với tài liệu nào."
            
        question_vec = np.array([self._get_embedding(question)]).astype('float32')
        distances, indices = self.index.search(question_vec, top_k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
                
        return "\n\n---\n\n".join(results)
