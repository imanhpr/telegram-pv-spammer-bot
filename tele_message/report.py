from dataclasses import dataclass, field
from datetime import datetime


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
