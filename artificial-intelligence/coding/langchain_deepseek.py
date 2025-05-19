from typing import Any
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import BaseLLM
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import LLMResult

class Deepseek(BaseLLM):
  def _generate(self, prompts: list[str], stop: list[str] | None = None, run_manager: CallbackManagerForLLMRun | None = None, **kwargs: Any) -> LLMResult:
    return super()._generate(prompts, stop, run_manager, **kwargs)

  @property
  def _llm_type(self):
    return ''

class ChatDeepseek(BaseChatModel):
  pass

