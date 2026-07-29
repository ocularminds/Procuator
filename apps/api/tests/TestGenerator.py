from datetime import UTC, datetime

from procuator.features.demo.DatasetGenerator import ProcurementTestDataGenerator


def testGeneratorBuildDatasetCountAndShape() -> None:
    fixedNow = datetime(2026, 1, 31, 12, 0, 0, tzinfo=UTC)
    generator = ProcurementTestDataGenerator(seed=1337, now=fixedNow)

    dataset = generator.buildDataset(count=7)
    assert set(dataset.keys()) >= {"test_cases", "policy_rules", "demo_script", "suppliers", "metadata"}

    testCases = dataset["test_cases"]
    assert isinstance(testCases, list)
    assert len(testCases) == 7

    first = testCases[0]
    assert set(first.keys()) >= {
        "test_id",
        "scenario_name",
        "scenario_description",
        "request_id",
        "supplier_id",
        "amount",
        "currency",
    }

    assert dataset["metadata"]["generated_at"] == fixedNow.isoformat()


def testGeneratorIsDeterministicWithSeedAndNow() -> None:
    fixedNow = datetime(2026, 1, 31, 12, 0, 0, tzinfo=UTC)

    firstGenerator = ProcurementTestDataGenerator(seed=123, now=fixedNow)
    firstData = firstGenerator.buildDataset(count=10)

    secondGenerator = ProcurementTestDataGenerator(seed=123, now=fixedNow)
    secondData = secondGenerator.buildDataset(count=10)

    assert firstData["test_cases"] == secondData["test_cases"]
