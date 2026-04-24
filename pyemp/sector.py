"""Data about a sector"""

from dataclasses import dataclass

#######################################################################################
type opt_int = opt_int | None


#######################################################################################
#######################################################################################
#######################################################################################
@dataclass
class Sector:
    """A single sector"""

    x: int
    y: int
    des: str
    sdes: str = ""
    eff: opt_int = None
    mob: opt_int = None
    min: opt_int = None
    gold: opt_int = None
    fert: opt_int = None
    ocontent: opt_int = None
    uran: opt_int = None
    work: opt_int = None
    avail: opt_int = None
    terr: opt_int = None
    civ: opt_int = None
    mil: opt_int = None
    uw: opt_int = None
    food: opt_int = None
    shell: opt_int = None
    gun: opt_int = None
    pet: opt_int = None
    iron: opt_int = None
    dust: opt_int = None
    bar: opt_int = None  # pylint: disable=disallowed-name
    oil: opt_int = None
    lcm: opt_int = None
    hcm: opt_int = None
    rad: opt_int = None
    u_del: opt_int = None
    f_del: opt_int = None
    s_del: opt_int = None
    g_del: opt_int = None
    p_del: opt_int = None
    i_del: opt_int = None
    d_del: opt_int = None
    b_del: opt_int = None
    o_del: opt_int = None
    l_del: opt_int = None
    h_del: opt_int = None
    r_del: opt_int = None
    u_cut: opt_int = None
    f_cut: opt_int = None
    s_cut: opt_int = None
    g_cut: opt_int = None
    p_cut: opt_int = None
    i_cut: opt_int = None
    d_cut: opt_int = None
    b_cut: opt_int = None
    o_cut: opt_int = None
    l_cut: opt_int = None
    h_cut: opt_int = None
    r_cut: opt_int = None
    dist_x: opt_int = None
    dist_y: opt_int = None
    c_dist: opt_int = None
    m_dist: opt_int = None
    u_dist: opt_int = None
    f_dist: opt_int = None
    s_dist: opt_int = None
    g_dist: opt_int = None
    p_dist: opt_int = None
    i_dist: opt_int = None
    d_dist: opt_int = None
    b_dist: opt_int = None
    o_dist: opt_int = None
    l_dist: opt_int = None
    h_dist: opt_int = None
    r_dist: opt_int = None
    road: opt_int = None
    rail: opt_int = None
    defense: opt_int = None
    fallout: opt_int = None
    coast: opt_int = None
    c_del: opt_int = None
    m_del: opt_int = None
    c_cut: opt_int = None
    m_cut: opt_int = None
    terr1: opt_int = None
    terr2: opt_int = None
    terr3: opt_int = None


# EOF
