import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
  user = User(username=username, email=email)
  db.session.add(user)
  db.session.commit()
  return user


class TestUserService(BaseTestCase):
  """Test for the Users Service."""

  def test_users(self):
    """Ensure the /ping route behaves correctly."""
    response = self.client.get('/users/ping')
    data = json.loads(response.data.decode())
    self.assertEqual(response.status_code, 200)
    self.assertIn('pong!', data['message'])
    self.assertIn('success', data['status'])

  def test_add_user(self):
    with self.client:
      response = self.client.post(
        '/users',
        data=json.dumps({
          'username': 'michael',
          'email': 'test@test.com'
        }),
        content_type='application/json',
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 201)
      self.assertIn('test@test.com was added!', data['message'])
      self.assertIn('success', data['status'])

  def test_add_user_invalid_json(self):
    with self.client:
      response = self.client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 400)
      self.assertIn('Invalid payload.', data['message'])
      self.assertIn('fail', data['status'])

  def test_add_user_duplicate_email(self):
    with self.client:
      response = self.client.post(
        '/users',
        data=json.dumps({
          'username': 'michael',
          'email': 'test@test.com'
        }),
        content_type='application/json',
      )
      response = self.client.post(
        '/users',
        data=json.dumps({
          'username': 'michael',
          'email': 'test@test.com'
        }),
        content_type='application/json',
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 400)
      self.assertIn('Sorry. That email already exists.', data['message'])
      self.assertIn('fail', data['status'])

  def test_single_user(self):
    user = add_user('michael', 'test@test.com')
    with self.client:
      response = self.client.get(f'/users/{user.id}')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 200)
      self.assertIn('michael', data['data']['username'])
      self.assertIn('test@test.com', data['data']['email'])
      self.assertIn('success', data['status'])

  def test_single_user_no_id(self):
    with self.client:
      response = self.client.get(f'/users/blah')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 404)
      self.assertIn('User does not exist', data['message'])
      self.assertIn('fail', data['status'])

  def test_single_user_incorrect_id(self):
    with self.client:
      response = self.client.get(f'/users/999')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 404)
      self.assertIn('User does not exist', data['message'])
      self.assertIn('fail', data['status'])

  def test_all_users(self):
    add_user('michael', 'test@test.com')
    add_user('fletcher', 'test1@test.com')
    with self.client:
      response = self.client.get('/users')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 200)
      self.assertEqual(len(data['data']['users']), 2)
      self.assertIn('michael', data['data']['users'][0]['username'])
      self.assertIn('test@test.com', data['data']['users'][0]['email'])
      self.assertIn('fletcher', data['data']['users'][1]['username'])
      self.assertIn('test1@test.com', data['data']['users'][1]['email'])
      self.assertIn('success', data['status'])

  def test_main_no_users(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'<h1>All Users</h1>', response.data)
    self.assertIn(b'<p>No users!</p>', response.data)

  def test_main_with_users(self):
    add_user('michael', 'michael@test.com')
    add_user('fletcher', 'fletcher@test.com')
    with self.client:
      response = self.client.get('/')
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'<h1>All Users</h1>', response.data)
      self.assertNotIn(b'<p>No users!</p>', response.data)
      self.assertIn(b'michael', response.data)
      self.assertIn(b'fletcher', response.data)

  def test_main_add_user(self):
    with self.client:
      response = self.client.post(
        '/',
        data=dict(username='michael', email='michael@test.com'),
        follow_redirects=True
      )
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'<h1>All Users</h1>', response.data)
      self.assertNotIn(b'<p>No users!</p>', response.data)
      self.assertIn(b'michael', response.data)


if __name__ == '__main__':
  unittest.main()
