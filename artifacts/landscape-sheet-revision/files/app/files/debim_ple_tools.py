"""
DEBIM PLE Engineering Tools
Deterministic BIM/IFC4 generator and geometry validator for Physical-Engineering's Last Exam.
"""

import json
from typing import List, Dict, Any, Tuple

def create_ifc4_step_model(
    project_name: str,
    site_name: str,
    buildings: List[Dict[str, Any]],
    networks_payload: Dict[str, Any],
    output_path: str
) -> None:
    """
    Generates a valid ISO-10303-21 STEP physical file conforming to IFC4 and DCBim ifc_contract.md.
    
    buildings is a list of dicts:
    {
        "id": "DH1",
        "type": "data_hall",
        "phase": 1,
        "height": 9.0,
        "points": [(10.0, 10.0), (50.0, 10.0), (50.0, 35.0), (10.0, 35.0)], # 2D footprint polygon in metres
        "storeys": [0.0, 4.5], # Elevations of storeys
        "gross_floor_area_m2": 2000.0 # Optional or calculated from footprint * len(storeys)
    }
    """
    lines = []
    lines.append("ISO-10303-21;")
    lines.append("HEADER;")
    lines.append("FILE_DESCRIPTION(('ViewDefinition[DesignTransferView]'),'2;1');")
    lines.append("FILE_NAME('/dev/null','2026-11-11T00:00:00+00:00',(''),(''),'debim 1.0','debim 1.0','Nobody');")
    lines.append("FILE_SCHEMA(('IFC4'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")
    
    eid = 1
    
    # 1. Project and Units
    id_project = eid; eid += 1
    id_len_unit = eid; eid += 1
    id_area_unit = eid; eid += 1
    id_vol_unit = eid; eid += 1
    id_unit_assign = eid; eid += 1
    id_origin_pt = eid; eid += 1
    id_z_dir = eid; eid += 1
    id_x_dir = eid; eid += 1
    id_axis_placement = eid; eid += 1
    id_rep_context = eid; eid += 1
    id_body_subcontext = eid; eid += 1
    id_site = eid; eid += 1
    id_rel_agg_project_site = eid; eid += 1
    
    # Pre-allocate building IDs
    bldg_records = []
    bldg_ids_for_site = []
    
    for b in buildings:
        b_id = eid; eid += 1
        b_pts_id = eid; eid += 1
        b_poly_id = eid; eid += 1
        b_prof_id = eid; eid += 1
        b_origin_id = eid; eid += 1
        b_zdir_id = eid; eid += 1
        b_xdir_id = eid; eid += 1
        b_place_id = eid; eid += 1
        b_extdir_id = eid; eid += 1
        b_solid_id = eid; eid += 1
        b_shape_rep_id = eid; eid += 1
        b_prod_def_id = eid; eid += 1
        
        # Storeys
        storeys = b.get("storeys", [0.0])
        storey_ids = []
        for s in storeys:
            s_id = eid; eid += 1
            storey_ids.append((s_id, s))
            
        rel_agg_bldg_storey = eid; eid += 1
        
        # Pset DCD_Layout
        pset_id = eid; eid += 1
        p_layout_id = eid; eid += 1
        p_type_id = eid; eid += 1
        p_phase_id = eid; eid += 1
        p_height_id = eid; eid += 1
        p_gfa_id = eid; eid += 1
        rel_def_prop_id = eid; eid += 1
        
        bldg_records.append({
            "data": b,
            "b_id": b_id,
            "pts_id": b_pts_id,
            "poly_id": b_poly_id,
            "prof_id": b_prof_id,
            "origin_id": b_origin_id,
            "zdir_id": b_zdir_id,
            "xdir_id": b_xdir_id,
            "place_id": b_place_id,
            "extdir_id": b_extdir_id,
            "solid_id": b_solid_id,
            "shape_rep_id": b_shape_rep_id,
            "prod_def_id": b_prod_def_id,
            "storeys": storey_ids,
            "rel_agg_storey": rel_agg_bldg_storey,
            "pset_id": pset_id,
            "p_layout_id": p_layout_id,
            "p_type_id": p_type_id,
            "p_phase_id": p_phase_id,
            "p_height_id": p_height_id,
            "p_gfa_id": p_gfa_id,
            "rel_def_prop_id": rel_def_prop_id
        })
        bldg_ids_for_site.append(f"#{b_id}")
        
    id_rel_agg_site_bldgs = eid; eid += 1
    
    # Networks property set on site
    id_site_pset_networks = eid; eid += 1
    id_prop_json = eid; eid += 1
    id_rel_site_networks = eid; eid += 1

    # Format Project & Context
    lines.append(f"#{id_project}=IFCPROJECT('1lXF4C$jXBsAD$f8IpBH0l',$,'{project_name}',$,$,$,$,(#{id_rep_context}),#{id_unit_assign});")
    lines.append(f"#{id_len_unit}=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);")
    lines.append(f"#{id_area_unit}=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);")
    lines.append(f"#{id_vol_unit}=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);")
    lines.append(f"#{id_unit_assign}=IFCUNITASSIGNMENT((#{id_area_unit},#{id_vol_unit},#{id_len_unit}));")
    lines.append(f"#{id_origin_pt}=IFCCARTESIANPOINT((0.,0.,0.));")
    lines.append(f"#{id_z_dir}=IFCDIRECTION((0.,0.,1.));")
    lines.append(f"#{id_x_dir}=IFCDIRECTION((1.,0.,0.));")
    lines.append(f"#{id_axis_placement}=IFCAXIS2PLACEMENT3D(#{id_origin_pt},#{id_z_dir},#{id_x_dir});")
    lines.append(f"#{id_rep_context}=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.0E-5,#{id_axis_placement},$);")
    lines.append(f"#{id_body_subcontext}=IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Body','Model',*,*,*,*,#{id_rep_context},$,.MODEL_VIEW.,$);")
    lines.append(f"#{id_site}=IFCSITE('00gV76XNn5wxa7Ft1prHlq',$,'{site_name}',$,$,$,$,$,$,$,$,$,$,$);")
    lines.append(f"#{id_rel_agg_project_site}=IFCRELAGGREGATES('0wwycbEKfAaAnqlHQK9hBC',$,$,$,#{id_project},(#{id_site}));")
    
    # Site aggregation of buildings
    bldg_str = ",".join(bldg_ids_for_site)
    lines.append(f"#{id_rel_agg_site_bldgs}=IFCRELAGGREGATES('2GHO6f6Ej0n9uKrB$iqoEL',$,$,$,#{id_site},({bldg_str}));")
    
    # Format each building
    for rec in bldg_records:
        b = rec["data"]
        name = b["id"]
        height = float(b["height"])
        raw_pts = b["points"]
        
        # Ensure polygon is closed
        pts = list(raw_pts)
        if pts[0] != pts[-1]:
            pts.append(pts[0])
            
        pts_str = ",".join([f"({p[0]:.4f},{p[1]:.4f})" for p in pts])
        idx_str = ",".join([str(i+1) for i in range(len(pts))])
        
        # Body shape definition
        lines.append(f"#{rec['b_id']}=IFCBUILDING('107qwQvHb1puCtejP3qw{rec['b_id']:02d}',$,'{name}',$,$,$,#{rec['prod_def_id']},$,$,$,$,$);")
        lines.append(f"#{rec['pts_id']}=IFCCARTESIANPOINTLIST2D(({pts_str}));")
        lines.append(f"#{rec['poly_id']}=IFCINDEXEDPOLYCURVE(#{rec['pts_id']},(IFCLINEINDEX(({idx_str}))),$);")
        lines.append(f"#{rec['prof_id']}=IFCARBITRARYCLOSEDPROFILEDEF(.AREA.,$,#{rec['poly_id']});")
        
        # Base placement: z = -0.3 if height == 0 (ground works), else 0.0
        base_z = -0.3 if height <= 0.001 else 0.0
        extrude_h = 0.3 if height <= 0.001 else height
        
        lines.append(f"#{rec['origin_id']}=IFCCARTESIANPOINT((0.,0.,{base_z:.4f}));")
        lines.append(f"#{rec['zdir_id']}=IFCDIRECTION((0.,0.,1.));")
        lines.append(f"#{rec['xdir_id']}=IFCDIRECTION((1.,0.,0.));")
        lines.append(f"#{rec['place_id']}=IFCAXIS2PLACEMENT3D(#{rec['origin_id']},#{rec['zdir_id']},#{rec['xdir_id']});")
        lines.append(f"#{rec['extdir_id']}=IFCDIRECTION((0.,0.,1.));")
        lines.append(f"#{rec['solid_id']}=IFCEXTRUDEDAREASOLID(#{rec['prof_id']},#{rec['place_id']},#{rec['extdir_id']},{extrude_h:.4f});")
        lines.append(f"#{rec['shape_rep_id']}=IFCSHAPEREPRESENTATION(#{id_body_subcontext},'Body','SweptSolid',(#{rec['solid_id']}));")
        lines.append(f"#{rec['prod_def_id']}=IFCPRODUCTDEFINITIONSHAPE($,$,(#{rec['shape_rep_id']}));")
        
        # Storeys
        storey_ids_str = []
        for s_id, s_elev in rec["storeys"]:
            lines.append(f"#{s_id}=IFCBUILDINGSTOREY('3SNw4jIMT2v8cK4NTNp{s_id:02d}',$,'{name}_S{len(storey_ids_str)+1}',$,$,$,$,$,$,{float(s_elev):.4f});")
            storey_ids_str.append(f"#{s_id}")
            
        lines.append(f"#{rec['rel_agg_storey']}=IFCRELAGGREGATES('0DQRMvDED7jwNzGORP{rec['b_id']:02d}',$,$,$,#{rec['b_id']},({','.join(storey_ids_str)}));")
        
        # Pset DCD_Layout
        gfa = float(b.get("gross_floor_area_m2", 0.0))
        lines.append(f"#{rec['p_layout_id']}=IFCPROPERTYSINGLEVALUE('LayoutId',$,IFCLABEL('{name}'),$);")
        lines.append(f"#{rec['p_type_id']}=IFCPROPERTYSINGLEVALUE('LayoutType',$,IFCLABEL('{b['type']}'),$);")
        lines.append(f"#{rec['p_phase_id']}=IFCPROPERTYSINGLEVALUE('Phase',$,IFCINTEGER({int(b.get('phase', 1))}),$);")
        lines.append(f"#{rec['p_height_id']}=IFCPROPERTYSINGLEVALUE('HeightM',$,IFCREAL({height:.4f}),$);")
        lines.append(f"#{rec['p_gfa_id']}=IFCPROPERTYSINGLEVALUE('GrossFloorAreaM2',$,IFCREAL({gfa:.4f}),$);")
        
        p_props = f"#{rec['p_layout_id']},#{rec['p_type_id']},#{rec['p_phase_id']},#{rec['p_height_id']},#{rec['p_gfa_id']}"
        lines.append(f"#{rec['pset_id']}=IFCPROPERTYSET('1osWCvdxHCEgxO$SzAV{rec['b_id']:02d}',$,'DCD_Layout',$,({p_props}));")
        lines.append(f"#{rec['rel_def_prop_id']}=IFCRELDEFINESBYPROPERTIES('3rUtvHMJfFDh8G88I5U{rec['b_id']:02d}',$,$,$,(#{rec['b_id']}),#{rec['pset_id']});")

    # DCD_Networks Pset on site
    # Escape quotes for STEP format (single quotes doubled)
    json_raw = json.dumps(networks_payload)
    step_json = json_raw.replace("'", "''")
    lines.append(f"#{id_prop_json}=IFCPROPERTYSINGLEVALUE('json',$,IFCTEXT('{step_json}'),$);")
    lines.append(f"#{id_site_pset_networks}=IFCPROPERTYSET('0PzsSEexj23wOC3$n2c001',$,'DCD_Networks',$,(#{id_prop_json}));")
    lines.append(f"#{id_rel_site_networks}=IFCRELDEFINESBYPROPERTIES('0fXG4YtzTEBwPMjrI9j001',$,$,$,(#{id_site}),#{id_site_pset_networks});")
    
    lines.append("ENDSEC;")
    lines.append("END-ISO-10303-21;")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ==============================================================================
