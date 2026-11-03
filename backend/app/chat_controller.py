import sqlite3
from .chat_models import ChatError
from .provider import MockProvider, OpenAIProvider, Answer
from .retrieval import retrieve
from .reply_policy import reviewed_reply


class ChatController:
    def __init__(self, repository, settings, provider=None):
        self.repository, self.settings = repository, settings
        self.provider = provider or (MockProvider() if settings.mode == "mock" else OpenAIProvider(settings))

    async def submit(self, conversation_id, request_id, content):
        repo = self.repository
        attempt = repo.begin(conversation_id, request_id, content)
        if attempt is None:
            return repo.exchange(conversation_id, request_id)
        try:
            fixed = reviewed_reply(content)
            if fixed is not None:
                repo.set_provider(request_id, attempt, 'local', 'reviewed-rules-v1', False)
                repo.finish(conversation_id, request_id, attempt, fixed, [], 'not_requested')
                return repo.exchange(conversation_id, request_id)
            provider, fallback = self.provider, False
            repo.set_provider(request_id, attempt, provider.mode, provider.model, fallback)
            if provider.mode == "openai":
                if not self.settings.configured:
                    raise ChatError("provider_not_configured", "Live chat is not configured. Breathing and support still work.")
                if not repo.reserve_live(self.settings.demo_session):
                    provider, fallback = MockProvider(), True
            repo.set_provider(request_id, attempt, provider.mode, provider.model, fallback)
            sql = await provider.propose(content)
            records = retrieve(repo.path, sql, conversation_id)
            answer = Answer.model_validate(await provider.answer(content, records))
            allowed_ids = {row.get("id", row.get("profile_id")) for row in records}
            if not set(answer.record_ids).issubset(allowed_ids):
                raise ChatError("ungrounded_reply", "The reply cited an unavailable record. Your message is saved; you can retry.")
            repo.finish(conversation_id, request_id, attempt, answer.content,
                        answer.record_ids, "selected" if records else "empty")
            return repo.exchange(conversation_id, request_id)
        except (ChatError, sqlite3.Error, OSError) as error:
            # A storage error may also prevent marking failure. Never mask the original error.
            try:
                repo.fail(request_id, attempt, error.code if isinstance(error, ChatError) else "storage_unavailable")
            except (sqlite3.Error, OSError):
                pass
            raise
