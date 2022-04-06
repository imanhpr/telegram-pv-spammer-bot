import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ReportNameGenerator:
    name: str
    PATTERN: str = field(default="{name}-{date}.csv", init=False, repr=False)

    @property
    def full_name(self) -> str:
        return self.PATTERN.format(
            name=self.name,
            date=datetime.now().replace(microsecond=0).isoformat(),
        )


def write_csv_report(
    file_name: str, fieldnames: list[str], data: Iterable[dict]
) -> tuple[str, str]:
    name = ReportNameGenerator(file_name)
    path = Path(name.full_name)
    with path.open("w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return name.full_name, path.absolute()