# PHYSICAL ENGINEERING CALCULATIONS (CIVIL, STRUCTURAL, ELECTRICAL, MECHANICAL)
# ==============================================================================

import math
from typing import Optional

# --- Civil Engineering ---

def calculate_stormwater_retention(
    impervious_area_m2: float,
    design_factor: float = 0.12,
    runoff_coefficient: float = 0.90,
    design_storm_depth_mm: Optional[float] = None
) -> Dict[str, Any]:
    """
    Sizes data center stormwater retention basins.
    Surface area >= design_factor (default 12%) of impervious area,
    or volumetric sizing based on design storm depth.
    """
    required_area_m2 = impervious_area_m2 * design_factor
    volume_m3 = (runoff_coefficient * (design_storm_depth_mm / 1000.0) * impervious_area_m2) if design_storm_depth_mm else (required_area_m2 * 1.5)
    return {
        "impervious_area_m2": round(impervious_area_m2, 2),
        "design_factor": design_factor,
        "required_retention_area_m2": round(required_area_m2, 2),
        "estimated_retention_volume_m3": round(volume_m3, 2),
        "assumed_depth_m": 1.5 if design_storm_depth_mm is None else round(volume_m3 / required_area_m2, 2)
    }

def check_environmental_setbacks(
    building_footprints: List[Dict[str, Any]],
    property_boundary: List[Tuple[float, float]],
    wetland_polygons: List[List[Tuple[float, float]]],
    min_property_setback_m: float = 18.0,
    min_wetland_buffer_m: float = 0.0
) -> Dict[str, Any]:
    """Validates setback distances from site boundaries and wetland buffers."""
    violations = []
    def min_dist_pt_to_seg(p, a, b):
        px, py = p; ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0: return math.hypot(px - ax, py - ay)
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

    for b in building_footprints:
        b_id = b.get("id", "unknown")
        pts = b.get("points", [])
        min_prop_dist = float("inf")
        n_prop = len(property_boundary)
        for p in pts:
            for i in range(n_prop):
                dist = min_dist_pt_to_seg(p, property_boundary[i], property_boundary[(i + 1) % n_prop])
                if dist < min_prop_dist: min_prop_dist = dist
        if min_prop_dist < min_property_setback_m:
            violations.append({
                "building": b_id, "type": "property_setback",
                "distance_m": round(min_prop_dist, 3), "required_m": min_property_setback_m,
                "deficit_m": round(min_property_setback_m - min_prop_dist, 3)
            })
        for w_idx, wetland in enumerate(wetland_polygons):
            min_w_dist = float("inf")
            n_w = len(wetland)
            for p in pts:
                for i in range(n_w):
                    dist = min_dist_pt_to_seg(p, wetland[i], wetland[(i + 1) % n_w])
                    if dist < min_w_dist: min_w_dist = dist
            if min_w_dist < min_wetland_buffer_m:
                violations.append({
                    "building": b_id, "type": "wetland_buffer", "wetland_index": w_idx,
                    "distance_m": round(min_w_dist, 3), "required_m": min_wetland_buffer_m,
                    "deficit_m": round(min_wetland_buffer_m - min_w_dist, 3)
                })
    return {"pass": len(violations) == 0, "violations": violations, "total_buildings_checked": len(building_footprints)}

