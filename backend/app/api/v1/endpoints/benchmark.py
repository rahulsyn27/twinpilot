from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.benchmark.datasets import DATASETS, get_dataset
from app.benchmark.evaluator import evaluate_fixed_testset
from app.benchmark.plugins.registry import create_plugin, list_plugins
from app.core.config import settings
from app.schemas.benchmark import BenchmarkRunRequest, BenchmarkRunResponse

router = APIRouter(prefix="/benchmark", tags=["Benchmark"])

RUNS: list[BenchmarkRunResponse] = []


@router.get("/plugins")
async def plugins() -> list[dict[str, object]]:
    return list_plugins()


@router.get("/datasets")
async def datasets() -> list[dict[str, object]]:
    return list(DATASETS.values())


@router.get("/runs", response_model=list[BenchmarkRunResponse])
async def runs() -> list[BenchmarkRunResponse]:
    return RUNS


@router.post("/runs", response_model=BenchmarkRunResponse)
async def run_benchmark(request: BenchmarkRunRequest) -> BenchmarkRunResponse:
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY is required to run a benchmark.")
    try:
        corpus, tests = get_dataset(request.dataset_id)
        plugin = create_plugin(request.plugin_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown benchmark resource: {exc.args[0]}") from exc

    try:
        plugin.build(corpus, {"top_k": request.top_k})
        result = evaluate_fixed_testset(plugin.answer, tests)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    run = BenchmarkRunResponse(
        id=str(uuid4()), plugin_id=request.plugin_id, dataset_id=request.dataset_id, status="completed",
        result={"created_at": datetime.now(UTC).isoformat(), **result},
    )
    RUNS.insert(0, run)
    return run
