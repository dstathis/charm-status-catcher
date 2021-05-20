from ops.model import MaintenanceStatus, BlockedStatus, WaitingStatus


class DeferEventError(Exception):
    def __init__(self, event, reason):
        super().__init__()
        self.event = event
        self.reason = reason


class BlockedStatusError(Exception):
    pass


class WaitingStatusError(Exception):
    pass


def status_catcher(func):
    @functools.wraps(func)
    def new_func(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except DeferEventError as e:
            logger.info("Defering event: %s because: %s", str(e.event), e.reason)
            self.unit.status = MaintenanceStatus()
            e.event.defer()
        except BlockedStatusError as e:
            self.unit.status = BlockedStatus(str(e))
        except WaitingStatusError as e:
            self.unit.status = WaitingStatus(str(e))

    return new_func