def calculate_noise_attenuation(
    generator_sound_power_db: float,
    distance_to_boundary_m: float,
    barrier_attenuation_db: float = 0.0,
    ground_absorption_factor: float = 0.5
) -> Dict[str, Any]:
    """Calculates sound pressure level (dBA) at site boundary from standby generators."""
    r = max(1.0, distance_to_boundary_m)
    divergence_loss = 20.0 * math.log10(r) + 11.0
    ground_loss = ground_absorption_factor * 2.0
    spl_boundary = generator_sound_power_db - divergence_loss - barrier_attenuation_db - ground_loss
    return {
        "generator_sound_power_db": generator_sound_power_db,
        "distance_to_boundary_m": round(distance_to_boundary_m, 2),
        "barrier_attenuation_db": barrier_attenuation_db,
        "sound_pressure_level_at_boundary_dba": round(spl_boundary, 2),
        "compliant_with_residential_55dba": spl_boundary <= 55.0,
        "compliant_with_commercial_65dba": spl_boundary <= 65.0
    }

# --- Structural Engineering ---

def calculate_wind_diaphragm_shear(
    basic_wind_speed_mph: float,
    building_length_ft: float,
    building_width_ft: float,
    mean_roof_height_ft: float,
    exposure_category: str = "C",
    risk_category: str = "IV"
) -> Dict[str, Any]:
    """Calculates roof diaphragm lateral shear per ASCE 7."""
    kd = 0.85; kzt = 1.0; ke = 1.0
    z = max(15.0, mean_roof_height_ft)
    if exposure_category.upper() == "B": kz = 2.01 * (z / 1200.0) ** (2.0 / 7.0)
    elif exposure_category.upper() == "D": kz = 2.01 * (z / 700.0) ** (2.0 / 11.5)
    else: kz = 2.01 * (z / 900.0) ** (2.0 / 9.5)
    qz = 0.00256 * kz * kzt * kd * ke * (basic_wind_speed_mph ** 2)
    G = 0.85; net_wall_cp = 1.3
    trib_h = mean_roof_height_ft / 2.0
    wind_force_len = qz * G * net_wall_cp * building_length_ft * trib_h
    shear_width_plf = wind_force_len / (2.0 * building_width_ft)
    wind_force_width = qz * G * net_wall_cp * building_width_ft * trib_h
    shear_len_plf = wind_force_width / (2.0 * building_length_ft)
    return {
        "qz_psf": round(qz, 2), "kz": round(kz, 3),
        "wind_force_loading_length_lbs": round(wind_force_len, 1),
        "wind_force_loading_width_lbs": round(wind_force_width, 1),
        "unit_shear_along_width_plf": round(shear_width_plf, 2),
        "unit_shear_along_length_plf": round(shear_len_plf, 2),
        "max_unit_shear_plf": round(max(shear_width_plf, shear_len_plf), 2),
        "governing_direction": "width_reaction" if shear_width_plf >= shear_len_plf else "length_reaction"
    }

def calculate_seismic_diaphragm_shear(
    s_ds: float,
    diaphragm_weight_kips: float,
    building_length_ft: float,
    building_width_ft: float,
    risk_category: str = "IV"
) -> Dict[str, Any]:
    """Calculates seismic diaphragm design force Fpx and unit shear per ASCE 7."""
    ie = 1.5 if risk_category.upper() == "IV" else 1.0
    c_px = max(0.2 * s_ds * ie, min(0.4 * s_ds * ie, 0.4 * s_ds * ie))
    f_px_kips = c_px * diaphragm_weight_kips
    shear_width_plf = (f_px_kips * 1000.0) / (2.0 * building_width_ft)
    shear_length_plf = (f_px_kips * 1000.0) / (2.0 * building_length_ft)
    return {
        "s_ds": s_ds, "importance_factor_ie": ie,
        "governing_cpx": round(c_px, 4), "f_px_kips": round(f_px_kips, 2),
        "unit_shear_width_plf": round(shear_width_plf, 2),
        "unit_shear_length_plf": round(shear_length_plf, 2),
        "max_seismic_unit_shear_plf": round(max(shear_width_plf, shear_length_plf), 2)
    }

