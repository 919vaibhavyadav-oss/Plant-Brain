"""Generate the synthetic document corpus for PlantBrain.

Creates a fictional plant — Bharat Ispat & Energy Ltd, Unit 2 (BIEL-2) — with
deliberately engineered patterns the intelligence layer should surface:
  * P-101 cooling water pump: recurring mechanical seal failures (~45 day cycle)
  * C-201 gas compressor: vibration trend that precedes two incidents
  * COB-1 coke oven battery: gas pressure excursions logged but never linked to permits
  * TR-501 transformer: overdue statutory inspection (compliance gap)
  * CV-401 conveyor: guard interlock bypass appearing in both a near-miss and an audit
"""
import csv
import os
import random
from datetime import date, timedelta

random.seed(42)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TODAY = date(2026, 7, 16)


def d(iso):
    return date.fromisoformat(iso)


# ---------------------------------------------------------------- equipment
EQUIPMENT = [
    # tag, name, type, area, criticality, oem, installed
    ("P-101", "Cooling Water Pump A", "Centrifugal Pump", "Power Plant", "High", "KSB Pumps", "2014-03-12"),
    ("P-102", "Cooling Water Pump B", "Centrifugal Pump", "Power Plant", "High", "KSB Pumps", "2014-03-12"),
    ("P-201", "Boiler Feed Pump", "Multistage Pump", "Power Plant", "Critical", "Flowserve", "2015-08-20"),
    ("C-201", "Coke Oven Gas Compressor", "Screw Compressor", "Coke Oven", "Critical", "Kirloskar", "2013-11-05"),
    ("C-202", "Instrument Air Compressor", "Reciprocating Compressor", "Utilities", "Medium", "Atlas Copco", "2018-02-14"),
    ("B-301", "Boiler No. 3", "Water Tube Boiler", "Power Plant", "Critical", "BHEL", "2012-06-30"),
    ("COB-1", "Coke Oven Battery 1", "Coke Oven Battery", "Coke Oven", "Critical", "SAIL Engg", "2010-01-15"),
    ("CV-401", "Coal Conveyor 401", "Belt Conveyor", "Material Handling", "High", "TRF Ltd", "2016-09-01"),
    ("CV-402", "Coke Conveyor 402", "Belt Conveyor", "Material Handling", "Medium", "TRF Ltd", "2016-09-01"),
    ("TR-501", "Main Power Transformer", "Oil-Filled Transformer", "Switchyard", "Critical", "CGL", "2011-04-22"),
    ("TR-502", "Auxiliary Transformer", "Oil-Filled Transformer", "Switchyard", "High", "CGL", "2013-07-18"),
    ("V-601", "Ammonia Storage Vessel", "Pressure Vessel", "By-Product Plant", "Critical", "L&T", "2012-12-01"),
    ("F-701", "ESP Fan", "Induced Draft Fan", "Power Plant", "High", "Howden", "2015-05-09"),
    ("GD-801", "CO Gas Detector Array - Battery Top", "Gas Detection System", "Coke Oven", "Critical", "Honeywell", "2019-10-11"),
    ("EOT-901", "EOT Crane 20T", "Overhead Crane", "Material Handling", "High", "Anupam", "2014-10-27"),
]

FAILURE_MODES = {
    "Centrifugal Pump": ["mechanical seal leak", "bearing overheating", "impeller wear", "coupling misalignment"],
    "Multistage Pump": ["thrust bearing failure", "seal leak", "cavitation damage"],
    "Screw Compressor": ["high vibration", "rotor bearing wear", "oil carryover", "discharge temperature high"],
    "Reciprocating Compressor": ["valve plate failure", "piston ring wear"],
    "Water Tube Boiler": ["tube leak", "burner flame instability", "refractory damage"],
    "Coke Oven Battery": ["door seal leakage", "gas pressure excursion", "refractory spalling"],
    "Belt Conveyor": ["belt tracking fault", "idler bearing seizure", "pull cord switch fault", "guard interlock fault"],
    "Oil-Filled Transformer": ["oil leak", "buchholz alarm", "high dissolved gas reading"],
    "Pressure Vessel": ["relief valve passing", "flange gasket weep"],
    "Induced Draft Fan": ["impeller imbalance", "bearing vibration"],
    "Gas Detection System": ["sensor drift", "calibration overdue"],
    "Overhead Crane": ["brake lining wear", "limit switch failure", "wire rope wear"],
}

TECHS = ["R. Sharma", "V. Patil", "S. Iyer", "A. Khan", "M. Reddy", "D. Bose", "K. Nair", "P. Singh"]


