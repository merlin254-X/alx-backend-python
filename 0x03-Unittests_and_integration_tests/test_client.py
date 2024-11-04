#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")   
    def test_org(self, org_name, expected_json, mock_get_json):
        # Configure the mock to return the expected JSON payload
        mock_get_json.return_value = expected_json

        # Instantiate GithubOrgClient and call the org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Check if the result matches the expected JSON
        self.assertEqual(result, expected_json)

        # Ensure get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
    
    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            # Set the return value for the mocked property
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/myorg/repos'}
            # Instantiate the client with an example organization name
            client = GithubOrgClient('myorg')
            # Check if _public_repos_url returns the correct repos_url
            self.assertEqual(client._public_repos_url, 'https://api.github.com/orgs/myorg/repos')

    @patch("client.get_json")

    def test_public_repos(self, mock_get_json):
        # Set up the mock payload and URL
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        mock_get_json.return_value = mock_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/myorg/repos"

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("myorg")

            # Call the public_repos method
            result = client.public_repos()

            # Check if the result matches the expected list of repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Verify the mocked property and get_json were called once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/myorg/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("myorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

class TestIntegrationGithubOrgClient(unittest.TestCase):
    @parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
    @classmethod
    def setUpClass(cls):
        """Set up the patcher for requests.get before any tests run."""
        cls.get_patcher = patch('requests.get')

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Configure the side_effect for mock_get based on the expected URLs
        cls.mock_get.side_effect = cls.get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests have run."""
        cls.get_patcher.stop()

    @staticmethod
    def get_json_side_effect(url):
        """Return different payloads based on the URL."""
        if "orgs" in url:
            return org_payload
        elif "repos" in url:
            return repos_payload
        return None

    def test_public_repos(self):
        """Test the public_repos method returns the correct list of repos."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method filters repos by license."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
