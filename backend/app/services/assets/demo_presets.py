import uuid
from typing import Dict, Any, List
from app.schemas.scene_schema import (
    ScenePlan, SceneObjectData, TransformData, MaterialData,
    ComponentData, AnimationData, EnvironmentData, LightData, CameraData
)

def get_demo_scenes() -> Dict[str, ScenePlan]:
    demos: Dict[str, ScenePlan] = {}

    # 1. Wedding Stage
    demos["wedding_stage"] = ScenePlan(
        id="demo_wedding_stage",
        title="Grand Luxury Royal Wedding Stage",
        intent="CREATE_SCENE",
        scene_type="event_stage",
        user_prompt="Create a grand luxury wedding decoration with flowers, LED backdrop, sofa, lighting and elegant entrance decoration.",
        language="en",
        observed_from_image=[],
        inferred_elements=["mandap canopy", "golden floral pillars", "velvet royal couch", "crystal chandelier", "stage platform"],
        environment=EnvironmentData(
            sky_color="#1a0b2e",
            ground_color="#2b1055",
            fog_color="#1a0b2e",
            fog_density=0.015,
            ambient_color="#ffeedd",
            ambient_intensity=0.8
        ),
        lighting=[
            LightData(type="directional", color="#ffd280", intensity=2.0, position=[5.0, 10.0, 8.0]),
            LightData(type="spot", color="#e879f9", intensity=3.5, position=[0.0, 8.0, 4.0]),
            LightData(type="point", color="#facc15", intensity=2.5, position=[-4.0, 4.0, 2.0]),
            LightData(type="point", color="#facc15", intensity=2.5, position=[4.0, 4.0, 2.0])
        ],
        camera=CameraData(position=[0.0, 3.5, 9.0], target=[0.0, 1.2, 0.0], fov=45.0),
        explanation_targets=["stage_platform", "royal_sofa", "floral_arch", "crystal_chandelier", "gold_pillar_left"],
        objects=[
            SceneObjectData(
                id="stage_platform",
                name="Tiered Velvet Stage Platform",
                category="structure",
                purpose="Elevates the ceremonial area, creating visual grandeur and VIP seating.",
                description="Carpeted tiered luxury wooden platform with gold leaf perimeter beading.",
                geometry_type="box",
                geometry_params={"width": 9.0, "height": 0.4, "depth": 6.0},
                transform=TransformData(position=[0.0, -0.2, 0.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]),
                material=MaterialData(color="#881337", roughness=0.6, metalness=0.1, name="Burgundy Velvet Carpet"),
                is_estimated=False
            ),
            SceneObjectData(
                id="royal_sofa",
                name="Royal Throne Sofa",
                category="furniture",
                purpose="Primary seating for the bride and groom.",
                description="Tufted ivory velvet settee with hand-carved baroque gold leaf frame.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.4, -0.5], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]),
                material=MaterialData(color="#faf5ff", roughness=0.3, metalness=0.1, name="Ivory Silk Silk"),
                components=[
                    ComponentData(
                        id="sofa_seat",
                        name="Cushion Base",
                        purpose="Plush seating surface",
                        geometry_type="box",
                        geometry_params={"width": 2.4, "height": 0.4, "depth": 0.9},
                        transform=TransformData(position=[0.0, 0.0, 0.0]),
                        material=MaterialData(color="#fdf4ff", roughness=0.4, metalness=0.0),
                        explode_offset=[0.0, 0.3, 0.4]
                    ),
                    ComponentData(
                        id="sofa_backrest",
                        name="Tufted Backrest",
                        purpose="High-back luxury support",
                        geometry_type="box",
                        geometry_params={"width": 2.4, "height": 1.1, "depth": 0.3},
                        transform=TransformData(position=[0.0, 0.65, -0.35]),
                        material=MaterialData(color="#fdf4ff", roughness=0.4, metalness=0.0),
                        explode_offset=[0.0, 0.8, -0.4]
                    ),
                    ComponentData(
                        id="sofa_gold_trim",
                        name="Carved Gold Trim",
                        purpose="Ornamental perimeter accent",
                        geometry_type="torus",
                        geometry_params={"radius": 1.2, "tube": 0.08},
                        transform=TransformData(position=[0.0, 1.0, -0.35]),
                        material=MaterialData(color="#fbbf24", roughness=0.2, metalness=0.85),
                        explode_offset=[0.0, 1.2, -0.2]
                    )
                ]
            ),
            SceneObjectData(
                id="floral_arch",
                name="Cascading Floral Arch & LED Wall",
                category="decor",
                purpose="Central framing backdrop that diffuses soft romantic luminescence.",
                description="Massive circular floral arch dense with white orchids, blush roses and integrated warm fairy light matrix.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 2.2, -2.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]),
                material=MaterialData(color="#fce7f3", roughness=0.5, metalness=0.0),
                components=[
                    ComponentData(
                        id="led_backdrop",
                        name="Ambient Backlit LED Panel",
                        geometry_type="plane",
                        geometry_params={"width": 6.5, "height": 4.5},
                        transform=TransformData(position=[0.0, 0.0, -0.2]),
                        material=MaterialData(color="#fff1f2", roughness=0.2, emissive="#e879f9", emissive_intensity=0.8),
                        explode_offset=[0.0, 0.0, -0.8]
                    ),
                    ComponentData(
                        id="flower_torus",
                        name="Floral Ring Garland",
                        geometry_type="torus",
                        geometry_params={"radius": 2.2, "tube": 0.35},
                        transform=TransformData(position=[0.0, 0.2, 0.0]),
                        material=MaterialData(color="#fbcfe8", roughness=0.7),
                        explode_offset=[0.0, 0.4, 0.6]
                    )
                ]
            ),
            SceneObjectData(
                id="crystal_chandelier",
                name="Grand Crystal Chandelier",
                category="lighting_fixture",
                purpose="Radiates multifaceted refraction over the centerpiece.",
                description="Multi-tiered crystal pendant chandelier with warm incandescent core.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 4.2, 0.0], rotation=[0.0, 0.0, 0.0], scale=[0.8, 0.8, 0.8]),
                animation=AnimationData(type="rotate", axis="y", speed=0.3),
                components=[
                    ComponentData(
                        id="chandelier_tier1",
                        name="Upper Crystal Prism Ring",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.8, "radiusBottom": 0.6, "height": 0.4},
                        transform=TransformData(position=[0.0, 0.2, 0.0]),
                        material=MaterialData(color="#e0f2fe", roughness=0.1, metalness=0.9, transmission=0.7),
                        explode_offset=[0.0, 0.5, 0.0]
                    ),
                    ComponentData(
                        id="chandelier_tier2",
                        name="Lower Droplet Cluster",
                        geometry_type="cone",
                        geometry_params={"radius": 0.5, "height": 0.8},
                        transform=TransformData(position=[0.0, -0.4, 0.0]),
                        material=MaterialData(color="#e0f2fe", roughness=0.1, metalness=0.9, emissive="#fef08a", emissive_intensity=0.5),
                        explode_offset=[0.0, -0.5, 0.0]
                    )
                ]
            ),
            SceneObjectData(
                id="gold_pillar_left",
                name="Fluted Golden Pillar (Left)",
                category="architecture",
                purpose="Structural ornamentation defining the ceremonial boundary.",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.25, "radiusBottom": 0.3, "height": 3.8},
                transform=TransformData(position=[-3.2, 1.7, -1.0]),
                material=MaterialData(color="#f59e0b", roughness=0.25, metalness=0.85, name="Polished Brass")
            ),
            SceneObjectData(
                id="gold_pillar_right",
                name="Fluted Golden Pillar (Right)",
                category="architecture",
                purpose="Structural ornamentation defining the ceremonial boundary.",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.25, "radiusBottom": 0.3, "height": 3.8},
                transform=TransformData(position=[3.2, 1.7, -1.0]),
                material=MaterialData(color="#f59e0b", roughness=0.25, metalness=0.85, name="Polished Brass")
            )
        ]
    )

    # 2. Futuristic Mars Colony
    demos["mars_station"] = ScenePlan(
        id="demo_mars_station",
        title="Ares-VII Mars Surface Research Station",
        intent="CREATE_SCENE",
        scene_type="sci_fi_outpost",
        user_prompt="Create a futuristic Mars research station with bio-domes, terrain, rovers and lighting.",
        language="en",
        environment=EnvironmentData(
            sky_color="#2b1108",
            ground_color="#7c2d12",
            fog_color="#431407",
            fog_density=0.02,
            ambient_color="#fdba74",
            ambient_intensity=0.9
        ),
        lighting=[
            LightData(type="directional", color="#ffedd5", intensity=2.2, position=[8.0, 15.0, 6.0]),
            LightData(type="point", color="#38bdf8", intensity=4.0, position=[0.0, 3.5, 0.0])
        ],
        camera=CameraData(position=[0.0, 6.0, 14.0], target=[0.0, 1.0, 0.0], fov=48.0),
        explanation_targets=["central_biodome", "pressurized_habitat", "mars_rover", "solar_array"],
        objects=[
            SceneObjectData(
                id="mars_terrain",
                name="Martian Regolith Basin",
                category="terrain",
                purpose="Cratered iron-oxide rich red soil foundation.",
                geometry_type="plane",
                geometry_params={"width": 30.0, "height": 30.0},
                transform=TransformData(position=[0.0, -0.05, 0.0], rotation=[-1.5708, 0.0, 0.0]),
                material=MaterialData(color="#9a3412", roughness=0.9, metalness=0.1)
            ),
            SceneObjectData(
                id="central_biodome",
                name="Hydroponic Geodesic Bio-Dome",
                category="habitat",
                purpose="Pressurized synthetic ecosystem supporting oxygen generation and food production.",
                description="Hexagonal reinforced polycarbonate geodesic dome enclosing hydroponic flora.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#0284c7", roughness=0.1, metalness=0.3, transmission=0.6, opacity=0.75),
                components=[
                    ComponentData(
                        id="dome_glass",
                        name="Pressurized Hex-Dome Shell",
                        geometry_type="sphere",
                        geometry_params={"radius": 3.0, "phiStart": 0, "phiLength": 6.28, "thetaStart": 0, "thetaLength": 1.57},
                        transform=TransformData(position=[0.0, 0.0, 0.0]),
                        material=MaterialData(color="#38bdf8", roughness=0.1, transmission=0.7, opacity=0.6),
                        explode_offset=[0.0, 2.5, 0.0]
                    ),
                    ComponentData(
                        id="inner_reactor_core",
                        name="Atmospheric Oxygenator Core",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.4, "radiusBottom": 0.5, "height": 2.0},
                        transform=TransformData(position=[0.0, 1.0, 0.0]),
                        material=MaterialData(color="#22c55e", roughness=0.3, emissive="#10b981", emissive_intensity=1.2),
                        explode_offset=[0.0, 0.0, 0.0]
                    ),
                    ComponentData(
                        id="airlock_corridor",
                        name="Pressurized Transfer Airlock",
                        geometry_type="box",
                        geometry_params={"width": 1.0, "height": 1.2, "depth": 2.5},
                        transform=TransformData(position=[0.0, 0.6, 2.5]),
                        material=MaterialData(color="#e2e8f0", roughness=0.3, metalness=0.7),
                        explode_offset=[0.0, 0.0, 1.5]
                    )
                ]
            ),
            SceneObjectData(
                id="mars_rover",
                name="Pathfinder-6 Autonomous Rover",
                category="vehicle",
                purpose="Remote sample collection and geological core drilling.",
                description="Six-wheel all-terrain rover with articulated robotic sensor mast.",
                geometry_type="compound",
                transform=TransformData(position=[4.5, 0.5, 3.0], rotation=[0.0, -0.6, 0.0]),
                animation=AnimationData(type="bounce", axis="y", speed=1.2, amplitude=0.08),
                components=[
                    ComponentData(
                        id="rover_chassis",
                        name="Titanium Alloy Chassis",
                        geometry_type="box",
                        geometry_params={"width": 1.6, "height": 0.6, "depth": 2.2},
                        material=MaterialData(color="#f8fafc", roughness=0.3, metalness=0.8),
                        explode_offset=[0.0, 0.5, 0.0]
                    ),
                    ComponentData(
                        id="rover_wheels",
                        name="Rocker-Bogie Titanium Mesh Wheels",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.35, "radiusBottom": 0.35, "height": 0.25},
                        transform=TransformData(position=[0.9, -0.2, 0.7], rotation=[0.0, 0.0, 1.57]),
                        material=MaterialData(color="#334155", roughness=0.5, metalness=0.9),
                        explode_offset=[0.6, -0.2, 0.4]
                    ),
                    ComponentData(
                        id="sensor_mast",
                        name="Stereo Vision LiDAR Mast",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.08, "radiusBottom": 0.08, "height": 1.0},
                        transform=TransformData(position=[0.0, 0.8, -0.6]),
                        material=MaterialData(color="#0ea5e9", roughness=0.2, emissive="#0284c7", emissive_intensity=0.8),
                        explode_offset=[0.0, 0.9, -0.3]
                    )
                ]
            ),
            SceneObjectData(
                id="solar_array",
                name="Bifacial Photovoltaic Solar Wing",
                category="energy",
                purpose="Converts faint Martian sunlight into 45kW of continuous DC energy.",
                geometry_type="box",
                geometry_params={"width": 4.5, "height": 0.1, "depth": 1.8},
                transform=TransformData(position=[-5.0, 1.5, -2.0], rotation=[0.5, 0.3, 0.0]),
                material=MaterialData(color="#1e3a8a", roughness=0.1, metalness=0.9, emissive="#1d4ed8", emissive_intensity=0.3)
            )
        ]
    )

    # 3. Interactive Solar System
    demos["solar_system"] = ScenePlan(
        id="demo_solar_system",
        title="Orbital Interactive Solar System",
        intent="CREATE_SCENE",
        scene_type="astronomy",
        user_prompt="Create a 3D solar system and explain the planets.",
        language="en",
        environment=EnvironmentData(
            sky_color="#030712",
            ground_color="#030712",
            fog_color="#030712",
            fog_density=0.005,
            show_grid=False,
            show_axes=False,
            ambient_color="#1e1b4b",
            ambient_intensity=0.3
        ),
        lighting=[
            LightData(type="point", color="#ffedd5", intensity=5.0, position=[0.0, 0.0, 0.0]),
            LightData(type="ambient", color="#4338ca", intensity=0.2)
        ],
        camera=CameraData(position=[0.0, 10.0, 18.0], target=[0.0, 0.0, 0.0], fov=50.0),
        explanation_targets=["sun", "earth", "mars", "jupiter", "saturn"],
        objects=[
            SceneObjectData(
                id="sun",
                name="The Sun (Sol)",
                category="star",
                purpose="G-type main-sequence star containing 99.86% of the solar system's total mass.",
                description="Blazing plasma sphere driven by nuclear fusion, emitting high luminosity and solar wind.",
                geometry_type="sphere",
                geometry_params={"radius": 2.2, "widthSegments": 32, "heightSegments": 32},
                transform=TransformData(position=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#f59e0b", roughness=0.2, emissive="#ea580c", emissive_intensity=2.0),
                animation=AnimationData(type="rotate", axis="y", speed=0.5)
            ),
            SceneObjectData(
                id="earth",
                name="Earth (Terra)",
                category="planet",
                purpose="Third planet from the Sun; only known astronomical object harboring organic life.",
                description="Terrestrial world featuring liquid oceans, nitrogen-oxygen atmosphere, and active tectonics.",
                geometry_type="sphere",
                geometry_params={"radius": 0.7, "widthSegments": 24, "heightSegments": 24},
                transform=TransformData(position=[5.2, 0.0, 0.0]),
                material=MaterialData(color="#2563eb", roughness=0.4, metalness=0.1),
                animation=AnimationData(type="orbit", axis="y", speed=1.0, amplitude=5.2)
            ),
            SceneObjectData(
                id="mars",
                name="Mars",
                category="planet",
                purpose="Fourth terrestrial planet from the Sun, target for human interplanetary exploration.",
                description="Red planet with thin carbon dioxide atmosphere and vast extinct shield volcanoes.",
                geometry_type="sphere",
                geometry_params={"radius": 0.5, "widthSegments": 24, "heightSegments": 24},
                transform=TransformData(position=[7.5, 0.0, 0.0]),
                material=MaterialData(color="#dc2626", roughness=0.6, metalness=0.1),
                animation=AnimationData(type="orbit", axis="y", speed=0.8, amplitude=7.5)
            ),
            SceneObjectData(
                id="jupiter",
                name="Jupiter",
                category="planet",
                purpose="Gas giant and largest planet, shielding inner worlds from cometary impacts.",
                description="Massive gas sphere consisting predominantly of hydrogen and helium with dynamic atmospheric bands.",
                geometry_type="sphere",
                geometry_params={"radius": 1.4, "widthSegments": 24, "heightSegments": 24},
                transform=TransformData(position=[11.0, 0.0, 0.0]),
                material=MaterialData(color="#d97706", roughness=0.5, metalness=0.1),
                animation=AnimationData(type="orbit", axis="y", speed=0.5, amplitude=11.0)
            ),
            SceneObjectData(
                id="saturn",
                name="Saturn & Ring System",
                category="planet",
                purpose="Gas giant famous for its spectacular, highly reflective planetary ring system.",
                description="Second largest planet with prominent rings composed of water ice, rock and tholin dust.",
                geometry_type="compound",
                transform=TransformData(position=[15.0, 0.0, 0.0]),
                animation=AnimationData(type="orbit", axis="y", speed=0.35, amplitude=15.0),
                components=[
                    ComponentData(
                        id="saturn_body",
                        name="Saturn Core Sphere",
                        geometry_type="sphere",
                        geometry_params={"radius": 1.1, "widthSegments": 24, "heightSegments": 24},
                        material=MaterialData(color="#fde68a", roughness=0.5)
                    ),
                    ComponentData(
                        id="saturn_rings",
                        name="Ice Dust Rings",
                        geometry_type="torus",
                        geometry_params={"radius": 2.2, "tube": 0.35, "radialSegments": 4, "tubularSegments": 32},
                        transform=TransformData(rotation=[1.2, 0.2, 0.0]),
                        material=MaterialData(color="#fed7aa", roughness=0.3, opacity=0.85)
                    )
                ]
            )
        ]
    )

    # 4. Mechanical Engine / Machine
    demos["machine"] = ScenePlan(
        id="demo_machine",
        title="High-Performance V-Twin Mechanical Engine",
        intent="CREATE_SCENE",
        scene_type="mechanical_engineering",
        user_prompt="Explain the three main components and show them as an interactive 3D model.",
        language="en",
        environment=EnvironmentData(
            sky_color="#0f172a",
            ground_color="#1e293b",
            fog_density=0.015,
            ambient_color="#94a3b8",
            ambient_intensity=0.9
        ),
        lighting=[
            LightData(type="directional", color="#ffffff", intensity=2.2, position=[6.0, 10.0, 6.0]),
            LightData(type="spot", color="#38bdf8", intensity=2.5, position=[-4.0, 6.0, 4.0])
        ],
        camera=CameraData(position=[0.0, 2.5, 6.5], target=[0.0, 0.8, 0.0], fov=45.0),
        explanation_targets=["engine_assembly"],
        objects=[
            SceneObjectData(
                id="engine_assembly",
                name="Internal Combustion Power Unit",
                category="powertrain",
                purpose="Converts thermal energy released by fuel combustion into rotating kinetic torque.",
                description="Multi-part reciprocating piston engine featuring cast iron block, dual cylinders, and forged crankshaft.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.8, 0.0]),
                components=[
                    ComponentData(
                        id="engine_block",
                        name="Engine Crankcase & Sump",
                        purpose="Structural foundation housing the oil pan and crankshaft bearings.",
                        geometry_type="box",
                        geometry_params={"width": 1.8, "height": 1.0, "depth": 1.5},
                        transform=TransformData(position=[0.0, -0.4, 0.0]),
                        material=MaterialData(color="#475569", roughness=0.3, metalness=0.85, name="Cast Iron"),
                        explode_offset=[0.0, -0.8, 0.0]
                    ),
                    ComponentData(
                        id="cylinder_left",
                        name="Left Cylinder Head & Cooling Fins",
                        purpose="Houses the combustion chamber where air-fuel mixture ignites.",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.45, "radiusBottom": 0.5, "height": 1.4},
                        transform=TransformData(position=[-0.7, 0.6, 0.0], rotation=[0.0, 0.0, 0.35]),
                        material=MaterialData(color="#94a3b8", roughness=0.2, metalness=0.9, name="Billet Aluminum"),
                        explode_offset=[-1.2, 1.2, 0.0]
                    ),
                    ComponentData(
                        id="cylinder_right",
                        name="Right Cylinder Head & Cooling Fins",
                        purpose="Complementary reciprocating combustion chamber.",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.45, "radiusBottom": 0.5, "height": 1.4},
                        transform=TransformData(position=[0.7, 0.6, 0.0], rotation=[0.0, 0.0, -0.35]),
                        material=MaterialData(color="#94a3b8", roughness=0.2, metalness=0.9, name="Billet Aluminum"),
                        explode_offset=[1.2, 1.2, 0.0]
                    ),
                    ComponentData(
                        id="crankshaft_flywheel",
                        name="Forged Steel Flywheel & Crankshaft",
                        purpose="Smooths engine pulses and transfers rotational inertia to the transmission.",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.6, "radiusBottom": 0.6, "height": 0.25},
                        transform=TransformData(position=[0.0, -0.4, 0.85], rotation=[1.5708, 0.0, 0.0]),
                        material=MaterialData(color="#e2e8f0", roughness=0.1, metalness=0.95, name="Chromoly Steel"),
                        explode_offset=[0.0, 0.0, 1.4]
                    ),
                    ComponentData(
                        id="intake_manifold",
                        name="High-Flow Intake Manifold",
                        purpose="Channels atomized air-fuel mixture directly into cylinder intake ports.",
                        geometry_type="torus",
                        geometry_params={"radius": 0.6, "tube": 0.12},
                        transform=TransformData(position=[0.0, 1.2, 0.0]),
                        material=MaterialData(color="#ef4444", roughness=0.3, metalness=0.4, name="Anodized Red Intake"),
                        explode_offset=[0.0, 1.5, 0.0]
                    )
                ]
            )
        ]
    )

    # 5. Modern AI Startup Office
    demos["modern_office"] = ScenePlan(
        id="demo_modern_office",
        title="Futuristic AI Innovation Lab",
        intent="CREATE_SCENE",
        scene_type="interior_workspace",
        user_prompt="Transform this empty room into a luxury modern AI startup office.",
        language="en",
        environment=EnvironmentData(
            sky_color="#0f172a",
            ground_color="#1e293b",
            fog_density=0.012,
            ambient_color="#e0e7ff",
            ambient_intensity=0.85
        ),
        lighting=[
            LightData(type="directional", color="#ffffff", intensity=1.8, position=[5.0, 9.0, 4.0]),
            LightData(type="spot", color="#6366f1", intensity=3.0, position=[0.0, 6.0, 0.0])
        ],
        camera=CameraData(position=[0.0, 4.0, 8.5], target=[0.0, 1.0, 0.0], fov=50.0),
        explanation_targets=["executive_desk", "hologram_pod", "ai_server_rack"],
        objects=[
            SceneObjectData(
                id="office_floor",
                name="Polished Concrete & Terrazzo Floor",
                category="architecture",
                geometry_type="plane",
                geometry_params={"width": 14.0, "height": 10.0},
                transform=TransformData(position=[0.0, 0.0, 0.0], rotation=[-1.5708, 0.0, 0.0]),
                material=MaterialData(color="#334155", roughness=0.3, metalness=0.2)
            ),
            SceneObjectData(
                id="executive_desk",
                name="Curved Ergonomic Workstation",
                category="furniture",
                purpose="Primary creative workbench with integrated cable management.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.75, 0.0]),
                components=[
                    ComponentData(
                        id="desk_surface",
                        name="Solid Oak Desktop",
                        geometry_type="box",
                        geometry_params={"width": 3.0, "height": 0.08, "depth": 1.4},
                        material=MaterialData(color="#e2e8f0", roughness=0.2, metalness=0.1),
                        explode_offset=[0.0, 0.4, 0.0]
                    ),
                    ComponentData(
                        id="desk_legs",
                        name="Matte Black Steel Frame",
                        geometry_type="box",
                        geometry_params={"width": 2.8, "height": 0.7, "depth": 0.1},
                        transform=TransformData(position=[0.0, -0.38, 0.0]),
                        material=MaterialData(color="#0f172a", roughness=0.5, metalness=0.8),
                        explode_offset=[0.0, -0.4, 0.0]
                    ),
                    ComponentData(
                        id="ultrawide_monitor",
                        name="Curved 49-inch OLED Display",
                        geometry_type="box",
                        geometry_params={"width": 1.6, "height": 0.6, "depth": 0.06},
                        transform=TransformData(position=[0.0, 0.35, -0.3]),
                        material=MaterialData(color="#0284c7", roughness=0.1, emissive="#38bdf8", emissive_intensity=0.8),
                        explode_offset=[0.0, 0.5, -0.4]
                    )
                ]
            ),
            SceneObjectData(
                id="ai_server_rack",
                name="Quantum AI Neural Node Rack",
                category="technology",
                purpose="On-premise GPU inference cluster powering real-time 3D simulation.",
                geometry_type="box",
                geometry_params={"width": 0.9, "height": 2.4, "depth": 0.9},
                transform=TransformData(position=[-3.5, 1.2, -2.0]),
                material=MaterialData(color="#090d16", roughness=0.2, metalness=0.9, emissive="#10b981", emissive_intensity=0.6)
            )
        ]
    )

    # 6. Restaurant
    demos["restaurant"] = ScenePlan(
        id="demo_restaurant",
        title="Modern Luxury Bistro Lounge",
        intent="CREATE_SCENE",
        scene_type="interior_dining",
        user_prompt="Create a modern restaurant with dining tables, lighting and bar counter.",
        language="en",
        environment=EnvironmentData(
            sky_color="#18181b", ground_color="#27272a", fog_density=0.015,
            ambient_color="#fed7aa", ambient_intensity=0.75
        ),
        lighting=[
            LightData(type="directional", color="#ffedd5", intensity=1.5, position=[4.0, 8.0, 5.0]),
            LightData(type="point", color="#f97316", intensity=3.0, position=[0.0, 3.0, 0.0])
        ],
        camera=CameraData(position=[0.0, 3.5, 7.5], target=[0.0, 1.0, 0.0], fov=45.0),
        explanation_targets=["center_dining_table", "wine_bar_counter"],
        objects=[
            SceneObjectData(
                id="center_dining_table",
                name="Calacatta Marble Dining Table",
                category="furniture",
                purpose="Intimate dining center with brass pedestal base.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.75, 0.0]),
                components=[
                    ComponentData(
                        id="table_marble_top",
                        name="Honed Marble Tabletop",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 1.2, "radiusBottom": 1.2, "height": 0.08},
                        material=MaterialData(color="#f8fafc", roughness=0.2, metalness=0.1),
                        explode_offset=[0.0, 0.4, 0.0]
                    ),
                    ComponentData(
                        id="table_brass_pillar",
                        name="Brushed Brass Pedestal",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.15, "radiusBottom": 0.4, "height": 0.7},
                        transform=TransformData(position=[0.0, -0.38, 0.0]),
                        material=MaterialData(color="#eab308", roughness=0.3, metalness=0.85),
                        explode_offset=[0.0, -0.3, 0.0]
                    )
                ]
            )
        ]
    )

    # 7. Futuristic Cyberpunk City
    demos["futuristic_city"] = ScenePlan(
        id="demo_futuristic_city",
        title="Neo-Kyoto Cyberpunk Metropolis",
        intent="CREATE_SCENE",
        scene_type="sci_fi_urban",
        user_prompt="Design a futuristic city with glowing skyscrapers and monorails.",
        language="en",
        environment=EnvironmentData(
            sky_color="#030712", ground_color="#090d16", fog_color="#0f172a",
            fog_density=0.02, ambient_color="#ec4899", ambient_intensity=0.8
        ),
        lighting=[
            LightData(type="directional", color="#06b6d4", intensity=2.0, position=[-6.0, 14.0, 6.0]),
            LightData(type="spot", color="#f43f5e", intensity=3.5, position=[0.0, 10.0, 0.0])
        ],
        camera=CameraData(position=[0.0, 7.0, 16.0], target=[0.0, 3.0, 0.0], fov=50.0),
        explanation_targets=["central_spire", "sky_bridge"],
        objects=[
            SceneObjectData(
                id="central_spire",
                name="Megacorp Hyper-Structure",
                category="skyscraper",
                purpose="Vertical city tower housing 40,000 residents and sky-gardens.",
                geometry_type="box",
                geometry_params={"width": 3.0, "height": 12.0, "depth": 3.0},
                transform=TransformData(position=[0.0, 6.0, -2.0]),
                material=MaterialData(color="#0f172a", roughness=0.1, metalness=0.9, emissive="#06b6d4", emissive_intensity=0.8)
            ),
            SceneObjectData(
                id="tower_left",
                name="Neon Residential Arcology",
                category="skyscraper",
                geometry_type="box",
                geometry_params={"width": 2.2, "height": 8.5, "depth": 2.2},
                transform=TransformData(position=[-4.5, 4.25, -1.0]),
                material=MaterialData(color="#1e1b4b", roughness=0.2, metalness=0.85, emissive="#a855f7", emissive_intensity=0.7)
            ),
            SceneObjectData(
                id="tower_right",
                name="Synthetic Quantum Datacenter",
                category="skyscraper",
                geometry_type="box",
                geometry_params={"width": 2.4, "height": 9.5, "depth": 2.4},
                transform=TransformData(position=[4.5, 4.75, -1.0]),
                material=MaterialData(color="#1e293b", roughness=0.2, metalness=0.85, emissive="#f43f5e", emissive_intensity=0.7)
            )
        ]
    )

    # 8. Modern Villa
    demos["modern_house"] = ScenePlan(
        id="demo_modern_house",
        title="Minimalist Architectural Cantilever Villa",
        intent="CREATE_SCENE",
        scene_type="architecture",
        user_prompt="Create a luxury modern architectural villa.",
        language="en",
        environment=EnvironmentData(
            sky_color="#0284c7", ground_color="#14532d", fog_density=0.01,
            ambient_color="#ffffff", ambient_intensity=0.9
        ),
        lighting=[LightData(type="directional", color="#ffffff", intensity=2.2, position=[8.0, 14.0, 10.0])],
        camera=CameraData(position=[0.0, 4.5, 12.0], target=[0.0, 1.5, 0.0]),
        explanation_targets=["villa_cantilever"],
        objects=[
            SceneObjectData(
                id="villa_cantilever",
                name="Suspended Glass & Concrete Pavilion",
                category="architecture",
                purpose="Seamless indoor-outdoor living wing projecting over the landscape.",
                geometry_type="box",
                geometry_params={"width": 6.5, "height": 2.8, "depth": 4.5},
                transform=TransformData(position=[0.0, 2.0, 0.0]),
                material=MaterialData(color="#f8fafc", roughness=0.3, metalness=0.1)
            )
        ]
    )

    # 9. High-Tech Factory
    demos["factory"] = ScenePlan(
        id="demo_factory",
        title="Autonomous Smart Robotics Assembly Line",
        intent="CREATE_SCENE",
        scene_type="industrial",
        user_prompt="Create a high-tech factory with automated robotic arms.",
        language="en",
        environment=EnvironmentData(
            sky_color="#1e293b", ground_color="#0f172a", fog_density=0.015,
            ambient_color="#94a3b8", ambient_intensity=0.85
        ),
        lighting=[LightData(type="directional", color="#ffffff", intensity=2.0, position=[6.0, 12.0, 5.0])],
        camera=CameraData(position=[0.0, 3.5, 8.0], target=[0.0, 1.0, 0.0]),
        explanation_targets=["robotic_arm"],
        objects=[
            SceneObjectData(
                id="robotic_arm",
                name="6-Axis High-Precision Articulated Robot",
                category="robotics",
                purpose="High-speed micro-precision spot welding and automated component placement.",
                geometry_type="compound",
                transform=TransformData(position=[0.0, 0.0, 0.0]),
                animation=AnimationData(type="rotate", axis="y", speed=0.8),
                components=[
                    ComponentData(
                        id="robot_base",
                        name="Anchored Turntable Base",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.6, "radiusBottom": 0.8, "height": 0.4},
                        transform=TransformData(position=[0.0, 0.2, 0.0]),
                        material=MaterialData(color="#f59e0b", roughness=0.3, metalness=0.8),
                        explode_offset=[0.0, -0.3, 0.0]
                    ),
                    ComponentData(
                        id="robot_bicep",
                        name="Hydraulic Primary Arm",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.2, "radiusBottom": 0.2, "height": 1.6},
                        transform=TransformData(position=[0.0, 1.1, 0.0], rotation=[0.3, 0.0, 0.0]),
                        material=MaterialData(color="#0284c7", roughness=0.2, metalness=0.9),
                        explode_offset=[0.0, 0.6, 0.4]
                    )
                ]
            )
        ]
    )

    # 10. Sci-Fi Product Showroom
    demos["product_showroom"] = ScenePlan(
        id="demo_product_showroom",
        title="Holographic Luxury Gadget Showroom",
        intent="CREATE_SCENE",
        scene_type="showroom",
        user_prompt="Create a sci-fi product showroom displaying a futuristic luxury device.",
        language="en",
        environment=EnvironmentData(
            sky_color="#030712", ground_color="#090d16", fog_density=0.015,
            ambient_color="#c084fc", ambient_intensity=0.8
        ),
        lighting=[
            LightData(type="directional", color="#38bdf8", intensity=2.0, position=[3.0, 7.0, 4.0]),
            LightData(type="point", color="#a855f7", intensity=3.5, position=[0.0, 2.5, 0.0])
        ],
        camera=CameraData(position=[0.0, 2.0, 5.0], target=[0.0, 0.8, 0.0], fov=40.0),
        explanation_targets=["luxury_device"],
        objects=[
            SceneObjectData(
                id="pedestal",
                name="Levitating Magnetic Pedestal",
                category="display",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 1.1, "radiusBottom": 1.4, "height": 0.4},
                transform=TransformData(position=[0.0, 0.2, 0.0]),
                material=MaterialData(color="#090d16", roughness=0.2, metalness=0.9, emissive="#8b5cf6", emissive_intensity=0.5)
            ),
            SceneObjectData(
                id="luxury_device",
                name="Chronos-IX Holographic Smartwatch",
                category="consumer_tech",
                purpose="Next-gen neural interface timepiece with floating volumetric sapphire display.",
                geometry_type="compound",
                asset_url="/models/luxury_watch.glb",
                transform=TransformData(position=[0.0, 1.1, 0.0]),
                animation=AnimationData(type="rotate", axis="y", speed=0.7),
                components=[
                    ComponentData(
                        id="watch_chassis",
                        name="Grade 5 Ceramic Case",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.5, "radiusBottom": 0.5, "height": 0.18},
                        material=MaterialData(color="#1e293b", roughness=0.1, metalness=0.9),
                        explode_offset=[0.0, -0.4, 0.0]
                    ),
                    ComponentData(
                        id="crystal_bezel",
                        name="Sapphire Crystal Lens",
                        geometry_type="cylinder",
                        geometry_params={"radiusTop": 0.45, "radiusBottom": 0.45, "height": 0.05},
                        transform=TransformData(position=[0.0, 0.12, 0.0]),
                        material=MaterialData(color="#38bdf8", roughness=0.05, transmission=0.8, emissive="#0284c7", emissive_intensity=0.7),
                        explode_offset=[0.0, 0.5, 0.0]
                    )
                ]
            )
        ]
    )

    return demos
