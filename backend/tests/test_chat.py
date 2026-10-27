"""Deterministic fictional exchanges, storage failures and SQL security boundaries."""
import asyncio
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import httpx
from fastapi.testclient import TestClient
from app.main import create_app
from app.config import Settings, load_settings
from app.chat_repository import ChatRepository
from app.chat_controller import ChatController
from app.chat_models import ChatError
from app.provider import MockProvider, OpenAIProvider, Answer
from app.retrieval import QUERIES, retrieve, validate_sql
from tests.test_repository import fictional_session, SESSION_ID


class FakeProvider(MockProvider):
    def __init__(self):
        self.calls = 0
        self.fail_stage = None
        self.sql = None
        self.bad_ids = False

    async def propose(self, question):
        self.calls += 1
        if self.fail_stage == 'query':
            raise ChatError('provider_failed', 'The AI could not reply. Your message is saved; you can retry.')
        return self.sql or await super().propose(question)

    async def answer(self, question, records):
        self.calls += 1
        if self.fail_stage == 'answer':
            raise ChatError('provider_failed', 'The AI could not reply. Your message is saved; you can retry.')
        if self.bad_ids:
            return Answer(content='Unverified claim.', record_ids=['not-retrieved'])
        return await super().answer(question, records)


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite3'
        self.provider = FakeProvider()
        self.client = self.enterContext(TestClient(create_app(self.path, Settings(), self.provider)))
        self.repo = ChatRepository(self.path)
        self.conversation, self.request = str(uuid4()), str(uuid4())
        self.url = f'/api/conversations/{self.conversation}/messages/{self.request}'

    def submit(self, content='What happened in my last session?'):
        return self.client.put(self.url, json={'content': content})

    def history(self):
        return self.client.get(f'/api/conversations/{self.conversation}').json()['messages']

    def test_empty_retrieval_is_honest_and_saved(self):
        body = self.submit().json()
        self.assertTrue(body['saved'])
        self.assertEqual(body['provider_mode'], 'mock')
        self.assertEqual(body['messages'][1]['retrieval_status'], 'empty')
        self.assertEqual(body['messages'][1]['content'], 'No matching saved records were found.')
        self.assertEqual(self.provider.calls, 2)

    def test_selected_records_ids_and_restart_no_duplicate(self):
        self.client.put(f'/api/sessions/{SESSION_ID}', json=fictional_session())
        body = self.submit().json()
        self.assertEqual(body['messages'][1]['record_ids'], [SESSION_ID])
        self.assertIn('20 active seconds', body['messages'][1]['content'])
        self.assertEqual(self.submit().json(), body)
        self.assertEqual(self.provider.calls, 2)
        with TestClient(create_app(self.path, Settings(), self.provider)) as restarted:
            self.assertEqual(restarted.get(f'/api/conversations/{self.conversation}').json()['messages'], body['messages'])
            self.assertEqual(restarted.put(self.url, json={'content': 'What happened in my last session?'}).json(), body)
        with closing(self.repo.connect()) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0], 2)
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_conflicting_retry_and_validation(self):
        self.submit()
        self.assertEqual(self.submit('Different').status_code, 409)
        for value in ('', '   ', 'a' * 1001):
            self.assertEqual(self.client.put(self.url, json={'content': value}).status_code, 422)
        self.assertEqual(self.client.put(self.url, json={'content': 'Hi', 'profile_id': 'other'}).status_code, 422)
        self.assertEqual(self.provider.calls, 2)

    def test_both_provider_failures_preserve_user_and_retry(self):
        for stage in ('query', 'answer'):
            with self.subTest(stage=stage):
                self.provider.fail_stage = stage
                response = self.submit()
                self.assertEqual(response.status_code, 503)
                rows = self.history()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]['status'], 'failed')
        original_id = self.history()[0]['id']
        self.provider.fail_stage = None
        self.assertEqual(self.submit().status_code, 200)
        self.assertEqual(len(self.history()), 2)
        self.assertEqual(self.history()[0]['id'], original_id)

    def test_rejected_write_query_does_not_run_second_call_or_change_sessions(self):
        self.client.put(f'/api/sessions/{SESSION_ID}', json=fictional_session())
        self.provider.sql = 'DELETE FROM sessions'
        self.assertEqual(self.submit().json()['error']['code'], 'retrieval_rejected')
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual(len(self.client.get('/api/sessions').json()['sessions']), 1)
        self.assertEqual(len(self.history()), 1)

    def test_retrieval_failure_distinct_from_empty(self):
        with patch('app.chat_controller.retrieve', side_effect=ChatError('retrieval_unavailable', 'History unavailable.')):
            self.assertEqual(self.submit().json()['error']['code'], 'retrieval_unavailable')
        self.assertEqual(self.history()[0]['status'], 'failed')
        self.assertEqual(self.provider.calls, 1)

    def test_rejects_invented_citations(self):
        self.provider.bad_ids = True
        self.assertEqual(self.submit().json()['error']['code'], 'ungrounded_reply')
        self.assertEqual(len(self.history()), 1)

    def test_failed_reply_save_never_returns_saved_or_invents_reply(self):
        with patch.object(ChatRepository, 'finish', side_effect=sqlite3.OperationalError('fictional failure')):
            response = self.submit()
        self.assertEqual(response.status_code, 503)
        self.assertNotIn('saved', response.json())
        self.assertEqual(len(self.history()), 1)
        self.assertEqual(self.history()[0]['error_code'], 'storage_unavailable')
        self.assertEqual(self.submit().status_code, 200)
        self.assertEqual(len(self.history()), 2)

    def test_initial_save_failure_makes_no_provider_call(self):
        with patch.object(ChatRepository, 'begin', side_effect=sqlite3.OperationalError('fictional failure')):
            self.assertEqual(self.submit().status_code, 503)
        self.assertEqual(self.provider.calls, 0)

    def test_pending_lease_rejects_duplicate_and_expired_retry_preserves_user(self):
        attempt = self.repo.begin(self.conversation, self.request, 'What happened in my last session?')
        self.assertEqual(self.submit().status_code, 409)
        self.assertEqual(self.provider.calls, 0)
        with closing(self.repo.connect()) as db, db:
            db.execute('UPDATE chat_requests SET lease_until = 0')
        self.assertEqual(self.history()[0]['error_code'], 'attempt_interrupted')
        self.assertEqual(self.submit().status_code, 200)
        self.assertEqual(len(self.history()), 2)
        with self.assertRaises(ChatError):
            self.repo.finish(self.conversation, self.request, attempt, 'Late', [], 'empty')

    def test_conversation_message_order_and_pagination(self):
        self.submit('How does breathing work?')
        url = f'/api/conversations/{self.conversation}/messages/{uuid4()}'
        self.client.put(url, json={'content': 'What did I say?'})
        rows = self.history()
        self.assertEqual([r['role'] for r in rows], ['user', 'assistant', 'user', 'assistant'])
        self.assertEqual(len({r['id'] for r in rows}), 4)
        page = self.client.get(f'/api/conversations/{self.conversation}?limit=2&offset=2').json()['messages']
        self.assertEqual(page, rows[2:])
        self.assertEqual(self.client.get('/api/conversations').json()['conversations'][0]['id'], self.conversation)

    def test_crisis_and_off_topic_mock_do_not_claim_clinical_help(self):
        body = self.submit('Fictional Alex says: I want to hurt myself.').json()
        self.assertIn('Crisis support', body['messages'][1]['content'])
        self.assertEqual(self.client.get('/api/health').status_code, 200)
        self.assertEqual(self.client.get('/api/sessions').status_code, 200)
        self.assertIn('cannot assess', asyncio.run(self.provider.answer('Diagnose me', [])).content)

    def test_preferences_round_trip_and_reset(self):
        self.assertFalse(self.client.get('/api/preferences').json()['saved'])
        values = {'mode': 'motion', 'simple': False, 'font_size': 'large'}
        self.assertEqual(self.client.put('/api/preferences', json=values).json()['preferences'], values)
        self.assertEqual(self.client.get('/api/preferences').json()['preferences'], values)
        self.assertEqual(self.client.put('/api/preferences', json={'mode': 'invalid'}).status_code, 422)
        self.client.put('/api/preferences', json={'mode': 'text', 'simple': True, 'font_size': 'standard'})
        with TestClient(create_app(self.path, Settings())) as restarted:
            self.assertEqual(restarted.get('/api/preferences').json()['preferences']['mode'], 'text')

    def test_missing_live_configuration_no_calls_and_no_secret_in_response(self):
        with TestClient(create_app(self.path, Settings(mode='openai'))) as live:
            health = live.get('/api/health').json()
            self.assertFalse(health['provider_configured'])
            response = live.put(self.url, json={'content': 'Hello'})
            self.assertEqual(response.json()['error']['code'], 'provider_not_configured')
            self.assertEqual(live.get('/api/health').json()['live_calls_reserved'], 0)

    def test_persistent_budget_fallback_caps_two_call_exchanges(self):
        fake = FakeProvider()
        fake.mode, fake.model = 'openai', 'test-only'
        settings = Settings(mode='openai', api_key='fictional', model='test-only')
        with TestClient(create_app(self.path, settings, fake)) as live:
            for _ in range(24):
                self.assertTrue(self.repo.reserve_live(settings.demo_session))
            first = live.put(self.url, json={'content': 'How does breathing work?'}).json()
            self.assertEqual(first['provider_mode'], 'openai')
            self.assertEqual(fake.calls, 2)
        with TestClient(create_app(self.path, settings, fake)) as restarted:
            fallback = restarted.put(f'/api/conversations/{self.conversation}/messages/{uuid4()}', json={'content': 'How does breathing work?'}).json()
            self.assertTrue(fallback['budget_fallback'])
            self.assertEqual(fallback['provider_mode'], 'mock')
            self.assertEqual(restarted.get('/api/health').json()['live_calls_reserved'], 50)
            self.assertEqual(fake.calls, 2)

    def test_sql_rejects_scope_changes_functions_comments_and_multiple_statements(self):
        bad = [
            'SELECT * FROM sessions', QUERIES['sessions'] + '; DELETE FROM sessions',
            QUERIES['sessions'] + ';', QUERIES['sessions'] + ' -- comment',
            QUERIES['sessions'].replace('profile_id = :profile_id', '1 = 1'),
            QUERIES['sessions'].replace('LIMIT 5', 'LIMIT 5000'),
            'PRAGMA table_info(messages)', 'SELECT load_extension(:path)',
            'WITH x AS (SELECT * FROM sessions) SELECT * FROM x',
            QUERIES['messages'].replace('AND conversation_id = :conversation_id', ''),
            QUERIES['sessions'] + ' UNION SELECT * FROM messages',
        ]
        for sql in bad:
            with self.subTest(sql=sql), self.assertRaises(ChatError): validate_sql(sql)
        for sql in QUERIES.values(): self.assertEqual(validate_sql(sql.replace(' ', '\n')), sql)

    def test_sql_scoped_to_current_conversation_and_demo_profile(self):
        self.submit('First fictional message')
        other_id = str(uuid4())
        self.client.put(f'/api/conversations/{other_id}/messages/{uuid4()}', json={'content': 'Other conversation'})
        records = retrieve(self.path, QUERIES['messages'], self.conversation)
        self.assertNotIn('Other conversation', json.dumps(records))
        with closing(self.repo.connect()) as db, db:
            db.execute("INSERT INTO demo_profiles VALUES ('other', 1)")
            db.execute("INSERT INTO preferences VALUES ('other', 'motion', 0, 'large')")
        self.assertEqual(retrieve(self.path, QUERIES['preferences'], self.conversation), [])
        self.assertEqual(len(records), 2)

    def test_storage_unavailable_and_unknown_conversation(self):
        self.assertEqual(self.client.get(f'/api/conversations/{uuid4()}').status_code, 404)
        for query in ('limit=101', 'offset=-1'):
            self.assertEqual(self.client.get(f'/api/conversations?{query}').status_code, 422)
        with TestClient(create_app(Path(self.temp.name), Settings())) as broken:
            self.assertEqual(broken.put(self.url, json={'content': 'Fictional'}).status_code, 503)


class ProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_wire_schema_uses_bounded_structured_output_no_secrets_in_input(self):
        calls = []
        def handler(request):
            body = json.loads(request.content)
            calls.append(body)
            self.assertFalse(body['store'])
            self.assertTrue(body['text']['format']['strict'])
            self.assertNotIn('fictional-key', body['input'])
            payload = {'sql': QUERIES['sessions']} if len(calls) == 1 else {'content': 'No matching records.', 'record_ids': []}
            return httpx.Response(200, json={'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': json.dumps(payload)}]}]})
        provider = OpenAIProvider(Settings('openai', 'fictional-key', 'test-only'), httpx.MockTransport(handler))
        self.assertEqual(await provider.propose('Last session?'), QUERIES['sessions'])
        self.assertEqual((await provider.answer('Last session?', [])).record_ids, [])
        self.assertIn('schema_and_meanings', json.loads(calls[0]['input']))
        self.assertNotIn('selected_records', json.loads(calls[0]['input']))
        self.assertIn('selected_records', json.loads(calls[1]['input']))

    async def test_http_timeout_malformed_refusal_incomplete_and_oversize_fail(self):
        responses = [httpx.Response(401, text='fictional-secret-error'), httpx.Response(200, text='bad JSON'),
                     httpx.Response(200, json={'status': 'incomplete'}),
                     httpx.Response(200, json={'status': 'completed', 'output': []}),
                     httpx.Response(200, content=b'x' * 100001)]
        for response in responses:
            provider = OpenAIProvider(Settings('openai', 'fictional-key', 'test-only'), httpx.MockTransport(lambda req: response))
            with self.assertRaises(ChatError) as error:
                await provider.propose('Fictional')
            self.assertNotIn('secret', error.exception.message)
        def timeout(req): raise httpx.ReadTimeout('fictional timeout')
        provider = OpenAIProvider(Settings('openai', 'fictional-key', 'test-only'), httpx.MockTransport(timeout))
        with self.assertRaises(ChatError): await provider.propose('Fictional')

    async def test_env_loader_is_explicit_and_never_evaluates_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / '.env'
            path.write_text('PROVIDER_MODE=openai\nOPENAI_API_KEY="fictional-secret"\nOPENAI_MODEL=example\nDEMO_SESSION_ID=$(not-executed)\n')
            settings = load_settings(path)
            self.assertTrue(settings.configured)
            self.assertEqual(settings.demo_session, '$(not-executed)')
            self.assertNotIn('fictional-secret', repr(settings))
