from datetime import UTC, datetime

from procuator.data.generator import ProcurementTestDataGenerator


def test_generator_build_dataset_count_and_shape() -> None:
    fixed_now = datetime(2026, 1, 31, 12, 0, 0, tzinfo=UTC)
    gen = ProcurementTestDataGenerator(seed=1337, now=fixed_now)

    dataset = gen.build_dataset(count=7)
    assert set(dataset.keys()) >= {"test_cases", "policy_rules", "demo_script", "suppliers", "metadata"}

    test_cases = dataset["test_cases"]
    assert isinstance(test_cases, list)
    assert len(test_cases) == 7

    first = test_cases[0]
    assert set(first.keys()) >= {
        "test_id",
        "scenario_name",
        "scenario_description",
        "request_id",
        "supplier_id",
        "amount",
        "currency",
    }

    assert dataset["metadata"]["generated_at"] == fixed_now.isoformat()


def test_generator_is_deterministic_with_seed_and_now() -> None:
    fixed_now = datetime(2026, 1, 31, 12, 0, 0, tzinfo=UTC)

    gen1 = ProcurementTestDataGenerator(seed=123, now=fixed_now)
    data1 = gen1.build_dataset(count=10)

    gen2 = ProcurementTestDataGenerator(seed=123, now=fixed_now)
    data2 = gen2.build_dataset(count=10)

    assert data1["test_cases"] == data2["test_cases"]
