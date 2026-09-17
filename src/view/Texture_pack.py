class Texture_pack:
    def __init__(self, pack_path: str = DEFAULT_PACK) -> None:

        self._load_pack(pack_path)

    @staticmethod
    def check_missing_textures(pack_path: str) -> bool:

        folders_needed: list[str] = [
            "pac-man_textures",
            "ghosts_textures",
            "fruits_textures"
        ]
        textures_needed: list[str] = [
            "pac-man_closed",
            "pac-man_open",
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
            "apple",
            "strawberry",
            "orange",
            "cherry",
            "melon",
            "galaxian",
            "bell",
            "key"
        ]
        folders = {f.name: f.path for f in os.scandir(pack_path) if f.is_dir()}

        if not folders or folders != folders_needed:
            return False

        self.all_textures = {texture_name: "" for texture_name in textures_needed}
        for folder in folders.values():
            textures_found += rglob.find(folder, ".png", "jpg")

        if textures_found != textures_needed:
            return False



    def _load_pack(self, pack_path: str) -> None:

        folders = {f.name: f.path for f in os.scandir(pack_path) if f.is_dir()}

        self.pac_man: Pacman_text = Pacman_text(folders["pac-man_textures"])

        ghosts_files = 
        self.blinky: Ghost_text = Ghost_text(folders["ghosts_textures"])
        self.textures: dict[str, str] = {
            image_path for image_path in [
                "pac-man_closed",
                "pac-man_open",
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
                "apple",
                "strawberry",
                "orange",
                "cherry",
                "melon",
                "galaxian",
                "bell",
                "key"
                }
