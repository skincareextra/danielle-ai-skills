import json
import unittest
from pathlib import Path


class ContractConsumer:
    def __init__(self, auth_contract: dict, data_contract: dict) -> None:
        self.auth_contract = auth_contract
        self.data_contract = data_contract

    def can_bootstrap(self) -> bool:
        auth_ops = {op["name"] for op in self.auth_contract["public_operations"]}
        data_ops = {op["name"] for op in self.data_contract["public_operations"]}
        required_auth = {"authenticate", "authorize"}
        required_data = {"get_repository", "run_query"}
        return required_auth.issubset(auth_ops) and required_data.issubset(data_ops)

    def build_authenticate_payload(self, email: str, password: str, client_id: str) -> dict:
        return {"email": email, "password": password, "client_id": client_id}

    def build_query_payload(self, query_name: str, params: dict) -> dict:
        return {"query_name": query_name, "params": params}


class TestCoreContractIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        auth_path = repo_root / "core" / "auth-engine" / "contract.json"
        data_path = repo_root / "core" / "data-engine" / "contract.json"
        with auth_path.open("r", encoding="utf-8") as f:
            cls.auth_contract = json.load(f)
        with data_path.open("r", encoding="utf-8") as f:
            cls.data_contract = json.load(f)
        cls.consumer = ContractConsumer(cls.auth_contract, cls.data_contract)

    def test_contract_versions_are_declared(self) -> None:
        self.assertEqual(self.auth_contract["contract_version"], "1.0.0")
        self.assertEqual(self.data_contract["contract_version"], "1.0.0")

    def test_ok_lets_work_can_bootstrap_against_core_contracts(self) -> None:
        self.assertTrue(self.consumer.can_bootstrap())

    def test_payload_shapes_match_required_fields(self) -> None:
        auth_payload = self.consumer.build_authenticate_payload(
            email="owner@okletswork.test",
            password="super-secret-pass",
            client_id="ok-lets-work-web",
        )
        self.assertSetEqual(set(auth_payload.keys()), {"email", "password", "client_id"})

        query_payload = self.consumer.build_query_payload(
            query_name="tasks.list_by_owner",
            params={"owner_id": "user_123"},
        )
        self.assertSetEqual(set(query_payload.keys()), {"query_name", "params"})


if __name__ == "__main__":
    unittest.main()
