"""Handle a dump output"""

from pyemp.comms import emp_sock
from pyemp.map_data import MapData
from pyemp.sector import Sector, opt_int


#######################################################################################
def to_opt_int(in_str: str) -> opt_int:
    """Convert a str to an optional int"""
    try:
        return int(in_str)
    except ValueError:
        return None


#######################################################################################
def cmd_dump(sock: emp_sock) -> MapData:
    """Handle a dump command"""
    data = MapData()
    msg = sock.send("dump #")
    # First three lines are header info
    for line in msg[3:-1]:
        bits = line.split()
        s = Sector(
            x=int(bits[0]),
            y=int(bits[1]),
            des=bits[2],
            sdes=bits[3],
            eff=bits[4],
            mob=int(bits[5]),
            # off=to_opt_int(bits[6]),
            min=to_opt_int(bits[8]),
            gold=int(bits[9]),
            fert=int(bits[10]),
            ocontent=int(bits[11]),
            uran=int(bits[12]),
            work=int(bits[13]),
            avail=int(bits[14]),
            terr=int(bits[15]),
            civ=int(bits[16]),
            mil=int(bits[17]),
            uw=int(bits[18]),
            food=int(bits[19]),
            shell=int(bits[20]),
            gun=int(bits[21]),
            pet=int(bits[22]),
            iron=int(bits[23]),
            dust=int(bits[24]),
            bar=int(bits[25]),
            oil=int(bits[26]),
            lcm=int(bits[27]),
            hcm=int(bits[28]),
            rad=int(bits[29]),
            u_del=to_opt_int(bits[30]),
            f_del=to_opt_int(bits[31]),
            s_del=to_opt_int(bits[32]),
            g_del=to_opt_int(bits[33]),
            p_del=to_opt_int(bits[34]),
            i_del=to_opt_int(bits[35]),
            d_del=to_opt_int(bits[36]),
            b_del=to_opt_int(bits[37]),
            o_del=to_opt_int(bits[38]),
            l_del=to_opt_int(bits[39]),
            h_del=to_opt_int(bits[40]),
            r_del=to_opt_int(bits[41]),
            u_cut=to_opt_int(bits[42]),
            f_cut=to_opt_int(bits[43]),
            s_cut=to_opt_int(bits[44]),
            g_cut=to_opt_int(bits[45]),
            p_cut=to_opt_int(bits[46]),
            i_cut=to_opt_int(bits[47]),
            d_cut=to_opt_int(bits[48]),
            b_cut=to_opt_int(bits[49]),
            o_cut=to_opt_int(bits[50]),
            l_cut=to_opt_int(bits[51]),
            h_cut=to_opt_int(bits[52]),
            r_cut=to_opt_int(bits[53]),
            dist_x=int(bits[54]),
            dist_y=int(bits[55]),
            c_dist=int(bits[56]),
            m_dist=int(bits[57]),
            u_dist=int(bits[58]),
            f_dist=int(bits[59]),
            s_dist=int(bits[60]),
            g_dist=int(bits[61]),
            p_dist=int(bits[62]),
            i_dist=int(bits[63]),
            d_dist=int(bits[64]),
            b_dist=int(bits[65]),
            o_dist=int(bits[66]),
            l_dist=int(bits[67]),
            h_dist=int(bits[68]),
            r_dist=int(bits[69]),
            road=int(bits[70]),
            rail=int(bits[71]),
            defense=int(bits[72]),
            fallout=int(bits[73]),
            coast=int(bits[74]),
            c_del=to_opt_int(bits[75]),
            m_del=to_opt_int(bits[76]),
            c_cut=to_opt_int(bits[77]),
            m_cut=to_opt_int(bits[78]),
            terr1=to_opt_int(bits[79]),
            terr2=to_opt_int(bits[80]),
            terr3=to_opt_int(bits[81]),
        )
        data.add(s)

    return data
