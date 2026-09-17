import os
from pathlib import Path


DEFAULT_PACK: str = "src/view/assets/default_texture_pack/"


class Texture_pack:

    def __init__(self, pack_path: str = DEFAULT_PACK) -> None:

        self.folders_needed: list[str] = [
            "pac-man_sprites",
            "ghosts_sprites",
            "collectibles_sprites"
        ]
        self.textures_needed: list[str] = [
            "pac-man_up",
            "pac-man_down",
            "pac-man_right",
            "pac-man_left",
            "pac-man_death",
            "blinky_right",
            "blinky_left",
            "blinky_up",
            "blinky_down",
            "pinky_right",
            "pinky_left",
            "pinky_up",
            "pinky_down",
            "inky_right",
            "inky_left",
            "inky_up",
            "inky_down",
            "clyde_right",
            "clyde_left",
            "clyde_up",
            "clyde_down",
            "eyes_up",
            "eyes_down",
            "eyes_right",
            "eyes_left",
            "afraid_blue",
            "afraid_white",
            "apple",
            "strawberry",
            "orange",
            "cherry",
            "melon",
            "galaxian",
            "bell",
            "key",
            "pellet",
            "power_pellet"
        ]
        self._load_pack(pack_path)

    def _load_pack(self, pack_path: str) -> None:

        folders = {
            f.name: f.path for f in os.scandir(pack_path)
            if f.is_dir() and f.name in self.folders_needed
        }

        self.all_textures: dict = {}
        for folder in folders.values():
            self.all_textures.update({
                t.name.split(".")[0]: t.path
                for t in os.scandir(folder)
                if t.is_file() and t.name.split(".")[0] in self.textures_needed
            })

        textures_missing: list = [
            missing_text for missing_text in self.textures_needed
            if missing_text not in self.all_textures.keys()
        ]

        if not textures_missing:
            return

        self.get_missing_textures(textures_missing)

    def get_missing_textures(self, textures_missing: list[str]) -> None:

        for mis_text in textures_missing:

            self.all_textures[mis_text] = Path(DEFAULT_PACK).rglob(mis_text)

    def get_texture(self, texture_name: str) -> str:

        if texture_name not in self.all_textures:
            raise ValueError(f"Missing texture {texture_name} in texture pack")

        return str(self.all_textures[texture_name])
