from collections.abc import Generator
from contextlib import contextmanager
import enum
from io import BytesIO
import tempfile
from typing import Callable, Sequence, cast, final
from uuid import UUID
import uuid

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyMuPDFLoader,
    TextLoader,
)
from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents.base import Document as LangChainDocument

from app.core.logger import get_logger

logger = get_logger(__name__)


@final
class FileExtension(enum.Enum):
    PDF = ".pdf"
    DOCX = ".docx"
    MD = ".md"
    TXT = ".txt"


@final
class VectorService:

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[[BytesIO, str], list[LangChainDocument]]] = {
            FileExtension.PDF.value: self._load_pdf,
            FileExtension.DOCX.value: self._load_docx,
            FileExtension.MD.value: self._load_text,
            FileExtension.TXT.value: self._load_text,
        }

    def load_document_into_vector_database(
        self, document: BytesIO, file_extension: str, vector_store: QdrantVectorStore
    ) -> list[str]:
        _ = document.seek(0)
        handler = self._handlers[file_extension]

        lc_documents: list[LangChainDocument]
        lc_documents = (
            handler(document, file_extension)
            if file_extension in {".md", ".txt"}
            else handler(document, "")
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,  
            chunk_overlap=50,  
            length_function=len,
            is_separator_regex=False,
            separators=[
                "\n\n",
                "\n",
                " ",
                ".",
                ",",
            ],
        )
        chunks = text_splitter.split_documents(lc_documents)
        uuids = [str(uuid.uuid4()) for _ in range(len(chunks))]

        chunk_ids = vector_store.add_documents(documents=chunks, ids=uuids)
        return chunk_ids

    def drop_chunks_from_document_id(
        self, chunk_ids: list[str], vector_store: QdrantVectorStore
    ):
        _ = vector_store.delete(ids=cast(list[str | int], chunk_ids))

    @contextmanager
    def _temp_file(self, document: BytesIO, suffix: str) -> Generator[str, None, None]:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            _ = tmp.write(document.read())
            tmp.flush()
            _ = document.seek(0)
            yield tmp.name

    def _load_pdf(self, document: BytesIO, _: str) -> list[LangChainDocument]:
        with self._temp_file(document, ".pdf") as tmp_name:
            pdf_loader = PyMuPDFLoader(tmp_name)
            return pdf_loader.load()

    def _load_docx(self, document: BytesIO, _: str) -> list[LangChainDocument]:
        with self._temp_file(document, ".docx") as tmp_name:
            doc_loader = Docx2txtLoader(tmp_name)
            return doc_loader.load()

    def _load_text(
        self, document: BytesIO, file_extension: str
    ) -> list[LangChainDocument]:
        with self._temp_file(document, file_extension) as tmp_name:
            text_loader = TextLoader(tmp_name)
            return text_loader.load()

    def retrieve_documents(self, user_query: str, vector_store: QdrantVectorStore) -> list[LangChainDocument]:
        results = vector_store.similarity_search(user_query, k=3)  
        return results

service = VectorService()
