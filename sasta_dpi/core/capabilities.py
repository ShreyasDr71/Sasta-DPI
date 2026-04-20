import platform
import os
import ctypes

def is_admin() -> bool:
    """Check if the script is running with administrative privileges."""
    try:
        # Windows
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        # Unix/Linux/Mac
        elif os.name == 'posix':
            return os.getuid() == 0
        return False
    except Exception:
        return False

def can_use_raw_sockets() -> bool:
    """Check if raw sockets can be created (requires admin/root)."""
    # Simply mapping this to admin privileges for now as it's the 
    # most reliable cross-platform indicator before instantiation
    return is_admin()

def get_system_capabilities() -> dict:
    admin = is_admin()
    return {
        "is_admin": admin,
        "raw_sockets": admin,
        "os": platform.system(),
        "release": platform.release(),
    }