def calculate_footing_settlement_clay(
    footing_width_b_m: float,
    footing_length_l_m: float,
    applied_load_kn: float,
    clay_layer_thickness_h_m: float,
    initial_void_ratio_e0: float,
    compression_index_cc: float,
    initial_effective_stress_kpa: float,
    depth_to_mid_layer_m: float = 3.0
) -> Dict[str, Any]:
    """Calculates 1D consolidation settlement in clay layer under spread footing."""
    z = depth_to_mid_layer_m
    delta_sigma_kpa = applied_load_kn / ((footing_width_b_m + z) * (footing_length_l_m + z))
    final_stress = initial_effective_stress_kpa + delta_sigma_kpa
    settlement_m = (compression_index_cc * clay_layer_thickness_h_m / (1.0 + initial_void_ratio_e0)) * math.log10(final_stress / initial_effective_stress_kpa)
    settlement_mm = settlement_m * 1000.0
    return {
        "applied_stress_increase_delta_sigma_kpa": round(delta_sigma_kpa, 2),
        "initial_effective_stress_kpa": round(initial_effective_stress_kpa, 2),
        "final_stress_kpa": round(final_stress, 2),
        "settlement_mm": round(settlement_mm, 2),
        "settlement_inches": round(settlement_mm / 25.4, 3),
        "acceptable_for_data_center_under_25mm": settlement_mm <= 25.0
    }

# --- Electrical Engineering ---

def calculate_voltage_drop(
    current_amps: float,
    length_ft: float,
    nominal_voltage_v: float,
    system_type: str = "3_phase",
    wire_size: str = "500_kcmil",
    power_factor: float = 0.90,
    max_allowed_drop_percent: float = 3.0
) -> Dict[str, Any]:
    """Calculates voltage drop in volts and percentage per NEC guidelines."""
    r_map = {"4_awg": 0.308, "2/0_awg": 0.096, "4/0_awg": 0.060, "250_kcmil": 0.051, "350_kcmil": 0.038, "500_kcmil": 0.027}
    r = r_map.get(wire_size, 0.027)
    x = 0.05
    sin_phi = math.sqrt(max(0.0, 1.0 - power_factor ** 2))
    impedance = (r * power_factor) + (x * sin_phi)
    mult = math.sqrt(3) if system_type.lower() == "3_phase" else 2.0
    vd_volts = mult * current_amps * (length_ft / 1000.0) * impedance
    vd_percent = (vd_volts / nominal_voltage_v) * 100.0
    return {
        "current_amps": current_amps, "length_ft": length_ft, "wire_size": wire_size,
        "voltage_drop_volts": round(vd_volts, 2), "voltage_drop_percent": round(vd_percent, 2),
        "max_allowed_percent": max_allowed_drop_percent, "compliant": vd_percent <= max_allowed_drop_percent
    }

def size_data_center_generator_yard(
    total_it_load_mw: float,
    pue: float = 1.25,
    genset_capacity_mw: float = 2.5,
    redundancy: str = "N+1",
    fuel_autonomy_hours: float = 48.0
) -> Dict[str, Any]:
    """Sizes standby diesel generators and fuel oil storage for a data center campus."""
    facility_mw = total_it_load_mw * pue
    base_n = math.ceil(facility_mw / genset_capacity_mw)
    add_gens = 1 if redundancy.upper() == "N+1" else (2 if redundancy.upper() == "N+2" else base_n)
    total_gens = base_n + add_gens if redundancy.upper() != "2N" else base_n * 2
    fuel_liters = facility_mw * fuel_autonomy_hours * 250.0
    return {
        "it_load_mw": total_it_load_mw, "facility_load_mw": round(facility_mw, 2),
        "base_gensets_n": base_n, "redundancy": redundancy, "total_gensets": total_gens,
        "installed_capacity_mw": round(total_gens * genset_capacity_mw, 2),
        "fuel_storage_required_liters": round(fuel_liters, 0),
        "fuel_storage_required_gallons": round(fuel_liters * 0.264172, 0),
        "min_fire_separation_distance_m": 28.0
    }

def size_mv_substation_transformers(
    total_load_mva: float,
    primary_kv: float = 115.0,
    secondary_kv: float = 13.8,
    transformer_unit_mva: float = 30.0,
    redundancy: str = "2N"
) -> Dict[str, Any]:
    """Sizes medium-voltage site distribution substation transformers."""
    base_n = math.ceil(total_load_mva / transformer_unit_mva)
    total_tx = base_n * 2 if redundancy.upper() == "2N" else base_n + 1
    return {
        "total_connected_load_mva": total_load_mva,
        "base_transformers_n": base_n,
        "redundancy": redundancy,
        "total_transformers": total_tx,
        "transformer_unit_mva": transformer_unit_mva,
        "installed_substation_capacity_mva": total_tx * transformer_unit_mva
    }

# --- Mechanical Engineering ---

def calculate_data_hall_cooling_load(
    it_load_kw: float,
    delta_t_fahrenheit: float = 20.0,
    chw_supply_temp_f: float = 55.0,
    chw_return_temp_f: float = 67.0
) -> Dict[str, Any]:
    """Calculates total heat rejection load, Tons of Refrigeration, Chilled Water GPM, and CRAH CFM."""
    it_btu = it_load_kw * 3412.142
    total_cooling_btu = it_btu * 1.09
    tr = total_cooling_btu / 12000.0
    cfm = total_cooling_btu / (1.08 * delta_t_fahrenheit)
    chw_dt = max(1.0, chw_return_temp_f - chw_supply_temp_f)
    gpm = total_cooling_btu / (500.0 * chw_dt)
    return {
        "it_load_kw": it_load_kw, "total_cooling_btu_hr": round(total_cooling_btu, 1),
        "tons_of_refrigeration": round(tr, 2), "required_airflow_cfm": round(cfm, 1),
        "chilled_water_flow_gpm": round(gpm, 1), "ashrae_class": "A1/A2 Recommended"
    }

def calculate_pipe_volume_and_flushing(
    pipe_diameter_inches: float,
    total_pipe_length_ft: float,
    chemical_passivation_ppm: float = 50.0
) -> Dict[str, Any]:
    """Calculates PCW pipe water volume and chemical passivation dosage."""
    r_ft = (pipe_diameter_inches / 2.0) / 12.0
    vol_cu_ft = math.pi * (r_ft ** 2) * total_pipe_length_ft
    gallons = vol_cu_ft * 7.48052
    liters = gallons * 3.78541
    chem_kg = (liters * chemical_passivation_ppm) / 1000000.0
    return {
        "pipe_diameter_inches": pipe_diameter_inches, "total_length_ft": total_pipe_length_ft,
        "volume_gallons": round(gallons, 1), "volume_liters": round(liters, 1),
        "passivation_chemical_kg": round(chem_kg, 2)
    }

# --- Data Center Integrated Sizing ---

def calculate_pue_wue(
    it_power_kw: float,
    cooling_power_kw: float,
    electrical_loss_kw: float,
    lighting_misc_kw: float,
    annual_water_liters: float = 0.0
) -> Dict[str, Any]:
    """Calculate Power Usage Effectiveness (PUE) and Water Usage Effectiveness (WUE)."""
    facility_kw = it_power_kw + cooling_power_kw + electrical_loss_kw + lighting_misc_kw
    pue = facility_kw / it_power_kw
    annual_kwh = it_power_kw * 8760.0
    wue = (annual_water_liters / annual_kwh) if annual_water_liters > 0 else 0.0
    return {
        "it_power_kw": it_power_kw, "facility_power_kw": facility_kw,
        "pue": round(pue, 3), "wue_l_per_kwh": round(wue, 3)
    }

