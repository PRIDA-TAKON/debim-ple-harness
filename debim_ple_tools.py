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
