import enum
import logging
import tempfile
from contextlib import contextmanager
from io import BytesIO
from typing import Callable, Dict, List, Union, final, Generator
from app.core.config import QdrantSettings, get_qdrant_settings
from langchain_community.document_loaders import Docx2txtLoader, PyMuPDFLoader, TextLoader
from langchain_core.documents.base import Document
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import get_logger
from langchain_ollama import OllamaEmbeddings
from uuid import uuid4

logger = get_logger(__name__)

DocumentOutput = Union[str, List[Document]]


class FileExtension(enum.Enum):
    PDF = ".pdf"
    DOCX = ".docx"
    MD = ".md"
    TXT = ".txt"


class UnsupportedFileTypeError(Exception):
    """Exception raised when an unsupported file type is provided."""
    pass


@final
class DocumentService:

    def __init__(self, qdrant_settings: QdrantSettings) -> None:
        self._handlers: Dict[str, Callable[[BytesIO, str], DocumentOutput]] = {
            FileExtension.PDF.value: self._load_pdf,
            FileExtension.DOCX.value: self._load_docx,
            FileExtension.MD.value: self._load_text,
            FileExtension.TXT.value: self._load_text,
        }
        self.embeddings = OllamaEmbeddings(
            base_url=qdrant_settings.OLLAMA_URL,
            model="mxbai-embed-large",         
        )
        self.vector_store = QdrantVectorStore.from_existing_collection(
            embedding=self.embeddings,
            collection_name=qdrant_settings.QDRANT_COLLECTION_NAME,
            host=qdrant_settings.QDRANT_HOST,
            port=qdrant_settings.QDRANT_PORT
        )

    def load_document(self, document: BytesIO, file_extension: str) -> DocumentOutput:

        document.seek(0)
        handler = self._handlers.get(file_extension)

        if not handler:
            logger.error(
                "Unsupported file extension provided: %s", file_extension)
            raise UnsupportedFileTypeError(
                f"Unsupported file extension: {file_extension}")

        try:
            return handler(document, file_extension) if file_extension in {".md", ".txt"} else handler(document)
        except Exception as e:
            logger.exception("Failed to load document: %s", e)
            raise

    def create_chunks(self, list_of_documents: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,  # Modify
            chunk_overlap=20,  # Modify
            length_function=len,
            is_separator_regex=False,
            separators=[
                "\n\n",
                "\n",
                " ",
                ".",
                ",",
            ]
        )
        return text_splitter.split_documents(list_of_documents)
    
    
        

    def upload_chunks_to_qdrant(self, chunks: list[Document]) -> None:
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        self.vector_store.add_documents(
            documents=chunks,
            ids=uuids
        )
        
        
    @contextmanager
    def _temp_file(self, document: BytesIO, suffix: str) -> Generator[str, None, None]:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(document.read())
            tmp.flush()
            document.seek(0)
            yield tmp.name

    def _load_pdf(self, document: BytesIO) -> List[Document]:
        with self._temp_file(document, ".pdf") as tmp_name:
            pdf_loader = PyMuPDFLoader(tmp_name)
            return pdf_loader.load()

    def _load_docx(self, document: BytesIO) -> List[Document]:
        with self._temp_file(document, ".docx") as tmp_name:
            doc_loader = Docx2txtLoader(tmp_name)
            return doc_loader.load()

    def _load_text(self, document: BytesIO, file_extension: str) -> List[Document]:
        with self._temp_file(document, file_extension) as tmp_name:
            text_loader = TextLoader(tmp_name)
            return text_loader.load()


service = DocumentService(qdrant_settings=get_qdrant_settings())