"""Prove fixed application behavior independently of live-model wording."""
import unittest
from uuid import uuid4
from app.reply_policy import reviewed_reply
from app.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient
from tests import test_chat as fixtures


class ReplyPolicyTests(unittest.TestCase):
    setUp = fixtures.ChatTests.setUp
    def test_crisis_and_pause_questions_bypass_failed_provider_and_replay_once(self):
        self.provider.fail_stage = 'query'
        for question, expected in [
            ('Fictional Alex says: I want to hurt myself.', 'Open Crisis support'),
            ('Was my last completed session paused?', 'cannot tell'),
            ('Was my last practice uninterrupted?', 'cannot tell'),
        ]:
            with self.subTest(question=question):
                url = f'/api/conversations/{uuid4()}/messages/{uuid4()}'
                response = self.client.put(url, json={'content': question})
                self.assertEqual(response.status_code, 200)
                body = response.json()
                self.assertEqual(body['provider_mode'], 'local')
                self.assertEqual(body['messages'][1]['retrieval_status'], 'not_requested')
                self.assertEqual(body['messages'][1]['record_ids'], [])
                self.assertIn(expected, body['messages'][1]['content'])
                self.assertEqual(self.client.put(url, json={'content': question}).json(), body)
        self.assertEqual(self.provider.calls, 0)

    def test_reviewed_reply_needs_no_live_configuration_or_budget(self):
        with TestClient(create_app(self.path, Settings(mode='openai'))) as client:
            response = client.put(self.url, json={'content': 'Fictional: I want to end my life.'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['provider_mode'], 'local')
            self.assertEqual(client.get('/api/health').json()['live_calls_reserved'], 0)

    def test_documented_phrase_limits_do_not_claim_detection(self):
        self.assertIsNone(reviewed_reply('Fictional: I cannot go on.'))
        self.assertIsNotNone(reviewed_reply('Fictional: I do not want to hurt myself.'))
        self.assertIsNone(reviewed_reply('How do I pause the exercise?'))
        self.assertIsNone(reviewed_reply('What happened in my last session?'))


if __name__ == '__main__':
    unittest.main()
