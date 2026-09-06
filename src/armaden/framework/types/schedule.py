from collections.abc import Awaitable, Callable, Mapping, Sequence
type ScheduleCallback = Callable[..., object | Awaitable[object]]
type ScheduleCommand = str | Sequence[str]
type ScheduleCondition = Callable[[], object | Awaitable[object]]
type ScheduleConfiguration = Mapping[str, object]
type ScheduleHook = Callable[..., object | Awaitable[object]]
type ScheduleTag = str | type[object]
