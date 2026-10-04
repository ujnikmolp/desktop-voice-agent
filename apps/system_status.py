"""系统状态查询工具"""
import psutil


def get_system_status() -> str:
    """获取 CPU、内存、磁盘使用率"""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:/")

    mem_used = mem.used // (1024 ** 3)
    mem_total = mem.total // (1024 ** 3)
    disk_used = disk.used // (1024 ** 3)
    disk_total = disk.total // (1024 ** 3)

    return (
        f"CPU 使用率 {cpu}%，"
        f"内存 {mem.percent}%（{mem_used}GB / {mem_total}GB），"
        f"C 盘 {disk.percent}%（{disk_used}GB / {disk_total}GB）"
    )


def get_battery_status() -> str:
    """获取电池状态（笔记本才有效）"""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "此设备没有电池（台式机）"
        plugged = "充电中" if battery.power_plugged else "使用电池"
        return f"电量 {battery.percent}%，{plugged}"
    except Exception as e:
        return f"查询电池失败：{e}"