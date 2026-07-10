import streamlit as st
import theme as th
import textwrap

def make_sparkline(values, color="#10b981", width=200, height=32):
    if not values or len(values) < 2:
        return ""
    
    min_v, max_v = min(values), max(values)
    range_v = max_v - min_v if max_v != min_v else 1
    
    # Petites marges pour que le point final et la ligne ne soient pas coupés
    pad = 3
    coords = []
    for i, v in enumerate(values):
        x = (i / (len(values) - 1)) * (width - 2 * pad) + pad
        y = (height - pad) - ((v - min_v) / range_v) * (height - 2 * pad)
        coords.append((x, y))
    
    # Chemin en courbe lissée (quadratic bezier entre points milieux)
    path = f"M {coords[0][0]:.1f},{coords[0][1]:.1f} "
    for i in range(1, len(coords)):
        x0, y0 = coords[i - 1]
        x1, y1 = coords[i]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        path += f"Q {x0:.1f},{y0:.1f} {mx:.1f},{my:.1f} "
    path += f"T {coords[-1][0]:.1f},{coords[-1][1]:.1f}"
    
    # Zone de remplissage sous la courbe
    fill_path = path + f" L {coords[-1][0]:.1f},{height} L {coords[0][0]:.1f},{height} Z"
    
    last_x, last_y = coords[-1]
    gradient_id = f"grad-{abs(hash(color)) % 10000}"
    
    return f'''<svg width="{width}" height="{height}" style="display:block;">
        <defs>
            <linearGradient id="{gradient_id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{color}" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="{fill_path}" fill="url(#{gradient_id})" stroke="none"/>
        <path d="{path}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
        <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="2.5" fill="{color}"/>
    </svg>'''


def metric_card(title, value, icon, color, trend=None):
    accent = color or th.PRIMARY
    icon_html = f'<div style="font-size:22px; margin-bottom:8px;">{icon}</div>' if icon else ""
    sparkline_html = make_sparkline(trend, color=accent) if trend else ""
    
    html = textwrap.dedent(f"""
    <div style="
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 10px;
        border-left: 4px solid {accent};
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div>
            {icon_html}
            <div style="color:{th.TEXT}; font-size:13px; opacity:0.6; text-transform:uppercase; letter-spacing:0.5px;">
                {title}
            </div>
            <div style="color:{th.TEXT}; font-size:28px; font-weight:700; margin-top:4px;">
                {value}
            </div>
        </div>
        {sparkline_html}
    </div>
    """).strip()
    
    st.markdown(html, unsafe_allow_html=True)