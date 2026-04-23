"""Data about a sector"""

from dataclasses import dataclass

#######################################################################################
type opt_int = int | None


#######################################################################################
#######################################################################################
#######################################################################################
@dataclass
class Sector:
    """A single sector"""

    x: int
    y: int
    des: str
    sdes: str
    eff: str
    mob: int
    # off: opt_int
    min: int
    gold: int
    fert: int
    ocontent: int
    uran: int
    work: int
    avail: int
    terr: int
    civ: int
    mil: int
    uw: int
    food: int
    shell: int
    gun: int
    pet: int
    iron: int
    dust: int
    bar: int
    oil: int
    lcm: int
    hcm: int
    rad: int
    u_del: opt_int
    f_del: opt_int
    s_del: opt_int
    g_del: opt_int
    p_del: opt_int
    i_del: opt_int
    d_del: opt_int
    b_del: opt_int
    o_del: opt_int
    l_del: opt_int
    h_del: opt_int
    r_del: opt_int
    u_cut: opt_int
    f_cut: opt_int
    s_cut: opt_int
    g_cut: opt_int
    p_cut: opt_int
    i_cut: opt_int
    d_cut: opt_int
    b_cut: opt_int
    o_cut: opt_int
    l_cut: opt_int
    h_cut: opt_int
    r_cut: opt_int
    dist_x: int
    dist_y: int
    c_dist: int
    m_dist: int
    u_dist: int
    f_dist: int
    s_dist: int
    g_dist: int
    p_dist: int
    i_dist: int
    d_dist: int
    b_dist: int
    o_dist: int
    l_dist: int
    h_dist: int
    r_dist: int
    road: int
    rail: int
    defense: int
    fallout: int
    coast: int
    c_del: int
    m_del: int
    c_cut: int
    m_cut: int
    terr1: opt_int
    terr2: opt_int
    terr3: opt_int


# EOF
