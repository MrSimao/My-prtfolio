import flet as ft
import flet_video as ftv
import base64
import os

# ─────────────────────────────────────────────
# UTILITIES: ASSETS & DESIGN
# ─────────────────────────────────────────────
def get_icon(name: str):
    icons = getattr(ft, "Icons", None) or getattr(ft, "icons")
    return getattr(icons, name)

def load_image_base64(path: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, path)
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return "SuperK"

# ─────────────────────────────────────────────
# MAIN APPLICATION SETUP
# ─────────────────────────────────────────────
def main(page: ft.Page):
    
    video_url = "https://drive.google.com/file/d/1SnaRFN1_aPPfDyMxYvHkfg8JG1_19Jpq/view?usp=drive_link"
    page.clean()
    page.title = "Simao Korea | Engineering Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d0221" 
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    # Professional Palette
    primary   = "#E97A34"  
    secondary = "#4A1D96"  
    card      = "#1B0A3A"
    panel     = "#12032C"
    text      = "#FFFFFF"
    subtext   = "#C2C2C2"

    # ─────────────────────────────────────────────
    # DESIGN COMPONENTS (Modular & Reusable)
    # ─────────────────────────────────────────────
    def symmetric_padding(horizontal: int, vertical: int):
        return ft.Padding(horizontal, vertical, horizontal, vertical)

    def border_all(width: int, color: str):
        side = ft.BorderSide(width=width, color=color)
        return ft.Border(top=side, right=side, bottom=side, left=side)

    async def open_route(route: str):
        await page.push_route(route)

    def nav_link(label: str, section_key: str):
        route = "/" if section_key == "home" else f"/{section_key}"
        return ft.ElevatedButton(
            label,
            color=text,
            bgcolor=panel,
            elevation=0,
            on_click=lambda _: page.run_task(open_route, route),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
            ),
        )

    def section_title(label: str, title: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(label.upper(), size=14, color=primary, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=42, weight=ft.FontWeight.BOLD, color=text),
            ],
        )

    def feature_card(title: str, description: str, icon_name: str):
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=28,
            border=border_all(1, secondary),
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Icon(get_icon(icon_name), size=38, color=primary),
                    ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(description, size=16, color=subtext),
                ],
            ),
        )

    def stat_card(number: str, label: str):
        return ft.Container(
            bgcolor=card,
            padding=26,
            border_radius=12,
            border=border_all(1, secondary),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(number, size=38, weight=ft.FontWeight.BOLD, color=primary),
                    ft.Text(label, size=17, color=subtext),
                ],
            ),
        )

    
    page.add(section_title("Overview", "My Engineering Journey"))

    # ─────────────────────────────────────────────
    # ALL 6 CERTIFICATES
    # ─────────────────────────────────────────────
    certificates = [
        {
            "title": "MATLAB Onramp",
            "date": "28 April 2026",
            "description": "Completed the official MathWorks MATLAB Onramp course.",
            "image_path": "assets/matlab_onramp.jpg",
            "tag": "Onramp",
        },
        {
            "title": "Simulink Onramp",
            "date": "09 June 2026",
            "description": "Completed the official MathWorks Simulink Onramp course.",
            "image_path": "assets/simulink_onramp.jpg",
            "tag": "Onramp",
        },
        {
            "title": "Machine Learning Onramp",
            "date": "10 June 2026",
            "description": "Completed the MathWorks Machine Learning Onramp course.",
            "image_path": "assets/machine_learning.jpg",
            "tag": "Onramp",
        },
        {
            "title": "Circuit Simulation onramp",
            "date": "16 June 2026",
            "description": "Completed the Circuit Simulation onramp.",
            "image_path": "assets/circuit simulation onramp.jpg",
            "tag": "Onramp",
        },
        {
            "title": "MATLAB Desktop Tools",
            "date": "-",
            "description": "Completed MATLAB Desktop Tools and Troubleshooting Scripts.",
            "image_path": "assets/matlab_desktop.jpg",
            "tag": "Course",
        },
        {
            "title": "Explore Data with MATLAB Plots",
            "date": "13 June 2026",
            "description": "Completed Explore Data with MATLAB Plots course.",
            "image_path": "assets/explore_data.jpg",
            "tag": "Course",
        },
        {
            "title": "Make and Manipulate Matrices",
            "date": "-",
            "description": "Completed Make and Manipulate Matrices course.",
            "image_path": "assets/make_matrices.jpg",
            "tag": "Course",
        },
        {
            "title": "Calculations with Vectors and Matrices",
            "date": "10 June 2026",
            "description": "Completed Calculations with Vectors and Matrices course.",
            "image_path": "assets/calc_vectors.jpg",
            "tag": "Course",
        },
    ]

   # ─────────────────────────────────────────────
    # CERTIFICATE VIEWER DIALOG
    # ─────────────────────────────────────────────

    cert_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=card,
        actions=[
            ft.TextButton(
                "Close",
                style=ft.ButtonStyle(color=primary),
                on_click=lambda _: close_dialog(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_dialog():
        cert_dialog.open = False
        page.update()

    def open_cert(cert: dict):
        b64 = load_image_base64(cert["image_path"])

        cert_dialog.title = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Text(cert["title"], size=20, weight=ft.FontWeight.BOLD,
                        color=primary, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Completed: {cert['date']}", size=14,
                        color=subtext, text_align=ft.TextAlign.CENTER),
            ],
        )

        cert_dialog.content = ft.Container(
            width=700,
            height=470,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=f"data:image/png;base64,{b64}",  
                fit=ft.BoxFit.CONTAIN,
                width=680,
                height=460,
            ) if b64 else ft.Text("Image not found", color="red"),
        )

        cert_dialog.open = True
        if cert_dialog not in page.overlay:
            page.overlay.append(cert_dialog)
        page.update()
    # ─────────────────────────────────────────────
    # TAG COLOR HELPER
    # ─────────────────────────────────────────────
    def tag_color(tag: str) -> str:
        return {
            "Onramp":        "#00d9ff",
            "Learning Path": "#7b2cbf",
            "Course":        "#00b894",
        }.get(tag, primary)

    # ─────────────────────────────────────────────
    # CERTIFICATE CARD
    # ─────────────────────────────────────────────
    def cert_card(cert: dict):
        tc = tag_color(cert["tag"])
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=22,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    # Tag badge
                    ft.Container(
                        bgcolor="#0d0221",
                        border_radius=20,
                        padding=ft.Padding(10, 4, 10, 4),
                        border=border_all(1, tc),
                        content=ft.Text(
                            cert["tag"],
                            size=11,
                            color=tc,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    ft.Icon(get_icon("VERIFIED"), size=34, color=primary),
                    ft.Text(cert["title"], size=17, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(cert["description"], size=13, color=subtext),
                    ft.Text(cert["date"], size=12, color=primary, italic=True),
                    ft.ElevatedButton(
                        "View Certificate",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, c=cert: open_cert(c),
                        style=ft.ButtonStyle(
                            padding=ft.Padding(10, 6, 10, 6),
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                ],
            ),
        )

    # ─────────────────────────────────────────────
    # NAV BAR
    # ─────────────────────────────────────────────
    nav_items = [
        ("HOME",     "home"),
        ("ABOUT",    "about"),
        ("TIMELINE", "timeline"),
        ("MATLAB",   "matlab"),
        ("BLOG",     "blog"),
        ("GITHUB",   "github"),
        ("CONTACT",  "contact"),
    ]
    page.appbar = ft.AppBar(
        title=ft.Text("", size=28, weight=ft.FontWeight.BOLD, color=primary),
        bgcolor=panel,
        toolbar_height=76,
        actions=[nav_link(label, key) for label, key in nav_items],
        actions_padding=ft.Padding(0, 0, 28, 0),
    )

    # ─────────────────────────────────────────────
    # HERO
    # ─────────────────────────────────────────────
    hero_section = ft.Container(
        key="home",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        ft.Text("WELCOME TO", size=18, color=secondary, weight=ft.FontWeight.BOLD),
                        ft.Text("Simao Korea's Portfolio", size=58, weight=ft.FontWeight.BOLD, color=text),
                        ft.Text("Unam Engineering Student | OreGuide UI Architect, OreGuide App | Python Developer", size=24, color=subtext),
                        ft.Row(
                            spacing=16,
                            wrap=True,
                            controls=[
                                ft.Button("Hire Me", bgcolor=primary, color="#000000",
                                          on_click=lambda _: page.run_task(open_route, "/contact")),
                                ft.Button("View Projects",
                                          style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                          on_click=lambda _: page.run_task(open_route, "/timeline")),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=340, height=340, border_radius=170,
                            border=border_all(5, primary),
                            image=ft.DecorationImage(src="profile.jpg", fit=ft.BoxFit.COVER),
                        )
                    ],
                ),
            ],
        ),
    )

    features = ft.Container(
    padding=symmetric_padding(horizontal=40, vertical=30),
    content=ft.ResponsiveRow(
        run_spacing=20,
        controls=[
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                    "Python & Flet Development",
                    "Built responsive web interfaces and core application logic using Python and the Flet framework.",
                    "CODE"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                    "UI/UX Architecture",
                    "Translated Figma team prototypes into clean, responsive grid layouts and professional components.",
                    "DESIGN_SERVICES"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Mining & Metallurgy Module",
                "Contributed to the ore recognition system serving Mining and Metallurgical engineering students.",
                "TERRAIN"
            )]),
        ],
    ),
)
    # ─────────────────────────────────────────────
    # ABOUT
    # ─────────────────────────────────────────────
    about_section = ft.Container(
        key="about",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.ResponsiveRow(
            run_spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    controls=[
                        ft.Image(
    src="team1.jpeg",  
    border_radius=12, 
    fit=ft.BoxFit.COVER, 
    height=360, 
    width=620,
                        )
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        section_title("ABOUT ME", "Bridging Engineering & Design"),
                        ft.Text(
                            "I am a second-year Electrical Engineering student at UNAM and a qualified electrician artisan. "
                            "This dual background allows me to bridge the gap between high-level engineering theory and hands-on practical implementation. "
                            "In my recent group project, OreGuide, I played a key role in UI architecture—translating "
                            "our team's Figma prototypes into a clean, functional interface. I am passionate about "
                            "building tools that simplify complex engineering tasks, and this portfolio "
                            "showcases my commitment to building professional, data-driven applications using Python and Flet.",
            ),
                    ],
                ),
            ],
        ),
    )

    stats = ft.Container(
        padding=symmetric_padding(horizontal=40, vertical=30),
        content=ft.ResponsiveRow(
            run_spacing=20,
            controls=[
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("1",  "Project")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("20", "Commits")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("1000+",  "Lines of Code")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("6",   "Certificates")]),
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # TIMELINE
    # ─────────────────────────────────────────────
    timeline_cards = [
        (
       "Week 1: Project Ideation & Team Formation",
        "Our 17-member team met to brainstorm engineering applications. We evaluated multiple concepts for feasibility and academic impact. We collectively agreed to build an Ore Recognition App to assist students in Mining and Metallurgical engineering with mineral classification and identification."
    ),
    (
        "Week 2: Software Requirements & UI Design",
        "We collaborated on the Software Requirements Specification (SRS), defining our system architecture and user stories. I contributed to the interface requirements, specifically outlining the user flow for the ore classification module. We also began prototyping our visual interface using Figma to establish a professional design language."
    ),
    (
        "Week 3: Engineering Calculator Implementation",
        "I developed the core logic for the app's engineering calculators. This included implementing formulas for ore grade, recovery rates, and material cost estimations. I focused on building robust input validation and clear output displays, ensuring the calculators were both accurate and intuitive for engineering students."
    ),
    (
        "Week 4: Ore Display Module & UI Architecture",
        "Working in a sub-team of two, I was responsible for building the Ore Display module. We transitioned our Figma prototypes into code, focusing on responsive grid layouts and card styling. My task was to architect the data-handling logic to manage ore properties and image rendering within the UI. Once the module was finalized, we conducted code reviews and successfully merged our branch into the main repository, ensuring the module met our team’s visual and functional standards."
    ),
]
    timeline_section = ft.Container(
        key="timeline",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Project Timeline", size=42, weight=ft.FontWeight.BOLD, color=text),
                *[
                    ft.Container(
                        bgcolor=card, padding=24, border_radius=12, border=border_all(1, primary),
                        content=ft.Column(spacing=8, controls=[
                            ft.Text(week, size=23, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(description, color=subtext, size=16),
                        ]),
                    )
                    for week, description in timeline_cards
                ],
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # MATLAB SECTION — all 8 certificates
    # ─────────────────────────────────────────────
    matlab_section = ft.Container(
        key="matlab",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("MATLAB Achievement Hub", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "All MathWorks certificates earned by Simao Korea— click any card to view the full certificate.",
                    size=16, color=subtext,
                ),
                
                ft.Text("Onramp Certificates", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[0])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[1])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[2])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[3])]),
                    ],
                ),
               
                ft.Text("Core MATLAB Skills — Learning Path & Courses", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[4])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[5])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[6])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[7])]),
                    ],
                ),
            ],
        ),
    )

 # ── BLOG SECTION ──
    async def open_video(e):
        print("--- Video Button Clicked ---")
        print(f"Current video_url value: '{video_url}'")
        
        if not video_url:
            print("❌ ERROR: video_url is completely empty or undefined!")
        elif not video_url.startswith("http"):
            print("❌ ERROR: Your URL is missing 'https://'. Flet will ignore it silently.")
        else:
            print("🚀 Attempting to launch URL via Flet client...")
            await page.launch_url(video_url)

    blog_section = ft.Container(
        key="blog",
        padding=ft.Padding.symmetric(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("Technical Blog", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Confidence in Concepts — written technical explanations with video inserts.",
                        size=16, color=subtext),

               
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=ft.Border.all(width=1, color=secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("PLAY_CIRCLE"), size=38, color=primary),
                            ft.Text("Semester Project Reflection", size=22, weight=ft.FontWeight.BOLD, color=text),
                            ft.Text("In this reflection video, I discuss my contributions to the OreGuide project...", size=15, color=subtext),
                            ft.Image(src="favicon.png", width=640, height=360, fit=ft.BoxFit.COVER, border_radius=12),
                            
                           
                           ft.ElevatedButton(
                                content="▶ Watch Reflection Video",
                                on_click=open_video,
                                style=ft.ButtonStyle(
                                    bgcolor=primary,
                                    color="#000000",
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                            ),
                        ],
                    ),
                ),

                
                ft.Container(
                    bgcolor=card,
                    padding=28,
                    border_radius=12,
                    border=ft.Border.all(width=1, color=primary),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Icon(get_icon("FUNCTIONS"), size=38, color=primary),
                            ft.Text("Mathematical Notation", size=30, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text("When calculating the total material cost in mining operations...", size=15, color=subtext),
                            ft.Text("Total Cost = Σ (Qi × Pi) + Overheads", size=26, color=text, weight=ft.FontWeight.BOLD),
                        ],
                    ),
                ),
            ],
        ),
    )
    # ─────────────────────────────────────────────
    # GITHUB EVIDENCE DIALOG
    # ─────────────────────────────────────────────
    evidence_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=card,
        actions=[
            ft.TextButton(
                "Close",
                style=ft.ButtonStyle(color=primary),
                on_click=lambda _: close_evidence(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_evidence():
        evidence_dialog.open = False
        page.update()

    def open_evidence(title: str, image_path: str):
        b64 = load_image_base64(image_path)
        evidence_dialog.title = ft.Text(
            title, size=20, weight=ft.FontWeight.BOLD, color=primary
        )
        evidence_dialog.content = ft.Container(
            width=700,
            height=470,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=f"data:image/png;base64,{b64}",
                fit=ft.BoxFit.CONTAIN,
                width=680,
                height=460,
            ) if b64 else ft.Text("Image not found", color="red"),
        )
        evidence_dialog.open = True
        if evidence_dialog not in page.overlay:
            page.overlay.append(evidence_dialog)
        page.update()

    # ─────────────────────────────────────────────
    # GITHUB SECTION
    # ─────────────────────────────────────────────
    github_section = ft.Container(
        key="github",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("GitHub Evidence", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "My individual contributions to the OreGuide group project — verified via GitHub.",
                    size=16, color=subtext,
                ),

               
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Container(
                            width=180, height=180, border_radius=90,
                            border=border_all(4, primary),
                            content=ft.Image(
                               src=f"data:image/png;base64,{load_image_base64('assets/github_profile.png')}",
                               fit=ft.BoxFit.COVER,
                               width=200,
                               height=200,
                            ),
                        ),
                            ft.Text("Simao Korea", size=22, weight=ft.FontWeight.BOLD, color=text),
                            ft.Text("MrSimao", size=16, color=subtext),
                            ft.Button(
                                "View GitHub Profile",
                                bgcolor=primary,
                                color="#000000",
                                on_click=lambda _: __import__('webbrowser').open("https://github.com/MrSimao"),
                            ),
                        ],
                    ),
                ),

               
                # ── Pull Requests ──
                ft.Text("Commits through GitHub", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=22,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Icon(get_icon("MERGE_TYPE"), size=34, color=primary),
                            ft.Text("OrePhotos Branch — Pull Request to Main", size=17,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "GitHub Desktop showing the OrePhotos branch pushed to remote, "
                                "and the pull request merging 2 commits with 99 lines added into main.",
                                size=14, color=subtext,
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.ElevatedButton(
                                        "View commits",
                                        bgcolor=primary,
                                        color="#000000",
                                        on_click=lambda _: open_evidence(
                                            "Pull Request — OrePhotos Branch", "assets/Pull_request.jpg"
                                        ),
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(10, 6, 10, 6),
                                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "view commits",
                                        bgcolor=primary,
                                        color="#000000",
                                        on_click=lambda _: open_evidence(
                                            "Pull Request — Code Changes", "assets/pull_request2.jpg"
                                        ),
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(10, 6, 10, 6),
                                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),

                
                ft.Text("Project Contribution: Collaborative UI Design & Dev", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=22,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Icon(get_icon("GROUPS"), size=34, color=primary),
                            ft.Text("Bringing Team Vision to Life", size=17,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Collaborating with my team, I played a key role in bridging the gap between our team's "
                    "Figma design prototypes and a functional, professional-grade application. While our team "
                    "worked in unison to define the UI/UX branding, I focused on the technical architecture "
                    "needed to bring these visual standards to life. By translating our Figma-based layout "
                    "concepts into clean, responsive Flet code and integrating dynamic Firebase data, I helped "
                    "ensure the final product maintained the visual polish we aimed for. This collaborative "
                    "process allowed us to deliver a cohesive tool for mining and metallurgical students, "
                    "demonstrating my ability to work within a team to turn creative concepts into high-quality, "
                    "data-driven engineering solutions.",
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # CONTACT
    # ─────────────────────────────────────────────
    contact_section = ft.Container(
        key="contact",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Contact Me", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Available for freelance work and engineering projects.", size=18, color=subtext, text_align=ft.TextAlign.CENTER),
                ft.TextField(width=500, label="Your Name",  bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, label="Your Email", bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, min_lines=4, max_lines=6, multiline=True, label="Message", bgcolor=card, border_color=primary, color=text),
                ft.Button("Send Message", bgcolor=primary, color="#000000"),
            ],
        ),
    )

    footer = ft.Container(
        padding=30,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("(c) 2026 Simao Korea - Portfolio - All Rights Reserved", color=subtext),
    )

    # ─────────────────────────────────────────────
    # ROUTING
    # ─────────────────────────────────────────────
    pages = {
        "home":     [hero_section, features],
        "about":    [about_section, stats],
        "timeline": [timeline_section],
        "matlab":   [matlab_section],
        "blog":     [blog_section],
        "github":   [github_section],
        "contact":  [contact_section],
    }

    def render_route(_=None):
        section  = page.route.strip("/") or "home"
        controls = pages.get(section, pages["home"])
        page.controls.clear()
        page.add(ft.Column(spacing=0, controls=[*controls, footer]))
        page.update()

    page.on_route_change = render_route
    render_route()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