def size_data_hall_whitespace(
    total_it_mw: float,
    avg_rack_kw: float = 10.0,
    rack_width_m: float = 0.6,
    rack_depth_m: float = 1.2
) -> Dict[str, Any]:
    """Size data hall white space footprint and rack count based on IT load."""
    rack_count = math.ceil((total_it_mw * 1000.0) / avg_rack_kw)
    eff_depth = rack_depth_m + 1.1 # 1.2m cold + 1.0m hot aisle shared
    rack_net_area = rack_width_m * eff_depth * rack_count
    gross_area = rack_net_area * 1.35
    return {
        "total_it_mw": total_it_mw, "rack_count": rack_count,
        "avg_rack_kw": avg_rack_kw, "rack_net_area_sqm": round(rack_net_area, 1),
        "gross_whitespace_area_sqm": round(gross_area, 1),
        "power_density_w_per_sqm": round((total_it_mw * 1e6) / gross_area, 1)
    }

def check_tier_redundancy(
    tier_level: str,
    it_load_mw: float,
    generator_unit_mw: float = 2.5,
    ups_unit_kw: float = 1000.0,
    chiller_unit_tr: float = 500.0
) -> Dict[str, Any]:
    """Compute required equipment counts for Uptime Institute Tier I-IV."""
    t = tier_level.upper().replace("TIER", "").strip()
    n_gens = math.ceil((it_load_mw * 1.15) / generator_unit_mw)
    n_ups = math.ceil((it_load_mw * 1000.0) / ups_unit_kw)
    n_chillers = math.ceil((it_load_mw * 324.0) / chiller_unit_tr)
    if t in ["I", "1"]: gens_req, ups_req, ch_req = n_gens, n_ups, n_chillers
    elif t in ["II", "2"]: gens_req, ups_req, ch_req = n_gens + 1, n_ups + 1, n_chillers + 1
    elif t in ["III", "3"]: gens_req, ups_req, ch_req = n_gens + 1, n_ups * 2, n_chillers + 2
    else: gens_req, ups_req, ch_req = n_gens * 2, n_ups * 2, n_chillers * 2
    return {
        "tier": f"Tier {t}",
        "generators": {"n_required": n_gens, "total_installed": gens_req, "unit_mw": generator_unit_mw},
        "ups_units": {"n_required": n_ups, "total_installed": ups_req, "unit_kw": ups_unit_kw},
        "chillers": {"n_required": n_chillers, "total_installed": ch_req, "unit_tr": chiller_unit_tr}
    }

def calculate_data_hall_floor_load(
    rack_weight_kg: float = 1200.0,
    rack_footprint_sqm: float = 0.72,
    slab_capacity_kpa: float = 15.0
) -> Dict[str, Any]:
    """Verify structural floor load capacity for high-density server racks."""
    rack_kn = (rack_weight_kg * 9.80665) / 1000.0
    direct_kpa = rack_kn / rack_footprint_sqm
    uniform_kpa = rack_kn / (rack_footprint_sqm * 2.0)
    total_kpa = uniform_kpa + 0.5
    return {
        "rack_weight_kg": rack_weight_kg,
        "direct_rack_pressure_kpa": round(direct_kpa, 2),
        "total_imposed_kpa": round(total_kpa, 2),
        "slab_capacity_kpa": slab_capacity_kpa,
        "is_compliant": total_kpa <= slab_capacity_kpa
    }

# ==============================================================================
# 5 CORE ENGINEERING VERIFICATION (QA/QC) TOOLS
# ==============================================================================

def cross_check_counts(
    plan_counts: Dict[str, int],
    schedule_counts: Dict[str, int]
) -> Dict[str, Any]:
    """
    Cross-checks physical plan takeoff counts against schedule/estimate tables.
    Identifies discrepancies, missing items, and surplus entries.
    """
    all_keys = sorted(set(list(plan_counts.keys()) + list(schedule_counts.keys())))
    discrepancies = []
    matched = []
    
    for k in all_keys:
        p_val = plan_counts.get(k, 0)
        s_val = schedule_counts.get(k, 0)
        diff = p_val - s_val
        entry = {
            "item": k,
            "plan_count": p_val,
            "schedule_count": s_val,
            "variance": diff,
            "status": "MATCH" if diff == 0 else ("PLAN_EXCEEDS" if diff > 0 else "SCHEDULE_EXCEEDS")
        }
        if diff != 0:
            discrepancies.append(entry)
        else:
            matched.append(entry)
            
    return {
        "total_items_checked": len(all_keys),
        "discrepancy_count": len(discrepancies),
        "discrepancies": discrepancies,
        "matched": matched,
        "is_consistent": len(discrepancies) == 0
    }

