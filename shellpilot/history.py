from pathlib import Path
# from shellpilot.decorators import log_action

class BashHistory:
    HISTORY_FILES = [
        Path.home() / '.bash_history',
        Path.home() / '.zsh_history'
    ]
    
    @staticmethod
    def get_history_paths() -> list[str]:
        return  BashHistory.HISTORY_FILES
    @staticmethod
    def _read_history_file(path:Path) -> list[str]:
        
        if not path.exists():
            return []
        try:
            return path.read_text(encoding="utf-8",errors="ignore").splitlines()
        except Exception as e:
            print(f"Could not read {path} : {e}")
            return []
        
    @classmethod
    def load_all_commands(cls) -> list[str]:
        commands = []
        for path in cls.HISTORY_FILES:
            commands.extend(cls._read_history_file(path))
        return [cmd.strip() for cmd in commands if cmd.strip()]
    
    
    @classmethod
    def get_most_used_commands(cls, top_n: int = 10) -> dict[str, int]:
        """
        Return a dictionary of the top N most frequently used base commands
        using a manual frequency counter (not collections.Counter).
        """
        frequency_map: dict[str, int] = {}
        for line in cls.load_all_commands():
            parts = line.strip().split()
            if not parts:
                continue
            base = parts[0]
            if base in frequency_map:
                frequency_map[base] += 1
            else:
                frequency_map[base] = 1

        # Sort and slice the top N
        sorted_freq = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_freq[:top_n])

    @classmethod
    def search_commands(cls, keyword: str) -> list[str]:
        """Search all history for commands containing the given keyword."""
        return [cmd for cmd in cls.load_all_commands() if keyword.lower() in cmd.lower()]

    @classmethod
    def get_unique_commands(cls) -> list[str]:
        """Get sorted list of unique full command strings."""
        return sorted(set(cls.load_all_commands()))

    @classmethod
    def filter_by_prefix(cls, prefix: str) -> list[str]:
        """Filter history commands that start with a given prefix."""
        return [cmd for cmd in cls.load_all_commands() if cmd.startswith(prefix)]

    @classmethod
    def group_by_command(cls) -> dict[str, list[str]]:
        """Group full command lines by the base command."""
        grouped: dict[str, list[str]] = {}
        for cmd in cls.load_all_commands():
            parts = cmd.strip().split()
            if not parts:
                continue
            base = parts[0]
            grouped.setdefault(base, []).append(cmd)
        return grouped
        
    
    
    
if __name__ == "__main__":
    History_log = BashHistory() 
    
    function_name = input("Enter the function name to call :")
    print(getattr(History_log,function_name)())
    # print(History_log.function_name())