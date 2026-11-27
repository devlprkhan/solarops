from fastapi.testclient import TestClient

from solarops_api.main import app


def test_model_info():
    with TestClient(app) as client:
        response = client.get("/model/info")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == "v3"
        assert "poa_irradiance_o_149574" in data["features"]
        assert data["metrics"]["MAE"] > 0