def verify_unit_consistency(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    Validates dimensional and unit conversions across Imperial and Metric engineering units.
    """
    u_from = from_unit.strip().lower()
    u_to = to_unit.strip().lower()
    
    conversions = {
        ("in", "ft"): 1.0 / 12.0,
        ("ft", "in"): 12.0,
        ("ft", "m"): 0.3048,
        ("m", "ft"): 1.0 / 0.3048,
        ("lf", "ft"): 1.0,
        ("cy", "cf"): 27.0,
        ("cf", "cy"): 1.0 / 27.0,
        ("sqft", "sqm"): 0.092903,
        ("sqm", "sqft"): 1.0 / 0.092903,
        ("psi", "kpa"): 6.89476,
        ("kpa", "psi"): 1.0 / 6.89476,
        ("gpm", "cfs"): 0.002228,
        ("cfs", "gpm"): 448.831,
        ("kw", "tr"): 1.0 / 3.51685,
        ("tr", "kw"): 3.51685,
        ("kw", "hp"): 1.34102,
        ("hp", "kw"): 0.7457
    }
    
    if u_from == u_to:
        factor = 1.0
    elif (u_from, u_to) in conversions:
        factor = conversions[(u_from, u_to)]
    else:
        return {
            "error": f"Unsupported conversion from {from_unit} to {to_unit}",
            "is_valid": False
        }
        
    converted = value * factor
    return {
        "input_value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "conversion_factor": factor,
        "converted_value": round(converted, 4),
        "is_valid": True
    }

def audit_estimate_discrepancies(
    line_items: List[Dict[str, Any]],
    bond_rate_percent: float = 100.0,
    bond_round_up_nearest: int = 1000
) -> Dict[str, Any]:
    """
    Deterministic engineering cost estimate audit tool.
    Computes verified line totals, subtotals by section, and rounded performance bond amounts.
    
    Each line item dict:
    {
        "id": "2.36",
        "description": "60-inch Manhole",
        "quantity": 10.0,
        "unit": "EA",
        "unit_price": 7500.0,
        "section": "Section 2"
    }
    """
    sections = {}
    verified_items = []
    grand_subtotal = 0.0
    
    for item in line_items:
        qty = float(item.get("quantity", 0.0))
        rate = float(item.get("unit_price", 0.0))
        ext = qty * rate
        sec = item.get("section", "General")
        
        v_item = dict(item)
        v_item["extended_amount"] = round(ext, 2)
        verified_items.append(v_item)
        
        sections[sec] = sections.get(sec, 0.0) + ext
        grand_subtotal += ext
        
    rounded_sections = {s: round(val, 2) for s, val in sections.items()}
    grand_subtotal = round(grand_subtotal, 2)
    
    # Calculate bond
    bond_amount_exact = grand_subtotal * (bond_rate_percent / 100.0)
    if bond_round_up_nearest > 0:
        bond_rounded = math.ceil(bond_amount_exact / bond_round_up_nearest) * bond_round_up_nearest
    else:
        bond_rounded = round(bond_amount_exact, 2)
        
    return {
        "total_line_items": len(verified_items),
        "verified_items": verified_items,
        "section_subtotals": rounded_sections,
        "grand_subtotal": grand_subtotal,
        "bond_rate_percent": bond_rate_percent,
        "bond_amount_exact": round(bond_amount_exact, 2),
        "bond_amount_rounded": bond_rounded,
        "rounding_rule": f"Round up to next {bond_round_up_nearest}" if bond_round_up_nearest > 0 else "Exact"
    }


# ==============================================================================
# PLAN-TO-BIM / DRAWING INGESTION ENGINE & MEP ROUTE SYNTHESIZER
# Pure Python & NumPy (Zero external heavy dependencies like Pillow or OpenCV)
# ==============================================================================

import struct
import zlib
import numpy as np

def read_png_rgba(file_path: str) -> np.ndarray:
    """
    Pure Python PNG parser using standard zlib and numpy.
    Parses standard 8-bit/color RGBA or RGB PNGs without Pillow or OpenCV.
    Returns uint8 numpy array of shape (height, width, 4).
    """
    with open(file_path, "rb") as f:
        sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a valid PNG file: {file_path}")

        width = 0
        height = 0
        bit_depth = 8
        color_type = 6
        idat_chunks = []

        while True:
            header = f.read(8)
            if len(header) < 8:
                break
            length, chunk_type = struct.unpack(">I4s", header)
            chunk_data = f.read(length)
            f.read(4)  # CRC

            if chunk_type == b"IHDR":
                width, height, bit_depth, color_type, comp, filt, inter = struct.unpack(
                    ">IIBBBBB", chunk_data
                )
            elif chunk_type == b"IDAT":
                idat_chunks.append(chunk_data)
            elif chunk_type == b"IEND":
                break

    if not idat_chunks:
        raise ValueError("No IDAT chunks found in PNG")

    raw_decompressed = zlib.decompress(b"".join(idat_chunks))
    bpp = 4 if color_type == 6 else (3 if color_type == 2 else 1)
    stride = width * bpp
    img_data = bytearray(height * width * 4)

    # Decode filter per scanline
    src_idx = 0
    prev_row = bytearray(stride)
    curr_row = bytearray(stride)

    for y in range(height):
        filter_type = raw_decompressed[src_idx]
        src_idx += 1
        raw_row = raw_decompressed[src_idx : src_idx + stride]
        src_idx += stride

        if filter_type == 0:  # None
            curr_row[:] = raw_row
        elif filter_type == 1:  # Sub
            for i in range(stride):
                left = curr_row[i - bpp] if i >= bpp else 0
                curr_row[i] = (raw_row[i] + left) & 0xFF
        elif filter_type == 2:  # Up
            for i in range(stride):
                curr_row[i] = (raw_row[i] + prev_row[i]) & 0xFF
        elif filter_type == 3:  # Average
            for i in range(stride):
                left = curr_row[i - bpp] if i >= bpp else 0
                up = prev_row[i]
                curr_row[i] = (raw_row[i] + ((left + up) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth
            for i in range(stride):
                a = curr_row[i - bpp] if i >= bpp else 0
                b = prev_row[i]
                c = prev_row[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                curr_row[i] = (raw_row[i] + pr) & 0xFF

        # Copy to RGBA output
        dst_y = y * width * 4
        if bpp == 4:
            img_data[dst_y : dst_y + stride] = curr_row
        elif bpp == 3:
            for x in range(width):
                rx = x * 3
                dx = dst_y + x * 4
                img_data[dx] = curr_row[rx]
                img_data[dx + 1] = curr_row[rx + 1]
                img_data[dx + 2] = curr_row[rx + 2]
                img_data[dx + 3] = 255
        elif bpp == 1:
            for x in range(width):
                val = curr_row[x]
                dx = dst_y + x * 4
                img_data[dx] = val
                img_data[dx + 1] = val
                img_data[dx + 2] = val
                img_data[dx + 3] = 255

        prev_row[:] = curr_row

    arr = np.frombuffer(img_data, dtype=np.uint8).reshape((height, width, 4))
    return arr


def write_png_rgba(file_path: str, width: int, height: int, rgba_bytes: bytes) -> None:
    """Writes a standard uncompressed/zlib RGBA PNG using standard library."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    stride = width * 4
    raw_scanlines = bytearray()
    for y in range(height):
        raw_scanlines.append(0)  # filter type 0 (None)
        raw_scanlines.extend(rgba_bytes[y * stride : (y + 1) * stride])

    idat = zlib.compress(bytes(raw_scanlines), level=6)
    with open(file_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))


def crop_png(input_path: str, output_path: str, x: int, y: int, w: int, h: int) -> None:
    """Crops a region from a PNG and saves as a new PNG."""
    arr = read_png_rgba(input_path)
    h_max, w_max, _ = arr.shape
    x0 = max(0, min(w_max - 1, x))
    y0 = max(0, min(h_max - 1, y))
    x1 = max(x0 + 1, min(w_max, x + w))
    y1 = max(y0 + 1, min(h_max, y + h))
    cropped = arr[y0:y1, x0:x1]
    ch, cw, _ = cropped.shape
    write_png_rgba(output_path, cw, ch, cropped.tobytes())


