"""Data window for main display"""

import tabulate

from pyemp.lib_curses import Container, Widget, Label, TextViewer
from pyemp.map_data import MapData
from pyemp.sector import Sector, desig_name


#######################################################################################
#######################################################################################
#######################################################################################
class DataWindow(Container):
    """Window for displaying data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widgets: dict[str, Widget] = {}
        self.widgets["hex"] = Label(begin_y=1, begin_x=1, text="Hex -, -")
        self.widgets["desig"] = Label(begin_y=2, begin_x=1, text="")
        self.widgets["pop"] = Label(begin_y=3, begin_x=1, text="")
        self.widgets["resource"] = Label(begin_y=4, begin_x=1, text="")
        self.widgets["details"] = TextViewer(begin_y=6, begin_x=1, text="")
        for w in self.widgets.values():
            self.add_widget(w)

    ###################################################################################
    def update(self, x: int, y: int, mapdata: MapData):
        """Update details"""
        self.widgets["hex"].set_text(f"Hex {x}, {y}")
        if (x, y) not in mapdata:
            return
        m = mapdata[(x, y)]
        des_str = get_desig_str(m)
        self.widgets["desig"].set_text(des_str)
        if m.civ is None:
            return
        self.widgets["pop"].set_text(
            f"Civs: {m.civ}/{m.c_dist}, UW: {m.uw}/{m.u_dist}, Mil: {m.mil}/{m.m_dist}",
        )

        self.widgets["resource"].set_text(
            f"Resource: Iron: {m.min}, Gold: {m.gold}, "
            f"Fert: {m.fert}, Oil: {m.ocontent}, Uranium {m.uran}"
        )
        table = distribution_details_table(m).splitlines()
        self.widgets["details"].set_text(table)


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
