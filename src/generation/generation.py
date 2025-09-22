import os
import json
from typing import Annotated, Any, Dict, List, Literal, Optional, Type

from google import genai
from pydantic import BaseModel, ConfigDict, Field, confloat, conlist
from typing_extensions import Annotated

class Citation(BaseModel):
    label: str
    locator: str


class ResponseSchema(BaseModel):
    status: Literal["OK", "INSUFFICIENT_CONTEXT"]
    source_used: Literal["MEMORY", "RAG", "WEB", "TOOL", "NONE"]
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    confidence: Annotated[float, Field(ge=0, le=1)]
    missing: List[str] = Field(default_factory=list)

SYSTEM_PROMPT = """You are a research assistant that MUST ground answers in provided context.
Policy:
1) Use only the supplied CONTEXT and/or explicit SOURCE items.
2) If context is INSUFFICIENT to answer the QUESTION, return status=INSUFFICIENT_CONTEXT with what is missing.
3) If sufficient, answer concisely with citations (doc/page or URL) and a confidence score (0–1).
4) Never rely on parametric knowledge if it is not in the context.
5) Output MUST match the response schema exactly.
"""

RAG_TEMPLATE = (
    "CONTEXT:\n{context}\n"
    "---------------------\n"
    "QUESTION:\n{query}\n\n"
    "Task: Determine if the CONTEXT is sufficient to answer the QUESTION.\n"
    "- If sufficient: produce a grounded answer with citations and confidence.\n"
    "- If NOT sufficient: do NOT answer; return status=INSUFFICIENT_CONTEXT and list missing info.\n"
    "Fill the structured fields only.\n"
)


class StructuredResponseGen:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash-lite",
        system_prompt: str = SYSTEM_PROMPT,
        rag_template: str = RAG_TEMPLATE,
        temperature: float = 0.2,
    ):
        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.model = model
        self.system_prompt = system_prompt
        self.rag_template = rag_template
        self.temperature = temperature

    def generate(
        self,
        *,
        query: str,
        context_blocks: List[str],
        source_used: str = "RAG",
        schema: Type[BaseModel] = ResponseSchema,
    ) -> Dict[str, Any]:
        context = "\n\n".join(context_blocks).strip()
        user_prompt = self.rag_template.format(context=context, query=query)

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )


        output_text = getattr(response, "text", None)
        if not output_text:
            raise RuntimeError(f"Unexpected response payload: {response}")

        try:
            data = json.loads(output_text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {e}\nRaw: {output_text[:400]}")

        try:
            validated = ResponseSchema(**data).model_dump()
        except Exception as e:
            raise RuntimeError(f"Output does not match schema: {e}")

        validated["source_used"] = source_used
        return validated