import enum
import logging
import tempfile
from contextlib import contextmanager
from io import BytesIO
from typing import Callable, Dict, List, Union, final, Generator

import pymupdf
from langchain_community.document_loaders import Docx2txtLoader, PyMuPDFLoader
from langchain_core.documents.base import Document
from app.core.logger import get_logger

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
    
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[BytesIO], DocumentOutput]] = {
            FileExtension.PDF.value: self._load_pdf,
            FileExtension.DOCX.value: self._load_docx,
            FileExtension.MD.value: self._load_text,
            FileExtension.TXT.value: self._load_text,
        }

    def load_document(self, document: BytesIO, file_extension: str) -> DocumentOutput:
        
        document.seek(0)
        handler = self._handlers.get(file_extension)

        if not handler:
            logger.error("Unsupported file extension provided: %s", file_extension)
            raise UnsupportedFileTypeError(f"Unsupported file extension: {file_extension}")

        try:
            return handler(document)
        except Exception as e:
            logger.exception("Failed to load document: %s", e)
            raise

    @contextmanager
    def _temp_file(self, document: BytesIO, suffix: str) -> Generator[str, None, None]:
        with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
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

    def _load_text(self, document: BytesIO) -> str:
        return document.getvalue().decode("utf-8")


service = DocumentService()
