import theme as th

PLOTLY_TEMPLATE = "plotly_white"


def apply_plotly_defaults(fig):
    """Applique un thème global cohérent à tous les graphs Plotly"""

    fig.update_layout(
        plot_bgcolor=th.BG,
        paper_bgcolor=th.BG,
        font=dict(color=th.TEXT),

        margin=dict(l=40, r=40, t=60, b=60),

        title_font=dict(
            size=18,
            color=th.TEXT
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        )
    )

    return fig


def primary_color():
    return [th.PRIMARY]


def success_color():
    return [th.SUCCESS]


def danger_color():
    return [th.DANGER]