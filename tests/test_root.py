"""
Tests for the root endpoint (GET /).
"""

import pytest


class TestRoot:
    """Tests for the root endpoint."""

    def test_root_redirect(self, client):
        """Verify GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_follows(self, client):
        """Verify following redirect from / leads to index.html."""
        response = client.get("/", follow_redirects=True)
        # The static file mount returns 200
        assert response.status_code == 200