def generate_image_tiles(
    png_path: str,
    out_dir: str,
    tile_cols: int = 2,
    tile_rows: int = 2
) -> List[str]:
    """
    Safe Multimodal Reader: Slices a high-resolution drawing into small tiles
    to prevent multimodal API 400 Bad Request errors.
    """
    import os
    os.makedirs(out_dir, exist_ok=True)
    arr = read_png_rgba(png_path)
    h, w, _ = arr.shape
    base_name = os.path.splitext(os.path.basename(png_path))[0]

    tile_w = w // tile_cols
    tile_h = h // tile_rows
    tile_paths = []

    for r in range(tile_rows):
        for c in range(tile_cols):
            x = c * tile_w
            y = r * tile_h
            sub = arr[y : y + tile_h, x : x + tile_w]
            out_path = os.path.join(out_dir, f"{base_name}_r{r}_c{c}.png")
            write_png_rgba(out_path, tile_w, tile_h, sub.tobytes())
            tile_paths.append(out_path)

    return tile_paths


def detect_grid_anchors(arr_rgba: np.ndarray) -> Dict[str, Any]:
    """
    Detects structural grid lines and column anchors from a drawing raster.
    Uses luminance projections to locate horizontal and vertical grid lines.
    """
    # Convert RGBA to grayscale
    gray = (
        0.299 * arr_rgba[:, :, 0].astype(float)
        + 0.587 * arr_rgba[:, :, 1].astype(float)
        + 0.114 * arr_rgba[:, :, 2].astype(float)
    )
    # Drawing lines are dark on light background (invert so lines are peaks)
    inv = 255.0 - gray
    h, w = inv.shape

    # Marginal projection profiles
    proj_x = np.sum(inv[int(h * 0.1) : int(h * 0.9), :], axis=0)
    proj_y = np.sum(inv[:, int(w * 0.1) : int(w * 0.9)], axis=1)

    # Find dominant peaks with distance filtering
    def find_peaks(profile, min_dist=50, threshold_ratio=0.3):
        thresh = np.max(profile) * threshold_ratio
        peaks = []
        for i in range(1, len(profile) - 1):
            if profile[i] > thresh and profile[i] >= profile[i - 1] and profile[i] >= profile[i + 1]:
                if not peaks or (i - peaks[-1]) >= min_dist:
                    peaks.append(i)
                elif profile[i] > profile[peaks[-1]]:
                    peaks[-1] = i
        return peaks

    grid_x = find_peaks(proj_x, min_dist=int(w * 0.08))
    grid_y = find_peaks(proj_y, min_dist=int(h * 0.08))

    return {
        "image_width": w,
        "image_height": h,
        "grid_x_pixels": grid_x,
        "grid_y_pixels": grid_y,
        "estimated_col_bays": max(1, len(grid_x) - 1),
        "estimated_row_bays": max(1, len(grid_y) - 1),
    }