def gen_work_orders():
    rows = []
    wo_no = 24000
    # Engineered pattern: P-101 seal fails roughly every 45 days
    seal_dates = []
    cur = d("2025-01-08")
    while cur < TODAY:
        seal_dates.append(cur)
        cur += timedelta(days=random.randint(40, 52))
    for dt in seal_dates:
        wo_no += 1
        rows.append([f"WO-{wo_no}", "P-101", dt.isoformat(), "Corrective",
                     "Mechanical seal leak observed at gland; seal replaced with OEM cartridge seal. "
                     "Shaft sleeve scoring noted again — same as previous replacements.",
                     random.choice(TECHS), round(random.uniform(6, 14), 1), "Cartridge seal SK-CS-40"])
    # Engineered pattern: C-201 vibration climbing before the March 2026 incident
    for dt, desc in [
        ("2026-01-19", "High vibration alarm on DE bearing (6.8 mm/s). Trimmed balance, alarm cleared."),
        ("2026-02-16", "Vibration recurring at 7.9 mm/s on DE bearing. Bearing clearance at limit; replacement recommended at next opportunity."),
        ("2026-03-10", "Deferred bearing replacement — production priority. Vibration 9.2 mm/s, monitoring frequency increased."),
        ("2026-03-24", "EMERGENCY: DE bearing seizure and trip during operation. Rotor inspection, bearing replaced. 36 hr outage."),
    ]:
        wo_no += 1
        typ = "Emergency" if "EMERGENCY" in desc else "Corrective"
        rows.append([f"WO-{wo_no}", "C-201", dt, typ, desc, "V. Patil",
                     36.0 if typ == "Emergency" else round(random.uniform(4, 8), 1), "SKF 22320 bearing"])
    # Background corrective WOs across the fleet
    start = d("2024-07-01")
    for tag, name, etype, area, crit, oem, inst in EQUIPMENT:
        n = random.randint(4, 10)
        for _ in range(n):
            wo_no += 1
            dt = start + timedelta(days=random.randint(0, (TODAY - start).days))
            mode = random.choice(FAILURE_MODES[etype])
            rows.append([f"WO-{wo_no}", tag, dt.isoformat(), "Corrective",
                         f"{mode.capitalize()} reported by shift crew; rectified and tested OK.",
                         random.choice(TECHS), round(random.uniform(2, 12), 1), ""])
        # Preventive WOs quarterly
        cur = start
        while cur < TODAY:
            wo_no += 1
            rows.append([f"WO-{wo_no}", tag, cur.isoformat(), "Preventive",
                         f"Scheduled preventive maintenance as per PM plan for {name}.",
                         random.choice(TECHS), round(random.uniform(1, 4), 1), ""])
            cur += timedelta(days=random.randint(85, 95))
    rows.sort(key=lambda r: r[2])
    with open(os.path.join(BASE, "work_orders.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["wo_id", "equipment_tag", "date", "wo_type", "description", "technician", "downtime_hours", "parts_used"])
        w.writerows(rows)
    return len(rows)


def gen_inspections():
    rows = []
    insp_no = 5000
    plans = {
        # tag: (inspection type, frequency days, last done — TR-501 deliberately overdue)
        "B-301": ("Statutory boiler inspection (IBR)", 365, "2025-09-14"),
        "V-601": ("Pressure vessel thickness survey (PESO/SMPV)", 365, "2025-11-02"),
        "TR-501": ("Dissolved gas analysis + oil BDV test", 180, "2025-08-30"),  # OVERDUE
        "TR-502": ("Dissolved gas analysis + oil BDV test", 180, "2026-04-12"),
        "GD-801": ("Gas detector calibration (OISD-STD-163)", 90, "2026-02-08"),  # OVERDUE
        "EOT-901": ("Statutory crane load test (Factories Act S.29)", 365, "2026-01-25"),
        "CV-401": ("Conveyor guard & interlock audit", 180, "2026-05-20"),
        "CV-402": ("Conveyor guard & interlock audit", 180, "2025-12-10"),  # OVERDUE
        "COB-1": ("Battery door seal & gas leakage survey (OISD-STD-105)", 90, "2026-06-28"),
        "P-201": ("Vibration signature analysis", 90, "2026-05-30"),
        "C-201": ("Vibration signature analysis", 90, "2026-06-15"),
        "F-701": ("Vibration signature analysis", 90, "2026-04-02"),  # OVERDUE-ish
    }
    findings = ["No abnormality observed.", "Minor deviation noted, within acceptance limits.",
                "Deviation recorded; corrective work order raised.", "Satisfactory. Next due as per plan."]
    for tag, (itype, freq, last) in plans.items():
        # historical inspections leading up to `last`
        cur = d(last)
        hist = []
        for _ in range(3):
            hist.append(cur)
            cur -= timedelta(days=freq + random.randint(-10, 10))
        for dt in sorted(hist):
            insp_no += 1
            sev = random.choice(["OK", "OK", "Minor", "OK"])
            rows.append([f"INSP-{insp_no}", tag, dt.isoformat(), itype, random.choice(findings), sev, random.choice(TECHS)])
    # CV-401 special finding — connects to near-miss NM-2026-011
    insp_no += 1
    rows.append([f"INSP-{insp_no}", "CV-401", "2026-05-20", "Conveyor guard & interlock audit",
                 "Guard interlock on tail pulley found bridged with jumper wire. Jumper removed, "
                 "interlock function restored. Recommend awareness session — this is the second "
                 "such observation this year (see near-miss NM-2026-011).", "Major", "S. Iyer"])
    rows.sort(key=lambda r: r[2])
    with open(os.path.join(BASE, "inspections.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["inspection_id", "equipment_tag", "date", "inspection_type", "finding", "severity", "inspector"])
        w.writerows(rows)
    return len(rows)


def gen_equipment():
    with open(os.path.join(BASE, "equipment_master.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tag", "name", "equipment_type", "area", "criticality", "oem", "installed"])
        w.writerows(EQUIPMENT)
    return len(EQUIPMENT)


def gen_regulations():
    regs = [
        ["OISD-STD-105", "Work permit system for hot work, confined space entry and simultaneous operations in coke oven and gas handling areas.", "Coke Oven Battery|Gas Detection System", 90, "Gas leakage survey and permit audit"],
        ["OISD-STD-163", "Safety of control room and portable/fixed gas detection systems: calibration every 90 days with certified span gas.", "Gas Detection System", 90, "Gas detector calibration"],
        ["IBR-1950-Reg-391", "Indian Boiler Regulations: annual statutory inspection and hydraulic test of boilers by competent authority.", "Water Tube Boiler", 365, "Statutory boiler inspection"],
        ["FactoriesAct-S.28", "Factories Act 1948 Section 28: hoists and lifts to be thoroughly examined every 6 months.", "Overhead Crane", 180, "Hoist thorough examination"],
        ["FactoriesAct-S.29", "Factories Act 1948 Section 29: lifting machines — annual thorough examination and load test by competent person.", "Overhead Crane", 365, "Statutory crane load test"],
        ["FactoriesAct-S.21", "Factories Act 1948 Section 21: secure fencing of machinery — every dangerous part of machinery must be securely fenced; interlocked guards must not be defeated.", "Belt Conveyor", 180, "Conveyor guard & interlock audit"],
        ["PESO-SMPV-Rule-19", "SMPV (Unfired) Rules: periodic testing of pressure vessels storing compressed/liquefiable gas — annual external, 5-yearly hydro.", "Pressure Vessel", 365, "Pressure vessel thickness survey"],
        ["CEA-Reg-2010-R.30", "CEA (Measures relating to Safety and Electric Supply) Regulations: periodic condition monitoring of power transformers including DGA every 6 months for critical units.", "Oil-Filled Transformer", 180, "Dissolved gas analysis"],
        ["OISD-RP-124", "Predictive maintenance of rotating equipment: vibration monitoring of critical compressors and pumps at 90-day intervals.", "Screw Compressor|Centrifugal Pump|Multistage Pump|Induced Draft Fan", 90, "Vibration signature analysis"],
    ]
    with open(os.path.join(BASE, "regulations.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["clause_id", "requirement", "applies_to_types", "frequency_days", "evidence_inspection_type"])
        w.writerows(regs)
    return len(regs)


INCIDENTS = {
"INC-2026-003.md": """# Incident Report INC-2026-003 — C-201 Compressor Trip and Bearing Seizure

**Date:** 2026-03-24  |  **Area:** Coke Oven — Gas Handling  |  **Severity:** Level 3 (Major Equipment Damage)
**Equipment involved:** C-201 (Coke Oven Gas Compressor)

## Summary
At 02:40 hrs, C-201 tripped on high bearing temperature followed by audible seizure of the
drive-end bearing. Coke oven gas routing switched to flare, resulting in 36 hours of production
curtailment. No injuries.

## Sequence of Events
- Vibration on the DE bearing had been trending upward since January (see WO records dated
  2026-01-19 and 2026-02-16, which recommended bearing replacement).
- The replacement recommended in February was deferred on 2026-03-10 due to production priority.
- On 2026-03-24 the bearing seized in service.

## Root Cause
Deferred corrective maintenance on a known degrading bearing. The condition was detected two
months in advance, but the deferral decision was made without visibility of the vibration trend
or the OEM limit (Kirloskar manual: sustained vibration above 7.1 mm/s requires shutdown).

## Contributing Factors
- No mechanism linking condition-monitoring data to deferral approval workflow.
- Vibration reports stored in a separate system from work order history.

## Actions
1. Bearing replaced, rotor inspected — completed 2026-03-26.
2. Deferral of corrective work on Critical equipment now requires reliability engineer sign-off.
3. Recommendation: unified visibility of condition data at the point of deferral decision.
""",
"INC-2025-014.md": """# Incident Report INC-2025-014 — COB-1 Gas Pressure Excursion During Door Maintenance

**Date:** 2025-10-07  |  **Area:** Coke Oven Battery 1  |  **Severity:** Level 2 (Near-Miss, High Potential)
**Equipment involved:** COB-1 (Coke Oven Battery 1), GD-801 (CO Gas Detector Array)

## Summary
During oven door seal replacement on oven 23, collector main pressure rose from 7 mmWC to
19 mmWC over 40 minutes. CO detector GD-801 channel 4 alarmed at 108 ppm at the battery top
while a two-man crew was working under a valid maintenance permit. Crew evacuated; no exposure
injuries recorded.

## Sequence of Events
- A hot-work permit (PTW-2025-1873) and a door maintenance permit (PTW-2025-1875) were active
  simultaneously on adjacent ovens.
- Pressure excursion began after a charging sequence upstream; the control room saw the trend
  but was not aware maintenance crews were on the battery top.

## Root Cause
No linkage between the permit-to-work system and live process/gas-detection data. Each system
functioned correctly in isolation.

## Contributing Factors
- Permit register is paper-based; control room has no live view of active permits by location.
- GD-801 channel 4 had last been calibrated 2025-06-30 — outside the 90-day OISD-STD-163 window
  at the time of the event.

## Actions
1. Interim rule: battery-top permits now require control-room acknowledgement at issue.
2. Calibration schedule for GD-801 tightened; compliance to be tracked.
3. Recommendation: digital permit register cross-checked against live gas and process data.
""",
"NM-2026-011.md": """# Near-Miss Report NM-2026-011 — CV-401 Conveyor Started With Bridged Guard Interlock

**Date:** 2026-04-18  |  **Area:** Material Handling  |  **Severity:** Near-Miss (High Potential)
**Equipment involved:** CV-401 (Coal Conveyor 401)

## Summary
A cleaner working near the tail pulley of CV-401 noticed the conveyor start while the tail-end
guard was removed. He was outside the nip-point zone. Investigation found the guard interlock
had been bridged with a jumper wire, allowing start-up with the guard open.

## Root Cause
Guard interlock defeated to save time during recurring belt-tracking adjustments (see repeated
belt tracking fault work orders on CV-401). The interlock bypass was known informally to the
shift crew but never reported.

## Regulatory Reference
Factories Act 1948, Section 21 — secure fencing of machinery. Defeating an interlocked guard
is a statutory violation.

## Actions
1. Jumper removed; interlock tested.
2. Toolbox talk conducted for all material handling crews.
3. NOTE: The May 2026 conveyor audit (INSP series) found the interlock bridged AGAIN —
   this is a recurring behavioural pattern, not a one-off.
""",
"INC-2025-006.md": """# Incident Report INC-2025-006 — B-301 Boiler Tube Leak and Forced Outage

**Date:** 2025-05-12  |  **Area:** Power Plant  |  **Severity:** Level 2 (Forced Outage)
**Equipment involved:** B-301 (Boiler No. 3)

## Summary
Water wall tube leak detected in B-301 through abnormal make-up water consumption. Controlled
shutdown taken. Failed tube section showed long-term overheating creep damage near a previously
repaired area (2023 repair, documented only in a contractor PDF report not available to the
inspection team).

## Root Cause
Localized long-term overheating. The 2023 repair history was not visible to the planning team,
so the area was not included in the last thickness survey scope.

## Actions
1. Tube panel replaced; adjacent tubes UT-tested.
2. Recommendation: all repair records must be linked to the equipment record and searchable —
   fragmented history directly caused a missed inspection scope.
""",
"NM-2025-021.md": """# Near-Miss Report NM-2025-021 — TR-501 Buchholz Alarm With Stale Oil Test Data

**Date:** 2025-12-03  |  **Area:** Switchyard  |  **Severity:** Near-Miss
**Equipment involved:** TR-501 (Main Power Transformer)

## Summary
Buchholz gas-accumulation alarm on TR-501. Operations needed the latest dissolved gas analysis
(DGA) to decide between continued operation and emergency isolation, but the most recent DGA on
file was from 2025-08-30 — beyond the 6-month CEA requirement for critical transformers. The
transformer was isolated as a precaution; subsequent testing showed developing thermal fault
gases (ethylene trending).

## Root Cause
DGA schedule slipped without any alert. Test records live in the electrical lab's spreadsheet,
invisible to operations and compliance tracking.

## Actions
1. Oil sampling completed 2025-12-04; unit returned with load restriction.
2. Recommendation: statutory and condition-monitoring schedules need automated overdue alerts
   tied to the equipment record. NOTE: as of mid-2026 the next 180-day DGA is again overdue.
""",
}

SOPS = {
"SOP-CO-012.md": """# SOP-CO-012 — Coke Oven Battery Top Work Under Gas Hazard

**Applies to:** COB-1  |  **Rev:** 4  |  **References:** OISD-STD-105, PTW procedure BIEL-PTW-01

## Purpose
Safe execution of maintenance on the battery top where CO exposure is possible.

## Requirements
1. Valid permit issued per OISD-STD-105 with control-room acknowledgement.
2. Live CO reading from GD-801 at the work location must be below 25 ppm before entry.
3. Continuous personal CO monitors for all crew; evacuation at 50 ppm.
4. No simultaneous charging operations on adjacent ovens during door removal —
   simultaneous operations require section head approval.
5. Collector main pressure to be maintained between 5 and 12 mmWC during door work;
   work stops if pressure exceeds 15 mmWC.

## Emergency
On gas alarm: evacuate upwind muster point M-3, inform control room ext. 2201.
""",
"SOP-MH-004.md": """# SOP-MH-004 — Conveyor Maintenance and Guarding

**Applies to:** CV-401, CV-402  |  **Rev:** 2  |  **References:** Factories Act S.21, BIEL-LOTO-01

## Purpose
Safe conveyor maintenance including belt tracking adjustment, and absolute prohibition of
interlock defeat.

## Requirements
1. All belt tracking adjustments require conveyor stop + LOTO. Running adjustments prohibited.
2. Guard interlocks must never be bridged or bypassed. Any bypass requires a documented
   Temporary Defeat Authorization signed by the Safety Head, max duration 8 hours.
3. Pull-cord and guard interlock function test weekly, recorded in the inspection register.
4. Tail pulley guards may only be removed under LOTO with the isolation verified by trial start.
""",
"SOP-EL-007.md": """# SOP-EL-007 — Power Transformer Condition Monitoring

**Applies to:** TR-501, TR-502  |  **Rev:** 3  |  **References:** CEA-Reg-2010-R.30

## Requirements
1. DGA and oil BDV every 180 days for critical transformers; results entered in the equipment
   record within 48 hours of lab report.
2. Buchholz alarm response: obtain latest DGA; if older than 90 days, treat as unknown condition
   and isolate per emergency procedure.
3. Ethylene or acetylene rising trend = thermal/arcing fault indication; escalate to OEM (CGL).
""",
"SOP-ME-002.md": """# SOP-ME-002 — Rotating Equipment Vibration Management

**Applies to:** C-201, C-202, P-101, P-102, P-201, F-701  |  **Rev:** 5  |  **References:** OISD-RP-124, ISO 10816

## Requirements
1. Vibration survey every 90 days on critical rotating equipment.
2. Alert limit 4.5 mm/s RMS; alarm limit 7.1 mm/s RMS (per OEM Kirloskar manual for C-201).
3. Any reading above alarm limit: corrective work order within 7 days. Deferral of that work
   order requires reliability engineer AND section head approval with documented risk assessment.
4. Repeat failures (same failure mode 3+ times in 12 months) trigger a formal RCA.
""",
}


def gen_docs():
    os.makedirs(os.path.join(BASE, "incidents"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "sops"), exist_ok=True)
    for fname, content in INCIDENTS.items():
        with open(os.path.join(BASE, "incidents", fname), "w", encoding="utf-8") as f:
            f.write(content)
    for fname, content in SOPS.items():
        with open(os.path.join(BASE, "sops", fname), "w", encoding="utf-8") as f:
            f.write(content)
    return len(INCIDENTS) + len(SOPS)


if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    print("equipment:", gen_equipment())
    print("work orders:", gen_work_orders())
    print("inspections:", gen_inspections())
    print("regulations:", gen_regulations())
    print("documents:", gen_docs())
    print("Corpus written to", BASE)
