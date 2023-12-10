import urllib.request

import bchdesktopwallet.settings


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def get_img_bch_logo():
        logo_dir = bchdesktopwallet.settings.data_dir / "img"
        logo_name = "240px-Bitcoin_Cash.png"
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Bitcoin_Cash.png/240px-Bitcoin_Cash.png"

        # Download if not exist locally
        if not (logo_dir / logo_name).exists():
            logo_dir.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(logo_url, logo_dir / logo_name)

        return logo_dir / logo_name