def create_dc_hall_ifc(
    output_path: str,
    project_name: str = "DC Model",
    hall_name: str = "DATA HALL 1",
    storey_name: str = "LEVEL 1",
    building_name: str = "DC-01",
    hall_footprint_mm: Sequence[Tuple[float, float]] = [(0.0, 0.0), (27000.0, 0.0), (27000.0, 21000.0), (0.0, 21000.0)],
    hall_height_mm: float = 4500.0,
    racks: Sequence[Dict[str, Any]] = (),
    crahs: Sequence[Dict[str, Any]] = (),
    pdus: Sequence[Dict[str, Any]] = (),
    columns: Sequence[Dict[str, Any]] = (),
    sprinklers: Sequence[Dict[str, Any]] = (),
    cable_trays: Sequence[Dict[str, Any]] = (),
    busways: Sequence[Dict[str, Any]] = (),
    chw_pipes: Sequence[Dict[str, Any]] = ()
) -> None:
    """
    Creates a 100% compliant IFC4 STEP model for dc_model MEP routing benchmark.
    Follows EXPRESS rules (2D profiles only, OuterCurve.Dim == 2) and placement matrix
    conventions (matrix translations scaled to metres while file units are MILLIMETRES).
    """
    import ifcopenshell
    import ifcopenshell.api

    run = ifcopenshell.api.run

    model = run("project.create_file", version="IFC4")
    project = run("root.create_entity", model, ifc_class="IfcProject", name=project_name)
    run("unit.assign_unit", model, length={"is_metric": True, "raw": "MILLIMETERS"})

    ctx = run("context.add_context", model, context_type="Model")
    body = run("context.add_context", model, context_type="Model",
               context_identifier="Body", target_view="MODEL_VIEW", parent=ctx)

    site = run("root.create_entity", model, ifc_class="IfcSite", name="SITE")
    building = run("root.create_entity", model, ifc_class="IfcBuilding", name=building_name)
    storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name=storey_name)
    hall = run("root.create_entity", model, ifc_class="IfcSpace", name=hall_name)

    run("aggregate.assign_object", model, products=[site], relating_object=project)
    run("aggregate.assign_object", model, products=[building], relating_object=site)
    run("aggregate.assign_object", model, products=[storey], relating_object=building)
    run("aggregate.assign_object", model, products=[hall], relating_object=storey)

    # Helper for 2D closed polyline profile
    def make_profile_2d(pts_mm):
        pts = list(pts_mm)
        if pts[0] != pts[-1]:
            pts.append(pts[0])
        poly = model.create_entity(
            "IfcPolyline",
            Points=[
                model.create_entity("IfcCartesianPoint", Coordinates=(float(p[0]), float(p[1])))
                for p in pts
            ]
        )
        return model.create_entity("IfcArbitraryClosedProfileDef", ProfileType="AREA", OuterCurve=poly)

    def make_extruded_rep(profile_2d, depth_mm):
        solid = model.create_entity(
            "IfcExtrudedAreaSolid",
            SweptArea=profile_2d,
            Position=model.create_entity(
                "IfcAxis2Placement3D",
                Location=model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0))
            ),
            ExtrudedDirection=model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)),
            Depth=float(depth_mm)
        )
        return model.create_entity(
            "IfcShapeRepresentation",
            ContextOfItems=body,
            RepresentationIdentifier="Body",
            RepresentationType="SweptSolid",
            Items=[solid]
        )

    def make_box_rep(w_mm, d_mm, h_mm):
        prof = make_profile_2d([(0.0, 0.0), (w_mm, 0.0), (w_mm, d_mm), (0.0, d_mm)])
        return make_extruded_rep(prof, h_mm)

    def place_elem(elem, x_mm, y_mm, z_mm=0.0, rot_deg=0.0, pivot_mm=None):
        r = np.radians(float(rot_deg))
        c, s = np.cos(r), np.sin(r)
        rot_m = np.eye(4)
        rot_m[0, 0], rot_m[0, 1] = c, -s
        rot_m[1, 0], rot_m[1, 1] = s, c

        t_m = np.eye(4)
        t_m[:3, 3] = (float(x_mm), float(y_mm), float(z_mm))

        if rot_deg != 0.0 and pivot_mm is not None:
            px, py = pivot_mm
            p_to = np.eye(4); p_to[:3, 3] = (px, py, 0.0)
            p_back = np.eye(4); p_back[:3, 3] = (-px, -py, 0.0)
            mat = t_m @ p_to @ rot_m @ p_back
        elif rot_deg != 0.0:
            mat = t_m @ rot_m
        else:
            mat = t_m

        # Convert translation from mm to metres for edit_object_placement
        mat_ifc = np.array(mat, dtype=float, copy=True)
        mat_ifc[:3, 3] = mat_ifc[:3, 3] / 1000.0

        run("geometry.edit_object_placement", model, product=elem, matrix=mat_ifc)

    # Set hall space representation
    hall_prof = make_profile_2d(hall_footprint_mm)
    run("geometry.assign_representation", model, product=hall,
        representation=make_extruded_rep(hall_prof, hall_height_mm))
    place_elem(hall, 0.0, 0.0, 0.0)

    # Helper to add physical element
    def add_element(ifc_cls, name, w_mm, d_mm, h_mm, x_mm, y_mm, z_mm=0.0,
                    predefined=None, obj_type=None, rot_deg=0.0, pivot_mm=None, psets=None):
        prod = run("root.create_entity", model, ifc_class=ifc_cls, name=name)
        if predefined:
            prod.PredefinedType = predefined
        if obj_type:
            prod.ObjectType = obj_type

        run("spatial.assign_container", model, products=[prod], relating_structure=hall)
        rep = make_box_rep(w_mm, d_mm, h_mm)
        run("geometry.assign_representation", model, product=prod, representation=rep)
        place_elem(prod, x_mm, y_mm, z_mm, rot_deg=rot_deg, pivot_mm=pivot_mm)

        if psets:
            for pset_name, props in psets.items():
                pset = run("pset.add_pset", model, product=prod, name=pset_name)
                run("pset.edit_pset", model, pset=pset, properties=props)
        return prod

    # 1. Racks
    for idx, rk in enumerate(racks):
        name = rk.get("name", f"Rack_{idx+1}")
        w = float(rk.get("width_mm", 600.0))
        d = float(rk.get("depth_mm", 1200.0))
        h = float(rk.get("height_mm", 2000.0))
        x = float(rk.get("x_mm", 0.0))
        y = float(rk.get("y_mm", 0.0))
        z = float(rk.get("z_mm", 0.0))
        facing = rk.get("facing", "NORTH")
        rot = 0.0 if facing == "NORTH" else (180.0 if facing == "SOUTH" else (270.0 if facing == "EAST" else 90.0))
        psets = {"Pset_DCM_Rack": {"FacingDirection": facing}}
        add_element("IfcFurniture", name, w, d, h, x, y, z,
                    predefined="USERDEFINED", obj_type="Rack", rot_deg=rot,
                    pivot_mm=(w / 2.0, d / 2.0), psets=psets)

    # 2. Columns
    for idx, col in enumerate(columns):
        name = col.get("name", f"Col_{idx+1}")
        w = float(col.get("width_mm", 600.0))
        d = float(col.get("depth_mm", 600.0))
        h = float(col.get("height_mm", hall_height_mm))
        x = float(col.get("x_mm", 0.0))
        y = float(col.get("y_mm", 0.0))
        z = float(col.get("z_mm", 0.0))
        add_element("IfcColumn", name, w, d, h, x, y, z)

    # 3. CRAHs
    for idx, cr in enumerate(crahs):
        name = cr.get("name", f"CRAH_{idx+1}")
        w = float(cr.get("width_mm", 2400.0))
        d = float(cr.get("depth_mm", 1000.0))
        h = float(cr.get("height_mm", 2200.0))
        x = float(cr.get("x_mm", 0.0))
        y = float(cr.get("y_mm", 0.0))
        z = float(cr.get("z_mm", 0.0))
        add_element("IfcUnitaryEquipment", name, w, d, h, x, y, z, obj_type="CRAH")

    # 4. PDUs
    for idx, pdu in enumerate(pdus):
        name = pdu.get("name", f"PDU_{idx+1}")
        w = float(pdu.get("width_mm", 1000.0))
        d = float(pdu.get("depth_mm", 1000.0))
        h = float(pdu.get("height_mm", 2000.0))
        x = float(pdu.get("x_mm", 0.0))
        y = float(pdu.get("y_mm", 0.0))
        z = float(pdu.get("z_mm", 0.0))
        add_element("IfcUnitaryEquipment", name, w, d, h, x, y, z, obj_type="PDU")

    # 5. Sprinklers
    for idx, sp in enumerate(sprinklers):
        name = sp.get("name", f"Sprinkler_{idx+1}")
        w = float(sp.get("width_mm", 100.0))
        d = float(sp.get("depth_mm", 100.0))
        h = float(sp.get("height_mm", 100.0))
        x = float(sp.get("x_mm", 0.0))
        y = float(sp.get("y_mm", 0.0))
        z = float(sp.get("z_mm", 3800.0))
        add_element("IfcFlowTerminal", name, w, d, h, x, y, z, obj_type="Sprinkler")

    # 6. Overhead Services (Cable Tray, Busway, CHW Pipe)
    for idx, seg in enumerate(cable_trays):
        name = seg.get("name", f"Tray_{idx+1}")
        w = float(seg.get("width_mm", 600.0))
        d = float(seg.get("depth_mm", 100.0))
        h = float(seg.get("height_mm", 100.0))
        x = float(seg.get("x_mm", 0.0))
        y = float(seg.get("y_mm", 0.0))
        z = float(seg.get("z_mm", 3100.0))
        add_element("IfcCableCarrierSegment", name, w, d, h, x, y, z,
                    predefined="CABLETRAYSEGMENT", obj_type="CableTray")

    for idx, seg in enumerate(busways):
        name = seg.get("name", f"Busway_{idx+1}")
        w = float(seg.get("width_mm", 200.0))
        d = float(seg.get("depth_mm", 100.0))
        h = float(seg.get("height_mm", 100.0))
        x = float(seg.get("x_mm", 0.0))
        y = float(seg.get("y_mm", 0.0))
        z = float(seg.get("z_mm", 2750.0))
        add_element("IfcFlowSegment", name, w, d, h, x, y, z,
                    predefined="BUSWAY", obj_type="Busway")

    for idx, seg in enumerate(chw_pipes):
        name = seg.get("name", f"CHW_{idx+1}")
        w = float(seg.get("width_mm", 150.0))
        d = float(seg.get("depth_mm", 150.0))
        h = float(seg.get("height_mm", 150.0))
        x = float(seg.get("x_mm", 0.0))
        y = float(seg.get("y_mm", 0.0))
        z = float(seg.get("z_mm", 3400.0))
        add_element("IfcPipeSegment", name, w, d, h, x, y, z, obj_type="ChilledWaterPipe")

    model.write(output_path)


