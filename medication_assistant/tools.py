from datetime import datetime
from medication_assistant.storage import load_data, save_data

ALLOWED_STATUSES = {"taken", "missed", "skipped"}


def add_medication(name: str, dosage: str, times: list[str], instructions: str = ""):
    if not name or not dosage or not times:
        return {"success": False, "message": "Name, dosage, and times are required."}

    clean_name = name.strip()
    clean_dosage = dosage.strip()
    clean_times = [t.strip() for t in times if t.strip()]
    clean_instructions = instructions.strip()

    if not clean_times:
        return {"success": False, "message": "At least one valid time is required."}

    normalized_times = sorted(clean_times)
    data = load_data()

    for med in data["medications"]:
        existing_name = med.get("name", "").strip().lower()
        existing_dosage = med.get("dosage", "").strip().lower()
        existing_times = sorted([t.strip() for t in med.get("times", [])])

        if (
            existing_name == clean_name.lower()
            and existing_dosage == clean_dosage.lower()
            and existing_times == normalized_times
        ):
            return {
                "success": False,
                "message": f"{clean_name} {clean_dosage} is already in your medication list."
            }

    medication = {
        "name": clean_name,
        "dosage": clean_dosage,
        "times": normalized_times,
        "instructions": clean_instructions
    }

    data["medications"].append(medication)
    save_data(data)

    return {
        "success": True,
        "message": f"Added medication: {clean_name}",
        "medication": medication
    }


def get_today_schedule(date: str = None):
    data = load_data()
    schedule_date = date or datetime.now().strftime("%Y-%m-%d")

    schedule = []
    for med in data["medications"]:
        for med_time in med["times"]:
            schedule.append({
                "date": schedule_date,
                "name": med["name"],
                "dosage": med["dosage"],
                "time": med_time,
                "instructions": med.get("instructions", "")
            })

    schedule = sorted(schedule, key=lambda x: x["time"])

    return {
        "success": True,
        "date": schedule_date,
        "schedule": schedule
    }


def get_today_status(date: str = None):
    data = load_data()
    today = date or datetime.now().strftime("%Y-%m-%d")

    schedule = []
    for med in data["medications"]:
        for med_time in med["times"]:
            schedule.append({
                "date": today,
                "name": med["name"],
                "dosage": med["dosage"],
                "time": med_time,
                "instructions": med.get("instructions", "")
            })

    schedule = sorted(schedule, key=lambda x: x["time"])

    today_logs = [
        log for log in data["dose_logs"]
        if log.get("date") == today
    ]

    logged_map = {}
    for log in today_logs:
        key = (log.get("name", "").strip().lower(), log.get("time", "").strip())
        logged_map[key] = log.get("status", "").strip().lower()

    logged_so_far = []
    still_remaining = []

    for item in schedule:
        key = (item["name"].strip().lower(), item["time"].strip())
        if key in logged_map:
            logged_so_far.append({
                "name": item["name"],
                "dosage": item["dosage"],
                "time": item["time"],
                "status": logged_map[key]
            })
        else:
            still_remaining.append({
                "name": item["name"],
                "dosage": item["dosage"],
                "time": item["time"]
            })

    return {
        "success": True,
        "date": today,
        "today_medications": schedule,
        "logged_so_far": logged_so_far,
        "still_remaining": still_remaining
    }


def log_dose(name: str, time: str, status: str):
    if not name or not time or not status:
        return {"success": False, "message": "Name, time, and status are required."}

    clean_name = name.strip()
    clean_time = time.strip()
    clean_status = status.strip().lower()

    if clean_status not in ALLOWED_STATUSES:
        return {
            "success": False,
            "message": f"Invalid status. Allowed values: {', '.join(ALLOWED_STATUSES)}"
        }

    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    for log in data["dose_logs"]:
        existing_name = log.get("name", "").strip().lower()
        existing_time = log.get("time", "").strip()
        existing_status = log.get("status", "").strip().lower()
        existing_date = log.get("date", "")

        if (
            existing_name == clean_name.lower()
            and existing_time == clean_time
            and existing_status == clean_status
            and existing_date == today
        ):
            return {
                "success": False,
                "message": f"{clean_name} at {clean_time} is already logged as {clean_status} today."
            }

    log_entry = {
        "name": clean_name,
        "time": clean_time,
        "status": clean_status,
        "date": today
    }

    data["dose_logs"].append(log_entry)
    save_data(data)

    return {
        "success": True,
        "message": f"Logged {clean_status} for {clean_name} at {clean_time}.",
        "log_entry": log_entry
    }


def get_adherence_summary(days: int = 7):
    data = load_data()
    logs = data["dose_logs"]

    taken = sum(1 for log in logs if log["status"] == "taken")
    missed = sum(1 for log in logs if log["status"] == "missed")
    skipped = sum(1 for log in logs if log["status"] == "skipped")

    return {
        "success": True,
        "days": days,
        "summary": {
            "taken": taken,
            "missed": missed,
            "skipped": skipped,
            "total_logs": len(logs)
        }
    }