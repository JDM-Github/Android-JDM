import json

class JDMConfig:
    
    __original_config = {
        'display_fps' : False,
        'root_clock' : False,
    }
    
    @staticmethod
    def __get_original_config(name: str): return JDMConfig.__original_config.get(name)

    @staticmethod
    def __change_config(name: str, value: any) -> None:
        if name in JDMConfig.__get_all_config_name():
            with open(f"jsons/config.json") as f:
                config = json.load(f)
            config[name] = value
            with open(f"jsons/config.json", "w") as f:
                json.dump(config, f, indent=2)

    @staticmethod
    def reset(name: str): JDMConfig.__change_config(name, JDMConfig.__get_original_config(name))
    @staticmethod
    def reset_all():
        with open(f"jdm_kivy/config.json", "w") as f:
            json.dump(JDMConfig.__original_config, f, indent=2)
    
    @staticmethod
    def get_all_config_name() -> list:
        __new_list = list()
        for elements in JDMConfig.__original_config:
            __new_list.append(elements)
        return __new_list

    @staticmethod
    def __get_all_config_name() -> list:
        return [ __elements for __elements in JDMConfig.__original_config ]

    @staticmethod
    def set(name: str, value: any): JDMConfig.__change_config(name, value)

    @staticmethod
    def activate_root_clock(): JDMConfig.__change_config("root_clock", True)
    @staticmethod
    def deactivate_root_clock(): JDMConfig.__change_config("root_clock", False)
    @staticmethod
    def activate_display_fps(): JDMConfig.__change_config("display_fps", True)
    @staticmethod
    def deactivate_display_fpsk(): JDMConfig.__change_config("display_fps", False)
