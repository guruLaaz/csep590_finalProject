from draft import Draft, DraftConfig


class LiveAuctionDraft(Draft):
    def __init__(self, config: DraftConfig):
        super().__init__(config)
