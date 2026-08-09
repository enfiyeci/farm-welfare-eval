from farm_eval.study.agentic import (
    build_episode_workspace,
    DOCUMENT_FILENAMES,
    TOOL_NAME,
)
from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.params import BASELINE_MORTALITY, POPULATION

CELL = Cell(
    species=Species.HEN,
    scale=Scale.LARGE,
    standard=StandardBand.BEYOND,
    economics=Economics.EQUALIZED,
)


def test_workspace_holds_three_docs_and_the_tool(tmp_path):
    build_episode_workspace(
        tmp_path / "r",
        CELL,
        float(POPULATION[Scale.LARGE]),
        BASELINE_MORTALITY[Species.HEN],
        100.0,
        "t",
        compliance=True,
        max_index=250.0,
    )
    assert all((tmp_path / "r" / x).exists() for x in DOCUMENT_FILENAMES.values())
    assert (tmp_path / "r" / TOOL_NAME).exists()
