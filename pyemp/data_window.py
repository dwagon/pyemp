"""Data window for main display"""

import tabulate

from pyemp.lib_curses import Container, Label, TextViewer, FitType
from pyemp.map_data import MapData
from pyemp.sector import Sector, desig_name


#######################################################################################
#######################################################################################
#######################################################################################
class DataWindow(Container):
    """Window for displaying data"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.border = True
        self.hex_label = None
        self.desig_label = None
        self.pop_label = None
        self.resource_label = None
        self.details = None

    ###################################################################################
    def layout(self):
        """Layout the text fields"""
        self.hex_label = self.add(
            Label(begin_y=1, text="Hex -, -", height=1, fit=FitType.MAX_FIT),
            "Hex Label",
        )
        self.desig_label = self.add(
            Label(begin_y=2, text="", height=1, fit=FitType.MAX_FIT),
            "Desig Label",
        )
        self.pop_label = self.add(
            Label(begin_y=3, text="", height=1, fit=FitType.MAX_FIT),
            "Pop Label",
        )
        self.resource_label = self.add(
            Label(begin_y=4, text="", height=1, fit=FitType.MAX_FIT),
            "Resource Label",
        )
        self.details = self.add(
            TextViewer(begin_y=6, text="", height=14, fit=FitType.MAX_FIT),
            "Details",
        )
        super().layout()

    ###################################################################################
    def update(self, x: int, y: int, mapdata: MapData):
        """Update details"""
        self.hex_label.set_text(f"Hex {x}, {y}")
        if (x, y) not in mapdata:
            return
        m = mapdata[(x, y)]
        des_str = get_desig_str(m)
        self.desig_label.set_text(des_str)
        if m.civ is None and m.mil is None and m.uw is None:
            self.pop_label.set_text("")
        else:
            self.pop_label.set_text(
                f"Civs: {m.civ}/{m.c_dist}, UW: {m.uw}/{m.u_dist}, Mil: {m.mil}/{m.m_dist}",
            )

        self.resource_label.set_text(
            f"Resource: Iron: {m.min}, Gold: {m.gold}, "
            f"Fert: {m.fert}, Oil: {m.ocontent}, Uranium {m.uran}"
        )
        table = distribution_details_table(m).splitlines()
        self.details.set_text(table)


###################################################################################
def distribution_details_table(s: Sector) -> str:
    """Return the details about commodity distribution"""
    commodities = [
        ("Shells", "shell", "s_dist", "s_del", "s_cut"),
        ("Guns", "gun", "g_dist", "g_del", "g_cut"),
        ("Petrol", "pet", "p_dist", "p_del", "p_cut"),
        ("Iron", "iron", "i_dist", "i_del", "i_cut"),
        ("Gold Dust", "dust", "d_dist", "d_del", "d_cut"),
        ("Gold Bars", "bar", "b_dist", "b_del", "b_cut"),
        ("Oil", "oil", "s_dist", "o_del", "o_cut"),
        ("Light CM", "lcm", "l_dist", "l_del", "l_cut"),
        ("Heavy CM", "hcm", "h_dist", "h_del", "h_cut"),
        ("Rads", "rad", "r_dist", "r_del", "r_cut"),
    ]
    headers = ["Commodity", "Amount", "Threshold", "Deliver", "Cutoff"]

    table = []
    for name, amnt, thresh, deliv, cutoff in commodities:
        line = [name, s[amnt]]
        if s[thresh]:
            line.append(s[thresh])
        else:
            line.append("")
        if s[deliv]:
            line.append(s[deliv])
        else:
            line.append("")
        if s[cutoff]:
            line.append(s[cutoff])
        else:
            line.append("")
        table.append(line)
    return tabulate.tabulate(table, headers=headers)


###################################################################################
def get_desig_str(m: Sector) -> str:
    """Return the designation details for the current sector"""
    des_str = ""
    if m.des:
        des_str = f"{desig_name(m.des).title()} ({m.des})"
    if m.sdes and m.sdes != " ":
        des_str += f" Becoming {desig_name(m.sdes).title()} ({m.sdes})"
    return des_str


# EOF
