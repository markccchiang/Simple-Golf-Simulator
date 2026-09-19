from math import pi as PI, sqrt

#
# physical parameters
#
g       = 9.806 # (m/sec^2)
h       = 0.001 # (sec)

#
# Other parameters
#
 
#
# sub-functions
#
def cross_prod(a1, a2, a3, b1, b2, b3):
    vec_i = a2*b3 - b2*a3
    vec_j = b1*a3 - a1*b3
    vec_k = a1*b2 - b1*a2
    return vec_i, vec_j, vec_k

def unit_vec(c1, c2, c3):
    tmp_length = sqrt(c1*c1 + c2*c2 + c3*c3)
    unit_i = c1/tmp_length
    unit_j = c2/tmp_length
    unit_k = c3/tmp_length
    return unit_i, unit_j, unit_k

def accel(v_ball_i, v_ball_j, v_ball_k, \
          v_wind_i, v_wind_j, v_wind_k, \
          w_unit_i, w_unit_j, w_unit_k, \
          C_D, C_L, rho_air, m, D):
    #
    # Acceleration of the ball (drag, lift and gravity), returned as its i, j, k components
    #
    A = (D/2)**2*PI
    #
    U_i = -1*v_ball_i + v_wind_i
    U_j = -1*v_ball_j + v_wind_j
    U_k = -1*v_ball_k + v_wind_k
    #
    abs_FD = C_D*A*rho_air*(U_i**2 + U_j**2 + U_k**2)/2
    abs_FL = C_L*A*rho_air*(U_i**2 + U_j**2 + U_k**2)/2
    #
    U_unit_i,  U_unit_j,  U_unit_k = unit_vec(U_i, U_j, U_k)
    FL_unit_i, FL_unit_j, FL_unit_k = cross_prod(U_unit_i, U_unit_j, U_unit_k, \
                                                 w_unit_i, w_unit_j, w_unit_k)
    ans_i = abs_FD*U_unit_i + abs_FL*FL_unit_i
    ans_j = abs_FD*U_unit_j + abs_FL*FL_unit_j
    ans_k = abs_FD*U_unit_k + abs_FL*FL_unit_k - m*g
    return ans_i/m, ans_j/m, ans_k/m

def RK4(tn, \
        xn, yn, zn, \
        v_xn, v_yn, v_zn, \
        v_wind_i, v_wind_j, v_wind_k, \
        w_unit_i, w_unit_j, w_unit_k, \
        C_D, C_L, rho_air, m, D):
    #---------------------------------------
    kx1, ky1, kz1 = accel(v_xn, v_yn, v_zn, v_wind_i, v_wind_j, v_wind_k, w_unit_i, w_unit_j, w_unit_k, C_D, C_L, rho_air, m, D)
    #---------------------------------------
    kx2, ky2, kz2 = accel(v_xn+kx1*h/2, v_yn+ky1*h/2, v_zn+kz1*h/2, v_wind_i, v_wind_j, v_wind_k, w_unit_i, w_unit_j, w_unit_k, C_D, C_L, rho_air, m, D)
    #---------------------------------------
    kx3, ky3, kz3 = accel(v_xn+kx2*h/2, v_yn+ky2*h/2, v_zn+kz2*h/2, v_wind_i, v_wind_j, v_wind_k, w_unit_i, w_unit_j, w_unit_k, C_D, C_L, rho_air, m, D)
    #---------------------------------------
    kx4, ky4, kz4 = accel(v_xn+kx3*h, v_yn+ky3*h, v_zn+kz3*h, v_wind_i, v_wind_j, v_wind_k, w_unit_i, w_unit_j, w_unit_k, C_D, C_L, rho_air, m, D)
    #---------------------------------------
    v_xn1 = v_xn + h*(kx1+2*kx2+2*kx3+kx4)/6
    v_yn1 = v_yn + h*(ky1+2*ky2+2*ky3+ky4)/6
    v_zn1 = v_zn + h*(kz1+2*kz2+2*kz3+kz4)/6
    #---------------------------------------
    tn1 = tn + h
    #---------------------------------------
    xn1 = xn + (v_xn+v_xn1)*h/2
    yn1 = yn + (v_yn+v_yn1)*h/2
    zn1 = zn + (v_zn+v_zn1)*h/2
    #---------------------------------------
    return tn1, v_xn1, v_yn1, v_zn1, xn1, yn1, zn1

